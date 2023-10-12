import time
import warnings
from datetime import datetime as dt
from datetime import timedelta as td

import numpy as np
import pandas as pd
import psycopg2
import pulp as p

from .connection import connect_db

warnings.filterwarnings("ignore")
# server = '10.20.2.5'
# database = 'citus'
# username = 'citus'
# password = 'BKyKr8VggoGN'
# server = '10.50.2.4'
# database = 'citus'
# username = 'slctuatappuser'
# password = 'sPkDtKh2pJy5tihGMV'
# cnxn = psycopg2.connect( host=server,database=database,user=username,password=password)
cnxn = connect_db()

# def get_inputs_csv(rake_id,operation_start):

#     rake_details = pd.read_csv('inputs/rake_details.csv',index_col=[0],parse_dates=['WHARFAGE_START','DEMURRAGE_START','RELEASE_TIME','PLACEMENT_TIME'])
#     demurrage_rate = pd.read_csv('inputs/demurrage_rate.csv',index_col=[0])
#     wharfage_rate = pd.read_csv('inputs/wharfage_rate.csv',index_col=[0])
#     crwc_rate = pd.read_csv('inputs/crwc_rate.csv',index_col=[0])
#     rake_handling_cost = pd.read_csv('inputs/rake_handling_cost.csv',index_col=[0])
#     crwc_cost = pd.read_csv('inputs/crwc_cost.csv',index_col=[0])
#     gd_cost = pd.read_csv('inputs/gd_cost.csv',index_col=[0])
#     gd_handling_cost = pd.read_csv('inputs/gd_handling_cost.csv',index_col=[0])
#     lifting_pattern = pd.read_csv('inputs/lifting_pattern.csv',index_col=[0],parse_dates=['START_TIME','END_TIME',"EXPECTED_LIFTING_TIME"])
#     lifting_pattern['LIFTING_HOURS'] = lifting_pattern['EXPECTED_LIFTING_TIME'].dt.hour - operation_start.hour
#     lifting_pattern['HOURLY_LIFTING'] = np.where(lifting_pattern['LIFTING_QTY']!=0,lifting_pattern['LIFTING_QTY']/lifting_pattern['LIFTING_HOURS'],0)
#     lifting_effeciency = pd.read_csv('inputs/lifting_effeciency.csv',index_col=[0])

#     return rake_details, demurrage_rate, wharfage_rate, crwc_rate,\
#           rake_handling_cost, crwc_cost, gd_cost, gd_handling_cost,\
#               lifting_pattern, lifting_effeciency


class GdVsWharfageHelper:
    def run_model(
        rake_id,
        next_rake_arrival_datetime,
        wagon_qty,
        rake_point_code,
        operation_start,
        operation_end,
        serve_gd,
        serve_crwc,
        serve_wharfage,
    ):
        (
            model_df,
            rake_qty,
            lifting_pattern,
            lifting_effeciency,
            wharfage_rate,
        ) = get_model_data(
            rake_id,
            next_rake_arrival_datetime,
            wagon_qty,
            operation_start,
            operation_end,
            rake_point_code,
        )
        final_output = pd.DataFrame()

        final_status = []

        for idx, row in rake_qty.iterrows():
            df = (
                model_df[
                    (model_df["BRAND"] == row["BRAND"])
                    & (model_df["GRADE"] == row["GRADE"])
                    & (model_df["PACKAGING"] == row["PACKAGING"])
                    & (model_df["CUST_CATEGORY"] == row["CUST_CATEGORY"])
                ]
                .copy()
                .reset_index(drop=True)
            )
            df = get_wharfage_hours(
                df, lifting_effeciency, lifting_pattern, wharfage_rate, wagon_qty
            )
            df.loc[df["CMPLSRY_ALLOC"] != True, "DEMURRAGE_HOURS"] = (
                df.loc[df["CMPLSRY_ALLOC"] != True, "WHARFAGE_HOURS"]
                + df.iloc[1]["DEMURRAGE_HOURS"]
            )
            # df = df[df['WHARFAGE_HOURS']!=1000].reset_index(drop=True)
            wagon_no = df["NO_OF_WAGONS"].unique()[0]
            output, status = model(
                df,
                wagon_no,
                rake_qty,
                lifting_pattern,
                lifting_effeciency,
                serve_gd,
                serve_crwc,
                serve_wharfage,
                wagon_qty,
            )
            final_output = final_output.append(output, ignore_index=True)
            final_status.append(status)

        if "Infeasible" in final_status:
            status = "Infeasible"
        else:
            status = "Optimal"

        return final_output, status


