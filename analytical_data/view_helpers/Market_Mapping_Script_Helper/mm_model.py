from datetime import datetime as dt

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta as rd
from django.conf import settings

from ..connection import connect_db
from .calc_market_branding_budget import calculate_brand_budget
from .channel_strategy import find_channel_stretegy
from .counter_strategy import find_counter_strategy
from .potential_rating import district_matrix
from .pricing_strategy import find_pricing_strategy
from .state_classifier import state_classification
from .static import (
    branding_budget_sql,
    channel_data_sql,
    growth_potential_sql,
    market_potential_sql,
    ncr_3_year_sql,
    ncr_threshold_sql,
    price_data_sql,
)
from .target_setting import target_setting


def get_inputs(plan_date):
    cnxn = connect_db()

    month = plan_date.strftime("%Y-%m-%d")

    target_setting_change = pd.read_sql(
        growth_potential_sql.format(
            month=(plan_date - rd(months=1)).strftime("%Y-%m-%d")
        ),
        cnxn,
    )
    target_setting_change["MONTH"] = target_setting_change["MONTH"].astype("str")
    unused_target_setting_change = target_setting_change.copy()

    market_share = pd.read_sql(market_potential_sql, cnxn)
    market_share["MONTH"] = market_share["MONTH"].astype("str")
    unused_market_share = market_share.copy()

    ncr_data = pd.read_sql(ncr_3_year_sql.format(month=month), cnxn)
    ncr_data["MONTH"] = ncr_data["MONTH"].astype("str")
    unused_ncr_data = ncr_data.copy()

    threshold_df = pd.read_sql(
        ncr_threshold_sql.format(
            month=month, month_start=(plan_date - rd(months=4)).strftime("%Y-%m-%d")
        ),
        cnxn,
    )
    unused_threshold_df = threshold_df.copy()

    # channel_data = pd.read_csv(settings.MARKET_MAPPING_CSV)
    # channel_data.columns = channel_data.columns.str.lower()

    channel_data = pd.read_sql(channel_data_sql, cnxn)
    # channel_data['COLLECTED_ON'] = channel_data['COLLECTED_ON'].astype('str')
    channel_data.columns = channel_data.columns.str.lower()

    # channel_data_cols_fnl = []
    # channel_data_cols = channel_data.columns.tolist()
    # for i in channel_data_cols:
    #     if ('sales' not in i) and (('retail' in i) or ('wholesale' in i)):
    #         channel_data_cols_fnl.append(i+'_sale')
    #     else:
    #         channel_data_cols_fnl.append(i)
    # channel_data.columns = channel_data_cols_fnl

    pricing_data = pd.read_sql(price_data_sql, cnxn)

    market_brand_data = pd.read_sql(branding_budget_sql, cnxn)

    cnxn.close()

    return (
        market_share,
        unused_market_share,
        ncr_data,
        unused_ncr_data,
        threshold_df,
        unused_threshold_df,
        target_setting_change,
        unused_target_setting_change,
        pricing_data,
        market_brand_data,
        channel_data,
    )


