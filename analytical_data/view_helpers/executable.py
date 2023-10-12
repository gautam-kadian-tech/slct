# -*- coding: utf-8 -*-
import random
import sys
import warnings
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta as td
from operator import contains

import numpy as np
import pandas as pd
import psycopg2
from django.conf import settings

from . import static
from .connection import connect_db, createorupdate

warnings.filterwarnings("ignore")


# yard_time = {
#     "FGA": 3,
#     "FGB": 3,
#     "FGC": 3,
#     "FGF": 3,
#     "FGG": 3,
#     "FGH": 3,
#     "FGI": 3,
#     "FGJ": 3,
#     "FGK": 3,
#     "FGL": 3,
#     "FGM": 3,
#     "FGN": 3,
#     "FGO": 3,
#     "FGP": 3,
#     "FGQ": 3,
#     "FGR": 3,
#     "FGS": 3,
#     "FGW": 3,
# }
# order_exec = {
#     "FGA": 6,
#     "FGB": 6,
#     "FGC": 6,
#     "FGF": 6,
#     "FGG": 6,
#     "FGH": 6,
#     "FGI": 6,
#     "FGJ": 6,
#     "FGK": 6,
#     "FGL": 6,
#     "FGM": 6,
#     "FGN": 6,
#     "FGO": 6,
#     "FGP": 6,
#     "FGQ": 6,
#     "FGR": 6,
#     "FGS": 6,
#     "FGW": 6,
# }

shift_map = {1: "00:01", 2: "08:01", 3: "16:01"}


def is_hour_between(start, end, now):
    is_between = False
    is_between |= start <= now <= end
    is_between |= end <= start and (start <= now or now <= end)

    return is_between


def check_shift(df):
    if df.TOD_EXECUTABLE_SHIFT >= pd.to_datetime(
        "00:00"
    ) and df.TOD_EXECUTABLE_SHIFT <= pd.to_datetime("08:00"):
        return 1
    elif df.TOD_EXECUTABLE_SHIFT >= pd.to_datetime(
        "08:00"
    ) and df.TOD_EXECUTABLE_SHIFT <= pd.to_datetime("16:00"):
        return 2
    else:
        return 3


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


# def check_date(df):
#     date = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')

#     date = '2023-01-23 00:00'
#     date = datetime.strptime(date, '%Y-%m-%d %H:%M')
#     if df['TS'] < date:
#         return date
#     return pd.to_datetime(df['TS'])


def check_date(cnxn, df, date, plant_input=[]):
    df.sort_values(["PLANT_ID", "PP_CALLING_SEQUENCE"], inplace=True)

    if len(plant_input) == 0:
        plants = df.PLANT_ID.unique()
    else:
        plants = plant_input
    final_df = pd.DataFrame()

    for plant in plants:
        packer_constraints = get_packer_constraints(cnxn, plant)
        exec_orders = get_exec_orders(cnxn, plant, date.strftime("%Y-%m-%d"))

        shift_qty_max = packer_constraints["CAPACITY"].sum() * 5 * 3
        temp_df = df[df["PLANT_ID"] == plant]

        start_date = date

        qty = exec_orders[
            (exec_orders["EXECUTABLE_DATE"] == start_date.strftime("%Y-%m-%d"))
        ]["ORDER_QUANTITY"].sum()

        for idx, row in temp_df.iterrows():
            if row["ORDER_EXECUTABLE"] != 1:
                if row["TS"] <= date:
                    if (row["ORDER_QUANTITY"] + qty) <= shift_qty_max:
                        qty += row["ORDER_QUANTITY"]
                    else:
                        start_date = start_date + td(days=1)

                        qty = exec_orders[
                            (
                                exec_orders["EXECUTABLE_DATE"]
                                == start_date.strftime("%Y-%m-%d")
                            )
                        ]["ORDER_QUANTITY"].sum()

                    d = start_date.strftime("%Y-%m-%d")
                    s = "00:00"

                    temp_df.loc[idx, "TS"] = pd.to_datetime(
                        f"{d} {s}", format="%Y-%m-%d %H:%M"
                    )

        final_df = final_df.append(temp_df, ignore_index=True)

    return final_df


