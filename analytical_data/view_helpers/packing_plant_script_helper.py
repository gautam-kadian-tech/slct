import warnings
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta as td

import numpy as np
import pandas as pd
import psycopg2

from .connection import connect_db, createorupdate

warnings.filterwarnings("ignore")
shift_map = {
    1: "06:00:00.000000-08:00",
    2: "02:00:00.000000-08:00",
    3: "10:00:00.000000-08:00",
}
cnxn = connect_db()


def get_schedule(change_input_file, packers_data, used_time_cns=False):
    for f in change_input_file["PLANT"].unique():
        for p in change_input_file.loc[change_input_file["PLANT"] == f][
            "PACKER"
        ].unique():
            # for p in change_input_file['PACKER'].unique():
            tl_df = packers_data[
                (packers_data["PACKER"] == p) & (change_input_file["PLANT"] == f)
            ][
                [
                    "PACKER_RATED_CAPACITY_MT/HR",
                    "TRUCK_LOADER",
                    "TL_RATED_CAPACITY_MT/HR",
                ]
            ].reset_index(
                drop=True
            )
            for idx in range(1, len(tl_df)):
                tl_df.loc[idx, "TL_RATED_CAPACITY_MT/HR"] += tl_df.loc[
                    idx - 1, "TL_RATED_CAPACITY_MT/HR"
                ]
            tl_df = tl_df[
                tl_df["TL_RATED_CAPACITY_MT/HR"]
                <= tl_df["PACKER_RATED_CAPACITY_MT/HR"].max()
            ]
            tl = tl_df["TRUCK_LOADER"].unique().tolist()

            if used_time_cns:
                tl_num = len(tl)
                inde = (
                    change_input_file[(change_input_file["PACKER"] == p)]
                    .iloc[0:tl_num]
                    .index.tolist()
                )
                change_input_file.loc[inde, "TRUCK_LOADER"] = tl

                # change_input_file.loc[inde,'USED_TIME'] = change_input_file['ORDER_QUANTITY']/average_packers_per_hr+(5/60)
                change_input_file.loc[inde, "USED_TIME"] = change_input_file[
                    "ORDER_QUANTITY"
                ] / 120 + (5 / 60)
                change_input_file.loc[
                    inde, "ORDER_PROCESSING_TIME"
                ] = change_input_file["ORDER_QUANTITY"] / 120 + (5 / 60)

            else:
                tl_num = 0
            # change_input_file[change_input_file['PACKER']==p].iloc[tl_num:][['TRUCK_LOADER','USED_TIME']] = [None,None]

            for idx, row in (
                change_input_file[
                    (change_input_file["PACKER"] == p)
                    & (change_input_file["PLANT"] == f)
                ]
                .iloc[tl_num:]
                .iterrows()
            ):
                if row["USED_TIME"] == None:
                    df1 = (
                        change_input_file[change_input_file["PACKER"] == p][
                            ["TRUCK_LOADER", "USED_TIME", "PACKER"]
                        ]
                        .sort_values(
                            ["PACKER", "TRUCK_LOADER", "USED_TIME"], ascending=False
                        )
                        .drop_duplicates(subset=["PACKER", "TRUCK_LOADER"])
                    )
                    tl_code = df1.sort_values(by=["USED_TIME"], ascending=True).iloc[0][
                        "TRUCK_LOADER"
                    ]
                    if (
                        change_input_file[
                            (change_input_file["PACKER"] == p)
                            & (change_input_file["TRUCK_LOADER"] == tl_code)
                        ]["USED_TIME"].max()
                        <= 7.7
                    ):
                        used_time = df1.sort_values(
                            by=["USED_TIME"], ascending=True
                        ).iloc[0]["USED_TIME"]
                        change_input_file.loc[idx, "TRUCK_LOADER"] = tl_code
                        # change_input_file['NEW_TIME']=change_input_file['SHIFT_TIME']-change_input_file['USED_TIME']-(20/60)

                        # change_input_file.loc[idx,"USED_TIME"] = used_time+(row['ORDER_QUANTITY']/average_packers_per_hr)+(5/60)
                        if row["AUTO_TAGGED_MODE"] == "RAIL":
                            change_input_file.loc[idx, "ORDER_PROCESSING_TIME"] = (
                                row["ORDER_QUANTITY"] / 120
                            )
                            change_input_file.loc[idx, "USED_TIME"] = used_time + (
                                row["ORDER_QUANTITY"] / 120
                            )
                        else:
                            change_input_file.loc[idx, "ORDER_PROCESSING_TIME"] = (
                                row["ORDER_QUANTITY"] / 120
                            ) + (5 / 60)
                            change_input_file.loc[idx, "USED_TIME"] = (
                                used_time + (row["ORDER_QUANTITY"] / 120) + (5 / 60)
                            )
                    else:
                        pass

    return change_input_file


