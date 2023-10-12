import traceback
from datetime import datetime as dt

import numpy as np
import pandas as pd

from .connection import connect_db


def check_shift(date):
    if (
        date.time() >= pd.to_datetime("00:00").time()
        and date.time() <= pd.to_datetime("08:00").time()
    ):
        return 1
    elif (
        date.time() >= pd.to_datetime("08:00").time()
        and date.time() <= pd.to_datetime("16:00").time()
    ):
        return 2
    else:
        return 3


def get_inbound_trucks(cnxn):
    date = dt.now().strftime("%Y-%m-%d")
    date_time = dt.now().strftime("%Y-%m-%d %H:%M")

    df_inbound = pd.read_sql(
        f"""
            select * from etl_zone."BACKHAULING_INBOUND_TRUCK" bit2
            where "ARRIVAL_DATE" >= '{date}'
            and "DEPARTURE_DATE" >= '{date_time}'
            """,
        cnxn,
    )
    df_inbound["PACK_TYPE"] = np.where(
        df_inbound["VEHICLE_TYPE"] == "BULKER", "LOOSE", "PACKED"
    )
    df_inbound["ORDER_CLUBBED"] = False
    df_inbound["CLUB_ID"] = np.NaN

    return df_inbound


def get_passing_destinations(cnxn, df_inbound):
    dest_pass_master = pd.read_sql(
        """
        select
        "SOURCE_STATE"
        ,"SOURCE_DISTRICT"
        ,"DESTINATION_STATE"
        ,"DESTINATION_DISTRICT"
        ,"PASSING_STATE"
        ,"PASSING_DISTRICT"
        from etl_zone."BACKUNLOADING_ENROUTE_MARKETS_MASTER"
        """,
        cnxn,
    )

    # dest_pass_master = pd.read_csv("data/backunloading_enroutre_market_master.csv")

    # uncomment line number 27 while moving to prod
    add_master = pd.read_sql(
        """ select
        "CITY" as "PASSING_CITY",
        "CITY_ID" as "PASSING_DESTINATION",
        "STATE" as "PASSING_STATE",
        "DISTRICT" as "PASSING_DISTRICT"
        from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
        where "ACTIVE" = 'Y'
        --and "Active" = 1
        and
            (
            "ATTRIBUTE1" is not null
            or "ATTRIBUTE2" is not null
            or "ATTRIBUTE3" is not null
            )
        """,
        cnxn,
    )

    # add_master = pd.read_csv("data/address_link.csv")

    plant_source = pd.read_sql(
        """
            select
            substring("PARTY_NAME",1,3) as "PLANT_ID",
            "STATE" as "SOURCE_STATE",
            "DISTRICT" as "SOURCE_DISTRICT"
            from target."TGT_PLANT_DEPO_MASTER" tpdm
            where "PARTY_NAME" like 'FG%'
            and "CATEGORY_CODE" != 'BRICKS'
            """,
        cnxn,
    )

    # plant_source = pd.read_csv("data/plant_depo_master.csv")

    df_inbound = df_inbound.merge(plant_source, on="PLANT_ID", how="inner")

    df_inbound = df_inbound.merge(
        dest_pass_master,
        on=[
            "SOURCE_STATE",
            "SOURCE_DISTRICT",
            "DESTINATION_STATE",
            "DESTINATION_DISTRICT",
        ],
    )
    df_inbound = df_inbound.merge(add_master, on=["PASSING_STATE", "PASSING_DISTRICT"])

    return df_inbound


def get_orders(cnxn, arrival_date, departure_date, plant_id):
    arr_dt = arrival_date.strftime("%Y-%m-%d")
    dp_dt = departure_date.strftime("%Y-%m-%d")

    arr_shift = check_shift(arrival_date)
    dp_shift = check_shift(departure_date)

    orders_df = pd.read_sql(
        f"""
            select
            lsom."ID" as "ORDER_MASTER_ID"
            ,lsom."ORDER_ID"
            ,lsom."ORDER_HEADER_ID"
            ,lsom."ORDER_LINE_ID"
            ,lsom."DELIVERY_DETAIL_ID"
            ,case
                when lsom."CHANGED_SOURCE" is null then lsom."AUTO_TAGGED_SOURCE"
                else lsom."CHANGED_SOURCE"
            end as "PLANT_ID"
            ,lsom."ORDER_TYPE"
            ,lsom."BRAND"
            ,lsom."PACK_TYPE"
            ,lsom."ORDER_QUANTITY" as "VEHICLE_SIZE"
            ,lsom."SHIP_STATE" as "PASSING_STATE"
            ,lsom."SHIP_DISTRICT" as "PASSING_DISTRICT"
            ,lsom."SHIP_CITY" as "PASSING_CITY"
            ,lsed."EXECUTABLE_DATE"
            ,lsed."EXECUTABLE_SHIFT"
            ,lsed."TOTAL_SCORE"
            from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom , etl_zone."LP_SCHEDULING_EXECUTABLE_DTL" lsed
            where "ORDER_EXECUTABLE" = true
            and lsom."ID" = lsed."ORDER_MASTER_ID"
            and lsom."AUTO_TAGGED_MODE" = 'ROAD'
            and
            (
                lsed."EXECUTABLE_DATE" >= '{arr_dt}'
                and lsed."EXECUTABLE_SHIFT" >= '{arr_shift}'
            )
            and
            (
                lsed."EXECUTABLE_DATE" <= '{dp_dt}'
                and lsed."EXECUTABLE_SHIFT" <= '{dp_shift}'
            )
            """,
        cnxn,
    )

    # orders_df = pd.read_csv("data/order_master.csv")

    orders_df = orders_df[orders_df["PLANT_ID"] == plant_id]

    return orders_df


