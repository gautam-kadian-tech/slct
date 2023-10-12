import pandas as pd
from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
import dateutil.relativedelta
from .static import *


# org_brand_map = {102: 'Shree',
#                  103: 'Bangur',
#                  104: 'Rockstrong'
#                  }


def find_market_share_rating(req_brand_mark_share, delta=False):
    zones = req_brand_mark_share.Zone.unique()
    market_rating = pd.DataFrame()
    for zone in zones:
        df = req_brand_mark_share.loc[req_brand_mark_share.Zone == zone]
        # print(df.columns)
        states = df.Brand.unique()

        for state in states:
            state_data = df.loc[df.Brand == state]
            if delta:
                potential = state_data['delta']
                # perc_50 = np.percentile(potential, q=50)
                state_data['delta_market_share_rating'] = np.where(
                    state_data['delta'] >= 0, 'High', 'Low')

            else:
                potential = state_data['market_share_div_leader']
                perc_50 = np.percentile(potential, q=50)
                # print(state, perc_50)
                state_data['perc'] = perc_50
                state_data['market_share_rating'] = np.where(
                    state_data['market_share_div_leader'] >= perc_50, 'High', 'Low')
            market_rating = market_rating.append(state_data)
    return market_rating


def form_matrix(final_market_potential, market_share_potential, ncr_final_potential):

    # final_market_potential.drop(
    #     columns=['Month', 'Market share'], inplace=True)  # 'Zone', 'Region','Sale'

    # keys = ['State', 'Zone', 'Brand']
    # for key in keys:
    #     final_market_potential[key] = final_market_potential[key].str.capitalize(
    #     )
    #     market_share_potential[key] = market_share_potential[key].str.capitalize(
    #     )

    # mark_share = final_market_potential.set_index(keys).join(
    #     market_share_potential.set_index(keys), how='inner')
    # mark_share.reset_index(inplace=True)
    # # final_df = mark_share.set_index(['State', 'District', 'Brand']).join(ncr_final_potential.set_index(['State', 'District', 'Brand']),
    # #                                                                      how='outer')
    # keys = ['State', 'Zone', 'Brand']
    # for key in keys:
    #     ncr_final_potential[key] = ncr_final_potential[key].str.capitalize()
    #     mark_share[key] = mark_share[key].str.capitalize()

    # final_df = mark_share.merge(ncr_final_potential, on=keys,
    #                             how='inner')
    # final_df.reset_index(inplace=True)
    # final_df.drop(columns=['Ncr_x',  'rank', 'level_0', #'Quanity_invoiced',
    #                        #'Market_potential',
    #                        'index', 'Zone_x', 'Region_x',
    #                        'Sale', 'Zone_y', 'Region_y', 'prev_month_month',
    #                        'prev_month_sales', 'prev_month_share', 'prev_year_month',
    #                        'prev_year_sales', 'prev_year_share',
    #                        # 'prev_month_share_delta',
    #                        # 'prev_year_share_delta',
    #                        #'delta',
    #                        'market_share_max',
    #                         # 'delta_market_share_max',
    #                        #'Ncr_y',
    #                        'weighted_qty', 'Ncr_threshold', 'ncr_perc', 'Market share'],
    #               errors='ignore', inplace=True)
    # return final_df

    mark_pot = final_market_potential.drop(
        columns=['prev_month_market_share', 'prev_year_market_share'])
    # 'delta_share_month', 'delta_share_year', 'delta'#,Market_potential', 'market_share',

    market_share = market_share_potential.drop(columns=['Market_potential',
                                                        'market_share', 'prev_month_market_share', 'prev_year_market_share',
                                                        'delta_share_month', 'delta_share_year', 'delta'])
    # ncr_rating = ncr_final_potential.drop(columns= ['weighted_qty', 'avg_ncr', 'ncr_thresh'])
    ncr_rating = ncr_final_potential.copy()

    keys = ['State', 'Zone', 'Brand', 'Month']

    share_pot = mark_pot.merge(market_share, on=keys)
    ncr_share_pot = share_pot.merge(ncr_rating, on=keys)

    return ncr_share_pot


def get_market_strategy(df):
    df['market_position'] = df['delta_market_share_rating'] + \
        '|' + df['market_share_rating']
    df['market_position'] = df['market_position'].map(market_pos)

    df['market_lucrativeness'] = df['ncr_rating'] + \
        '|' + df['market_potential_rating']
    df['market_lucrativeness'] = df['market_lucrativeness'].map(market_luc)

    df['market_growth_strategy'] = df['market_position'] + \
        '|' + df['market_lucrativeness']
    df['market_growth_strategy'] = df['market_growth_strategy'].map(
        market_growth)

    return df