def get_inputs(rake_id, operation_start, rake_point_code):
    # rake_hdetails = pd.read_excel('inputs/inputs.xlsx',sheet_name='rake_details')
    rake_details = pd.read_sql(
        f"""SELECT "RAKE_ID",
    "RAKE_POINT","RAKE_POINT_CODE","DEPOT_CODE","QTY","BRAND","GRADE","PACKAGING","CUST_CATEGORY",
    "PLACEMENT_TIME","RELEASE_TIME","DEMURRAGE_START","WHARFAGE_START" FROM(select "RLD_ID",
    "PLACEMENT_DATE" as "PLACEMENT_TIME",
    "ACTUAL_TIME_FOR_RAKE_RELEASE" as "RELEASE_TIME",
    "FREE_TIME_FOR_RAKE_RELEASE" as "DEMURRAGE_START",
    "FREE_TIME_FOR_MATERIAL_CLEARANCE" as "WHARFAGE_START"
    from target."TGT_RAKE_UNLOADING_DETAILS") A,
	(select rld."RLD_ID", rld."RAKE_ID", rld."RAKE_POINT", rld."RAKE_POINT_CODE",
	SUBSTR(rld."SHIP_TO_DEPOT",1,3) AS "DEPOT_CODE", rld."QTY_DISPATCH_FRM_PLANT" AS "QTY", rld."ORG_ID" AS "BRAND",
    rld."INVENTORY_ITEM_ID",
    case
    WHEN rld."PACKING_TYPE" = 'PAPER' then 'PAPER'
    WHEN rld."PACKING_TYPE" = 'ROOFON' then 'PAPER'
    else 'HDPE' end as "PACKAGING",
	rld."SEGMENT" AS "CUST_CATEGORY",a."MEANING" as "GRADE" from target."TGT_RAKE_LOADING_DETAILS" rld,
	(select "MEANING","LOOKUP_CODE" from etl_zone."T_OEBS_FND_LOOKUP_VALUES" oflv
	where oflv."LOOKUP_TYPE" = 'SCL_CEMENT_ITEMS'
	and oflv."ZD_EDITION_NAME" = 'SET2') a
	where rld."INVENTORY_ITEM_ID"::bigint = a."LOOKUP_CODE"::bigint)B
	WHERE A."RLD_ID" = B."RLD_ID" AND  "RAKE_ID"='{rake_id}' and "RAKE_POINT_CODE"='{rake_point_code}'
    """,
        cnxn,
    )

    demurrage_rate = pd.read_sql(
        """ select "DEMURRAGE_HOURS_MIN" AS "START","DEMURRAGE_HOURS_MAX" AS "END","DEMURRAGE_RATE_PER_MT_PER_HOUR"
    AS "COST_PER_HR_PER_MT"  from etl_zone."DEMURRAGE_SLABS" """,
        cnxn,
    )

    wharfage_rate = pd.read_sql(
        """ select "DEMURRAGE_HOURS_MIN" AS "START","DEMURRAGE_HOURS_MAX" AS "END","DEMURRAGE_RATE_PER_MT_PER_HOUR"
    AS "COST_PER_HR_PER_MT"  from etl_zone."DEMURRAGE_SLABS" """,
        cnxn,
    )
    wharfage_rate["WHARFAGE_ID"] = wharfage_rate.index

    crwc_rate = pd.read_sql(
        f""" select "RAKE_POINT","RAKE_POINT_CODE","MIN_DAYS" AS "START_DAYS",
    "MAX_DAYS" AS "END_DAYS","RATE_PER_DAY_PER_MT" AS "COST_PER_DAY_PER_MT"
    from etl_zone."CRWC_CHARGES_MASTER" where "RAKE_POINT"='{rake_point_code}' """,
        cnxn,
    )  # Discussed with lakshya later will change column name

    rake_handling_cost = pd.read_sql(
        f"""SELECT "RAKE_POINT",	"RAKE_POINT_CODE",	 SUBSTR("DEPOT_NAME",1,3) as "DEPOT_CODE",
                                   CASE WHEN "PACKAGING" = 'PAPER' then 'PAPER'
                                        WHEN "PACKAGING" = 'ROOFON' then 'PAPER'
    else 'HDPE' end as "PACKAGING",  "RAKE_HANDLING"
    AS "RAKE_HANDLING_COST_PER_MT" from	etl_zone."HANDLING_MASTERS" where
   "RAKE_POINT_CODE"='{rake_point_code}' """,
        cnxn,
    )

    crwc_cost = pd.read_sql(
        f""" SELECT DISTINCT A."RAKE_POINT",A."RAKE_POINT_CODE",A."DEPOT_CODE",
        A."PACKAGING", B."CRWC_FREIGHT_PER_MT"
        FROM (SELECT "RAKE_POINT", "RAKE_POINT_CODE",SUBSTR("DEPOT_NAME",1,3) AS "DEPOT_CODE","BRAND",
        CASE
                    WHEN "PACKAGING" = 'PAPER' then 'PAPER'
                    WHEN "PACKAGING" = 'ROOFON' then 'PAPER'
                    else 'HDPE'
                end as "PACKAGING","CARTAGE_COST" from etl_zone."HANDLING_MASTERS")A,
        (SELECT MAX("MONTH_YEAR"::DATE) AS "MONTH_YEAR","DEPO_CODE" ,
        "SALE_TYPE",
        CASE
                    WHEN "PACK_MAT" = 'PAPER' then 'PAPER'
                    WHEN "PACK_MAT" = 'ROOFON' then 'PAPER'
                    else 'HDPE'
                end as "PACKAGING"
        ,AVG("AVERAGE_FREIGHT") AS "CRWC_FREIGHT_PER_MT"
        FROM etl_zone."DEPO_WISE_FREIGHT_MASTER"
        WHERE "SALE_TYPE"='RK'
        GROUP BY "DEPO_CODE","SALE_TYPE"
        --  ,"AVERAGE_FREIGHT"
        ,"PACKAGING")B
        WHERE A."DEPOT_CODE"=B."DEPO_CODE" AND A."PACKAGING"=B."PACKAGING"
        and "RAKE_POINT_CODE"='{rake_point_code}'
        """,
        cnxn,
    )
    crwc_cost["CRWC_HANDLING_CHARGES_PER_MT"] = 120

    gd_cost = pd.read_sql(
        f"""  SELECT DISTINCT A."RAKE_POINT",A."RAKE_POINT_CODE",A."DEPOT_CODE",
            A."PACKAGING", B."GD_FREIGHT_PER_MT",
            A."CARTAGE_COST" AS "TRANSFER_COST_PER_MT"
            FROM (SELECT "RAKE_POINT", "RAKE_POINT_CODE",SUBSTR("DEPOT_NAME",1,3) AS "DEPOT_CODE","BRAND",
            CASE
                        WHEN "PACKAGING" = 'PAPER' then 'PAPER'
                        WHEN "PACKAGING" = 'ROOFON' then 'PAPER'
                        else 'HDPE'
                    end as "PACKAGING","CARTAGE_COST" from etl_zone."HANDLING_MASTERS")A,
            (SELECT MAX("MONTH_YEAR"::DATE) AS "MONTH_YEAR","DEPO_CODE" ,
            "SALE_TYPE",
            CASE
            WHEN "PACK_MAT" = 'PAPER' then 'PAPER'
            WHEN "PACK_MAT" = 'ROOFON' then 'PAPER'
            else 'HDPE'
        end as "PACKAGING"
         ,AVG("AVERAGE_FREIGHT") AS "GD_FREIGHT_PER_MT"
        FROM etl_zone."DEPO_WISE_FREIGHT_MASTER"
        WHERE "SALE_TYPE"='GD-RK'
        GROUP BY "DEPO_CODE","SALE_TYPE"
        --  ,"AVERAGE_FREIGHT"
        ,"PACKAGING")B
        WHERE A."DEPOT_CODE"=B."DEPO_CODE" AND A."PACKAGING"=B."PACKAGING" AND
		"RAKE_POINT_CODE" ='{rake_point_code}'
        """,
        cnxn,
    )

    gd_handling_cost = pd.read_sql(
        f""" SELECT "RAKE_POINT",	"RAKE_POINT_CODE",	 SUBSTR("DEPOT_NAME",1,3) as "DEPOT_CODE",
                                 CASE WHEN "BRAND" = 'SHREE' then 102
                                        WHEN "BRAND" = 'BANGUR' then 103
                                        else 104 end as "BRAND",
                                   CASE WHEN "PACKAGING" = 'PAPER' then 'PAPER'
                                        WHEN "PACKAGING" = 'ROOFON' then 'PAPER'
    else 'HDPE' end as "PACKAGING",  "ROAD_HANDLING_FROM_GODOWN"
    AS "GD_HANDLING_CHARGES_PER_MT" from	etl_zone."HANDLING_MASTERS"
    WHERE "RAKE_POINT_CODE"='{rake_point_code}' """,
        cnxn,
    )

    lifting_pattern = pd.read_sql(
        f""" select "RAKE_ID",
        "BRAND" ,"MIN_TIME" as"START_TIME","MAX_TIME" AS "END_TIME","EXPECTED_LIFTING_TIME",
        "PACKAGING" as "PACKAGING","GRADE","CUST_CATEGORY",	"SLAB_ID",
        "LIFTING_QTY" from etl_zone."LIFTING_PATTERN" where "RAKE_POINT_CODE"='{rake_point_code}' and "RAKE_ID"='{rake_id}' """,
        cnxn,
    )

    lifting_pattern.index = lifting_pattern["SLAB_ID"]
    lifting_pattern["EXPECTED_LIFTING_TIME"] = pd.to_datetime(
        lifting_pattern["EXPECTED_LIFTING_TIME"]
    )
    print(lifting_pattern.info())

    lifting_pattern["LIFTING_HOURS"] = np.ceil(
        (
            lifting_pattern["EXPECTED_LIFTING_TIME"] - lifting_pattern["START_TIME"]
        ).dt.total_seconds()
        / 3600
    )
    lifting_pattern["HOURLY_LIFTING"] = np.where(
        lifting_pattern["LIFTING_QTY"] != 0,
        lifting_pattern["LIFTING_QTY"] / lifting_pattern["LIFTING_HOURS"],
        0,
    )

    lifting_effeciency = pd.read_sql(
        f"""select (extract(hour from "MIN_TIME" ))as "START",
		(extract(hour from "MAX_TIME")) as "END",
		"LIFTING_EFFICIENCY_PER" AS "LIFTING_PERC"
		from etl_zone."HOURLY_LIFTING_EFFICIENCY"
	 WHERE "RAKE_POINT_CODE"='{rake_point_code}'  """,
        cnxn,
    )

    return (
        rake_details,
        demurrage_rate,
        wharfage_rate,
        crwc_rate,
        rake_handling_cost,
        crwc_cost,
        gd_cost,
        gd_handling_cost,
        lifting_pattern,
        lifting_effeciency,
    )