class BackHaulingViewHelper:
    def run_model(cnxn):
        df_inbound = get_inbound_trucks(cnxn)

        df_inbound = get_passing_destinations(cnxn, df_inbound)

        df_inbound["KEY"] = df_inbound[
            [
                "PASSING_STATE",
                "PASSING_DISTRICT",
                "PASSING_CITY",
                "PACK_TYPE",
                "PLANT_ID",
            ]
        ].sum(axis=1)

        id_un = df_inbound["ID"].unique()

        df_fnl = pd.DataFrame()

        for id in id_un:
            df_tmp = df_inbound[df_inbound["ID"] == id]
            vehicle_size = df_tmp.iloc[0]["VEHICLE_SIZE"]

            orders_df = get_orders(
                cnxn,
                df_tmp.iloc[0]["ARRIVAL_DATE"],
                df_tmp.iloc[0]["DEPARTURE_DATE"],
                df_tmp.iloc[0]["PLANT_ID"],
            )

            if len(orders_df) == 0:
                continue

            df_tmp_full_size = df_tmp.merge(
                orders_df,
                how="inner",
                on=[
                    "PASSING_STATE",
                    "PASSING_DISTRICT",
                    "PASSING_CITY",
                    "VEHICLE_SIZE",
                    "PACK_TYPE",
                    "PLANT_ID",
                ],
            )

            orders_df = orders_df[
                (
                    ~orders_df["ORDER_MASTER_ID"].isin(
                        df_tmp_full_size["ORDER_MASTER_ID"]
                    )
                )
                & (orders_df["VEHICLE_SIZE"] < vehicle_size)
            ]
            orders_df["KEY"] = orders_df[
                [
                    "PASSING_STATE",
                    "PASSING_DISTRICT",
                    "PASSING_CITY",
                    "PACK_TYPE",
                    "PLANT_ID",
                ]
            ].sum(axis=1)
            orders_df = orders_df[orders_df["KEY"].isin(df_tmp["KEY"])]

            df_tmp_club = pd.DataFrame(
                columns=[
                    "ID",
                    "ORDER_MASTER_ID",
                    "ORDER_CLUBBED",
                    "CLUB_ID",
                    "TOTAL_SCORE",
                ]
            )
            # Get gratest club id
            club_id = 100
            if len(orders_df) > 0:
                key_un = orders_df["KEY"].unique()

                for key in key_un:
                    order_tmp = (
                        orders_df[orders_df["KEY"] == key]
                        .sort_values("TOTAL_SCORE", ascending=False)
                        .reset_index()
                    )
                    df_tmp_key = df_tmp[df_tmp["KEY"] == key]

                    # Add check for Brand, Grade
                    for idx in range(len(order_tmp) - 1):
                        for idx_next in range(idx + 1, len(order_tmp)):
                            if (
                                order_tmp.loc[idx, "ORDER_MASTER_ID"]
                                not in df_tmp_club["ORDER_MASTER_ID"].tolist()
                            ) and (
                                order_tmp.loc[idx_next, "ORDER_MASTER_ID"]
                                not in df_tmp_club["ORDER_MASTER_ID"].tolist()
                            ):
                                if (
                                    order_tmp.loc[idx, "BRAND"]
                                    == order_tmp.loc[idx_next, "BRAND"]
                                ):
                                    if (
                                        order_tmp.loc[
                                            [idx, idx_next], "VEHICLE_SIZE"
                                        ].sum()
                                        == vehicle_size
                                    ):
                                        df_tmp_club.loc[len(df_tmp_club)] = [
                                            id,
                                            order_tmp.loc[idx, "ORDER_MASTER_ID"],
                                            True,
                                            club_id,
                                            order_tmp.loc[idx, "TOTAL_SCORE"],
                                        ]
                                        df_tmp_club.loc[len(df_tmp_club)] = [
                                            id,
                                            order_tmp.loc[idx_next, "ORDER_MASTER_ID"],
                                            True,
                                            club_id,
                                            order_tmp.loc[idx_next, "TOTAL_SCORE"],
                                        ]
                                        club_id += 1

                    # print(order_tmp)

            df_tmp_full_size = df_tmp_full_size[
                ["ID", "ORDER_MASTER_ID", "ORDER_CLUBBED", "CLUB_ID", "TOTAL_SCORE"]
            ]

            df_fnl = df_fnl.append(df_tmp_full_size, ignore_index=True)
            df_fnl = df_fnl.append(df_tmp_club, ignore_index=True)

        df_fnl.rename(columns={"ID": "INBOUND"}, inplace=True)
        df_fnl.rename(columns={"ORDER_MASTER_ID": "ORDER_MASTER"}, inplace=True)

        return df_fnl

    # if __name__=='__main__':

    #     cnxn = connect_db()
    #     # cnxn = None

    #     try:

    #         # etl_zone."BACKHAULING_OPPORTUNITIES"
    #         df_fnl = run_model(cnxn)

    #     except Exception as e:
    #         print(traceback.print_exc())

    #     finally:

    #         cnxn.close()