def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df

def state_classification(ncr_data, market_share, plan_month):
    # now = datetime.now()
    last_month = plan_month + dateutil.relativedelta.relativedelta(months=-2)
    this_month = last_month.month
    this_year = last_month.year
    # plan_month = now.replace(
    #     day=1) + dateutil.relativedelta.relativedelta(months=+1)

    # this_month = datetime.now().month
    # this_month = 9
    # this_year = datetime.now().year
    today = datetime.today()
    # today = '2022-10-01'  # datetime.now()
    # today = datetime.strptime(today, '%Y-%m-%d')
    prev_4 = today - relativedelta(months=4)

    # ncr_data = pd.read_csv('ncr_3_year.csv')
    # ncr_data = ncr_data[['STATE',	'DISTRICT', 'BRAND',
    #                      'PRODUCT', 'MONTH', 'NCR', 'QUANTITY_INVOICED']]
    ncr_data = convert_data_to_upper(ncr_data)
    ncr_data['MONTH'] = pd.to_datetime(ncr_data['MONTH'])
    ncr_avg_zone = ncr_data.loc[(ncr_data.MONTH.dt.month == this_month) &
                           (ncr_data.MONTH.dt.year == this_year)]
    ncr_avg_zone.columns = ncr_avg_zone.columns.str.title()

    
    # FIND AVG NCR
    
    ncr_avg_zone['weighted_qty'] = ncr_avg_zone['Quantity_Invoiced'] * \
        ncr_avg_zone['Ncr']

    avg_ncr = ncr_avg_zone.groupby(['State', 'Zone', 'Month', 'Brand'])[
        'Quantity_Invoiced', 'weighted_qty'].sum()
    avg_ncr['avg_ncr'] = avg_ncr['weighted_qty'] / avg_ncr['Quantity_Invoiced']

    # -----------------------------------------------------------------
    # FIND ZONE LEVEL NCR THRESH - SHIVANSH - AND THEN FIND NCR THRESHOLD

    # ncr_avg_zone['weighted_qty'] = ncr_avg_zone['Quantity_Invoiced'] * ncr_avg_zone['Ncr']
    # req_month = this_month - relativedelta(months=3)
    ncr_avg_thres_req = ncr_avg_zone.loc[(
        ncr_avg_zone.Month > prev_4) & (ncr_avg_zone.Month <= today)]
    avg_ncr_thres = ncr_avg_thres_req.groupby(['Zone', 'Brand'], as_index=False)[
        'Quantity_Invoiced', 'weighted_qty'].sum()
    avg_ncr_thres['ncr_thresh'] = avg_ncr_thres['weighted_qty'] / \
        avg_ncr_thres['Quantity_Invoiced']
    avg_ncr_thres = avg_ncr_thres[['Zone', 'Brand', 'ncr_thresh']]

    # avg_ncr_thres.to_csv('ncr_thres.csv')
    keys = ['Zone', 'Brand']
    avg_ncr.reset_index(inplace=True)
    ncr_joined = avg_ncr.merge(avg_ncr_thres, on=keys)
    ncr_joined['ncr_rating'] = np.where(
        ncr_joined['avg_ncr'] >= ncr_joined['ncr_thresh'], 'High', 'Low')
    ncr_joined.replace({'Brand': org_brand_map}, inplace=True)
    # -------------------------------------------------------------------------

    # --------------------------------------------------------------
    # read market share and form req data
    # market_share = pd.read_csv('market_potential.csv')
    market_share.columns = market_share.columns.str.capitalize()
    market_share = convert_data_to_upper(market_share)
    # market_share.drop(columns=['Zone'], inplace=True, errors='ignore')

    market_share['Month'] = pd.to_datetime(
        market_share['Month'])
    # keys = ['State', 'District']
    # market_share_zone = market_share.merge(zone_data, on=keys)

    market_share_state = market_share.groupby(
        ['State', 'Zone', 'Brand', 'Month'], as_index=False)['Sales'].sum()
    market_pot = market_share[[
        'State', 'Zone', 'District', 'Month', 'Market_potential']].drop_duplicates()
    market_pot_state = market_pot.groupby(['State', 'Zone', 'Month'], as_index=False)[
        'Market_potential'].sum()
    market_share_state = market_share_state.merge(
        market_pot_state, on=['State', 'Zone', 'Month'])
    market_share_state = market_share_state.loc[market_share_state.Sales != 0]
    market_share_state['market_share'] = market_share_state['Sales'] / \
        market_share_state['Market_potential']

    curr_market_share = market_share_state.loc[(market_share_state.Month.dt.month == this_month) &
                                               (market_share_state.Month.dt.year == this_year)]

    if this_month != 1:
        prev_month = this_month - 1
        this_year_m = this_year
    else:
        prev_month = 12
        this_year_m = this_year-1

    prev_month_market_share = market_share_state.loc[(market_share_state.Month.dt.month == prev_month) &
                                                     (market_share_state.Month.dt.year == this_year_m)]
    prev_month_market_share.drop(
        columns=['Sales', 'Month', 'Market_potential'], inplace=True)
    prev_month_market_share.rename(
        columns={'market_share': 'prev_month_market_share'}, inplace=True)

    prev_year_market_share = market_share_state.loc[(market_share_state.Month.dt.month == this_month) &
                                                    (market_share_state.Month.dt.year == this_year-1)]
    prev_year_market_share.drop(
        columns=['Sales', 'Month', 'Market_potential'], inplace=True)
    prev_year_market_share.rename(
        columns={'market_share': 'prev_year_market_share'}, inplace=True)

    keys = ['State', 'Zone', 'Brand']

    fin_mark_share = curr_market_share.merge(prev_month_market_share, on=keys)
    fin_mark_share = fin_mark_share.merge(prev_year_market_share, on=keys)

    # -----------------------------------------------------------------------------
    # find max market share leader
    mark_leader = fin_mark_share.loc[~fin_mark_share.Brand.str.upper().isin(
        ['SHREE', 'ROCKSTRONG', 'SCL', 'BANGUR'])]
    leader_data = mark_leader.groupby(['Zone', 'State', 'Month'], as_index=False)[
        'market_share'].max()
    keys = ['Zone', 'State', 'Month', 'market_share']
    market_leader_brand = leader_data.merge(mark_leader, on=keys)

    req_mark_share = fin_mark_share.loc[fin_mark_share.Brand.str.upper().isin(
        ['SHREE', 'ROCKSTRONG', 'SCL', 'BANGUR'])]

    # req_brand_mark_share = req_mark_share.append(market_leader_brand, ignore_index= True) UNCOMMENT TO GET LEADER BRAND NAME IN DATA< IMPACT: REMOVE THIS BRAND WHEN CALCULATING MARKET SHARE RATING
    leader_data.rename(
        columns={'market_share': 'leader_market_share'}, inplace=True)
    req_brand_mark_share = req_mark_share.merge(
        leader_data, on=['Zone', 'State', 'Month'])
    # ---------------------------
    # Divide market share by market share leader
    req_brand_mark_share['market_share_div_leader'] = req_brand_mark_share['market_share'] / \
        req_brand_mark_share['leader_market_share']

    req_brand_mark_share['delta_share_month'] = req_brand_mark_share['market_share'] - \
        req_brand_mark_share['prev_month_market_share']
    req_brand_mark_share['delta_share_year'] = req_brand_mark_share['market_share'] - \
        req_brand_mark_share['prev_year_market_share']
    thres = 0.5
    req_brand_mark_share['delta'] = thres * (
        req_brand_mark_share['delta_share_month'] + req_brand_mark_share['delta_share_year'])

    # -----------------------------------------------------------------------------------
    # FIND DELTA MARKET SHARE RATING
    market_rating = find_market_share_rating(req_brand_mark_share, delta=False)
    market_rating = find_market_share_rating(market_rating, delta=True)

    # --------------------------------------------------------------------------------
    # Market_potential

    zones = req_brand_mark_share.Zone.unique()
    final_market_potential = pd.DataFrame()

    for zone in zones:
        df = req_brand_mark_share.loc[req_brand_mark_share.Zone == zone]
        potential = df['Market_potential']
        perc_50 = np.percentile(potential, q=50)
        df['market_potential_rating'] = np.where(
            df['Market_potential'] >= perc_50, 'High', 'Low')

        final_market_potential = final_market_potential.append(df)
    # -----------------------------------------------------------------------

    final_df = form_matrix(final_market_potential, market_rating, ncr_joined)

    final_df = get_market_strategy(final_df)

    final_df['plan_month'] = plan_month
    final_df.columns = final_df.columns.str.upper()
    final_df.drop(columns=['SALES_Y', 'LEADER_MARKET_SHARE_Y',
                'MARKET_SHARE_DIV_LEADER_Y'], inplace=True)
    final_df.rename(columns={'SALES_X':  'SALES', 
                            'LEADER_MARKET_SHARE_X': 'LEADER_MARKET_SHARE',
                            'MARKET_SHARE_DIV_LEADER_X': 'MARKET_SHARE_DIV_LEADER'}, 
                   inplace=True)
    # final_df.to_csv('state_classification_out2.csv')
    
    return final_df