def get_order_master(cnxn, plant_input, date_input, shift_input):
    sql = f"""
        select
        lsom."ID",
        lsom."BRAND",
        lsom."GRADE",
        lsom."PACKAGING",
        lsom."ORDER_TYPE",
        lsom."ORDER_QUANTITY" as "ORDER_QUANTITY",
        lsom."SHIP_STATE",
		lsom."SHIP_DISTRICT",
		lsom."SHIP_CITY",
		lsom."CUSTOMER_TYPE",
		lsom."CUST_SUB_CAT",
        lsom."CUSTOMER_CODE",
        lsom."CUST_NAME",
        lsom."PP_CALL",
        case
            when lsom."CHANGED_SOURCE" is null then lsom."AUTO_TAGGED_SOURCE"
            else lsom."CHANGED_SOURCE"
        end as "PLANT",
        case
            when lsom."CHANGED_MODE" is null then lsom."AUTO_TAGGED_MODE"
            else lsom."CHANGED_MODE"
        end as "AUTO_TAGGED_MODE",
        lscc."PP_CALLING",
        lsed."EXECUTABLE_SHIFT",
        ppot."ORDER_MASTER_ID" as "PP_TAGGED"
        from etl_zone."LP_SCHEDULING_ORDER_MASTER" lsom
        inner join(
        select
        "ORDER_MASTER_ID",
        "EXEC_CALLING_SEQUENCE" as "PP_CALLING"
        from
        etl_zone."LP_SCHEDULING_PP_CALL_DTL"
        ) lscc on lscc."ORDER_MASTER_ID" = lsom."ID"
        inner join(
        select
        "ORDER_MASTER_ID",
        "EXECUTABLE_SHIFT"
        from
        etl_zone."LP_SCHEDULING_EXECUTABLE_DTL"
        where "ORIGINAL_SOURCE" = '{plant_input}'
        and "EXECUTABLE_DATE" = '{date_input}'
        and "EXECUTABLE_SHIFT" = {shift_input}
        ) lsed on lsed."ORDER_MASTER_ID" = lsom."ID"
        left join (
            select distinct on ("ORDER_MASTER_ID")
            "ORDER_MASTER_ID"
            from etl_zone."PP_ORDER_TAGGING"
        ) ppot on ppot."ORDER_MASTER_ID" = lsom."ID"
        where lsom."ORDER_EXECUTABLE" = true
        and lsom."TRANSFERRED_TO_DEPOT" = false
    """
    df = pd.read_sql(sql, cnxn)
    print(df)
    return df