def get_hourly_slabs(
    rake_details, next_rake_arrival_datetime, operation_start, operation_end
):
    print(rake_details)
    hourly_slabs = pd.DataFrame(columns=["RAKE_ID", "START_TIME", "END_TIME"])
    print(hourly_slabs)

    hourly_slabs.loc[len(hourly_slabs)] = rake_details.iloc[0][
        ["RAKE_ID", "WHARFAGE_START"]
    ].tolist() + [rake_details.iloc[0]["WHARFAGE_START"] + td(hours=1)]
    for date_ in pd.date_range(
        start=hourly_slabs.iloc[-1]["END_TIME"] + td(hours=1),
        end=next_rake_arrival_datetime,
        freq="H",
    ):
        hourly_slabs.loc[len(hourly_slabs)] = hourly_slabs.iloc[-1][
            ["RAKE_ID", "END_TIME"]
        ].tolist() + [date_]
    hourly_slabs["size"] = 1

    bgpt = rake_details.groupby(
        ["BRAND", "GRADE", "PACKAGING", "CUST_CATEGORY", "DEPOT_CODE"], as_index=False
    ).size()
    bgpt["size"] = 1

    hourly_slabs = hourly_slabs.merge(bgpt, on=["size"])
    hourly_slabs.drop(columns=["size"], inplace=True)
    hourly_slabs["HOURLY_SLAB_ID"] = hourly_slabs.index

    hourly_slabs["START_TIME"] = hourly_slabs["START_TIME"].apply(
        lambda x: x.replace(minute=0, second=0)
    )
    hourly_slabs["END_TIME"] = hourly_slabs["END_TIME"].apply(
        lambda x: x.replace(minute=0, second=0)
    )

    return hourly_slabs