if __name__ == '__main__':
    now = datetime.now()
    last_month = now + dateutil.relativedelta.relativedelta(months=-2)
    this_month = last_month.month
    this_year = last_month.year
    plan_month = now.replace(
        day=1) + dateutil.relativedelta.relativedelta(months=+1)

    # this_month = datetime.now().month
    # this_month = 9
    # this_year = datetime.now().year
    # today = datetime.today()
    today = '2022-10-01'  # datetime.now()
    today = datetime.strptime(today, '%Y-%m-%d')
    prev_4 = today - relativedelta(months=4)

    ncr_data = pd.read_csv('ncr_3_year.csv')
    # ncr_data = ncr_data[['STATE',	'DISTRICT', 'BRAND',
    #                      'PRODUCT', 'MONTH', 'NCR', 'QUANTITY_INVOICED']]
    ncr_data = convert_data_to_upper(ncr_data)
    ncr_data['MONTH'] = pd.to_datetime(ncr_data['MONTH'])
    ncr_avg_zone = ncr_data.loc[(ncr_data.MONTH.dt.month == this_month) &
                           (ncr_data.MONTH.dt.year == this_year)]
    ncr_avg_zone.columns = ncr_avg_zone.columns.str.title()

    
    # FIND AVG NCR
    
    ncr_avg_zone['weighted_qty'] = ncr_avg_zone['Quantity_Invoiced'] * \
        ncr_avg_zone['Ncr']

    avg_ncr = ncr_avg_zone.groupby(['State', 'Zone', 'Month', 'Brand'])[
        'Quantity_Invoiced', 'weighted_qty'].sum()
    avg_ncr['avg_ncr'] = avg_ncr['weighted_qty'] / avg_ncr['Quantity_Invoiced']

    # -----------------------------------------------------------------
    # FIND ZONE LEVEL NCR THRESH - SHIVANSH - AND THEN FIND NCR THRESHOLD

    # ncr_avg_zone['weighted_qty'] = ncr_avg_zone['Quantity_Invoiced'] * ncr_avg_zone['Ncr']
    # req_month = this_month - relativedelta(months=3)
    ncr_avg_thres_req = ncr_avg_zone.loc[(
        ncr_avg_zone.Month > prev_4) & (ncr_avg_zone.Month <= today)]
    avg_ncr_thres = ncr_avg_thres_req.groupby(['Zone', 'Brand'], as_index=False)[
        'Quantity_Invoiced', 'weighted_qty'].sum()
    avg_ncr_thres['ncr_thresh'] = avg_ncr_thres['weighted_qty'] / \
        avg_ncr_thres['Quantity_Invoiced']
    avg_ncr_thres = avg_ncr_thres[['Zone', 'Brand', 'ncr_thresh']]

    avg_ncr_thres.to_csv('ncr_thres.csv')
    keys = ['Zone', 'Brand']
    avg_ncr.reset_index(inplace=True)
    ncr_joined = avg_ncr.merge(avg_ncr_thres, on=keys)
    ncr_joined['ncr_rating'] = np.where(
        ncr_joined['avg_ncr'] >= ncr_joined['ncr_thresh'], 'High', 'Low')
    ncr_joined.replace({'Brand': org_brand_map}, inplace=True)
    # -------------------------------------------------------------------------

    # --------------------------------------------------------------
    # read market share and form req data
    market_share = pd.read_csv('market_potential.csv')
    market_share.columns = market_share.columns.str.capitalize()
    market_share = convert_data_to_upper(market_share)
    # market_share.drop(columns=['Zone'], inplace=True, errors='ignore')

    market_share['Month'] = pd.to_datetime(
        market_share['Month'])
    # keys = ['State', 'District']
    # market_share_zone = market_share.merge(zone_data, on=keys)

    market_share_state = market_share.groupby(
        ['State', 'Zone', 'Brand', 'Month'], as_index=False)['Sales'].sum()
    market_pot = market_share[[
        'State', 'Zone', 'District', 'Month', 'Market_potential']].drop_duplicates()
    market_pot_state = market_pot.groupby(['State', 'Zone', 'Month'], as_index=False)[
        'Market_potential'].sum()
    market_share_state = market_share_state.merge(
        market_pot_state, on=['State', 'Zone', 'Month'])
    market_share_state = market_share_state.loc[market_share_state.Sales != 0]
    market_share_state['market_share'] = market_share_state['Sales'] / \
        market_share_state['Market_potential']

    curr_market_share = market_share_state.loc[(market_share_state.Month.dt.month == this_month) &
                                               (market_share_state.Month.dt.year == this_year)]

    if this_month != 1:
        prev_month = this_month - 1
    else:
        prev_month = 12

    prev_month_market_share = market_share_state.loc[(market_share_state.Month.dt.month == prev_month) &
                                                     (market_share_state.Month.dt.year == this_year)]
    prev_month_market_share.drop(
        columns=['Sales', 'Month', 'Market_potential'], inplace=True)
    prev_month_market_share.rename(
        columns={'market_share': 'prev_month_market_share'}, inplace=True)

    prev_year_market_share = market_share_state.loc[(market_share_state.Month.dt.month == this_month) &
                                                    (market_share_state.Month.dt.year == this_year-1)]
    prev_year_market_share.drop(
        columns=['Sales', 'Month', 'Market_potential'], inplace=True)
    prev_year_market_share.rename(
        columns={'market_share': 'prev_year_market_share'}, inplace=True)

    keys = ['State', 'Zone', 'Brand']

    fin_mark_share = curr_market_share.merge(prev_month_market_share, on=keys)
    fin_mark_share = fin_mark_share.merge(prev_year_market_share, on=keys)

    # -----------------------------------------------------------------------------
    # find max market share leader
    mark_leader = fin_mark_share.loc[~fin_mark_share.Brand.str.upper().isin(
        ['SHREE', 'ROCKSTRONG', 'SCL', 'BANGUR'])]
    leader_data = mark_leader.groupby(['Zone', 'State', 'Month'], as_index=False)[
        'market_share'].max()
    keys = ['Zone', 'State', 'Month', 'market_share']
    market_leader_brand = leader_data.merge(mark_leader, on=keys)

    req_mark_share = fin_mark_share.loc[fin_mark_share.Brand.str.upper().isin(
        ['SHREE', 'ROCKSTRONG', 'SCL', 'BANGUR'])]

    # req_brand_mark_share = req_mark_share.append(market_leader_brand, ignore_index= True) UNCOMMENT TO GET LEADER BRAND NAME IN DATA< IMPACT: REMOVE THIS BRAND WHEN CALCULATING MARKET SHARE RATING
    leader_data.rename(
        columns={'market_share': 'leader_market_share'}, inplace=True)
    req_brand_mark_share = req_mark_share.merge(
        leader_data, on=['Zone', 'State', 'Month'])
    # ---------------------------
    # Divide market share by market share leader
    req_brand_mark_share['market_share_div_leader'] = req_brand_mark_share['market_share'] / \
        req_brand_mark_share['leader_market_share']

    req_brand_mark_share['delta_share_month'] = req_brand_mark_share['market_share'] - \
        req_brand_mark_share['prev_month_market_share']
    req_brand_mark_share['delta_share_year'] = req_brand_mark_share['market_share'] - \
        req_brand_mark_share['prev_year_market_share']
    thres = 0.5
    req_brand_mark_share['delta'] = thres * (
        req_brand_mark_share['delta_share_month'] + req_brand_mark_share['delta_share_year'])

    # -----------------------------------------------------------------------------------
    # FIND DELTA MARKET SHARE RATING
    market_rating = find_market_share_rating(req_brand_mark_share, delta=False)
    market_rating = find_market_share_rating(market_rating, delta=True)

    # --------------------------------------------------------------------------------
    # Market_potential

    zones = req_brand_mark_share.Zone.unique()
    final_market_potential = pd.DataFrame()

    for zone in zones:
        df = req_brand_mark_share.loc[req_brand_mark_share.Zone == zone]
        potential = df['Market_potential']
        perc_50 = np.percentile(potential, q=50)
        df['market_potential_rating'] = np.where(
            df['Market_potential'] >= perc_50, 'High', 'Low')

        final_market_potential = final_market_potential.append(df)
    # -----------------------------------------------------------------------

    final_df = form_matrix(final_market_potential, market_rating, ncr_joined)

    final_df = get_market_strategy(final_df)

    final_df['plan_month'] = plan_month
    final_df.columns = final_df.columns.str.upper()
    final_df.drop(columns=['SALES_Y', 'LEADER_MARKET_SHARE_Y',
                'MARKET_SHARE_DIV_LEADER_Y'], inplace=True)
    final_df.rename(columns={'SALES_X':  'SALES', 
                            'LEADER_MARKET_SHARE_X': 'LEADER_MARKET_SHARE',
                            'MARKET_SHARE_DIV_LEADER_X': 'MARKET_SHARE_DIV_LEADER'}, 
                   inplace=True)
    final_df.to_csv('state_classification_out2.csv')
    
