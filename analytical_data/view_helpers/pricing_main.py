import datetime

import numpy as np
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from dateutil.relativedelta import relativedelta
from django.conf import settings

from .connection import connect_db
from .pricing_static import (
    market_growth,
    market_luc,
    market_pos,
    org_brand_map,
    pricing_strategy_map,
)

cnxn = connect_db()


class PricingHelper:
    def run_model(date):
        # Input Files:
        market_share = pd.read_sql(
            f""" SELECT "ID",	"ZONE",	"STATE",	"DISTRICT",	upper("BRAND") as "BRAND",	"MONTH",	"SALES",	"MARKET_POTENTIAL",	"MARKET_SHARE",	"DELTA_MARKET_SHARE",	"business_segment",	"grade" FROM target."NM_MARKET_SHARE_POTENTIAL" where "MONTH"='{date}' """,
            cnxn,
        )  # NEW MARKET, MS,MP, DMS
        # market_share.to_csv('market_share.csv')
        price_of_competitors = pd.read_sql(
            f""" SELECT * FROM etl_zone."COMPETITION_PRICE_NEW_MARKETS" WHERE "PRICE"='WSP' and "DATE"='{date}' """,
            cnxn,
        )
        # price_of_competitors.to_csv('price_of_competitors.csv')

        # for prod

        ncr_input_files = pd.read_sql(
            """select  "STATE","DISTRICT","NCR","QUANTITY_INVOICED","ORG_ID" from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
                                    WHERE "INVOICE_DATE" > current_timestamp - interval '30 day' """,
            cnxn,
        )  # for last 30 days

        # do changes in MS SHARE file i.e base file
        state_file = pd.read_csv(settings.STATE_FILE_CSV)
        market_share = pd.merge(market_share, state_file, on="STATE", how="left")

        # for prod

        ncr_input_files_threshold = pd.read_sql(
            """select "STATE","DISTRICT","NCR","QUANTITY_INVOICED","ORG_ID" from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
                                            WHERE "INVOICE_DATE" >= current_date - interval '3' year and
                                            "INVOICE_DATE" < current_date """,
            cnxn,
        )  # for last 3 years

        # for prod
        market_mapping_market_potential = pd.read_sql(
            """ select "ID", "STATE", "DISTRICT", upper("BRAND") as "BRAND" , "MONTH", "SALES",
            "MARKET_POTENTIAL", "MARKET_SHARE" from etl_zone."MARKET_MAPPING_MARKET_POTENTIAL"
                                                    where "MONTH" = (date_trunc('month',now() - interval '2 month')::timestamp::date) """,
            cnxn,
        )  # 2 months before of plan month

        # Making a final table from all combinations and concept
        # In ncr input files org id is given not brand name so making brand column
        ncr_input_files["BRAND"] = ncr_input_files["ORG_ID"].map(org_brand_map)
        ncr_input_files_threshold["BRAND"] = ncr_input_files_threshold["ORG_ID"].map(
            org_brand_map
        )

        # Ready Master table i.e main_table
        ncr_input_files["STATE_ERP"] = ncr_input_files["STATE"].copy()
        ms_and_ncr = pd.merge(
            market_share, ncr_input_files, on=["STATE_ERP", "BRAND"], how="left"
        )  # merge market share and ncr input files on the basis of State

        options_south_west_ncr = ["Andhra Pradesh", "Karnatatak", "Telangana"]
        south_west_percentile_ncr = ms_and_ncr[
            ms_and_ncr["STATE_x"].isin(options_south_west_ncr)
        ]
        south_west_percentile_ncr = south_west_percentile_ncr[
            ["QUANTITY_INVOICED", "NCR"]
        ].mean()
        print(south_west_percentile_ncr)

        options_north_ncr = ["Jammu Kashmir", "Himachal"]
        north_percentile_ncr = ms_and_ncr[ms_and_ncr["STATE_x"].isin(options_north_ncr)]
        north_percentile_ncr = north_percentile_ncr[["QUANTITY_INVOICED", "NCR"]].mean()
        print(north_percentile_ncr)

        options_east_ncr = ["Bihar", "Bihar-S", "Jharkhand", "Orissa", "West Bengal"]
        east_percentile_ncr = ms_and_ncr[ms_and_ncr["STATE_x"].isin(options_east_ncr)]
        east_percentile_ncr = east_percentile_ncr[["QUANTITY_INVOICED", "NCR"]].mean()
        print(east_percentile_ncr)

        for i in range(0, len(ms_and_ncr)):
            if (ms_and_ncr["STATE_ERP"][i] == "Tamil Nadu") or (
                ms_and_ncr["STATE_ERP"][i] == "Kerela"
            ):
                ms_and_ncr["QUANTITY_INVOICED"][i] = south_west_percentile_ncr[0]
                ms_and_ncr["NCR"][i] = south_west_percentile_ncr[1]

            if (
                (ms_and_ncr["STATE_ERP"][i] == "Gujarat")
                or (ms_and_ncr["STATE_ERP"][i] == "Punjab")
                or (ms_and_ncr["STATE_ERP"][i] == "Punjab-S")
                or (ms_and_ncr["STATE_ERP"][i] == "Rajasthan-A")
                or (ms_and_ncr["STATE_ERP"][i] == "Rajasthan-B")
                or (ms_and_ncr["STATE_ERP"][i] == "Rajasthan-C")
            ):
                ms_and_ncr["QUANTITY_INVOICED"][i] = north_percentile_ncr[0]
                ms_and_ncr["NCR"][i] = north_percentile_ncr[1]

            if (
                (ms_and_ncr["STATE_ERP"][i] == "Meghalaya")
                or (ms_and_ncr["STATE_ERP"][i] == "Arunachal Pradesh")
                or (ms_and_ncr["STATE_ERP"][i] == "Nagaland")
                or (ms_and_ncr["STATE_ERP"][i] == "Mazipur")
                or (ms_and_ncr["STATE_ERP"][i] == "Tripura")
                or (ms_and_ncr["STATE_ERP"][i] == "Mizoram")
                or (ms_and_ncr["STATE_ERP"][i] == "Sikkim")
            ):
                ms_and_ncr["QUANTITY_INVOICED"][i] = east_percentile_ncr[0]
                ms_and_ncr["NCR"][i] = east_percentile_ncr[1]

        # ms_and_ncr.to_csv('ms_and_ncr.csv')

        ms_and_ncr["MUL"] = ms_and_ncr["NCR"] * ms_and_ncr["QUANTITY_INVOICED"]
        ms_and_ncr = ms_and_ncr.groupby(["STATE_x", "BRAND"], as_index=False).sum("MUL")
        ms_and_ncr["FINAL_VALUE"] = (
            ms_and_ncr["MUL"] / ms_and_ncr["QUANTITY_INVOICED"]
        )  # Sum product concept on the basis of NCR and quantity on the basis of state and brand

        ms_and_ncr.rename(columns={"STATE_x": "STATE"}, inplace=True)

        main_table = pd.merge(
            market_share, ms_and_ncr, on=["STATE", "BRAND"], how="left"
        )  # merge market share and ncr input files on the basis of State
        main_table.rename(
            columns={
                "ID_x": "ID",
                "SALES_x": "SALES",
                "MARKET_POTENTIAL_x": "MARKET_POTENTIAL",
                "MARKET_SHARE_x": "MARKET_SHARE",
                "DELTA_MARKET_SHARE_x": "DELTA_MARKET_SHARE",
                "business_segment": "BUSINESS_SEGMENT",
                "grade": "GRADE",
                "FINAL_VALUE": "NCR_VALUE",
            },
            inplace=True,
        )
        main_table = main_table[
            [
                "ID",
                "ZONE",
                "STATE",
                "DISTRICT",
                "BRAND",
                "MONTH",
                "SALES",
                "MARKET_POTENTIAL",
                "MARKET_SHARE",
                "DELTA_MARKET_SHARE",
                "BUSINESS_SEGMENT",
                "GRADE",
                "QUANTITY_INVOICED",
                "ORG_ID",
                "NCR_VALUE",
                "STATE_ERP",
            ]
        ]

        # Merge Main table and ncr threshold
        ncr_input_files_threshold["STATE_ERP"] = ncr_input_files_threshold[
            "STATE"
        ].copy()
        ncr_input_files_threshold["MUL_NCR_THRESHOLD"] = (
            ncr_input_files_threshold["NCR"]
            * ncr_input_files_threshold["QUANTITY_INVOICED"]
        )
        ncr_input_files_threshold = ncr_input_files_threshold.groupby(
            ["STATE_ERP", "BRAND"], as_index=False
        ).sum("MUL_NCR_THRESHOLD")
        ncr_input_files_threshold["FINAL_VALUE_NCR_THRESHOLD"] = (
            ncr_input_files_threshold["MUL_NCR_THRESHOLD"]
            / ncr_input_files_threshold["QUANTITY_INVOICED"]
        )  # Sum product concept on the basis of NCR and quantity on the basis of state and brand

        # ncr_input_files_threshold.rename(columns = {'STATE_x':'STATE'}, inplace = True)
        ncr_input_files_threshold = ncr_input_files_threshold[
            ["STATE_ERP", "BRAND", "FINAL_VALUE_NCR_THRESHOLD"]
        ]
        # ncr_input_files_threshold.rename(columns = {'STATE_ERP':'STATE'}, inplace = True)
        main_table = pd.merge(
            main_table, ncr_input_files_threshold, on=["STATE_ERP", "BRAND"], how="left"
        )  # merge market share and ncr input files on the basis of State

        options_south_west_ncr_thres = ["Andhra Pradesh", "Karnatatak", "Telangana"]
        south_west_percentile_ncr_thres = main_table[
            main_table["STATE"].isin(options_south_west_ncr_thres)
        ]
        south_west_percentile_ncr_thres = south_west_percentile_ncr_thres[
            ["FINAL_VALUE_NCR_THRESHOLD"]
        ].mean()
        print(south_west_percentile_ncr_thres)

        options_north_ncr_thres = ["Jammu Kashmir", "Himachal"]
        north_percentile_ncr_thres = main_table[
            main_table["STATE"].isin(options_north_ncr_thres)
        ]
        north_percentile_ncr_thres = north_percentile_ncr_thres[
            ["FINAL_VALUE_NCR_THRESHOLD"]
        ].mean()
        print(north_percentile_ncr_thres)

        options_east_ncr_thres = [
            "Bihar",
            "Bihar-S",
            "Jharkhand",
            "Orissa",
            "West Bengal",
        ]
        east_percentile_ncr_thres = main_table[
            main_table["STATE"].isin(options_east_ncr_thres)
        ]
        east_percentile_ncr_thres = east_percentile_ncr_thres[
            ["FINAL_VALUE_NCR_THRESHOLD"]
        ].mean()
        print(east_percentile_ncr_thres)

        for i in range(0, len(main_table)):
            if (main_table["STATE_ERP"][i] == "Tamil Nadu") or (
                main_table["STATE_ERP"][i] == "Kerela"
            ):
                main_table["FINAL_VALUE_NCR_THRESHOLD"][
                    i
                ] = south_west_percentile_ncr_thres

            if (
                (main_table["STATE_ERP"][i] == "Gujarat")
                or (main_table["STATE_ERP"][i] == "Punjab")
                or (main_table["STATE_ERP"][i] == "Punjab-S")
                or (main_table["STATE_ERP"][i] == "Rajasthan-A")
                or (main_table["STATE_ERP"][i] == "Rajasthan-B")
                or (main_table["STATE_ERP"][i] == "Rajasthan-C")
            ):
                main_table["FINAL_VALUE_NCR_THRESHOLD"][i] = north_percentile_ncr_thres

            if (
                (main_table["STATE_ERP"][i] == "Meghalaya")
                or (main_table["STATE_ERP"][i] == "Arunachal Pradesh")
                or (main_table["STATE_ERP"][i] == "Nagaland")
                or (main_table["STATE_ERP"][i] == "Mazipur")
                or (main_table["STATE_ERP"][i] == "Tripura")
                or (main_table["STATE_ERP"][i] == "Mizoram")
                or (main_table["STATE_ERP"][i] == "Sikkim")
            ):
                main_table["FINAL_VALUE_NCR_THRESHOLD"][i] = east_percentile_ncr_thres

        main_table = main_table[
            [
                "ID",
                "ZONE",
                "STATE",
                "STATE_ERP",
                "DISTRICT",
                "BRAND",
                "MONTH",
                "SALES",
                "MARKET_POTENTIAL",
                "MARKET_SHARE",
                "DELTA_MARKET_SHARE",
                "BUSINESS_SEGMENT",
                "GRADE",
                "QUANTITY_INVOICED",
                "NCR_VALUE",
                "FINAL_VALUE_NCR_THRESHOLD",
            ]
        ]
        # main_table.to_csv('final_table.csv')

        # Merge Main table and market mapping market potential
        market_potential_share_base_50_percentile = (
            market_mapping_market_potential.groupby(["STATE", "BRAND"], as_index=False)[
                "MARKET_POTENTIAL", "MARKET_SHARE"
            ].quantile(0.50)
        )
        # for new state and district
        options_south_west = ["Andhra Pradesh", "Karnatatak", "Telangana"]
        south_west_percentile = market_mapping_market_potential[
            market_mapping_market_potential["STATE"].isin(options_south_west)
        ]
        south_west_percentile = south_west_percentile[
            ["MARKET_POTENTIAL", "MARKET_SHARE"]
        ].quantile(0.5)

        # for jk and himachal
        options_north = ["Jammu Kashmir", "Himachal"]
        north_percentile = market_mapping_market_potential[
            market_mapping_market_potential["STATE"].isin(options_north)
        ]
        north_percentile = north_percentile[
            ["MARKET_POTENTIAL", "MARKET_SHARE"]
        ].quantile(0.5)

        # will do for meghalaya naga etc.
        options_east = ["Bihar", "Bihar-S", "Jharkhand", "Orissa", "West Bengal"]
        east_percentile = market_mapping_market_potential[
            market_mapping_market_potential["STATE"].isin(options_east)
        ]
        east_percentile = east_percentile[
            ["MARKET_POTENTIAL", "MARKET_SHARE"]
        ].quantile(0.5)

        market_potential_share_base_50_percentile.rename(
            columns={
                "MARKET_POTENTIAL": "MARKET_POTENTIAL_BASE",
                "MARKET_SHARE": "MARKET_SHARE_BASE",
            },
            inplace=True,
        )
        market_potential_share_base_50_percentile.loc[
            market_potential_share_base_50_percentile["STATE"] == "Chhattisgarh",
            "STATE",
        ] = "Chattisgarh"
        ms_and_mpms_base = pd.merge(
            market_share,
            market_potential_share_base_50_percentile,
            on=["STATE", "BRAND"],
            how="left",
        )  # merge market share and market mapping market potential on the basis of State
        final_base_table = pd.merge(
            ms_and_mpms_base, main_table, on=["DISTRICT", "BRAND"], how="left"
        )  # merge market share and market mapping market potential on the basis of State

        final_base_table.rename(
            columns={
                "ID_x": "ID",
                "ZONE_x": "ZONE",
                "STATE_x": "STATE",
                "MONTH_x": "MONTH",
                "SALES_x": "SALES",
                "MARKET_POTENTIAL_x": "MARKET_POTENTIAL",
                "MARKET_SHARE_x": "MARKET_SHARE",
                "DELTA_MARKET_SHARE_x": "DELTA_MARKET_SHARE",
            },
            inplace=True,
        )
        final_base_table = final_base_table[
            [
                "ID",
                "ZONE",
                "STATE",
                "DISTRICT",
                "BRAND",
                "MONTH",
                "SALES",
                "MARKET_POTENTIAL",
                "MARKET_POTENTIAL_BASE",
                "MARKET_SHARE",
                "MARKET_SHARE_BASE",
                "DELTA_MARKET_SHARE",
                "BUSINESS_SEGMENT",
                "GRADE",
                "QUANTITY_INVOICED",
                "NCR_VALUE",
                "FINAL_VALUE_NCR_THRESHOLD",
            ]
        ]

        # for new state and district
        for i in range(0, len(final_base_table)):
            if (final_base_table["STATE"][i] == "Tamil Nadu") or (
                final_base_table["STATE"][i] == "Kerela"
            ):
                final_base_table["MARKET_POTENTIAL_BASE"][i] = south_west_percentile[0]
                final_base_table["MARKET_SHARE_BASE"][i] = south_west_percentile[1]

            if (
                (main_table["STATE_ERP"][i] == "Gujarat")
                or (main_table["STATE_ERP"][i] == "Punjab")
                or (main_table["STATE_ERP"][i] == "Punjab-S")
                or (main_table["STATE_ERP"][i] == "Rajasthan-A")
                or (main_table["STATE_ERP"][i] == "Rajasthan-B")
                or (main_table["STATE_ERP"][i] == "Rajasthan-C")
            ):
                final_base_table["MARKET_POTENTIAL_BASE"][i] = north_percentile[0]
                final_base_table["MARKET_SHARE_BASE"][i] = north_percentile[1]

            if (
                (main_table["STATE_ERP"][i] == "Meghalaya")
                or (main_table["STATE_ERP"][i] == "Arunachal Pradesh")
                or (main_table["STATE_ERP"][i] == "Nagaland")
                or (main_table["STATE_ERP"][i] == "Mazipur")
                or (main_table["STATE_ERP"][i] == "Tripura")
                or (main_table["STATE_ERP"][i] == "Mizoram")
                or (main_table["STATE_ERP"][i] == "Sikkim")
            ):
                final_base_table["MARKET_POTENTIAL_BASE"][i] = east_percentile[0]
                final_base_table["MARKET_SHARE_BASE"][i] = east_percentile[1]

        final_base_table["MARKET_POTENTIAL_THRESHOLD"] = None
        for i in range(len(final_base_table)):
            if (
                final_base_table["MARKET_POTENTIAL"][i]
                <= final_base_table["MARKET_POTENTIAL_BASE"][i]
            ):
                final_base_table["MARKET_POTENTIAL_THRESHOLD"][i] = "Low"
            else:
                final_base_table["MARKET_POTENTIAL_THRESHOLD"][i] = "High"

        final_base_table["MARKET_SHARE_THRESHOLD"] = None
        for i in range(len(final_base_table)):
            if (
                final_base_table["MARKET_SHARE"][i]
                <= final_base_table["MARKET_SHARE_BASE"][i]
            ):
                final_base_table["MARKET_SHARE_THRESHOLD"][i] = "Low"
            else:
                final_base_table["MARKET_SHARE_THRESHOLD"][i] = "High"

        final_base_table["DELTA_MARKET_SHARE_THRESHOLD"] = None
        for i in range(len(final_base_table)):
            if final_base_table["DELTA_MARKET_SHARE"][i] >= 0:
                final_base_table["DELTA_MARKET_SHARE_THRESHOLD"][i] = "High"
            else:
                final_base_table["DELTA_MARKET_SHARE_THRESHOLD"][i] = "Low"

        final_base_table["NCR_VALUE_THRESHOLD"] = None
        for i in range(len(final_base_table)):
            if (
                final_base_table["NCR_VALUE"][i]
                >= final_base_table["FINAL_VALUE_NCR_THRESHOLD"][i]
            ):
                final_base_table["NCR_VALUE_THRESHOLD"][i] = "High"
            else:
                final_base_table["NCR_VALUE_THRESHOLD"][i] = "Low"

        # SECTION 2
        def get_market_strategy(final_base_table):
            final_base_table["MARKET_POSITION"] = (
                final_base_table["DELTA_MARKET_SHARE_THRESHOLD"]
                + "|"
                + final_base_table["MARKET_SHARE_THRESHOLD"]
            )
            final_base_table["MARKET_POSITION"] = final_base_table[
                "MARKET_POSITION"
            ].map(market_pos)

            final_base_table["MARKET_LUCRATIVENESS"] = (
                final_base_table["NCR_VALUE_THRESHOLD"]
                + "|"
                + final_base_table["MARKET_POTENTIAL_THRESHOLD"]
            )
            final_base_table["MARKET_LUCRATIVENESS"] = final_base_table[
                "MARKET_LUCRATIVENESS"
            ].map(market_luc)

            final_base_table["MARKET_GROWTH_STRATEGY"] = (
                final_base_table["MARKET_POSITION"]
                + "|"
                + final_base_table["MARKET_LUCRATIVENESS"]
            )
            final_base_table["MARKET_GROWTH_STRATEGY"] = final_base_table[
                "MARKET_GROWTH_STRATEGY"
            ].map(market_growth)

            final_base_table["PRICING_STRATEGY"] = (
                final_base_table["MARKET_POSITION"]
                + "|"
                + final_base_table["MARKET_LUCRATIVENESS"]
            )
            final_base_table["PRICING_STRATEGY"] = final_base_table[
                "PRICING_STRATEGY"
            ].map(pricing_strategy_map)

            return final_base_table

        result = get_market_strategy(final_base_table)

        # Pricing Part
        # Merging Price competitor and final result

        percentile_50th_price = price_of_competitors.groupby(
            ["DISTRICT"], as_index=False
        )["VALUE"].quantile(0.5)
        percentile_70th_price = price_of_competitors.groupby(
            ["DISTRICT"], as_index=False
        )["VALUE"].quantile(0.7)
        percentile_90th_price = price_of_competitors.groupby(
            ["DISTRICT"], as_index=False
        )["VALUE"].quantile(0.9)
        percentile_50_70th_price_final = pd.merge(
            percentile_50th_price, percentile_70th_price, on="DISTRICT", how="inner"
        )
        percentile_50_70_90th_price_final = pd.merge(
            percentile_50_70th_price_final,
            percentile_90th_price,
            on="DISTRICT",
            how="inner",
        )
        percentile_50_70_90th_price_final.rename(
            columns={
                "VALUE_x": "50TH_PERCENTILE",
                "VALUE_y": "70TH_PERCENTILE",
                "VALUE": "90TH_PERCENTILE",
            },
            inplace=True,
        )

        result = pd.merge(
            result, percentile_50_70_90th_price_final, on=["DISTRICT"], how="left"
        )
        result["FINAL_PRICE"] = None
        for i in range(0, len(result)):
            if result["PRICING_STRATEGY"][i] == "Accommodative":
                result["FINAL_PRICE"][i] = result["50TH_PERCENTILE"][i]
            elif result["PRICING_STRATEGY"][i] == "Assertive":
                result["FINAL_PRICE"][i] = result["70TH_PERCENTILE"][i]
            elif result["PRICING_STRATEGY"][i] == "Aggressive":
                result["FINAL_PRICE"][i] = result["90TH_PERCENTILE"][i]

        result = result[
            [
                "ID",
                "ZONE",
                "STATE",
                "DISTRICT",
                "BRAND",
                "MONTH",
                "SALES",
                "MARKET_POTENTIAL",
                "MARKET_POTENTIAL_BASE",
                "MARKET_SHARE",
                "MARKET_SHARE_BASE",
                "DELTA_MARKET_SHARE",
                "BUSINESS_SEGMENT",
                "GRADE",
                "QUANTITY_INVOICED",
                "NCR_VALUE",
                "FINAL_VALUE_NCR_THRESHOLD",
                "MARKET_POTENTIAL_THRESHOLD",
                "MARKET_SHARE_THRESHOLD",
                "DELTA_MARKET_SHARE_THRESHOLD",
                "NCR_VALUE_THRESHOLD",
                "MARKET_POSITION",
                "MARKET_LUCRATIVENESS",
                "MARKET_GROWTH_STRATEGY",
                "PRICING_STRATEGY",
                "FINAL_PRICE",
            ]
        ]

        leader = price_of_competitors.loc[
            price_of_competitors.groupby("DISTRICT")["VALUE"].idxmax(),
            ["BRAND", "VALUE", "DISTRICT", "REGION"],
        ]
        result = pd.merge(result, leader, on="DISTRICT", how="left")
        result.rename(
            columns={"BRAND_x": "BRAND", "BRAND_y": "MARKET LEADER"}, inplace=True
        )

        result["PREV_MONTH_SHARE_DELTA"] = 0.0
        result["PREV_YEAR_SHARE_DELTA"] = 0.0
        result["LEADER_MARKET_SHARE"] = 0.0
        result["MARKET_SHARE_MAX"] = 0.0
        result["DELTA_MARKET_SHARE_MAX"] = 0.0
        # m= (datetime.date.today() + relativedelta(months=1)).replace(day=1)
        print("result_plan_month_before", date)
        result["PLAN_MONTH"] = (pd.to_datetime(date) + relativedelta(months=1)).replace(
            day=1
        )
        print("result_plan_month_after", result["PLAN_MONTH"])
        print(result.info)
        result["PLAN_MONTH"] = result["PLAN_MONTH"].astype("datetime64[ns]")
        result["MONTH"] = result["MONTH"].astype("datetime64[ns]")
        print(result.info)

        result["WSP_PRICE"] = result["FINAL_PRICE"]
        result["RSP_PRICE"] = result["FINAL_PRICE"]
        result["pricing_strategy_driver"] = result["PRICING_STRATEGY"]

        result.rename(
            columns={
                "GRADE": "PRODUCT",
                "NCR_VALUE": "NCR",
                "NCR_VALUE_THRESHOLD": "NCR_MARKET_POTENTIAL_RATING",
                "MARKET_POTENTIAL_THRESHOLD": "MARKET_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE": "DELTA",
                "MARKET_SHARE_THRESHOLD": "MARKET_SHARE_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE_THRESHOLD": "DELTA_MARKET_SHARE_POTENTIAL_RATING",
                "PRICING_STRATEGY": "pricing_strategy",
                "BUSINESS_SEGMENT": "business_segment",
            },
            inplace=True,
        )

        result = result[
            [
                "STATE",
                "DISTRICT",
                "BRAND",
                "SALES",
                "PRODUCT",
                "NCR",
                "NCR_MARKET_POTENTIAL_RATING",
                "PREV_MONTH_SHARE_DELTA",
                "PREV_YEAR_SHARE_DELTA",
                "MARKET_POTENTIAL_RATING",
                "ID",
                "MONTH",
                "MARKET_POTENTIAL",
                "MARKET_SHARE",
                "ZONE",
                "REGION",
                "LEADER_MARKET_SHARE",
                "MARKET_SHARE_MAX",
                "MARKET LEADER",
                "DELTA",
                "DELTA_MARKET_SHARE_MAX",
                "MARKET_SHARE_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE_POTENTIAL_RATING",
                "PLAN_MONTH",
                "MARKET_POSITION",
                "MARKET_LUCRATIVENESS",
                "MARKET_GROWTH_STRATEGY",
                "pricing_strategy_driver",
                "pricing_strategy",
                "WSP_PRICE",
                "RSP_PRICE",
                "business_segment",
            ]
        ]
        # result.to_csv('result_final_30_may_new.csv')
        return result

    # For inserting data into database in table NM_MARKET_4X4_OUTPUT:

    def execute_values(cnxn, final_data):
        print(final_data.columns)
        tuples = [tuple(x) for x in final_data.to_numpy()]
        col = " "
        for i in list(final_data.columns):
            col += '"{0}"'.format(i) + ","
        col = col.strip(",")
        query = "INSERT INTO %s(%s) VALUES %%s" % (
            'etl_zone."NM_MARKET_4x4_OUTPUT"',
            col,
        )
        cursor = cnxn.cursor()

        try:
            extras.execute_values(cursor, query, tuples)
            cnxn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            cnxn.rollback()
            cursor.close()
            return 1
        print("the dataframe is inserted")
        cursor.close()

    # if __name__ == '__main__':
    #     date = datetime.date.today().replace(day=1)
    #     print(date)
    #     final_data = run_model(date)
    #     print(final_data)
    #     # execute_values(cnxn,final_data)