def get_demurrage_wharfage_free_period(
    df, rake_details, next_rake_arrival_datetime, demurrage_rate
):
    for idx, row in (
        rake_details.groupby(
            ["BRAND", "GRADE", "PACKAGING", "CUST_CATEGORY", "DEPOT_CODE"],
            as_index=False,
        )
        .size()
        .iterrows()
    ):
        df_idx = df.index.max() + 1
        df.loc[df_idx] = df[df["BRAND"] == row["BRAND"]].iloc[0]
        df.loc[
            df_idx,
            [
                "START_TIME",
                "END_TIME",
                "BRAND",
                "GRADE",
                "PACKAGING",
                "CUST_CATEGORY",
                "DEPOT_CODE",
                "DEMURRAGE_HOURS",
                "WHARFAGE_HOURS",
                "DEMURRAGE_RATE",
                "CMPLSRY_ALLOC",
            ],
        ] = rake_details.iloc[0][["PLACEMENT_TIME", "DEMURRAGE_START"]].tolist() + [
            row["BRAND"],
            row["GRADE"],
            row["PACKAGING"],
            row["CUST_CATEGORY"],
            row["DEPOT_CODE"],
            0,
            0,
            0,
            True,
        ]
        demurrage_hours = (
            rake_details.iloc[0]["WHARFAGE_START"]
            - rake_details.iloc[0]["DEMURRAGE_START"]
        ).total_seconds() / 3600
        demurrage = demurrage_rate.query(
            f""" {demurrage_hours}>=START & {demurrage_hours}<END """
        )["COST_PER_HR_PER_MT"].item()

        df.loc[df_idx + 1] = df[df["BRAND"] == row["BRAND"]].iloc[0]
        df.loc[
            df_idx + 1,
            [
                "START_TIME",
                "END_TIME",
                "BRAND",
                "GRADE",
                "PACKAGING",
                "CUST_CATEGORY",
                "DEPOT_CODE",
                "DEMURRAGE_HOURS",
                "WHARFAGE_HOURS",
                "DEMURRAGE_RATE",
                "CMPLSRY_ALLOC",
            ],
        ] = rake_details.iloc[0][["DEMURRAGE_START", "WHARFAGE_START"]].tolist() + [
            row["BRAND"],
            row["GRADE"],
            row["PACKAGING"],
            row["CUST_CATEGORY"],
            row["DEPOT_CODE"],
            demurrage_hours,
            0,
            demurrage,
            True,
        ]

    df["CMPLSRY_ALLOC"] = df["CMPLSRY_ALLOC"].fillna(False)
    # df.to_csv('df_get_demmurag_anuradha.csv')

    return df


def get_demurrage_wharfage_rates(df, rake_details, demurrage_rate, wharfage_rate):
    demurrage_start = rake_details.iloc[0]["DEMURRAGE_START"]
    wharfage_start = rake_details.iloc[0]["WHARFAGE_START"]
    # print(demurrage_start)
    df["DEMURRAGE_HOURS"] = df["END_TIME"].apply(
        lambda x: (x - demurrage_start).total_seconds() / 3600
    )
    df["WHARFAGE_HOURS"] = df["END_TIME"].apply(
        lambda x: (x - wharfage_start).total_seconds() / 3600
    )
    df["DEMURRAGE_RATE"] = df["DEMURRAGE_HOURS"].apply(
        lambda x: demurrage_rate.query(f""" {x}>=START & {x}<END """)[
            "COST_PER_HR_PER_MT"
        ].item()
    )

    return df


def get_crwc_rates(df, rake_details, crwc_rate):
    crwc_rate = crwc_rate.sort_values("START_DAYS", ascending=True).reset_index(
        drop=True
    )

    crwc_rate["CRWC_SLAB"] = crwc_rate.index

    crwc_rate["SLAB_DAYS"] = crwc_rate["END_DAYS"] - crwc_rate["START_DAYS"]

    crwc_rate.loc[0, "SLAB_DAYS"] -= 1

    crwc_rate["SLAB_COST"] = crwc_rate["SLAB_DAYS"] * crwc_rate["COST_PER_DAY_PER_MT"]

    wharfage_start = rake_details.iloc[0]["WHARFAGE_START"]

    df["CRWC_DAYS"] = df["END_TIME"].apply(
        lambda x: np.ceil((x - wharfage_start).total_seconds() / 86400)
    )

    df["CRWC_START_DAY"] = df["CRWC_DAYS"].apply(
        lambda x: crwc_rate.query(f""" {x}>=START_DAYS & {x}<END_DAYS """)[
            "START_DAYS"
        ].item()
    )

    df["CRWC_SLAB"] = df["CRWC_DAYS"].apply(
        lambda x: crwc_rate.query(f""" {x}>=START_DAYS & {x}<END_DAYS """)[
            "CRWC_SLAB"
        ].item()
    )

    df["CRWC_RATE"] = df["CRWC_DAYS"].apply(
        lambda x: crwc_rate.query(f""" {x}>=START_DAYS & {x}<END_DAYS """)[
            "COST_PER_DAY_PER_MT"
        ].item()
    )

    for idx, row in df.iterrows():
        if row["CRWC_SLAB"] > 0:
            days = (
                1
                if (row["CRWC_DAYS"] - row["CRWC_START_DAY"]) == 0
                else (row["CRWC_DAYS"] - row["CRWC_START_DAY"])
            )

            updated_rate = round(
                (
                    crwc_rate.loc[: row["CRWC_SLAB"] - 1]["SLAB_COST"].sum()
                    + (days * row["CRWC_RATE"])
                )
                / row["CRWC_DAYS"],
                1,
            )

            df.loc[idx, "CRWC_RATE"] = updated_rate

    df.drop(columns=["CRWC_START_DAY", "CRWC_SLAB"], inplace=True)

    return df


def get_costs(df, rake_handling_cost, crwc_cost, gd_cost, gd_handling_cost):
    print(df.columns)
    print(gd_cost.columns)
    df = df.merge(
        rake_handling_cost[["PACKAGING", "RAKE_HANDLING_COST_PER_MT", "DEPOT_CODE"]],
        on=["PACKAGING", "DEPOT_CODE"],
    )

    df = df.merge(
        crwc_cost[
            [
                "PACKAGING",
                "CRWC_HANDLING_CHARGES_PER_MT",
                "CRWC_FREIGHT_PER_MT",
                "DEPOT_CODE",
            ]
        ],
        on=["PACKAGING", "DEPOT_CODE"],
    )
    print(df["BRAND"])
    print(df["DEPOT_CODE"])
    df = df.merge(
        gd_cost[
            ["PACKAGING", "TRANSFER_COST_PER_MT", "GD_FREIGHT_PER_MT", "DEPOT_CODE"]
        ],
        on=["PACKAGING", "DEPOT_CODE"],
        how="left",
    )
    df["TRANSFER_COST_PER_MT"] = df["TRANSFER_COST_PER_MT"].fillna(1000000)
    df["GD_FREIGHT_PER_MT"] = df["GD_FREIGHT_PER_MT"].fillna(1000000)
    df = df.merge(
        gd_handling_cost[
            ["BRAND", "PACKAGING", "GD_HANDLING_CHARGES_PER_MT", "DEPOT_CODE"]
        ],
        on=["BRAND", "PACKAGING", "DEPOT_CODE"],
    )
    return df


