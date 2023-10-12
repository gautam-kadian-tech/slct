import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta as rd

from .connection import connect_db, createorupdate

ncr_map = {1: 4, 2: 3, 3: 2, 4: 1}

order_map = {0: 0, 15: 1, 30: 2, 40: 3, 60: 4}

party_map = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

cust_map = {"TR": 3, "KFY": 2, "NT": 1}


def convert_datetime(df, col):
    df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M")
    return df


def get_order_rank(df):
    if df["ORDER_QUANTITY"] >= 0 and df["ORDER_QUANTITY"] < 15:
        return 0
    elif df["ORDER_QUANTITY"] >= 15 and df["ORDER_QUANTITY"] < 30:
        return 1
    elif df["ORDER_QUANTITY"] >= 30 and df["ORDER_QUANTITY"] < 40:
        return 2
    elif df["ORDER_QUANTITY"] >= 40 and df["ORDER_QUANTITY"] < 60:
        return 3
    elif df["ORDER_QUANTITY"] >= 60:
        return 4


def get_data(cnxn):
    sql = """
        select
        lsom."ID" as "ORDER_MASTER_ID",
        lsom."ORDER_DATE",
        lsom."DELIVERY_DUE_DATE",
        lsom."CUSTOMER_TYPE",
        lsom."ORDER_QUANTITY",
        case
            when lsom."CHANGED_SOURCE" is null then lsom."AUTO_TAGGED_SOURCE"
            else lsom."CHANGED_SOURCE"
        end as "PLANT_ID",
        lscc."NCR_QUARTILE",
        lscc."PARTY_CATEGORY",
        lscc."TRUCKS_PENDING_FOR_EPOD_CONFIRMATION",
        tosrm."ROUTE_ID",
        tosrm."DISTANCE",
        dc."DEALER_CATEGORY",
        upper(lsom."BRAND") as "BRAND",
        lsom."GRADE" as "PRODUCT",
        lsom."SHIP_STATE" as "STATE",
        lsom."SHIP_DISTRICT" as "DISTRICT"
        from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom
        left join(
        select
        "ORDER_MASTER_ID",
        coalesce("NCR_QUARTILE",0) as "NCR_QUARTILE",
        coalesce("PARTY_CATEGORY",'C') as "PARTY_CATEGORY",
        coalesce("TRUCKS_PENDING_FOR_EPOD_CONFIRMATION",0) as "TRUCKS_PENDING_FOR_EPOD_CONFIRMATION"
        from
        etl_zone."LP_SCHEDULING_CRM_CHECKS"
        ) lscc on lscc."ORDER_MASTER_ID" = lsom."ID"
        left join (
            select "ROUTE_ID" ,"DISTANCE"::int  from etl_zone."T_OEBS_SCL_ROUTE_MASTER"
            where "ACTIVE_FLAG" = 'Y'
        ) tosrm on tosrm."ROUTE_ID" = lsom."ROUTE"::float
        left join (
        select
        "COUNTER_CODE" ,"DEALER_CATEGORY"
        from etl_zone."DEALER_CATEGORIZATION_UAT"
        ) dc on dc."COUNTER_CODE" = lsom."CUSTOMER_CODE"
        where lsom."PP_CALL" = false
        and lsom."TRANSFERRED_TO_DEPOT" = false
        and lsom."DELIVERY_DUE_DATE" is not null
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_eta(cnxn, df):
    plant_zone = pd.read_sql(
        """
        select
        "Zone" as "ZONE",
        "ORG" as "PLANT_ID"
        from target."TGT_PLANT_LOOKUP" tpl
        where "ORG" like 'FG%'
        """,
        cnxn,
    )

    df = df.merge(plant_zone, on=["PLANT_ID"], how="left")
    df.replace(to_replace=[None], value=np.nan, inplace=True)
    df["ZONE"] = df["ZONE"].fillna("North")
    df["DISTANCE"] = df["DISTANCE"].fillna(0)

    df["ZONE"] = df["ZONE"].map({"North": 25, "South": 18, "East": 15})
    df["ZONE"] = df["ZONE"].fillna(25)
    df["TRAVEL_TIME_WITHOUT_STOP"] = df["DISTANCE"] / df["ZONE"]
    df.drop(columns=["ZONE"], inplace=True)

    df["PIT_STOP_WAITING_TIME"] = 0

    for i in range(0, len(df)):
        if df["TRAVEL_TIME_WITHOUT_STOP"][i] < 4:
            df["PIT_STOP_WAITING_TIME"][i] = 0.5
        elif (df["TRAVEL_TIME_WITHOUT_STOP"][i] >= 4) & (
            df["TRAVEL_TIME_WITHOUT_STOP"][i] < 8
        ):
            df["PIT_STOP_WAITING_TIME"][i] = 1
        elif (df["TRAVEL_TIME_WITHOUT_STOP"][i] >= 8) & (
            df["TRAVEL_TIME_WITHOUT_STOP"][i] < 12
        ):
            df["PIT_STOP_WAITING_TIME"][i] = 2
        elif (df["TRAVEL_TIME_WITHOUT_STOP"][i] >= 12) & (
            df["TRAVEL_TIME_WITHOUT_STOP"][i] <= 24
        ):
            df["PIT_STOP_WAITING_TIME"][i] = 2 + round(
                (df["TRAVEL_TIME_WITHOUT_STOP"][i] - 12) / 3
            )
        else:
            rem = df["TRAVEL_TIME_WITHOUT_STOP"][i] % 24
            quo = np.ceil(df["TRAVEL_TIME_WITHOUT_STOP"][i] / 24)
            if rem < 4:
                value = 0.5
            elif (rem >= 4) & (rem < 8):
                value = 1
            elif (rem >= 8) & (rem < 12):
                value = 2
            elif (rem >= 12) & (rem < 24):
                value = 2 + round(rem / 3)

            df["PIT_STOP_WAITING_TIME"][i] = (
                quo * (2 + round((df["TRAVEL_TIME_WITHOUT_STOP"][i] - 12) / 3)) + value
            )

    return df


def get_no_entry(cnxn, df):
    no_entry_time = pd.read_sql(
        """ select * from etl_zone."ETA_UPDATED_NO_ENTRY" """, cnxn
    )
    no_entry_time = no_entry_time[
        [
            "Route_ID",
            "START_TIME",
            "END_TIME",
            "START_TIME_NO_ENTRY_2",
            "END_TIME_NO_ENTRY_2",
            "START_TIME_NO_ENTRY_3",
            "END_TIME_NO_ENTRY_3",
        ]
    ]
    no_entry_time.rename({"Route_ID": "ROUTE_ID"}, axis=1, inplace=True)

    df = pd.merge(
        df, no_entry_time, on="ROUTE_ID", how="left"
    )  # merge on the basis of ROUTE_ID
    df[df.filter(regex=("START_|END_")).columns] = df[
        df.filter(regex=("START_|END_")).columns
    ].fillna(dt.time(0, 0))

    for idx, row in df.iterrows():
        if (row["END_TIME"].hour - row["START_TIME"].hour) > 0:
            if (row["DELIVERY_DUE_DATE"].time() > row["START_TIME"]) and (
                row["DELIVERY_DUE_DATE"].time() < row["END_TIME"]
            ):
                df.loc[idx, "DELIVERY_DUE_DATE"] = df.loc[
                    idx, "DELIVERY_DUE_DATE"
                ].replace(hour=row["END_TIME"].hour, minute=row["END_TIME"].minute)
                continue

        if (row["END_TIME_NO_ENTRY_2"].hour - row["START_TIME_NO_ENTRY_2"].hour) > 0:
            if (row["DELIVERY_DUE_DATE"].time() > row["START_TIME_NO_ENTRY_2"]) and (
                row["DELIVERY_DUE_DATE"].time() < row["END_TIME_NO_ENTRY_2"]
            ):
                df.loc[idx, "DELIVERY_DUE_DATE"] = df.loc[
                    idx, "DELIVERY_DUE_DATE"
                ].replace(
                    hour=row["END_TIME_NO_ENTRY_2"].hour,
                    minute=row["END_TIME_NO_ENTRY_2"].minute,
                )
                continue

        if (row["END_TIME_NO_ENTRY_3"].hour - row["START_TIME_NO_ENTRY_3"].hour) > 0:
            if (row["DELIVERY_DUE_DATE"].time() > row["START_TIME_NO_ENTRY_3"]) and (
                row["DELIVERY_DUE_DATE"].time() < row["END_TIME_NO_ENTRY_3"]
            ):
                df.loc[idx, "DELIVERY_DUE_DATE"] = df.loc[
                    idx, "DELIVERY_DUE_DATE"
                ].replace(
                    hour=row["END_TIME_NO_ENTRY_3"].hour,
                    minute=row["END_TIME_NO_ENTRY_3"].minute,
                )
                continue

    return df


def get_yard_time(cnxn):
    yard_time = pd.read_sql(
        """
    select
    substring("PLANT_NAME",1,3) as "PLANT_ID",
    substring("SLA_TO_DISPATCH",1,2)::float as "PLANT_TIME"
    from etl_zone."PLANT_DEPO_SLA_NEW" pdsn
    where "PRODUCT" = 'Cement'
    """,
        cnxn,
    )

    yard_time = yard_time.set_index("PLANT_ID")["PLANT_TIME"].to_dict()

    return yard_time


def get_ncr(cnxn, df):
    month = (datetime.now() - rd(months=1)).strftime("%Y-%m-01")

    ncr_data = pd.read_sql(
        f"""
        select
        "STATE" ,"DISTRICT" ,"BRAND", "PRODUCT" , "NCR"
        from semantic."NSH_CONTRIBUTION_MV" ncm
        where "MONTH" = '{month}'
        """,
        cnxn,
    )

    df = df.merge(ncr_data, on=["STATE", "DISTRICT", "BRAND", "PRODUCT"], how="left")
    df["NCR"] = df["NCR"].fillna(0)

    df["NCR_QUARTILE"] = pd.qcut(df["NCR"], 4, labels=False, duplicates="drop") + 1
    df["NCR_QUARTILE"] = df["NCR_QUARTILE"].fillna(1)

    return df


def run_pp_call_model(cnxn, plant_input=[]):
    time_now = datetime.strptime(
        datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M"
    )
    # time_now = datetime.strptime('2023-06-12 00:00', '%Y-%m-%d %H:%M')

    # plant_time = 13  # hours

    df = get_data(cnxn)

    if len(plant_input) > 0:
        df = df[df["PLANT_ID"].isin(plant_input)]

    df = get_ncr(cnxn, df)

    df = get_eta(cnxn, df)

    df = get_no_entry(cnxn, df)

    yard_time = get_yard_time(cnxn)

    df["YARD_TIME"] = df["PLANT_ID"].map(yard_time)

    if len(df) != 0:
        date_cols = ["ORDER_DATE", "DELIVERY_DUE_DATE"]
        for col in date_cols:
            df = convert_datetime(df, col)

        # df = convert_datetime(df, col = 'DELIVERY_DUE_DATE', ''
        df["TIME_REMAINING_TO_DELIVER"] = (
            ((df["DELIVERY_DUE_DATE"] - df["ORDER_DATE"]) / np.timedelta64(1, "h"))
            - df["PIT_STOP_WAITING_TIME"]
            - df["TRAVEL_TIME_WITHOUT_STOP"]
        )

        df["Order in Pipeline (Time)"] = (time_now - df["ORDER_DATE"]) / np.timedelta64(
            1, "h"
        )

        df["Score - Delivery Timeline"] = np.ceil(
            df["TIME_REMAINING_TO_DELIVER"] - df["YARD_TIME"]
        )

        df["RANK_ON_DELIVERY_TIME"] = df["Score - Delivery Timeline"].rank(
            method="min", ascending=False
        )

        df["Score - Order in pending time"] = np.ceil(
            (time_now - df["ORDER_DATE"]) / np.timedelta64(1, "h")
        )
        df["RANK_ON_ORDER_IN_PENDING_TIME"] = df["Score - Order in pending time"].rank(
            method="min"
        )
        df["NCR Score"] = df["NCR_QUARTILE"]

        df["CUSTOMER_CATEGORIZATION_SCORE"] = df["CUSTOMER_TYPE"].map(cust_map)

        df["ORDER_QUANTITY Score"] = df.apply(get_order_rank, axis=1)

        df["Party Score"] = df["DEALER_CATEGORY"].map(party_map)
        df[
            [
                "RANK_ON_DELIVERY_TIME",
                "RANK_ON_ORDER_IN_PENDING_TIME",
                "NCR Score",
                "CUSTOMER_CATEGORIZATION_SCORE",
                "ORDER_QUANTITY Score",
                "Party Score",
                "TRUCKS_PENDING_FOR_EPOD_CONFIRMATION",
            ]
        ] = df[
            [
                "RANK_ON_DELIVERY_TIME",
                "RANK_ON_ORDER_IN_PENDING_TIME",
                "NCR Score",
                "CUSTOMER_CATEGORIZATION_SCORE",
                "ORDER_QUANTITY Score",
                "Party Score",
                "TRUCKS_PENDING_FOR_EPOD_CONFIRMATION",
            ]
        ].fillna(
            0
        )
        df["TOTAL_SCORE"] = (
            df["RANK_ON_DELIVERY_TIME"]
            + df["RANK_ON_ORDER_IN_PENDING_TIME"]
            + df["NCR Score"]
            + df["CUSTOMER_CATEGORIZATION_SCORE"]
            + df["ORDER_QUANTITY Score"]
            + df["Party Score"]
            - df["TRUCKS_PENDING_FOR_EPOD_CONFIRMATION"]
        )

        plants = df.PLANT_ID.unique()
        final_df = pd.DataFrame()
        for plant in plants:
            plant_df = df[df.PLANT_ID == plant].copy()
            plant_df["PP_CALLING_SEQUENCE"] = (
                plant_df[
                    [
                        "TOTAL_SCORE",
                        "RANK_ON_DELIVERY_TIME",
                        "RANK_ON_ORDER_IN_PENDING_TIME",
                        "NCR_QUARTILE",
                        "CUSTOMER_CATEGORIZATION_SCORE",
                    ]
                ]
                .apply(tuple, axis=1)
                .rank(method="dense", ascending=False)
            )
            potential = plant_df["TOTAL_SCORE"]
            perc_50 = np.percentile(potential, q=50)
            plant_df["PRIORITIZED_ORDER"] = np.where(
                plant_df["TOTAL_SCORE"] >= perc_50, True, False
            )

            final_df = final_df.append(plant_df)

            final_df = final_df[
                [
                    "ORDER_MASTER_ID",
                    "PP_CALLING_SEQUENCE",
                    "PRIORITIZED_ORDER",
                    "TIME_REMAINING_TO_DELIVER",
                    "RANK_ON_DELIVERY_TIME",
                    "RANK_ON_ORDER_IN_PENDING_TIME",
                    "NCR_QUARTILE",
                    "CUSTOMER_CATEGORIZATION_SCORE",
                    "TOTAL_SCORE",
                ]
            ]

        df.drop(
            columns=[
                "ROUTE_ID",
                "DISTANCE",
                "TRAVEL_TIME_WITHOUT_STOP",
                "PIT_STOP_WAITING_TIME",
                "START_TIME",
                "END_TIME",
                "START_TIME_NO_ENTRY_2",
                "END_TIME_NO_ENTRY_2",
                "START_TIME_NO_ENTRY_3",
                "END_TIME_NO_ENTRY_3",
                "DEALER_CATEGORY",
                "STATE",
                "DISTRICT",
                "BRAND",
                "PRODUCT",
                "NCR",
            ],
            inplace=True,
        )

        createorupdate(
            final_df, "LP_SCHEDULING_PP_CALL_DTL", "ORDER_MASTER_ID", "ID", cnxn
        )