class MarketMappingViewHelper:
    def run_model(date_input):
        plan_date = dt.strptime(date_input, "%Y-%m-%d")

        run_id = 101

        (
            market_share,
            unused_market_share,
            ncr_data,
            unused_ncr_data,
            threshold_df,
            unused_threshold_df,
            target_setting_change,
            unused_target_setting_change,
            pricing_data,
            market_brand_data,
            channel_data,
        ) = get_inputs(plan_date)

        # ---------------------------------------------------------------------
        # 4X4 DISTRICT MONTHLY
        district_class = district_matrix(
            market_share, ncr_data, threshold_df, plan_date
        )
        # ----------------------------------------------------------------------
        # SALES TARGET
        market_share = unused_market_share.copy()
        ncr_data = unused_ncr_data.copy()
        matrix_strategy, total_target, product_target = target_setting(
            district_class, market_share, ncr_data, target_setting_change, plan_date
        )
        # ------------------------------------------------------------------------
        # PRICING STRATEGY
        pricing_strategy = find_pricing_strategy(
            matrix_strategy, pricing_data, plan_date
        )
        # ------------------------------------------------------------------------
        # MARKET BRAND BUDGETING
        ncr_data = unused_ncr_data.copy()
        brand_budget = calculate_brand_budget(
            total_target, market_brand_data, ncr_data, plan_date
        )
        # ------------------------------------------------------------------------
        # CHANNEL AND COUNTER STRATEGY
        channel_strategy = find_channel_stretegy(
            channel_data, matrix_strategy, total_target
        )

        counter_strategy = find_counter_strategy(channel_data)

        # -----------------------------------------------------------------
        # 4X4 MONTHLY STATE
        market_share = unused_market_share.copy()
        ncr_data = unused_ncr_data.copy()
        state_matrix = state_classification(ncr_data, market_share, plan_date)
        # ------------------------------------------------------------------

        matrix_strategy["RUN_ID"] = run_id
        total_target["RUN_ID"] = run_id
        product_target["RUN_ID"] = run_id
        state_matrix["RUN_ID"] = run_id
        channel_strategy["RUN_ID"] = run_id
        counter_strategy["RUN_ID"] = run_id
        brand_budget["RUN_ID"] = run_id
        pricing_strategy["RUN_ID"] = run_id

        matrix_strategy["Relative MS"] = np.nan
        matrix_strategy["Delta MS (Avg.)"] = np.nan
        matrix_strategy["UniqueID"] = np.nan
        matrix_strategy["ML Unique ID"] = np.nan
        matrix_strategy["MPS Unique ID"] = np.nan
        matrix_strategy["GS Unique ID"] = np.nan
        matrix_strategy["Targeted Market Share"] = np.nan

        matrix_strategy.rename(
            columns={"MARKET LEADER": "MARKET_LEADER", "NCR": "AVG_NCR"}, inplace=True
        )
        # 'Delta MS (Avg.)'
        matrix_db = matrix_strategy[
            [
                "RUN_ID",
                "ZONE",
                "STATE",
                "REGION",
                "DISTRICT",
                "BRAND",
                "PRODUCT",
                "SALES",
                "MARKET_POTENTIAL",
                "MARKET_SHARE",
                "PREV_YEAR_SHARE_DELTA",
                "PREV_MONTH_SHARE_DELTA",
                "LEADER_MARKET_SHARE",
                "MARKET_LEADER",
                "DELTA_MARKET_SHARE_MAX",
                # , 'UniqueID', 'ML Unique ID', 'MPS Unique ID', 'GS Unique ID',
                "NCR_MARKET_POTENTIAL_RATING",
                "MARKET_POTENTIAL_RATING",
                "MARKET_SHARE_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE_POTENTIAL_RATING",
                "MARKET_LUCRATIVENESS",
                "MARKET_POSITION",
                "MARKET_GROWTH_STRATEGY",
                "AVG_NCR",
            ]
        ]

        target_db = total_target[
            [
                "RUN_ID",
                "ZONE",
                "STATE",
                "REGION",
                "DISTRICT",
                "BRAND",
                "PRODUCT",
                "SALES",
                "TARGET_SALES",
                "NEXT",
                "FUTURE_MARKET_POTENTIAL",
            ]
        ]

        product_target.drop(columns=["TARGET_SALES"], inplace=True)
        product_target.rename(
            columns={"PROD_SALES_TARGET": "TARGET_SALES"}, inplace=True
        )
        product_target["SALES"] = np.nan
        product_target["FUTURE_MARKET_POTENTIAL"] = np.nan

        product_db = product_target[
            [
                "RUN_ID",
                "ZONE",
                "STATE",
                "REGION",
                "DISTRICT",
                "BRAND",
                "PRODUCT",
                "SALES",
                "TARGET_SALES",
                "NEXT",
                "FUTURE_MARKET_POTENTIAL",
            ]
        ]

        product_db.reset_index(inplace=True, drop=True)
        target_db.reset_index(inplace=True, drop=True)
        target_db_final = target_db.append(product_db, ignore_index=False)
        target_db_final = pd.concat([target_db, product_db], axis=0)

        # state_matrix['MARKET LEADER'] = 'NOT FETCHING IN THE CODE'
        state_matrix.rename(
            columns={
                "DELTA_SHARE_YEAR": "PREV_YEAR_SHARE_DELTA",
                "DELTA_SHARE_MONTH": "PREV_MONTH_SHARE_DELTA",
                "DELTA": "DELTA_MARKET_SHARE_MAX",
                "NCR_RATING": "NCR_MARKET_POTENTIAL_RATING",
                "MARKET_SHARE_RATING": "MARKET_SHARE_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE_RATING": "DELTA_MARKET_SHARE_POTENTIAL_RATING",
            },
            inplace=True,
        )

        state_db = state_matrix[
            [
                "RUN_ID",
                "ZONE",
                "STATE",
                "BRAND",
                "SALES",
                "AVG_NCR",
                "MARKET_POTENTIAL",
                "MARKET_SHARE",
                "PREV_YEAR_SHARE_DELTA",
                "PREV_MONTH_SHARE_DELTA",
                "LEADER_MARKET_SHARE",
                "DELTA_MARKET_SHARE_MAX",
                "NCR_MARKET_POTENTIAL_RATING",
                "MARKET_POTENTIAL_RATING",
                "MARKET_SHARE_POTENTIAL_RATING",
                "DELTA_MARKET_SHARE_POTENTIAL_RATING",
                "MARKET_LUCRATIVENESS",
                "MARKET_POSITION",
                "MARKET_GROWTH_STRATEGY",
            ]
        ]

        channel_strategy["ZONE"] = "DUMMY"
        channel_strategy["REGION"] = "DUMMY"
        channel_strategy.columns = channel_strategy.columns.str.upper()
        channel_strategy.reset_index(inplace=True, drop=False)
        # channel_strat_db = channel_strategy[['RUN_ID', 'STATE', 'DISTRICT', 'BRAND', 'FUTURE_MARKET_SHARE',
        #                                       'COUNTER_SHARE', 'ACV', 'COUNTER_SHARE_TARGET',
        #                                       'MIN_TARGET_ACV', 'MAX_TARGET_ACV']]
        if len(channel_strategy) == 0:
            channel_strategy = pd.DataFrame(
                columns=[
                    "RUN_ID",
                    "STATE",
                    "DISTRICT",
                    "BRAND",
                    "TOTAL_RETAIL_SALES",
                    "COUNTER_SHARE",
                    "TOTAL_SALES",
                    "ACV",
                    "MARKET_GROWTH_STRATEGY",
                    "MIN_TARGET_ACV",
                    "MAX_TARGET_ACV",
                    "FUTURE_MARKET_SHARE",
                    "FUTURE_MARKET_SHARE_THRES",
                    "COUNTER_SHARE_TARGET",
                    "COUNTER_SHARE_STRATEGY",
                    "RETAIL_SALE",
                ]
            )
        channel_strat_db = channel_strategy[
            [
                "RUN_ID",
                "STATE",
                "DISTRICT",
                "BRAND",
                "TOTAL_RETAIL_SALES",
                "COUNTER_SHARE",
                "TOTAL_SALES",
                "ACV",
                "MARKET_GROWTH_STRATEGY",
                "MIN_TARGET_ACV",
                "MAX_TARGET_ACV",
                "FUTURE_MARKET_SHARE",
                "FUTURE_MARKET_SHARE_THRES",
                "COUNTER_SHARE_TARGET",
                "COUNTER_SHARE_STRATEGY",
                "RETAIL_SALE",
            ]
        ]

        counter_strategy["ZONE"] = "DUMMY"
        counter_strategy["REGION"] = "DUMMY"
        counter_strategy.reset_index(inplace=True, drop=False)
        counter_strategy.columns = counter_strategy.columns.str.upper()
        # counter_strat_db = counter_strategy[['ZONE', 'STATE', 'REGION', 'DISTRICT', 'BRAND',
        #                                      'COUNTER_NAME', 'SCL_RETAIL_SALE', 'TOTAL_RETAIL_SALES',
        #                                      'COUNTER_SHARE', 'COUNTER_SHARE_ACTION']]
        counter_strat_db = counter_strategy[
            [
                "RUN_ID",
                "STATE",
                "DISTRICT",
                "BRAND",
                "COUNTER_NAME",
                "COUNTER_ID",
                "ADDRESS_BLOCK",  # 'COLLECTED_ON',
                "COUNTER_SHARE_ACTION",
                "TOTAL_RETAIL_SALES",
                "COUNTER_SHARE",
                "TOTAL_MARKET_SALE",  # 'CONTRIBUTION_TO_MARKET_SALE',
                "SCL_RETAIL_SALE",
                "SCL_COUNTER_SHARE",
                "RETAIL_SALE",
            ]
        ]
        counter_strat_db.rename(columns={"COUNTER_ID": "CRM_CUSTOMER_ID"}, inplace=True)
        counter_strat_db[
            [
                "SCL_RETAIL_SALE",
                "SCL_COUNTER_SHARE",
                "RETAIL_SALE",
                "COUNTER_SHARE",
                "TOTAL_MARKET_SALE",
                "TOTAL_RETAIL_SALES",
            ]
        ] = counter_strat_db[
            [
                "SCL_RETAIL_SALE",
                "SCL_COUNTER_SHARE",
                "RETAIL_SALE",
                "COUNTER_SHARE",
                "TOTAL_MARKET_SALE",
                "TOTAL_RETAIL_SALES",
            ]
        ].fillna(
            0
        )
        counter_strat_db[
            [
                "SCL_RETAIL_SALE",
                "SCL_COUNTER_SHARE",
                "RETAIL_SALE",
                "COUNTER_SHARE",
                "TOTAL_MARKET_SALE",
                "TOTAL_RETAIL_SALES",
            ]
        ] = counter_strat_db[
            [
                "SCL_RETAIL_SALE",
                "SCL_COUNTER_SHARE",
                "RETAIL_SALE",
                "COUNTER_SHARE",
                "TOTAL_MARKET_SALE",
                "TOTAL_RETAIL_SALES",
            ]
        ].replace(
            np.inf, 0
        )

        brand_budget["ZONE"] = "DUMMY"
        brand_budget["REGION"] = "DUMMY"
        brand_budget.columns = brand_budget.columns.str.upper()
        brand_budget.rename(
            columns={
                "TOT_COST_RS_LAC": "TOT_COST_RS_LAC",
                "PER MT COST": "PER_MT_COST",
            },
            inplace=True,
        )
        brand_budget = brand_budget[
            [
                "RUN_ID",
                "STATE",
                "DISTRICT",
                "BRAND",
                "TOT_COST_RS_LAC",
                "QUANTITY_INVOICED",
                "TARGET_SALES",
                "PER_MT_COST",
                "NEW_COST",
                "MULTIPLIER",
                "BUDGET",
                "POS_BUDGET",
                "OUTDOOR_BUDGET",
                "EVENT_BUDGET",
                "CORPORATE_BUDGET",
                "TOTAL_BUDGET",
            ]
        ]

        pricing_strategy["ZONE"] = "DUMMY"
        pricing_strategy["REGION"] = "DUMMY"
        pricing_strategy.reset_index(inplace=True, drop=False)
        # print(pricing)
        pricing_strategy.columns = pricing_strategy.columns.str.upper()
        # pricing_strat_db = pricing_strategy[['RUN_ID', 'ZONE', 'STATE', 'REGION',
        #                                      'DISTRICT', 'BRAND',
        #                                      'WSP_PRICE', 'RSP_PRICE', 'WSP Price Leader',
        #                                      'WSP_LEADER_PRICE', 'RSP_LEADER_PRICE', 'RSP_LEADER_GAP',
        #                                      'WSP_LEADER_GAP', 'RSP_LEADER_GAP', 'rsp_min_margin', 'rsp_max_margin', 'wsp_min_margin', 'wsp_max_margin']]

        # pricing_strategy.rename(columns= {'WSP PRICE LEADER': 'WSP_PRICE_LEADER', 'RSP PRICE LEADER':'RSP_PRICE_LEADER'}, inplace= True)
        # pricing_strategy = pricing_strategy[['RUN_ID', 'STATE', 'DISTRICT', 'BRAND', 'WSP_PRICE',
        #                                     'WSP_LEADER_PRICE', 'WSP_LEADER_GAP', 'WSP_PRICE_LEADER',
        #                                     'WSP_MIN_MARGIN', 'WSP_MAX_MARGIN', 'RSP_PRICE', 'RSP_LEADER_PRICE',
        #                                     'RSP_LEADER_GAP', 'RSP_PRICE_LEADER', 'RSP_MIN_MARGIN', 'RSP_MAX_MARGIN']]

        return (
            matrix_db,
            target_db_final,
            state_db,
            channel_strat_db,
            counter_strat_db,
            brand_budget,
            pricing_strategy,
        )

    # if __name__=='__main__':

    # date_input = '2023-03-01'

    # district_clsf,sales_target,state_clsf,channel_strat,counter_strat,brand_budget,pricing_strategy = run_model(date_input)

    # # print(district_clsf.to_csv('district_clsf.csv',index=False))
    # # print(state_clsf.to_csv('state_clsf.csv',index=False))
    # # print(sales_target.to_csv('sales_target.csv',index=False))
    # # channel_strat.to_csv('channel_strat.csv',index=False)
    # # counter_strat.to_csv('counter_strat.csv',index=False)
    # print(counter_strat)
    # brand_budget.to_csv('brand_budget.csv',index=False)

    # print(district_clsf)
    # print(state_clsf)
    # print(sales_target)