def get_wharfage_hours(
    df, lifting_effeciency, lifting_pattern, wharfage_rate, wagon_qty
):
    df["SLAB_ID"] = df["SLAB_ID"].astype(int)
    df["MAX_LIFTING_QTY"] = df.apply(
        lambda x: lifting_pattern.loc[x.SLAB_ID, "LIFTING_QTY"]
        if x["CMPLSRY_ALLOC"] == False
        else lifting_pattern.loc[x.SLAB_ID, "LIFTING_QTY"],
        axis=1,
    )
    df_size = df.groupby(["SLAB_ID"], as_index=False).size()
    df = df.merge(df_size, on=["SLAB_ID"])
    df["MAX_LIFTING_QTY"] = np.where(
        df["MAX_LIFTING_QTY"] != 0, df["MAX_LIFTING_QTY"] / df["size"], 0
    )
    df.drop(columns=["size"], inplace=True)
    slab_qty = lifting_pattern.copy()

    wharfage_id = 1
    if df["MAX_LIFTING_QTY"].sum() >= wagon_qty:
        idx = 0
        while idx < len(df):
            if (
                lifting_pattern.loc[df.loc[idx, "SLAB_ID"]]["END_TIME"]
                - lifting_pattern.loc[df.loc[idx, "SLAB_ID"]]["START_TIME"]
            ).total_seconds() / 3600 < 24:
                df.loc[idx, "MAX_LIFTING_QTY"] = lifting_pattern.loc[
                    df.loc[idx, "SLAB_ID"], "LIFTING_QTY"
                ]

            row = df.loc[idx]

            # if row['CMPLSRY_ALLOC'] == True:
            #     df.loc[idx,"WHARFAGE_ID"] = wharfage_id
            #     df.loc[idx,'WHARFAGE_RATE'] = 0
            #     wharfage_id += 1
            #     idx += 1
            #     continue

            if row["MAX_LIFTING_QTY"] <= 0:
                df.loc[idx, "WHARFAGE_HOURS"] = 1000
                df.loc[idx, "WHARFAGE_ID"] = wharfage_id
                wharfage_id += 1
                idx += 1
                continue

            if row["MAX_LIFTING_QTY"] >= wagon_qty:
                # slab_qty.loc[row['SLAB_ID'],"LIFTING_QTY"] -= row['MAX_LIFTING_QTY']
                # if slab_qty.loc[row['SLAB_ID'],"LIFTING_QTY"] <= 0:
                #     df.loc[df['SLAB_ID']==row['SLAB_ID'],'MAX_LIFTING_QTY'] = 0

                df.loc[idx, "WHARFAGE_ID"] = wharfage_id
                wharfage_id += 1
                idx += 1
                continue
            else:
                max_qty = row["MAX_LIFTING_QTY"]

                # slab_qty.loc[row['SLAB_ID'],"LIFTING_QTY"] -= row['MAX_LIFTING_QTY']
                # if slab_qty.loc[row['SLAB_ID'],"LIFTING_QTY"] <= 0:
                #     df.loc[df['SLAB_ID']==row['SLAB_ID'],'MAX_LIFTING_QTY'] = 0

                if df.loc[idx + 1 :, "MAX_LIFTING_QTY"].sum() + max_qty >= wagon_qty:
                    idx1 = idx + 1
                    while idx1 < len(df):
                        if (
                            lifting_pattern.loc[df.loc[idx1, "SLAB_ID"]]["END_TIME"]
                            - lifting_pattern.loc[df.loc[idx1, "SLAB_ID"]]["START_TIME"]
                        ).total_seconds() / 3600 < 24:
                            df.loc[idx1, "MAX_LIFTING_QTY"] = lifting_pattern.loc[
                                df.loc[idx1, "SLAB_ID"], "LIFTING_QTY"
                            ]
                        # else:
                        #     df.loc[idx1,"MAX_LIFTING_QTY"] = lifting_effeciency.loc[df.loc[idx1,"LIFTING_EFFECIENCY_ID"],"LIFTING_PERC"]*slab_qty.loc[df.loc[idx,'SLAB_ID'],"LIFTING_QTY"]
                        row1 = df.loc[idx1]
                        max_qty += row1["MAX_LIFTING_QTY"]

                        # slab_qty.loc[row1['SLAB_ID'],"LIFTING_QTY"] -= row1['MAX_LIFTING_QTY']
                        # if slab_qty.loc[row1['SLAB_ID'],"LIFTING_QTY"] <= 0:
                        #     df.loc[df['SLAB_ID']==row1['SLAB_ID'],'MAX_LIFTING_QTY'] = 0

                        if max_qty >= wagon_qty:
                            df.loc[idx:idx1, "WHARFAGE_HOURS"] = df.loc[
                                idx1, "WHARFAGE_HOURS"
                            ]
                            df.loc[idx:idx1, "MAX_LIFTING_QTY"] = max_qty
                            df.loc[idx:idx1, "WHARFAGE_ID"] = wharfage_id
                            wharfage_id += 1
                            idx = idx1 + 1
                            break
                        idx1 += 1
                else:
                    df.loc[idx:, "WHARFAGE_HOURS"] = 1000
                    df.loc[idx:, "WHARFAGE_ID"] = wharfage_id
                    wharfage_id += 1
                    idx = len(df)
    else:
        df["WHARFAGE_HOURS"] = 1000
        df["WHARFAGE_ID"] = wharfage_id
        wharfage_id += 1

    df["WHARFAGE_ID"] = df["WHARFAGE_ID"].fillna(df["WHARFAGE_ID"].max())
    df["WHARFAGE_RATE"] = df["WHARFAGE_HOURS"].apply(
        lambda x: wharfage_rate.query(f""" {x}>=START & {x}<END """)[
            "COST_PER_HR_PER_MT"
        ].item()
    )
    df.loc[df["CMPLSRY_ALLOC"] == True, "WHARFAGE_RATE"] = 0
    return df