def check_date1(cnxn, df, date, plant_input=[]):
    df.sort_values(["PLANT_ID", "PP_CALLING_SEQUENCE"], inplace=True)

    if len(plant_input) == 0:
        plants = df.PLANT_ID.unique()
    else:
        plants = plant_input
    final_df = pd.DataFrame()

    if is_hour_between(
        date.replace(hour=0, minute=0).time(),
        date.replace(hour=8, minute=0).time(),
        date.time(),
    ):
        shift = 1
    elif is_hour_between(
        date.replace(hour=8, minute=0).time(),
        date.replace(hour=16, minute=0).time(),
        date.time(),
    ):
        shift = 2
    else:
        shift = 3

    for plant in plants:
        packer_constraints = get_packer_constraints(cnxn, plant)
        exec_orders = get_exec_orders(cnxn, plant, date.strftime("%Y-%m-%d"))

        shift_qty_max = packer_constraints["CAPACITY"].sum() * 5
        temp_df = df[df["PLANT_ID"] == plant]

        start_shift = shift
        start_date = date

        qty = exec_orders[
            (exec_orders["EXECUTABLE_DATE"] == start_date.strftime("%Y-%m-%d"))
            & (exec_orders["EXECUTABLE_SHIFT"] == start_shift)
        ]["ORDER_QUANTITY"].sum()

        for idx, row in temp_df.iterrows():
            if row["ORDER_EXECUTABLE"] == 1:
                if row["TS"] <= date:
                    if (row["ORDER_QUANTITY"] + qty) <= shift_qty_max:
                        qty += row["ORDER_QUANTITY"]
                    else:
                        if start_shift != 3:
                            start_shift += 1
                        else:
                            start_shift = 1
                            start_date = start_date + td(days=1)
                        qty = exec_orders[
                            (
                                exec_orders["EXECUTABLE_DATE"]
                                == start_date.strftime("%Y-%m-%d")
                            )
                            & (exec_orders["EXECUTABLE_SHIFT"] == start_shift)
                        ]["ORDER_QUANTITY"].sum()

                    d = start_date.strftime("%Y-%m-%d")
                    s = shift_map[start_shift]

                    temp_df.loc[idx, "TS"] = pd.to_datetime(
                        f"{d} {s}", format="%Y-%m-%d %H:%M"
                    )

        final_df = final_df.append(temp_df, ignore_index=True)

    return final_df


def convert_data_to_upper(df):
    cols = df.select_dtypes("O")

    for col in cols:
        df[col] = df[col].str.upper()
    return df