def get_packer_details(cnxn, plant_input):
    sql = f"""
        select
        "PLANT",
        "PACKER",
        "WORKERS_REQ_FOR_PACKER",
        "PACKER_RATED_CAPACITY_MT/HR",
        "TRUCK_LOADER",
        "TL_RATED_CAPACITY_MT/HR",
        "WORKERS_REQ_FOR_TL",
        "CAN_RUN_MULTIPLE_BRANDS"
        from etl_zone."PACKER_RATED_CAPACITY" prc
        where "PLANT" = '{plant_input}'
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_tl_counts(cnxn, Packer_d):
    sql = f"""
         select
        "PACKER",
        count("TRUCK_LOADER") as "COUNT_OF_TL"
        from etl_zone."PACKER_RATED_CAPACITY" prc  where "PACKER" = '{Packer_d}'
		group by "PACKER"

    """
    df = pd.read_sql(sql, cnxn)
    return df.iloc[0, "COUNT_OF_TL"]


def get_switch_overtime(cnxn, plant_input):
    sql = f"""
        select
        "PLANT",
        "GRADE_SWITCH_TIME_MIN",
        "WORKER_SWITCH_TIME_DIFF_PACKER_MIN",
        "SWITCH_TIME_BW_TRUCKS_MIN",
        "BRAND_SWITCH_TIME_MIN",
        "TEA_BREAK_TIME_MIN"
        from etl_zone."PLANTWISE_SWITCHOVER_TIME" pst
        where "PLANT" = '{plant_input}'
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_ad_hoc(cnxn, plant_input, date_input, shift_input):
    sql = f"""
        select
        "PLANT",
        "GRADE",
        "BRAND",
        "ADHOC_QTY" as "ORDER_QUANTITY",
        "SHIFT"::int as "EXECUTABLE_SHIFT"
        from etl_zone."SHIFTWISE_ADHOC_QTY"
        where "PLANT" = '{plant_input}'
        and "DATE" = '{date_input}'
        and "SHIFT" = '{shift_input}'
        and "ADHOC_QTY" > 0
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_rail_qty(cnxn, plant_input, date_input, shift_input):
    sql = f"""
        select
        "ID" as "RAIL_ORDER_ID",
        "PLANT",
        "GRADE",
        "BRAND",
        "RAIL_PLANNED_QTY" as "ORDER_QUANTITY",
        "SHIFT"::int as "EXECUTABLE_SHIFT"
        from etl_zone."SHIFTWISE_ADHOC_QTY"
        where "PLANT" = '{plant_input}'
        and "DATE" = '{date_input}'
        and "SHIFT" = '{shift_input}'
        and "RAIL_PLANNED_QTY" > 0
    """
    df = pd.read_sql(sql, cnxn)

    return df


def get_pp_downtime(cnxn, plant_input, date_input, shift_input):
    sql = f"""
      select "PACKER_CODE" AS "PACKER",SUM("STOPPAGE_HRS") as "TOTAL_TL_DOWNTIME_HRS"
        from etl_zone."PACKER_SHIFT_LEVEL_STOPPAGES"
        where "PLANT" = '{plant_input}'
        and "DATE" = '{date_input}'
		and "SHIFT"='{shift_input}'
		group by "PACKER"
    """

    df = pd.read_sql(sql, cnxn)

    return df


class PackingPlantScriptHelper:
    def run_model(plant_input, date_input, shift_input):
        # "---------INPUT SHEETS FOR PACKING PLANT---------"

        input_brand_rank = pd.DataFrame(
            columns=["BRAND", "RANK_BRAND"],
            data=[["SHREE", 1], ["BANGUR", 2], ["ROCKSTRONG", 3]],
        )
        cnxn = connect_db()

        input_sheet = get_order_master(cnxn, plant_input, date_input, shift_input)
        input_sheet = input_sheet[
            [
                "ID",
                "BRAND",
                "GRADE",
                "PACKAGING",
                "ORDER_TYPE",
                "ORDER_QUANTITY",
                "CUSTOMER_CODE",
                "CUST_NAME",
                "PLANT",
                "AUTO_TAGGED_MODE",
                "PP_CALL",
                "PP_CALLING",
                "EXECUTABLE_SHIFT",
                "PP_TAGGED",
            ]
        ]
        print(input_sheet)

        # input_sheet.to_csv('input_sheet.csv',index=False)

        # input_sheet = pd.read_csv('input_sheet.csv')

        input_sheet_qty_new = (
            input_sheet[input_sheet["PP_TAGGED"].isna()]
            .groupby(["PLANT", "BRAND", "GRADE", "EXECUTABLE_SHIFT"], as_index=False)[
                "ORDER_QUANTITY"
            ]
            .sum()
        )
        print("input_sheet_qty_new", input_sheet_qty_new)
        ad_hoc_qty = get_ad_hoc(cnxn, plant_input, date_input, shift_input)
        if len(ad_hoc_qty) != 0:
            ad_hoc_qty["PP_CALLING"] = 10000
            # ad_hoc_qty = ad_hoc_qty.merge(input_sheet_qty_new,how='inner',on=['PLANT','BRAND','GRADE','EXECUTABLE_SHIFT'])
            ad_hoc_qty.fillna(0, inplace=True)
            # ad_hoc_qty['ORDER_QUANTITY'] = ad_hoc_qty['ORDER_QUANTITY_x'] - ad_hoc_qty['ORDER_QUANTITY_y'] discuss with jatin
            ad_hoc_qty = ad_hoc_qty[
                [
                    "PLANT",
                    "BRAND",
                    "GRADE",
                    "EXECUTABLE_SHIFT",
                    "PP_CALLING",
                    "ORDER_QUANTITY",
                ]
            ]

            input_sheet = input_sheet.append(ad_hoc_qty, ignore_index=True)

        rail_qty = get_rail_qty(cnxn, plant_input, date_input, shift_input)

        input_sheet["RAIL_RANK"] = np.NaN
        if len(rail_qty) != 0:
            rail_qty["RAIL_RANK"] = 1
            rail_qty_n = pd.DataFrame(columns=rail_qty.columns)
            for idx, row in rail_qty.iterrows():
                qty = row["ORDER_QUANTITY"]
                while (qty - 30) > 0:
                    qty -= 30
                    rail_qty_n.loc[len(rail_qty_n)] = [
                        row["RAIL_ORDER_ID"],
                        row["PLANT"],
                        row["GRADE"],
                        row["BRAND"],
                        30,
                        row["EXECUTABLE_SHIFT"],
                        row["RAIL_RANK"],
                    ]
                rail_qty_n.loc[len(rail_qty_n)] = [
                    row["RAIL_ORDER_ID"],
                    row["PLANT"],
                    row["GRADE"],
                    row["BRAND"],
                    qty,
                    row["EXECUTABLE_SHIFT"],
                    row["RAIL_RANK"],
                ]
            rail_qty_n["AUTO_TAGGED_MODE"] = "RAIL"
            input_sheet = input_sheet.append(rail_qty_n, ignore_index=True)
        # print(input_sheet)
        brand_count = input_sheet.groupby(["GRADE"], as_index=False)["BRAND"].nunique()
        brand_count.columns = ["GRADE", "COUNT_OF_BRANDS"]

        packers_data = get_packer_details(cnxn, plant_input)

        pp_downtime = get_pp_downtime(cnxn, plant_input, date_input, shift_input)
        pp_downtime["PACKER_DOWNTIME"] = 0
        for idx1, row1 in pp_downtime.iterrows():
            tl_df = packers_data[(packers_data["PACKER"] == row1["PACKER"])][
                [
                    "PACKER_RATED_CAPACITY_MT/HR",
                    "TRUCK_LOADER",
                    "TL_RATED_CAPACITY_MT/HR",
                ]
            ].reset_index(drop=True)
            for idx in range(1, len(tl_df)):
                tl_df.loc[idx, "TL_RATED_CAPACITY_MT/HR"] += tl_df.loc[
                    idx - 1, "TL_RATED_CAPACITY_MT/HR"
                ]
            tl_df = tl_df[
                tl_df["TL_RATED_CAPACITY_MT/HR"]
                <= tl_df["PACKER_RATED_CAPACITY_MT/HR"].max()
            ]
            no_tls = len(tl_df)
            pp_downtime.loc[idx1, "PACKER_DOWNTIME"] = (
                pp_downtime.loc[idx1, "TOTAL_TL_DOWNTIME_HRS"] / no_tls
            )

        # pp_downtime['PACKER_DOWNTIME']=pp_downtime['TOTAL_TL_DOWNTIME_HRS']/pp_downtime['COUNT_OF_TL']

        print("pp_downtime", pp_downtime)

        switch_overtime = get_switch_overtime(cnxn, plant_input)

        id_count = input_sheet.groupby(["PLANT", "GRADE"])[
            "ID"
        ].count()  # same as vehicle count
        print(input_sheet)

        plant_wise_grade_quantity = input_sheet.groupby(
            ["PLANT", "GRADE", "BRAND"], as_index=False
        )["ORDER_QUANTITY"].sum()

        plant_wise_grade_quantity = plant_wise_grade_quantity.groupby(
            ["PLANT", "GRADE"], as_index=False
        )["ORDER_QUANTITY"].sum()
        plant_wise_grade_quantity = plant_wise_grade_quantity.sort_values(
            by=["PLANT", "ORDER_QUANTITY"], ascending=False
        ).reset_index()
        plant_wise_grade_quantity = (
            pd.merge(plant_wise_grade_quantity, id_count, on="GRADE", how="left")
            .drop_duplicates()
            .reset_index()
        )  # ok
        plant_wise_grade_quantity.drop(columns=["level_0"], inplace=True)
        plant_wise_grade_quantity.drop(columns=["index"], inplace=True)  # ok
        plant_wise_grade_quantity.rename(columns={"ID": "COUNT_OF_ID"}, inplace=True)
        individual_brand_sum = input_sheet.groupby(["GRADE", "BRAND"])["BRAND"].count()
        plant_wise_grade_quantity["RANK"] = (
            plant_wise_grade_quantity.groupby("PLANT").cumcount() + 1
        )  # ok
        # print(id_count)
        provide_rank = plant_wise_grade_quantity[
            ["PLANT", "GRADE", "COUNT_OF_ID", "RANK"]
        ]
        provide_rank = pd.merge(
            input_sheet, provide_rank, on=["PLANT", "GRADE"], how="left"
        )

        packers_data_details = packers_data.groupby(
            ["PLANT", "PACKER", "PACKER_RATED_CAPACITY_MT/HR"], as_index=False
        )["TRUCK_LOADER"].count()
        input_packer_alot_sheet = packers_data.groupby(
            [
                "PLANT",
                "PACKER",
                "WORKERS_REQ_FOR_PACKER",
                "TRUCK_LOADER",
                "WORKERS_REQ_FOR_TL",
                "TL_RATED_CAPACITY_MT/HR",
            ],
            as_index=False,
        )["TRUCK_LOADER"].count()

        packers_data_details = packers_data.groupby(
            ["PLANT", "PACKER", "PACKER_RATED_CAPACITY_MT/HR"], as_index=False
        )["TRUCK_LOADER"].count()

        plant_wise_average_of_all_packers = packers_data.groupby(
            ["PLANT"], as_index=False
        )["PACKER_RATED_CAPACITY_MT/HR"].mean()
        # plant_wise_average_of_all_packers['GRADE_PER_AVG_PACKER']=plant_wise_average_of_all_packers['ORDER_QUANTITY']/
        plant_wise_grade_quantity = plant_wise_grade_quantity.merge(
            brand_count, on="GRADE"
        )
        # plant_wise_grade_quantity['COUNT_OF_BRANDS']=[3,1,2,2,3,2] # for a time being taken static

        plant_wise_grade_quantity["BRAND_SWITCH_TIME_MIN"] = 0
        print(plant_wise_grade_quantity)
        print(switch_overtime)

        for p in plant_wise_grade_quantity["PLANT"].unique():
            print(
                switch_overtime.loc[switch_overtime["PLANT"] == p][
                    "BRAND_SWITCH_TIME_MIN"
                ].values[0]
            )
            plant_wise_grade_quantity.loc[
                plant_wise_grade_quantity["PLANT"] == p, "BRAND_SWITCH_TIME_MIN"
            ] = (
                (
                    plant_wise_grade_quantity.loc[
                        plant_wise_grade_quantity["PLANT"] == p
                    ]["COUNT_OF_BRANDS"].sum()
                    - plant_wise_grade_quantity.loc[
                        plant_wise_grade_quantity["PLANT"] == p
                    ]["COUNT_OF_BRANDS"].count()
                )
            ) * (
                switch_overtime.loc[switch_overtime["PLANT"] == p][
                    "BRAND_SWITCH_TIME_MIN"
                ].values[0]
                / 60
            )
            plant_wise_grade_quantity.loc[
                plant_wise_grade_quantity["PLANT"] == p, "SWITCH_TIME_BW_TRUCKS_MIN"
            ] = plant_wise_grade_quantity.loc[plant_wise_grade_quantity["PLANT"] == p][
                "COUNT_OF_ID"
            ].values * (
                switch_overtime.loc[switch_overtime["PLANT"] == p][
                    "SWITCH_TIME_BW_TRUCKS_MIN"
                ].values[0]
                / 60
            )

            for i in plant_wise_grade_quantity[plant_wise_grade_quantity["PLANT"] == p][
                "GRADE"
            ]:
                plant_wise_grade_quantity.loc[
                    plant_wise_grade_quantity["PLANT"] == p, "ORDER_QUANTITY_TIME"
                ] = (
                    plant_wise_grade_quantity.loc[
                        plant_wise_grade_quantity["PLANT"] == p
                    ]["ORDER_QUANTITY"].values
                ) / (
                    plant_wise_average_of_all_packers.loc[
                        plant_wise_average_of_all_packers["PLANT"] == p
                    ]["PACKER_RATED_CAPACITY_MT/HR"].values[0]
                )
                plant_wise_grade_quantity["TOTAL_TIME_OF_EACH_PLANT"] = (
                    plant_wise_grade_quantity["BRAND_SWITCH_TIME_MIN"]
                    + plant_wise_grade_quantity["SWITCH_TIME_BW_TRUCKS_MIN"]
                    + plant_wise_grade_quantity["ORDER_QUANTITY_TIME"]
                )
            plant_wise_grade_quantity_sort = plant_wise_grade_quantity.sort_values(
                by=["PLANT", "ORDER_QUANTITY_TIME"], ascending=False
            )

        packers_data_details = pd.merge(
            packers_data_details, pp_downtime, on="PACKER", how="left"
        ).fillna(0)
        print(packers_data_details)

        shift_time = 8 - (20 / 60)
        packers_data_details["PACKERS_TIME"] = (
            shift_time - packers_data_details["PACKER_DOWNTIME"]
        )
        print(packers_data_details)

        for p in packers_data_details["PLANT"].unique():
            packers_data_details.loc[
                packers_data_details["PLANT"] == p, "CALCULATED_TIME"
            ] = (
                packers_data_details.loc[packers_data_details["PLANT"] == p][
                    "PACKER_RATED_CAPACITY_MT/HR"
                ]
                / (
                    plant_wise_average_of_all_packers.loc[
                        plant_wise_average_of_all_packers["PLANT"] == p
                    ]["PACKER_RATED_CAPACITY_MT/HR"].values
                )
            ) * packers_data_details[
                "PACKERS_TIME"
            ]
            packers_data_details = packers_data_details[
                [
                    "PLANT",
                    "PACKER",
                    "PACKER_RATED_CAPACITY_MT/HR",
                    "TRUCK_LOADER",
                    "TOTAL_TL_DOWNTIME_HRS",
                    "PACKER_DOWNTIME",
                    "CALCULATED_TIME",
                ]
            ]
            packers_data_details_cum = packers_data_details.sort_values(
                by=["PLANT", "CALCULATED_TIME"], ascending=False
            )
            packers_data_details_cum.reset_index(inplace=True)

        for p in packers_data_details_cum["PLANT"].unique():
            packers_data_details_cum.loc[
                packers_data_details_cum["PLANT"] == p, "CUMMULATIVE_VALUE"
            ] = packers_data_details_cum.loc[packers_data_details_cum["PLANT"] == p][
                "CALCULATED_TIME"
            ].cumsum(
                axis=0
            )
        packers_data_details_cum.drop(columns=["index"], inplace=True)
        # print(packers_data_details)

        packers_data_details_cum["PACKERS_REQUIRED"] = 0
        packers_data_details_total_plant_wise_sum = (
            plant_wise_grade_quantity_sort.copy()
        )
        packers_data_details_total_plant_wise_sum = (
            packers_data_details_total_plant_wise_sum.groupby(
                ["PLANT"], as_index=False
            )["TOTAL_TIME_OF_EACH_PLANT"].sum()
        )

        packers_data_details_cum = pd.merge(
            packers_data_details_cum,
            packers_data_details_total_plant_wise_sum,
            on="PLANT",
            how="left",
        )
        # print(packers_data_details_cum)

        for i in range(len(packers_data_details_cum)):
            if i == 0:
                packers_data_details_cum["PACKERS_REQUIRED"][i] = 1
            elif (
                packers_data_details_cum["CUMMULATIVE_VALUE"][i - 1]
                <= packers_data_details_cum["TOTAL_TIME_OF_EACH_PLANT"][i]
            ):
                packers_data_details_cum["PACKERS_REQUIRED"][i] = 1

        packers_required = packers_data_details_cum.groupby(["PLANT"], as_index=False)[
            "PACKERS_REQUIRED"
        ].sum()
        for i in range(len(packers_required)):
            if packers_required["PACKERS_REQUIRED"][i] > 0:
                packers_required["PACKERS_REQUIRED"][i] = (
                    packers_required["PACKERS_REQUIRED"][i] + 1
                )

        packers_data_details_cum_val = pd.merge(
            packers_data_details_cum, packers_required, on=["PLANT"], how="left"
        )
        # print(packers_data_details_cum_val)
        packers_data_details_cum_val = packers_data_details_cum_val.loc[
            packers_data_details_cum_val["PACKERS_REQUIRED_y"] != 0
        ].reset_index()

        # packers_data_details_cum_val.loc[packers_data_details_cum_val['CUMMULATIVE_VALUE'][i]!=0]& (packers_data_details_cum_val.loc[packers_data_details_cum_val['TOTAL_TIME_OF_EACH_PLANT'][i]==0])

        packers_data_details_cum_val = packers_data_details_cum_val.query(
            "CUMMULATIVE_VALUE<TOTAL_TIME_OF_EACH_PLANT + CALCULATED_TIME"
        )
        packers_data_details_cum_val.drop(columns=["index"], inplace=True)
        # print(packers_data_details_cum_val)
        input_sheet["PACKER"] = None

        new_combo1 = packers_data_details_cum_val.query(
            "PACKERS_REQUIRED_x==1"
        ).reset_index()
        new_combo1.drop(columns=["index"], inplace=True)
        new_combo1 = new_combo1[
            [
                "PLANT",
                "PACKER",
                "PACKER_RATED_CAPACITY_MT/HR",
                "TOTAL_TIME_OF_EACH_PLANT",
            ]
        ]
        new_combo1["QTY_MAX"] = new_combo1["PACKER_RATED_CAPACITY_MT/HR"] * (
            new_combo1["TOTAL_TIME_OF_EACH_PLANT"] / new_combo1["PACKER"].nunique()
        )
        # new_combo2=plant_wise_grade_quantity_sort[['PLANT','GRADE']]
        # print(new_combo1)
        # need to discuss with it shivansh is it the right way?
        # new_combo2['PACKER']=None
        # for i in range(len(new_combo2)):
        #     new_combo2['PACKER'][i]=new_combo1['PACKER'][i]

        provide_rank["BRAND"] = provide_rank["BRAND"].str.upper()
        provide_rank = pd.merge(provide_rank, input_brand_rank, on="BRAND", how="left")
        provide_rank = provide_rank.sort_values(
            by=["RANK", "RANK_BRAND", "EXECUTABLE_SHIFT"], ascending=[True, True, True]
        ).reset_index()
        provide_rank.drop(columns=["index"], inplace=True)

        # ------------------final_merge_file_before_alotment of packer and tl------------------
        # final_file=pd.merge(new_combo2,provide_rank,on=['PLANT','GRADE'],how='left')
        final_file = provide_rank.copy()
        final_file["PACKER"] = np.NaN
        final_file["PP_CALL"] = np.where(final_file["PP_CALL"] == True, 1, 2)

        final_file = final_file.sort_values(
            ["RAIL_RANK", "PP_CALL", "COUNT_OF_ID", "RANK_BRAND", "PP_CALLING"],
            ascending=[True, True, False, True, True],
        )

        for idx_pck, row_pck in new_combo1.iterrows():
            qty_max = row_pck["QTY_MAX"]
            for idx, row in final_file[final_file["PACKER"].isna()].iterrows():
                if (qty_max - row["ORDER_QUANTITY"]) > 0:
                    qty_max -= row["ORDER_QUANTITY"]
                    final_file.loc[idx, "PACKER"] = row_pck["PACKER"]
                else:
                    # final_file.loc[idx,'PACKER'] = row_pck['PACKER']
                    break

        final_file["TRUCK_LOADER"] = None
        final_file["USED_TIME"] = None

        # print(final_file[['ID','PLANT','BRAND','GRADE','PACKER','PP_CALL','PP_CALLING','RANK',"TRUCK_LOADER","USED_TIME"]])

        result = get_schedule(final_file, packers_data, used_time_cns=True)
        result.dropna(subset=["TRUCK_LOADER"], inplace=True)
        result["fix_val"] = 1
        result["PP_CALL_RANK"] = (
            result[["TRUCK_LOADER", "fix_val"]].groupby("TRUCK_LOADER").cumsum()
        )
        result["PP_CALL_SEQUENCE"] = None
        result["PP_CALL_RANK"] = (result["PP_CALL_RANK"]).astype(str)
        # for i in range(0, len(result)):
        result["PP_CALL_SEQUENCE"] = (
            result["TRUCK_LOADER"] + "_" + result["PP_CALL_RANK"]
        )
        date_input_seq = dt.strptime(
            f"{date_input} {shift_map[shift_input]}", "%Y-%m-%d %H:%M:%S.%f%z"
        )
        # date_input_seq = date_input_seq.time()
        # print(date_input_seq)

        result["TENTATIVE_PP_IN_TIME"] = result["USED_TIME"].apply(
            (lambda x: date_input_seq + td(seconds=x * 3600))
        )
        result["TENTATIVE_PP_IN_TIME"] = result["TENTATIVE_PP_IN_TIME"].dt.tz_localize(
            None
        )
        result["TENTATIVE_PP_IN_TIME"] = result["TENTATIVE_PP_IN_TIME"].dt.strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        )
        print(result["TENTATIVE_PP_IN_TIME"])

        result["RAIL_ORDER_ID"] = None

        print(result["TENTATIVE_PP_IN_TIME"])
        print(result)
        # result.to_csv('result_new.csv')

        result = result[
            [
                "ID",
                "BRAND",
                "GRADE",
                "PACKAGING",
                "ORDER_TYPE",
                "ORDER_QUANTITY",
                "CUSTOMER_CODE",
                "CUST_NAME",
                "PLANT",
                "AUTO_TAGGED_MODE",
                "PP_CALL",
                "PP_CALLING",
                "EXECUTABLE_SHIFT",
                "PP_TAGGED",
                "RAIL_RANK",
                "RAIL_ORDER_ID",
                "PACKER",
                "TRUCK_LOADER",
                "USED_TIME",
                "ORDER_PROCESSING_TIME",
                "PP_CALL_RANK",
                "PP_CALL_SEQUENCE",
                "TENTATIVE_PP_IN_TIME",
            ]
        ]
        print(result)

        # print(result[['ID','RAIL_ORDER_ID','PLANT','BRAND','GRADE',"ORDER_QUANTITY",'PACKER','PP_CALL','PP_CALLING','RANK',"TRUCK_LOADER","USED_TIME","PP_TAGGED"]])

        # result.to_csv('change_input_file.csv',index=False)
        result = result[result["PP_CALLING"] != 10000]

        order_details = result[~result["ID"].isna()][
            [
                "ID",
                "PACKER",
                "TRUCK_LOADER",
                "ORDER_PROCESSING_TIME",
                "PP_CALL_RANK",
                "PP_CALL_SEQUENCE",
                "TENTATIVE_PP_IN_TIME",
            ]
        ]
        order_details.columns = [
            "ORDER_MASTER_ID",
            "PACKER_CODE",
            "TL_CODE",
            "ORDER_PROCESSING_TIME",
            "PP_CALL_RANK",
            "PP_CALL_SEQUENCE",
            "TENTATIVE_PP_IN_TIME",
        ]

        # print(result)

        rail_order_details = result[~result["RAIL_ORDER_ID"].isna()][
            [
                "RAIL_ORDER_ID",
                "PACKER",
                "TRUCK_LOADER",
                "ORDER_PROCESSING_TIME",
                "BRAND",
                "GRADE",
                "ORDER_QUANTITY",
                "PP_CALL_RANK",
                "PP_CALL_SEQUENCE",
                "TENTATIVE_PP_IN_TIME",
                "EXECUTABLE_SHIFT",
            ]
        ]
        print(rail_order_details)
        rail_order_details.columns = [
            "RAIL_ORDER",
            "PACKER_CODE",
            "TL_CODE",
            "ORDER_PROCESSING_TIME",
            "BRAND",
            "GRADE",
            "QUNATITY",
            "PP_CALL_RANK",
            "PP_CALL_SEQUENCE",
            "TENTATIVE_PP_IN_TIME",
            "EXECUTABLE_SHIFT",
        ]
        print(rail_order_details)
        # exit()
        # rail_order_details = rail_order_details.groupby(["RAIL_ORDER_ID","PACKER_CODE",'TL_CODE','BRAND','GRADE'],as_index=False).sum()
        # rail_order_details.columns= ["RAIL_ORDER","PACKER_CODE","TL_CODE","BRAND","GRADE","ORDER_PROCESSING_TIME","PP_CALL_RANK","PP_CALL_SEQUENCE","TENTATIVE_PP_IN_TIME","EXECUTABLE_SHIFT","QUANTITY"]
        # print(rail_order_details)
        # rail_order_details.to_csv('rail_order_details.csv')
        # exit()

        shift_details = result.groupby(["PLANT"], as_index=False).agg(
            {"PACKER": pd.Series.nunique, "TRUCK_LOADER": pd.Series.nunique}
        )

        packer_details = get_packer_details(cnxn, plant_input)
        result = result.merge(packer_details, on=["PLANT", "PACKER", "TRUCK_LOADER"])
        shift_details.rename(
            columns={"PACKER": "number_of_packer", "TRUCK_LOADER": "number_of_tl"},
            inplace=True,
        )
        shift_details["NO_OF_PACKER_WORKERS"] = (
            result[["PACKER", "WORKERS_REQ_FOR_PACKER"]]
            .drop_duplicates()["WORKERS_REQ_FOR_PACKER"]
            .sum()
        )
        shift_details["NO_OF_LOADER_WORKERS"] = (
            result[["TRUCK_LOADER", "WORKERS_REQ_FOR_PACKER", "WORKERS_REQ_FOR_TL"]]
            .drop_duplicates()["WORKERS_REQ_FOR_TL"]
            .sum()
        )

        return shift_details, order_details, ad_hoc_qty, rail_order_details

    # if __name__ == '__main__':

    #     plant_input = 'FGR'
    #     date_input = '2023-07-19'
    #     shift_input = 1

    #     shift_details, order_details, ad_hoc_qty, rail_order_details = run_model(plant_input,date_input,shift_input)

    # print(shift_details)
    # print(order_details)
    # print(rail_order_details)
    # print(ad_hoc_qty)