def get_model_data(
    rake_id,
    next_rake_arrival_datetime,
    wagon_qty,
    operation_start,
    operation_end,
    rake_point_code,
):
    (
        rake_details,
        demurrage_rate,
        wharfage_rate,
        crwc_rate,
        rake_handling_cost,
        crwc_cost,
        gd_cost,
        gd_handling_cost,
        lifting_pattern,
        lifting_effeciency,
    ) = get_inputs(rake_id, operation_start, rake_point_code)

    # rake_details, demurrage_rate, wharfage_rate, crwc_rate,\
    #       rake_handling_cost, crwc_cost, gd_cost, gd_handling_cost,\
    #           lifting_pattern, lifting_effeciency = get_inputs_csv(rake_id,operation_start)

    model_df = get_hourly_slabs(
        rake_details, next_rake_arrival_datetime, operation_start, operation_end
    )

    model_df = get_demurrage_wharfage_rates(
        model_df, rake_details, demurrage_rate, wharfage_rate
    )

    model_df = get_crwc_rates(model_df, rake_details, crwc_rate)

    model_df = get_costs(
        model_df, rake_handling_cost, crwc_cost, gd_cost, gd_handling_cost
    )

    model_df = get_demurrage_wharfage_free_period(
        model_df, rake_details, next_rake_arrival_datetime, demurrage_rate
    )

    model_df = model_df.sort_values(["BRAND", "START_TIME", "END_TIME"]).reset_index(
        drop=True
    )

    # Rake Qty
    rake_qty = rake_details.groupby(
        ["BRAND", "GRADE", "PACKAGING", "CUST_CATEGORY"], as_index=False
    )["QTY"].sum()
    rake_qty["RAKE_QTY_ID"] = rake_qty.index
    rake_qty["NO_OF_WAGONS"] = np.ceil(rake_qty["QTY"] / wagon_qty)
    model_df = model_df.merge(
        rake_qty, on=["BRAND", "GRADE", "PACKAGING", "CUST_CATEGORY"]
    )

    # Lifting Effeciency
    # lifting_effeciency['LIFTING_EFFECIENCY_ID'] = lifting_effeciency.index
    # model_df['LIFTING_EFFECIENCY_ID'] = model_df['END_TIME'].apply(lambda x: lifting_effeciency.query(f''' {x.hour}>=START & {x.hour}<END ''')["LIFTING_EFFECIENCY_ID"].item())

    # Lifting Pattern
    for idx, row in model_df.iterrows():
        try:
            slab_id = lifting_pattern[
                (lifting_pattern["START_TIME"] <= row["START_TIME"])
                & (lifting_pattern["END_TIME"] >= row["END_TIME"])
                & (lifting_pattern["BRAND"].astype(int) == row["BRAND"])
                & (lifting_pattern["GRADE"] == row["GRADE"])
                & (lifting_pattern["PACKAGING"] == row["PACKAGING"])
                & (lifting_pattern["CUST_CATEGORY"] == row["CUST_CATEGORY"])
            ]["SLAB_ID"].item()
            hours_diff = (
                lifting_pattern.loc[slab_id]["END_TIME"]
                - lifting_pattern.loc[slab_id]["START_TIME"]
            ).total_seconds() / 3600
            if hours_diff < 24:
                model_df.loc[idx, "SLAB_ID"] = slab_id
            else:
                if (
                    (row["END_TIME"].time() <= operation_end.time())
                    and (row["START_TIME"].time() >= operation_start.time())
                    and (
                        row["END_TIME"]
                        <= lifting_pattern.loc[slab_id]["EXPECTED_LIFTING_TIME"]
                    )
                ):
                    model_df.loc[idx, "SLAB_ID"] = slab_id
        except Exception:
            pass

    model_df.dropna(subset=["SLAB_ID"], inplace=True)
    model_df.reset_index(inplace=True, drop=True)
    return model_df, rake_qty, lifting_pattern, lifting_effeciency, wharfage_rate