def calculate(
    qn_order_master_all,
    vehicle_constraints,
    plant_constraints,
    order_club_df,
    df_qc,
    plant_input=[],
):
    if len(plant_input) == 0:
        plants = qn_order_master_all.PLANT_ID.unique()
    else:
        plants = plant_input
    final_df = pd.DataFrame()
    # new_df = pd.DataFrame()
    date = datetime.strptime(
        datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M"
    )

    # date = "2023-01-23 00:00"
    # date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    for plant in plants:
        q = 0
        print(plant)
        qn_order_master = qn_order_master_all.loc[
            qn_order_master_all.PLANT_ID == plant
        ].reset_index(drop=True)

        # qn_order_master = qn_order_master.loc[qn_order_master .PACKAGING=='LOOSE']
        while len(qn_order_master[qn_order_master["row_processed"] == False]) != 0:
            # print(len(qn_order_master[qn_order_master['row_processed']==False]))
            for idx, qn in qn_order_master[
                qn_order_master["row_processed"] == False
            ].iterrows():
                qn_order_master.loc[idx, "row_processed"] = True

                qty_served = qn_order_master.loc[
                    (qn_order_master["ORDER_EXECUTABLE"] == 1)
                    & (qn["TS_DATE"] == qn_order_master["TS_DATE"])
                    & (qn_order_master["PLANT_ID"] == qn["PLANT_ID"][:3])
                    & (qn_order_master["GRADE"] == qn["GRADE"])
                ]["ORDER_QUANTITY"].sum()
                qty_served_dist = qn_order_master.loc[
                    (qn_order_master["ORDER_EXECUTABLE"] == 1)
                    & (qn_order_master["PLANT_ID"] == qn["PLANT_ID"][:3])
                    & (qn_order_master["GRADE"] == qn["GRADE"])
                    & (qn_order_master["BRAND"] == qn["BRAND"])
                    & (qn["TS_DATE"] == qn_order_master["TS_DATE"])
                    & (qn_order_master["SHIP_STATE"] == qn["SHIP_STATE"])
                    & (qn_order_master["SHIP_DISTRICT"] == qn["SHIP_DISTRICT"])
                ]["ORDER_QUANTITY"].sum()

                dpc = plant_constraints.loc[
                    (plant_constraints["PLANT_ID"] == qn["PLANT_ID"][:3])
                    & (plant_constraints["GRADE"] == qn["GRADE"])
                ]["CAPACITY"].sum()
                qty_cum = qty_served + qn["ORDER_QUANTITY"]
                qty_cum_dist = qty_served_dist + qn["ORDER_QUANTITY"]

                qc = df_qc.loc[
                    (df_qc["ORG"] == qn["PLANT_ID"][:3])
                    & (df_qc["BRAND"] == qn["BRAND"])
                    & (df_qc["SHIP_STATE"] == qn["SHIP_STATE"])
                    & (df_qc["SHIP_DISTRICT"] == qn["SHIP_DISTRICT"]),
                    "INV_QTY",
                ]

                if qc.empty:
                    qc = 200
                else:
                    qc = qc.item()
                qc = round(qc, 0)
                # print(qn['ORDER_ID'], qn['PACKAGING'])
                if ((qty_cum_dist <= qc * 1.1) and (dpc > 0)) or (
                    qty_cum <= (dpc / 24) * (24 - date.hour)
                    and (qty_cum_dist <= qc * 5)
                ):
                    list_of_unique_values_loose = vehicle_constraints.loc[
                        (vehicle_constraints["DATE"] == qn["TS_DATE"])
                        & (vehicle_constraints["PLANT"] == qn["PLANT_ID"][:3])
                        & (vehicle_constraints["VEHICLE_TYPE"] == "BULKER")
                    ]["VEHICLE_SIZE"].unique()

                    list_of_unique_values_packed = vehicle_constraints.loc[
                        (vehicle_constraints["DATE"] == qn["TS_DATE"])
                        & (vehicle_constraints["PLANT"] == qn["PLANT_ID"][:3])
                        & (vehicle_constraints["VEHICLE_TYPE"] != "BULKER")
                    ]["VEHICLE_SIZE"].unique()
                    # print(qn['ORDER_ID'], qn['PACKAGING'])
                    if "LOOSE" == qn["PACKAGING"]:
                        # print('---------')
                        # print(qn['ORDER_ID'])
                        # print(vehicle_constraints.loc[(vehicle_constraints['DATE'] == qn['TS_DATE']) & (vehicle_constraints['VEHICLE_TYPE'] == 'BULKER')])
                        # print((vehicle_constraints['PLANT'] == qn["PLANT_ID"][:3]) & (vehicle_constraints['VEHICLE_TYPE'] == 'BULKER'))

                        list_of_unique_values = list_of_unique_values_loose
                        # print(list_of_unique_values)
                    else:
                        list_of_unique_values = list_of_unique_values_packed
                    if len(list_of_unique_values) == 0:
                        # print('b')
                        continue

                    if qn["ORDER_QUANTITY"] in list_of_unique_values:
                        vhcl_detail = vehicle_constraints.loc[
                            (vehicle_constraints["DATE"] == qn["TS_DATE"])
                            & (vehicle_constraints["PLANT"] == qn["PLANT_ID"][:3])
                            & (
                                vehicle_constraints["VEHICLE_SIZE"]
                                == qn["ORDER_QUANTITY"]
                            )
                        ][["CURRENT_VEHICLES", "VEHICLE_TYPE"]]
                        check_truck = vhcl_detail["CURRENT_VEHICLES"].iloc[0]
                        check_type = vhcl_detail["VEHICLE_TYPE"].iloc[0]
                        pkg = qn["PACKAGING"]
                        if "LOOSE" in pkg:  # CHANGED
                            qn_order_master.loc[idx, "ORDER_EXECUTABLE"] = 1  # CHANGED
                            if check_truck > 0:  # CHANGED
                                vehicle_constraints.loc[
                                    (vehicle_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        vehicle_constraints["PLANT"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (
                                        vehicle_constraints["VEHICLE_SIZE"]
                                        == qn["ORDER_QUANTITY"]
                                    )
                                    & (vehicle_constraints["VEHICLE_TYPE"] == "BULKER"),
                                    "CURRENT_VEHICLES",
                                ] -= 1

                                plant_constraints.loc[
                                    (plant_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        plant_constraints["PLANT_ID"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (plant_constraints["GRADE"] == qn["GRADE"]),
                                    "CURRENT_CAPACITY",
                                ] -= qn["ORDER_QUANTITY"]
                                qn_order_master.loc[idx, "TRUCK_AVAILABLE"] = 1

                            else:
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 0  # CHANGED
                        else:
                            qn_order_master.loc[idx, "ORDER_EXECUTABLE"] = 1  # CHANGED
                            if check_truck > 0:  # CHANGED
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 1  # CHANGED
                                vehicle_constraints.loc[
                                    (vehicle_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        vehicle_constraints["PLANT"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (
                                        vehicle_constraints["VEHICLE_SIZE"]
                                        == qn["ORDER_QUANTITY"]
                                    ),
                                    "CURRENT_VEHICLES",
                                ] -= 1

                                plant_constraints.loc[
                                    (plant_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        plant_constraints["PLANT_ID"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (plant_constraints["GRADE"] == qn["GRADE"]),
                                    "CURRENT_CAPACITY",
                                ] -= qn["ORDER_QUANTITY"]
                            else:
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 0  # CHANGED

                    elif qn["ORDER_QUANTITY"] > max(list_of_unique_values):
                        remaining_qty = qn["ORDER_QUANTITY"] - max(
                            list_of_unique_values
                        )
                        # print(list_of_unique_values)
                        qn_order_master.loc[idx, "ORDER_QUANTITY"] = max(
                            list_of_unique_values
                        )
                        vhcl_detail = vehicle_constraints.loc[
                            (vehicle_constraints["DATE"] == qn["TS_DATE"])
                            & (vehicle_constraints["PLANT"] == qn["PLANT_ID"][:3])
                            & (
                                vehicle_constraints["VEHICLE_SIZE"]
                                == max(list_of_unique_values)
                            )
                        ][["CURRENT_VEHICLES", "VEHICLE_TYPE"]]
                        check_truck = vhcl_detail["CURRENT_VEHICLES"].iloc[0]
                        check_type = vhcl_detail["VEHICLE_TYPE"].iloc[0]
                        pkg = qn["PACKAGING"]
                        if "LOOSE" in pkg:
                            qn_order_master.loc[idx, "ORDER_EXECUTABLE"] = 1  # CHANGED
                            qn_order_master.loc[len(qn_order_master)] = qn  # CHANGED
                            qn_order_master.loc[
                                len(qn_order_master) - 1, "ORDER_QUANTITY"
                            ] = remaining_qty  # CHANGED

                            qn_order_master.loc[
                                len(qn_order_master) - 1, "row_processed"
                            ] = False  # CHANGED
                            # print('abc')
                            if check_truck > 0:  # CHANGED
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 1  # CHANGED
                                vehicle_constraints.loc[
                                    (vehicle_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        vehicle_constraints["PLANT"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (
                                        vehicle_constraints["VEHICLE_SIZE"]
                                        == max(list_of_unique_values)
                                    )
                                    & (vehicle_constraints["VEHICLE_TYPE"] == "BULKER"),
                                    "CURRENT_VEHICLES",
                                ] -= 1

                                plant_constraints.loc[
                                    (plant_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        plant_constraints["PLANT_ID"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (plant_constraints["GRADE"] == qn["GRADE"]),
                                    "CURRENT_CAPACITY",
                                ] -= qn["ORDER_QUANTITY"]
                                # print(qn_order_master.loc[len(qn_order_master)])
                            else:
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 0  # CHANGED

                        else:
                            qn_order_master.loc[idx, "ORDER_EXECUTABLE"] = 1  # CHANGED
                            qn_order_master.loc[len(qn_order_master)] = qn  # CHANGED
                            qn_order_master.loc[
                                len(qn_order_master) - 1, "ORDER_QUANTITY"
                            ] = remaining_qty  # CHANGED
                            qn_order_master.loc[
                                len(qn_order_master) - 1, "row_processed"
                            ] = False  # CHANGED
                            # print('def')
                            if check_truck > 0:  # CHANGED
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 1  # CHANGED
                                vehicle_constraints.loc[
                                    (vehicle_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        vehicle_constraints["PLANT"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (
                                        vehicle_constraints["VEHICLE_SIZE"]
                                        == max(list_of_unique_values)
                                    ),
                                    "CURRENT_VEHICLES",
                                ] -= 1

                                plant_constraints.loc[
                                    (plant_constraints["DATE"] == qn["TS_DATE"])
                                    & (
                                        plant_constraints["PLANT_ID"]
                                        == qn["PLANT_ID"][:3]
                                    )
                                    & (plant_constraints["GRADE"] == qn["GRADE"]),
                                    "CURRENT_CAPACITY",
                                ] -= qn["ORDER_QUANTITY"]
                            else:
                                qn_order_master.loc[
                                    idx, "TRUCK_AVAILABLE"
                                ] = 0  # CHANGED

                    else:
                        # df = df.drop(df[df.score < 50].index)
                        unique_data = order_club_df.loc[
                            (order_club_df["plant"] == qn["PLANT_ID"][:3])
                            & (order_club_df["ship_district"] == qn["SHIP_DISTRICT"])
                            & (order_club_df["ship_state"] == qn["SHIP_STATE"])
                            & (order_club_df["brand"] == qn["BRAND"])
                            & (order_club_df["clubbed"] == 0)
                        ]

                        if unique_data.empty:
                            order_club_df.loc[len(order_club_df)] = [
                                qn["ORDER_ID"],
                                idx,
                                qn["ORDER_QUANTITY"],
                                qn["PLANT_ID"],
                                qn["SHIP_STATE"],
                                qn["SHIP_DISTRICT"],
                                qn["BRAND"],
                                0,
                            ]
                        elif qn["ORDER_ID"] in order_club_df["ORDER_ID"]:
                            if (
                                qn["DELIVERY_DUE_DATE"] - qn["ORDER_DATE"]
                            ).dt.total_seconds() <= 0:
                                order_club_df.drop(
                                    order_club_df[
                                        (order_club_df["ORDER_ID"] == qn["ORDER_ID"])
                                    ].index.to_list()
                                )
                                qn_order_master.loc[idx, "ORDER_EXECUTABLE"] = 0
                        else:
                            unique_data = unique_data.loc[unique_data.clubbed == 0]
                            for ind, data in unique_data.iterrows():
                                if data["clubbed"] == 1:
                                    continue
                                elif (
                                    data["ORDER_QUANTITY"] + qn["ORDER_QUANTITY"]
                                    in list_of_unique_values
                                ):
                                    qn_order_master.loc[
                                        [idx, data["order_index"]], "ORDER_EXECUTABLE"
                                    ] = 0
                                    qn_order_master.loc[
                                        [idx, data["order_index"]], "ORDER_CLUBBED"
                                    ] = 1
                                    qn_order_master.loc[
                                        [idx, data["order_index"]], "CLUB_ID"
                                    ] = random.randint(100, 100000)
                                    unique_data.loc[
                                        data["order_index"]
                                        == unique_data["order_index"],
                                        "clubbed",
                                    ] = 1
                                    order_club_df.loc[
                                        data["order_index"]
                                        == order_club_df["order_index"],
                                        "clubbed",
                                    ] = 1
                                    # break

                else:
                    q += qn["ORDER_QUANTITY"]
                    qn_order_master.at[idx, "ORDER_EXECUTABLE"] = 0
                    # print(qn['ORDER_ID'])
                    # print(8)
                # except Exception as e:
                #     print('Exception in loop:'+str(e))
        # break
        final_df = final_df.append(qn_order_master)

    return final_df, vehicle_constraints, plant_constraints, order_club_df, df_qc


def get_vehicle_constraints(cnxn, date_):
    sql = f"""
    select * from etl_zone."LP_SCHEDULING_VEHICLE_CONSTRAINTS"
    where "DATE" >= '{date_}'
    """

    vehicle_constraints = pd.read_sql(sql, cnxn)

    vehicle_constraints.loc[
        vehicle_constraints["CURRENT_VEHICLES"].isna(), "CURRENT_VEHICLES"
    ] = vehicle_constraints.loc[
        vehicle_constraints["CURRENT_VEHICLES"].isna(), "NO_OF_VEHICLES"
    ]

    vehicle_constraints["DATE"] = pd.to_datetime(vehicle_constraints["DATE"])

    vehicle_constraints = convert_data_to_upper(vehicle_constraints)

    return vehicle_constraints


def get_plant_constraints(cnxn, date_):
    sql = f"""
    select
    "ID","DATE" , "PLANT_ID" , "GRADE" ,"CAPACITY" ,coalesce("CURRENT_CAPACITY","CAPACITY") as "CURRENT_CAPACITY"
    from etl_zone."LP_SCHEDULING_PLANT_CONSTRAINTS"
    where "DATE" >= '{date_}'
    """

    plant_constraints = pd.read_sql(sql, cnxn)

    plant_constraints["DATE"] = pd.to_datetime(plant_constraints["DATE"])

    plant_constraints = convert_data_to_upper(plant_constraints)

    return plant_constraints


def get_packer_constraints(cnxn, plant):
    sql = f"""
        select distinct on ("PACKER")
        "PACKER","PACKER_RATED_CAPACITY_MT/HR" as "CAPACITY"
        from etl_zone."PACKER_RATED_CAPACITY" prc
        where "PLANT" = '{plant}'
    """

    packer_constraints = pd.read_sql(sql, cnxn)

    return packer_constraints


def get_exec_orders(cnxn, plant, date_):
    sql = f"""
        select "ID","ORDER_QUANTITY","EXECUTABLE_DATE","EXECUTABLE_SHIFT" from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom
        inner join (
        select "ORDER_MASTER_ID","EXECUTABLE_DATE","EXECUTABLE_SHIFT" from etl_zone."LP_SCHEDULING_EXECUTABLE_DTL"
        where "EXECUTABLE_DATE" >= '{date_}'
        ) lsed on lsom."ID" = lsed."ORDER_MASTER_ID"
        where "AUTO_TAGGED_SOURCE" = '{plant}'
    """

    exec_orders = pd.read_sql(sql, cnxn)

    return exec_orders


def get_order_master(cnxn, date_):
    sql = f"""
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
        case
            when lsom."CHANGED_MODE" is null then lsom."AUTO_TAGGED_MODE"
            else lsom."CHANGED_MODE"
        end as "ORIGINAL_MODE",
        lsom."ORDER_ID" as "ORDER_ID_1",
        lsom."ORDER_HEADER_ID",
        lsom."ORDER_LINE_ID",
        lsom."BRAND",
        lsom."GRADE",
        lsom."PACKAGING",
        lsom."PACK_TYPE",
        lsom."ORDER_TYPE",
        lsom."SHIP_STATE",
        lsom."SHIP_DISTRICT",
        lsom."SHIP_CITY",
        lsom."CUSTOMER_CODE",
        lsom."CUST_SUB_CAT",
        lsom."CUST_NAME",
        lsom."AUTO_TAGGED_SOURCE",
        lsom."AUTO_TAGGED_MODE",
        lsom."SALES_OFFICER_CHANGED_SOURCE",
        lsom."DISPATCH_DUE_DATE",
        lsom."ORDER_STATUS",
        lsom."FULL_TRUCK_LOAD",
        case lsom."ORDER_CLUBBED"
            when true then 1
            else 0
        end as "ORDER_CLUBBED",
        lsom."CLUB_ID",
        lsom."DI_GENERATED",
        case lsom."ORDER_EXECUTABLE"
            when true then 1
            else 0
        end as "ORDER_EXECUTABLE",
        lsom."SELF_CONSUMPTION_FLAG",
        lsom."PP_CALL",
        lsom."REMARKS",
        lsom."Reason",
        lsom."DELIVERY_ID",
        lsom."DELIVERY_DETAIL_ID" as "ORDER_ID",
        lsom."ORG_ID",
        lsom."ORGANIZATION_ID",
        lsom."INVENTORY_ITEM_ID",
        lsom."Dispatched Quantity",
        lsom."DILINK_CREATION_DT",
        lsom."TAX_INVOICE_DATE",
        lsom."SHIP_TALUKA",
        lsom."Full Address",
        lsom."VEHICLE_TYPE",
        lsom."VEHICLE_NUMBER",
        lsom."PLANT_NAME",
        lsom."Ship_from_zone",
        lsom."WAREHOUSE",
        lsom."SHIP_TO_ORG_ID",
        lsom."FREIGHTTERMS",
        lsom."FOB",
        lsom."TOKEN_ID",
        lsom."ROUTE",
        lsom."SOURCE_LOCATION_ID",
        lsom."SHIPINGLOCATION",
        lsom."SALES_ORDER_TYPE",
        lsom."CHANGED_SOURCE",
        lsom."CHANGED_MODE",
        lsom."TRANSFERRED_TO_DEPOT",
        lscc."DELIVERY_TIME",
        lscc."PP_CALLING_SEQUENCE"
        from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom
        inner join(
        select
        "ORDER_MASTER_ID",
        "TIME_REMAINING_TO_DELIVER" as "DELIVERY_TIME",
        "PP_CALLING_SEQUENCE"
        from
        etl_zone."LP_SCHEDULING_PP_CALL_DTL"
        where "PP_CALL_DATE" is null
        or "PP_CALL_DATE" >= '{date_}'
        ) lscc on lscc."ORDER_MASTER_ID" = lsom."ID"
        where lsom."TRANSFERRED_TO_DEPOT" = false
        and lsom."DELIVERY_DUE_DATE" is not null
        and lsom."PP_CALL" = false
        and lsom."DI_GENERATED" = false
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_order_master_processed(cnxn, order_id):
    sql = f"""
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
        case
            when lsom."CHANGED_MODE" is null then lsom."AUTO_TAGGED_MODE"
            else lsom."CHANGED_MODE"
        end as "ORIGINAL_MODE",
        lsom."ORDER_ID",
        lsom."ORDER_HEADER_ID",
        lsom."ORDER_LINE_ID",
        lsom."BRAND",
        lsom."GRADE",
        lsom."PACKAGING",
        lsom."PACK_TYPE",
        lsom."ORDER_TYPE",
        lsom."SHIP_STATE",
        lsom."SHIP_DISTRICT",
        lsom."SHIP_CITY",
        lsom."CUSTOMER_CODE",
        lsom."CUST_SUB_CAT",
        lsom."CUST_NAME",
        lsom."AUTO_TAGGED_SOURCE",
        lsom."AUTO_TAGGED_MODE",
        lsom."SALES_OFFICER_CHANGED_SOURCE",
        lsom."DISPATCH_DUE_DATE",
        lsom."ORDER_STATUS",
        lsom."FULL_TRUCK_LOAD",
        lsom."ORDER_CLUBBED",
        lsom."CLUB_ID",
        lsom."DI_GENERATED",
        case lsom."ORDER_EXECUTABLE"
            when true then 1
            else 0
        end as "ORDER_EXECUTABLE",
        lsom."SELF_CONSUMPTION_FLAG",
        lsom."PP_CALL",
        lsom."REMARKS",
        lsom."Reason",
        lsom."DELIVERY_ID",
        lsom."DELIVERY_DETAIL_ID",
        lsom."ORG_ID",
        lsom."ORGANIZATION_ID",
        lsom."INVENTORY_ITEM_ID",
        lsom."Dispatched Quantity",
        lsom."DILINK_CREATION_DT",
        lsom."TAX_INVOICE_DATE",
        lsom."SHIP_TALUKA",
        lsom."Full Address",
        lsom."VEHICLE_TYPE",
        lsom."VEHICLE_NUMBER",
        lsom."PLANT_NAME",
        lsom."Ship_from_zone",
        lsom."WAREHOUSE",
        lsom."SHIP_TO_ORG_ID",
        lsom."FREIGHTTERMS",
        lsom."FOB",
        lsom."TOKEN_ID",
        lsom."ROUTE",
        lsom."SOURCE_LOCATION_ID",
        lsom."SHIPINGLOCATION",
        lsom."SALES_ORDER_TYPE",
        lsom."CHANGED_SOURCE",
        lsom."CHANGED_MODE",
        lsom."TRANSFERRED_TO_DEPOT",
        lscc."DELIVERY_TIME",
        lscc."TOTAL_SCORE",
        lscc."RANK_ON_DELIVERY_TIME",
        lscc."RANK_ON_ORDER_IN_PENDING_TIME",
        lscc."NCR_QUARTILE",
        lscc."CUSTOMER_CATEGORIZATION_SCORE"
        from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom
        inner join(
        select
        "ORDER_MASTER_ID",
        "TIME_REMAINING_TO_DELIVER" as "DELIVERY_TIME",
        "TOTAL_SCORE",
        "RANK_ON_DELIVERY_TIME",
        "RANK_ON_ORDER_IN_PENDING_TIME",
        "NCR_QUARTILE",
        "CUSTOMER_CATEGORIZATION_SCORE"
        from
        etl_zone."LP_SCHEDULING_PP_CALL_DTL"
        ) lscc on lscc."ORDER_MASTER_ID" = lsom."ID"
        where lsom."ORDER_ID" in {order_id}
    """
    df = pd.read_sql(sql, cnxn)

    return df


def run_executable_model(cnxn, plant_input=[]):
    date = datetime.strptime(
        datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M"
    )

    # date = "2023-01-23 00:00"
    # date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    date_ = date.date().strftime("%Y-%m-%d")
    cond_date = date + td(days=2)

    vehicle_constraints = get_vehicle_constraints(cnxn, date_)

    plant_constraints = get_plant_constraints(cnxn, date_)

    # df_qc = pd.read_csv(settings.FEB_DATA_FOR_SCRIPT)
    df_qc = pd.read_sql(
        """
    select
    "PLANT" as "ORG"
    ,"SHIP_STATE"
    ,"SHIP_DISTRICT"
    ,"BRAND"
    ,"INV_QTY"
    from etl_zone."LP_SCHEDULING_DPC" lsd
    """,
        cnxn,
    )
    df_qc = convert_data_to_upper(df_qc)

    qn_order_master_ = get_order_master(cnxn, date_)
    if len(qn_order_master_) == 0:
        return

    if len(qn_order_master_) == 0:
        return

    try:
        qn_order_master_.columns = qn_order_master_.columns.str.upper()
        order_club_df = pd.DataFrame(
            columns=[
                "ORDER_ID",
                "order_index",
                "ORDER_QUANTITY",
                "plant",
                "ship_state",
                "ship_district",
                "brand",
                "clubbed",
            ]
        )
        qn_order_master_ = qn_order_master_.loc[
            qn_order_master_.ORIGINAL_MODE.str.contains("ROAD")
        ]
    except Exception as e:
        print("Exception2:" + str(e))

    qn_order_master_["DELIVERY_DUE_DATE"] = pd.to_datetime(
        qn_order_master_["DELIVERY_DUE_DATE"], format="%Y-%m-%d %H:%M"
    )
    qn_order_master_["ORDER_DATE"] = pd.to_datetime(
        qn_order_master_["ORDER_DATE"], format="%Y-%m-%d %H:%M"
    )

    yard_time = get_yard_time(cnxn)
    for idx, row in qn_order_master_.iterrows():
        sub = yard_time[row["PLANT_ID"][:3]] + (0.9 * row["DELIVERY_TIME"])
        qn_order_master_.loc[[idx], "TS"] = row["DELIVERY_DUE_DATE"] - pd.Timedelta(
            hours=sub
        )

    # qn_order_master_['TS'] = qn_order_master_.apply(check_date, axis=1)
    qn_order_master_ = check_date(cnxn, qn_order_master_, date, plant_input)
    qn_order_master_["TS_DATE"] = qn_order_master_["TS"].dt.date
    qn_order_master_["TS_DATE"] = pd.to_datetime(
        qn_order_master_["TS_DATE"], format="%Y-%m-%d"
    )

    qn_order_master_["row_processed"] = False

    final_df, vehicle_constraints, plant_constraints, order_club_df, df_qc = calculate(
        qn_order_master_,
        vehicle_constraints,
        plant_constraints,
        order_club_df,
        df_qc,
        plant_input,
    )
    final_df.rename(
        columns={"ORDER_ID": "DELIVERY_DETAIL_ID", "ORDER_ID_1": "ORDER_ID"},
        inplace=True,
    )
    final_df[["ORDER_EXECUTABLE", "ORDER_CLUBBED"]] = final_df[
        ["ORDER_EXECUTABLE", "ORDER_CLUBBED"]
    ].fillna(0)

    final_df.loc[final_df["TS"].dt.date > cond_date.date(), "ORDER_EXECUTABLE"] = 0
    final_df["DISPATCH_DUE_DATE"] = final_df["TS"]

    order_id = tuple(final_df["ORDER_ID"].unique().tolist())

    order_master = final_df[static.order_master_cols]
    order_master.columns = static.order_master_cols_db
    order_master["ORDER_EXECUTABLE"] = order_master["ORDER_EXECUTABLE"].apply(
        lambda x: True if x == 1 else False
    )
    order_master["ORDER_CLUBBED"] = order_master["ORDER_CLUBBED"].apply(
        lambda x: True if x == 1 else False
    )
    order_master["CUST_NAME"] = order_master["CUST_NAME"].str.replace("'", "")
    order_master["Full Address"] = order_master["Full Address"].str.replace("'", "")

    # order_master[static.order_master_cols_db] = order_master[static.order_master_cols_db].fillna(psycopg2.extensions.AsIs('NULL').getquoted())
    createorupdate(
        order_master[order_master["ORDER_CLUBBED"] != True].drop(columns=["CLUB_ID"]),
        "LP_SCHEDULING_ORDER_MASTER",
        "ID",
        "ID",
        cnxn,
    )

    if len(order_master[order_master["ORDER_CLUBBED"] == True]) > 0:
        createorupdate(
            order_master[order_master["ORDER_CLUBBED"] == True],
            "LP_SCHEDULING_ORDER_MASTER",
            "ID",
            "ID",
            cnxn,
        )

    exec_out = get_order_master_processed(cnxn, order_id)
    exec_out = exec_out.merge(
        final_df[["ORDER_MASTER_ID", "TS", "PP_CALLING_SEQUENCE"]], on="ORDER_MASTER_ID"
    )

    # exec_out.to_csv("ds_out.csv", index=False)

    exec_out = exec_out.loc[exec_out.ORDER_EXECUTABLE == 1]
    exec_out = check_date1(cnxn, exec_out, date, plant_input)
    # exec_out.to_csv("exec_out.csv", index=False)
    if exec_out.empty:
        print("No executable orders")

    else:
        # ----------------------------------------------------------------------------
        # [ 'ORDER_MASTER_ID', 'PP_CALLING_SEQUENCE', 'PRIORITIZED_ORDER',  'RANK_ON_DELIVERY_TIME', 'RANK_ON_ORDER_IN_PENDING_TIME', 'NCR_QUARTILE', 'CUSTOMER_CATEGORIZATION_SCORE', 'TOTAL_SCORE']

        plants = exec_out.PLANT_ID.unique()
        rank_df = pd.DataFrame()
        for plant in plants:
            plant_df = exec_out.loc[exec_out.PLANT_ID == plant]
            plant_df["EXEC_CALLING_SEQUENCE"] = (
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
            rank_df = rank_df.append(plant_df)

        rank_df = rank_df[
            ["ORDER_MASTER_ID", "EXEC_CALLING_SEQUENCE"]
        ].drop_duplicates()

        createorupdate(
            rank_df, "LP_SCHEDULING_PP_CALL_DTL", "ORDER_MASTER_ID", "ID", cnxn
        )

        exec_out["EXECUTABLE_DATE"] = pd.to_datetime(exec_out["TS"]).dt.date
        exec_out["EXECUTABLE_SHIFT_TIME"] = pd.to_datetime(exec_out["TS"]).dt.time

        exec_out["TOD_EXECUTABLE_SHIFT"] = pd.to_datetime(
            exec_out["EXECUTABLE_SHIFT_TIME"].astype(str)
        )
        exec_out["EXECUTABLE_SHIFT"] = exec_out.apply(check_shift, axis=1)
        # exec_out.drop(columns=['TOD_EXECUTABLE_SHIFT', 'EXECUTABLE_SHIFT_TIME'], inplace=True)

        exec_out = exec_out[
            [
                "ORDER_MASTER_ID",
                "EXECUTABLE_DATE",
                "EXECUTABLE_SHIFT",
                "PLANT_ID",
                "AUTO_TAGGED_MODE",
                "TOTAL_SCORE",
            ]
        ]

        exec_out.columns = [
            "ORDER_MASTER_ID",
            "EXECUTABLE_DATE",
            "EXECUTABLE_SHIFT",
            "ORIGINAL_SOURCE",
            "ORIGINAL_MODE",
            "TOTAL_SCORE",
        ]

        exec_out["EXECUTABLE_DATE"] = pd.to_datetime(exec_out["EXECUTABLE_DATE"])

        createorupdate(
            exec_out, "LP_SCHEDULING_EXECUTABLE_DTL", "ORDER_MASTER_ID", "ID", cnxn
        )
    if len(vehicle_constraints) != 0:
        createorupdate(
            vehicle_constraints, "LP_SCHEDULING_VEHICLE_CONSTRAINTS", "ID", "ID", cnxn
        )
    createorupdate(
        plant_constraints, "LP_SCHEDULING_PLANT_CONSTRAINTS", "ID", "ID", cnxn
    )