def model(
    df,
    wagon_no,
    rake_qty,
    lifting_pattern,
    lifting_effeciency,
    serve_gd,
    serve_crwc,
    serve_wharfage,
    wagon_qty,
):
    # print(df)

    df["WHARFAGE_ID"] = df["WHARFAGE_ID"].astype("int")

    start = time.time()
    df["index"] = df.index
    # add variable names to dataframe

    df["var_demurrage"] = "d" + df.index.astype("str")
    df["var_wharfage"] = "w" + df.index.astype("str")
    df["var_crwc"] = "c" + df.index.astype("str")
    df["var_gd"] = "g" + df.index.astype("str")
    df["var_wharfage_wagon"] = "wag" + df["WHARFAGE_ID"].astype("str")
    df["var_wharfage_alloc"] = "wa" + df.index.astype("str")
    df["var_demurrage_alloc"] = "dm" + df.index.astype("str")

    # 1. initialize problem
    lp_prob = p.LpProblem("Minimize_Cost", p.LpMinimize)

    # 2. declare Variables
    var_demurrage = [
        p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_demurrage"]
    ]
    var_wharfage = [
        p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_wharfage"]
    ]
    var_crwc = [p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_crwc"]]
    var_gd = [p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_gd"]]
    var_wag = [
        p.LpVariable(i, lowBound=0, cat="Integer")
        for i in df["var_wharfage_wagon"].unique().tolist()
    ]
    var_wharfage_alloc = [
        p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_wharfage_alloc"]
    ]
    var_demurrage_alloc = [
        p.LpVariable(i, lowBound=0, cat="Integer") for i in df["var_demurrage_alloc"]
    ]

    # 3. declare Objective Function
    cost_demurrage = [
        (var_demurrage_alloc[i] * wagon_qty)
        * (df.loc[i, "DEMURRAGE_HOURS"] * df.loc[i, "DEMURRAGE_RATE"])
        + var_demurrage[i]
        * (df.loc[i, "RAKE_HANDLING_COST_PER_MT"] + df.loc[i, "CRWC_FREIGHT_PER_MT"])
        for i in range(len(var_demurrage))
    ]
    cost_wharfage = [
        (var_wharfage_alloc[i] * wagon_qty)
        * (df.loc[i, "WHARFAGE_HOURS"] * df.loc[i, "WHARFAGE_RATE"])
        + var_wharfage[i]
        * (df.loc[i, "RAKE_HANDLING_COST_PER_MT"] + df.loc[i, "CRWC_FREIGHT_PER_MT"])
        for i in range(len(var_wharfage))
    ]
    cost_crwc = [
        var_crwc[i]
        * (
            df.loc[i, "CRWC_DAYS"] * df.loc[i, "CRWC_RATE"]
            + df.loc[i, "RAKE_HANDLING_COST_PER_MT"]
            + df.loc[i, "CRWC_FREIGHT_PER_MT"]
            + df.loc[i, "CRWC_HANDLING_CHARGES_PER_MT"]
        )
        for i in range(len(var_crwc))
    ]
    cost_gd = [
        var_gd[i]
        * (
            df.loc[i, "RAKE_HANDLING_COST_PER_MT"]
            + df.loc[i, "TRANSFER_COST_PER_MT"]
            + df.loc[i, "GD_FREIGHT_PER_MT"]
            + df.loc[i, "GD_HANDLING_CHARGES_PER_MT"]
        )
        for i in range(len(var_gd))
    ]

    # 4. set objective function in model
    lp_prob += (
        p.lpSum(cost_demurrage)
        + p.lpSum(cost_wharfage)
        + p.lpSum(cost_crwc)
        + p.lpSum(cost_gd)
    )

    # Adding Constarints

    # Constraint 1 - Total Qty
    cns = df.groupby("RAKE_QTY_ID")["index"].apply(list)

    for idx, val in cns.items():
        lp_prob += (
            p.lpSum(
                [
                    var_demurrage[i] + var_wharfage[i] + var_crwc[i] + var_gd[i]
                    for i in val
                ]
            )
            >= rake_qty.loc[idx, "QTY"]
        )

    # Constraint 2 - Hourly Effeciency
    # df['MAX_LIFTING_QTY'] = df.apply(lambda x:lifting_pattern.loc[x.SLAB_ID,"LIFTING_QTY"] if x['CMPLSRY_ALLOC'] == False else lifting_pattern.loc[x.SLAB_ID,"LIFTING_QTY"],axis=1)
    # df_size = df.groupby(['SLAB_ID'],as_index=False).size()
    # df = df.merge(df_size,on=['SLAB_ID'])
    # df['MAX_LIFTING_QTY'] = np.where(df['MAX_LIFTING_QTY']!=0,df['MAX_LIFTING_QTY']/df['size'],0)
    # df.drop(columns=['size'],inplace=True)
    # for idx,row in df[df['CMPLSRY_ALLOC']==False].iterrows():

    #     lp_prob += p.lpSum([var_demurrage[idx]+var_wharfage[idx]])<=row['MAX_LIFTING_QTY']

    # Constraint 3 - Lifting Pattern
    cns = df.groupby("SLAB_ID")["index"].apply(list)

    for idx, val in cns.items():
        if (len(val) == 1) and (df.loc[val[0], "DEMURRAGE_HOURS"] == 0):
            lp_prob += (
                p.lpSum([var_demurrage[i] for i in val])
                == lifting_pattern.loc[idx, "LIFTING_QTY"]
            )
            if (serve_gd == True) or (serve_crwc == True):
                lp_prob += p.lpSum([var_wharfage[i] for i in val]) == 0

        elif (len(val) == 1) and (df.loc[val[0], "WHARFAGE_HOURS"] == 0):
            if serve_wharfage == True:
                lp_prob += (
                    p.lpSum([var_wharfage[i] for i in val])
                    == lifting_pattern.loc[idx, "LIFTING_QTY"]
                )
                lp_prob += p.lpSum([var_demurrage[i] for i in val]) == 0
            else:
                lp_prob += (
                    p.lpSum(
                        [var_demurrage[i] + var_wharfage[i] + var_crwc[i] for i in val]
                    )
                    >= lifting_pattern.loc[idx, "LIFTING_QTY"]
                )

        else:
            lp_prob += (
                p.lpSum([var_demurrage[i] + var_wharfage[i] + var_crwc[i] for i in val])
                >= lifting_pattern.loc[idx, "LIFTING_QTY"]
            )

    # Constraint 4 - Number of wagons
    lp_prob += p.lpSum(var_wag) == wagon_no

    # Constraint 5 - Wharfage Qty equal to wagon_qty
    for wag in var_wag:
        cns = (
            df[df["var_wharfage_wagon"] == str(wag)]
            .groupby("WHARFAGE_ID")["index"]
            .apply(list)
        )
        for idx, val in cns.items():
            lp_prob += (
                p.lpSum(
                    [
                        var_demurrage[i] + var_wharfage[i] + var_crwc[i] + var_gd[i]
                        for i in val
                    ]
                )
                == wagon_qty * wag
            )

    # Constraint 6 - Wharfage Alloc

    for i in range(len(var_wharfage)):
        lp_prob += var_wharfage_alloc[i] * wagon_qty >= var_wharfage[i]

    # Constraint 7 - Demurrage Alloc

    for i in range(len(var_demurrage)):
        lp_prob += var_demurrage_alloc[i] * wagon_qty >= var_demurrage[i]

    # Constraint 8 - Force no allocation as per user input

    if serve_gd == False:
        lp_prob += p.lpSum(var_gd) == 0

    if serve_crwc == False:
        lp_prob += p.lpSum(var_crwc) == 0

    if serve_wharfage == False:
        lp_prob += p.lpSum(var_wharfage) == 0

    # solve problem
    status = lp_prob.solve()

    print("Status = ", p.LpStatus[status])
    print("TC = ", p.value(lp_prob.objective))

    qty = {
        "demurrage": {},
        "wharfage": {},
        "crwc": {},
        "gd": {},
        "wharfage_wagon_no": {},
        "wharfage_wagon_alloc": {},
        "demurrage_wagon_alloc": {},
    }
    for d, w, c, g in zip(var_demurrage, var_wharfage, var_crwc, var_gd):
        qty["demurrage"][str(d)] = int(p.value(d))
        qty["wharfage"][str(w)] = int(p.value(w))
        qty["crwc"][str(c)] = int(p.value(c))
        qty["gd"][str(g)] = int(p.value(g))

    for wag in var_wag:
        qty["wharfage_wagon_no"][str(wag)] = int(p.value(wag))

    for wa in var_wharfage_alloc:
        qty["wharfage_wagon_alloc"][str(wa)] = int(p.value(wa))

    for dm in var_demurrage_alloc:
        qty["demurrage_wagon_alloc"][str(dm)] = int(p.value(dm))

    df["qty_demurrage"] = df["var_demurrage"].apply(lambda x: qty["demurrage"][x])
    df["qty_wharfage"] = df["var_wharfage"].apply(lambda x: qty["wharfage"][x])
    df["qty_crwc"] = df["var_crwc"].apply(lambda x: qty["crwc"][x])
    df["qty_gd"] = df["var_gd"].apply(lambda x: qty["gd"][x])
    df["wharfage_wagon_no"] = df["var_wharfage_wagon"].apply(
        lambda x: qty["wharfage_wagon_no"][x]
    )
    df["wharfage_wagon_alloc"] = df["var_wharfage_alloc"].apply(
        lambda x: qty["wharfage_wagon_alloc"][x]
    )
    df["demurrage_wagon_alloc"] = df["var_demurrage_alloc"].apply(
        lambda x: qty["demurrage_wagon_alloc"][x]
    )

    df = df[
        (df["qty_demurrage"] != 0)
        | (df["qty_wharfage"] != 0)
        | (df["qty_crwc"] != 0)
        | (df["qty_gd"] != 0)
    ]
    # Change Request Adding 14 new more columns
    df["total_demurrage"] = (df["demurrage_wagon_alloc"] * wagon_qty) * (
        df["DEMURRAGE_HOURS"] * df["DEMURRAGE_RATE"]
    )
    df["total_demurrage_rake_handling"] = df["qty_demurrage"] * (
        df["RAKE_HANDLING_COST_PER_MT"]
    )
    df["total_demurrage_freight_cost"] = df["qty_demurrage"] * (
        df["CRWC_FREIGHT_PER_MT"]
    )
    df["total_wharfage"] = (df["wharfage_wagon_alloc"] * wagon_qty) * (
        df["WHARFAGE_HOURS"] * df["WHARFAGE_RATE"]
    )
    df["total_wharfage_rake_handling"] = df["qty_wharfage"] * (
        df["RAKE_HANDLING_COST_PER_MT"]
    )
    df["total_wharfage_freight_cost"] = df["qty_wharfage"] * (df["CRWC_FREIGHT_PER_MT"])
    df["total_crwc_cost"] = df["qty_crwc"] * (df["CRWC_DAYS"] * df["CRWC_RATE"])
    df["total_crwc_rake_handling_cost"] = (
        df["qty_crwc"] * df["RAKE_HANDLING_COST_PER_MT"]
    )
    df["total_crwc_freight_cost"] = df["qty_crwc"] * df["CRWC_FREIGHT_PER_MT"]
    df["total_crwc_handling_charges_cost"] = (
        df["qty_crwc"] * df["CRWC_HANDLING_CHARGES_PER_MT"]
    )
    df["total_gd_rake_handling_cost"] = df["qty_gd"] * (df["RAKE_HANDLING_COST_PER_MT"])
    df["total_gd_transfer_cost"] = df["qty_gd"] * (df["TRANSFER_COST_PER_MT"])
    df["total_gd_freight_cost"] = df["qty_gd"] * (df["GD_FREIGHT_PER_MT"])
    df["total_gd_handling_charges"] = df["qty_gd"] * (df["GD_HANDLING_CHARGES_PER_MT"])

    df["cost_demurrage"] = (df["demurrage_wagon_alloc"] * wagon_qty) * (
        df["DEMURRAGE_HOURS"] * df["DEMURRAGE_RATE"]
    ) + df["qty_demurrage"] * (
        df["RAKE_HANDLING_COST_PER_MT"] + df["CRWC_FREIGHT_PER_MT"]
    )
    df["cost_wharfage"] = (df["wharfage_wagon_alloc"] * wagon_qty) * (
        df["WHARFAGE_HOURS"] * df["WHARFAGE_RATE"]
    ) + df["qty_wharfage"] * (
        df["RAKE_HANDLING_COST_PER_MT"] + df["CRWC_FREIGHT_PER_MT"]
    )
    df["cost_crwc"] = df["qty_crwc"] * (
        df["CRWC_DAYS"] * df["CRWC_RATE"]
        + df["RAKE_HANDLING_COST_PER_MT"]
        + df["CRWC_FREIGHT_PER_MT"]
        + df["CRWC_HANDLING_CHARGES_PER_MT"]
    )
    df["cost_gd"] = df["qty_gd"] * (
        df["RAKE_HANDLING_COST_PER_MT"]
        + df["TRANSFER_COST_PER_MT"]
        + df["GD_FREIGHT_PER_MT"]
        + df["GD_HANDLING_CHARGES_PER_MT"]
    )

    df["total_cost"] = (
        df["cost_demurrage"] + df["cost_wharfage"] + df["cost_crwc"] + df["cost_gd"]
    )
    df["START_TIME"] = df["START_TIME"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["END_TIME"] = df["END_TIME"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df, p.LpStatus[status]


# if __name__ == '__main__':

#     start = time.time()
#     # rake_point_code = 'JAB'
#     # rake_arrival_datetime = dt.strptime('2022-08-21 14:00:00','%Y-%m-%d %H:%M:%S')
#     rake_id = 10009
#     rake_point='GHAZIABAD'
#     rake_point_code='GZB'
#     next_rake_arrival_datetime = dt.strptime('2021-12-01 10:00:00','%Y-%m-%d %H:%M:%S')
#     wagon_qty = 64

#     serve_gd = False
#     serve_crwc = True
#     serve_wharfage = False

#     operation_start = dt.strptime('06:00:00','%H:%M:%S')
#     operation_end = dt.strptime('21:00:00','%H:%M:%S')

#     # wagon_no = 63

#     output, status = run_model(rake_id,next_rake_arrival_datetime,wagon_qty,operation_start,operation_end,serve_gd,serve_crwc,serve_wharfage)
#     output.to_excel(f"outputs/output_{start}.xlsx")
#     print(status)
#     print(output.groupby(['BRAND'],as_index=False)["qty_demurrage",'qty_wharfage','qty_crwc','qty_gd'].sum())
#     print("completed in ",time.time()-start)
