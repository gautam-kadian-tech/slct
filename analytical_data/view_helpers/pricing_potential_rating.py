# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:35:35 2022

@author: tanay
"""


# from typing import final
from .pricing_static import *
import dateutil.relativedelta
import pandas as pd
import numpy as np
from datetime import datetime
from .pricing_static import threshold, org_brand_map
import warnings
warnings.filterwarnings("ignore")


# now = datetime.now()
# last_month = now + dateutil.relativedelta.relativedelta(months=-1)
# this_month = last_month.month
# this_year = last_month.year
# plan_month = now.replace(
#     day=1) + dateutil.relativedelta.relativedelta(months=+1)
# plan_month = plan_month.strftime('%Y-%m-%d')


def find_market_share_potential(scl_data, this_month, this_year, delta=None):
    # print(scl_data.Month.unique())
    scl_data['Month'] = pd.to_datetime(
        scl_data['Month'],  format='%Y-%m-%d HH:MM:SS')
    scl_data = scl_data.loc[(scl_data.Month.dt.month == this_month) &
                            (scl_data.Month.dt.year == this_year)]

    states = scl_data.State.unique()
    final_market_share_pot = pd.DataFrame()
    for state in states:
        df = scl_data.loc[scl_data.State == state]
        districts = df.District.unique()

        for district in districts:
            district_lvl_df = df.loc[df.District == district]
            if delta:
                # max_market_share = district_lvl_df.loc[district_lvl_df.Brand.str.upper(
                # ) != 'SCL']
                # if max_market_share.empty:
                #     max_market_share = 0
                # else:
                #     max_market_share.fillna(0, inplace=True)
                #     max_market_share = max_market_share.loc[max_market_share['Market_share'].idxmax(
                #     )]
                # district_lvl_df['delta_market_share_max'] = district_lvl_df['delta']

                # district_lvl_df = district_lvl_df.loc[district_lvl_df.Brand.str.upper().isin(
                #     ['SHREE', 'BANGUR', 'ROCKSTRONG', 'SCL'])]
                district_lvl_df['delta_market_share_max'] = district_lvl_df['Market_share']

            else:
                max_market_share = district_lvl_df.loc[district_lvl_df.Brand.str.upper(
                ) != 'SCL']

                max_market_share.fillna(0, inplace=True)
                max_market_share = max_market_share.loc[max_market_share['Market_share'].idxmax(
                )]
                leader_brand = max_market_share['Brand']
                district_lvl_df['leader_market_share'] = max_market_share['Market_share']

                district_lvl_df['market_share_max'] = district_lvl_df['Market_share'] / \
                    district_lvl_df['leader_market_share']
                district_lvl_df = district_lvl_df.loc[district_lvl_df.Brand.str.upper().isin(
                    ['SHREE', 'BANGUR', 'ROCKSTRONG', 'SCL'])]

                district_lvl_df['market_share_max'] = np.minimum(
                    district_lvl_df['market_share_max'], 1)
                district_lvl_df['Market Leader'] = leader_brand
            district_lvl_df.fillna(0, inplace=True)
            final_market_share_pot = final_market_share_pot.append(
                district_lvl_df)

    return final_market_share_pot


def find_market_share_rating(final_market_share_pot, delta):
    states = final_market_share_pot.State.unique()
    market_rating = pd.DataFrame()
    for state in states:
        df = final_market_share_pot.loc[final_market_share_pot.State == state]
        brands = df.Brand.unique()
        for brand in brands:
            brand_data = df.loc[df.Brand == brand]
            if delta:
                potential = brand_data['delta_market_share_max']
                brand_data['delta_market_share_potential_rating'] = np.where(
                    brand_data['delta_market_share_max'] >= 0, 'High', 'Low')

            else:
                potential = brand_data['market_share_max']
                perc_50 = np.percentile(potential, q=50)
                brand_data['market_share_perc'] = perc_50
                brand_data['market_share_potential_rating'] = np.where(
                    brand_data['market_share_max'] >= perc_50, 'High', 'Low')

            market_rating = market_rating.append(brand_data)
    return market_rating


def find_market_potential(market_df):
    latest_market_df = market_df.copy()
    states = latest_market_df.State.unique()
    final_market_potential = pd.DataFrame()
    latest_market_df.columns = latest_market_df.columns.str.capitalize()

    for state in states:
        df = latest_market_df.loc[latest_market_df.State == state]
        if len(df) > 0:
            brands = df.Brand.unique()
            for brand in brands:

                brand_df = df.loc[df.Brand == brand]
                if len(brand_df) > 0:

                    potential = brand_df['Market_potential']
                    perc_50 = np.percentile(potential, q=50)

                    brand_df['market_potential_rating'] = np.where(
                        brand_df['Market_potential'] >= perc_50, 'High', 'Low')

                final_market_potential = final_market_potential.append(
                    brand_df, ignore_index=True)
    return final_market_potential


def add_scl_data(latest_market_df):
    states = latest_market_df.State.unique()
    final_market_potential = latest_market_df
    for state in states:
        df = latest_market_df.loc[latest_market_df.State == state]
        districts = df.District.unique()
        for district in districts:
            district_lvl_df = df.loc[df.District == district]

            month = district_lvl_df['Month'].iloc[0]
            brand = 'SCL'

            scl_mark_share = district_lvl_df.loc[district_lvl_df.Brand.isin(
                ['Shree', 'Bangur', 'Rockstrong'])]['Market share'].sum()

            final_market_potential.loc[len(final_market_potential)] = [
                district, brand, month, scl_mark_share, state]

    return final_market_potential


def find_market_share(market_share,this_month, this_year, add_scl=False):
    latest_market_df = market_share.loc[(market_share.Month.dt.month == this_month) &
                                        (market_share.Month.dt.year == this_year)]
    if add_scl:
        latest_market_df = add_scl_data(latest_market_df)

    prev_year = this_year - 1
    if this_month == 2:
        prev_month = 12
    elif this_month == 1:
        prev_month = 11
    else:
        prev_month = this_month - 1
    # now = datetime.now()
    # this_month = now + dateutil.relativedelta.relativedelta(months=-1)

    prev_month_scl_data = market_share.loc[(market_share.Month.dt.month == prev_month) &
                                           (market_share.Month.dt.year == this_year)]

    prev_month_scl_data = prev_month_scl_data.reset_index(drop=True)
    if add_scl:
        prev_month_scl_data = add_scl_data(prev_month_scl_data)

    prev_month_scl_data.rename(columns={'Month': 'prev_month_month',  # 'Sale': 'prev_month_sales',
                                        'Market_share': 'prev_month_share'}, inplace=True)

    prev_year_scl_data = market_share.loc[(market_share.Month.dt.month == this_month) &
                                          (market_share.Month.dt.year == prev_year)]
    prev_month_scl_data = prev_month_scl_data.reset_index(drop=True)
    if add_scl:
        prev_year_scl_data = add_scl_data(prev_year_scl_data)

    prev_year_scl_data.rename(columns={'Month': 'prev_year_month',  # 'Sale': 'prev_year_sales',
                                       'Market_share': 'prev_year_share'}, inplace=True)

    joining_keys = ['State', 'District', 'Brand']

    prev_month_scl_data.drop(columns=['Sales',
                                      'Market_potential'], inplace=True)
    prev_year_scl_data.drop(columns=['Sales',
                                     'Market_potential'], inplace=True)

    joined_market_share = latest_market_df.merge(
        prev_month_scl_data, on=joining_keys, how='left')

    joined_market_share = joined_market_share.join(
        prev_year_scl_data.set_index(joining_keys), joining_keys, 'left')
    joined_market_share['prev_month_share_delta'] = joined_market_share['Market_share'] - \
        joined_market_share['prev_month_share']
    joined_market_share['prev_year_share_delta'] = joined_market_share['Market_share'] - \
        joined_market_share['prev_year_share']

    thres = 0.5  # COME BACK TO TAKE IT GENERIC FROM TABLE
    joined_market_share['delta'] = thres * (
        joined_market_share['prev_month_share_delta'] + joined_market_share['prev_year_share_delta'])

    return joined_market_share


def find_ncr_market_potential(ncr_avg, threshold_df):

    ncr_avg.columns = ncr_avg.columns.str.title()
    threshold_df.columns = threshold_df.columns.str.title()
    ncr_avg['weighted_qty'] = ncr_avg['Ncr'] * ncr_avg['Quantity_Invoiced']
    threshold_df['weighted_qty'] = threshold_df['Ncr'] * \
        threshold_df['Quantity_Invoiced']

    # -----------------------------------------------------------------
    # SCL AT  PRODUCT LEVEL for NCR data
    scl = ncr_avg.groupby(['State', 'District', 'Product']
                          ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])
    scl['SCL_Ncr'] = scl['weighted_qty'] / scl['Quantity_Invoiced']
    scl = scl.reset_index()
    scl['Brand'] = 'SCL'
    scl.drop(columns=['Ncr'], inplace=True)
    scl.rename(columns={'SCL_Ncr': 'Ncr'}, inplace=True)

    ncr_avg = ncr_avg.append(scl)
    # print('ABOVE IS PRODUCT')
    # ----------------------------------------------------------------

    # BRAND LEVEL ALL for NCR data
    brand_all = ncr_avg.groupby(['State', 'District', 'Brand']
                                ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])
    brand_all['all_Ncr'] = brand_all['weighted_qty'] / \
        brand_all['Quantity_Invoiced']
    brand_all.drop(columns=['Ncr'], inplace=True)
    brand_all.reset_index(inplace=True)
    brand_all['Product'] = 'All'
    brand_all.rename(columns={'all_Ncr': 'Ncr'}, inplace=True)

    ncr_avg = ncr_avg.append(brand_all)
    # -------------------------------------------------------------------------------------
    # SCL AT  PRODUCT LEVEL for NCR threshold

    scl = threshold_df.groupby(['State', 'District', 'Product']
                               ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])
    scl['SCL_Ncr'] = scl['weighted_qty'] / scl['Quantity_Invoiced']
    scl = scl.reset_index()
    scl['Brand'] = 'SCL'
    scl.drop(columns=['Ncr'], inplace=True)
    scl.rename(columns={'SCL_Ncr': 'Ncr'}, inplace=True)

    threshold_df = threshold_df.append(scl)
    # ----------------------------------------------------------------

    # BRAND LEVEL ALL for NCR threshold
    brand_all = threshold_df.groupby(['State', 'Brand']  # District
                                     ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])

    brand_all['all_Ncr'] = brand_all['weighted_qty'] / \
        brand_all['Quantity_Invoiced']
    brand_all.drop(columns=['Ncr'], inplace=True)
    brand_all.reset_index(inplace=True)
    brand_all['Product'] = 'All'
    brand_all.rename(columns={'all_Ncr': 'Ncr'}, inplace=True)
    threshold_df = threshold_df.append(brand_all)

    threshold_df.rename(columns={'Ncr': 'Ncr_threshold'}, inplace=True)
    threshold_df.drop(columns=['Quantity_Invoiced',
                      'weighted_qty'], inplace=True)
    # -----------------------------------------------------------------------------------
    # JOINING NCR AND THRESHOLD TO GET EVERYTHING IN 1 LINE AND USE THRESHOLDS
    key = ['State', 'Brand', 'Product']
    joined_ncr = ncr_avg.set_index(key).join(
        threshold_df.set_index(key), how='left', lsuffix='_x', rsuffix='_y')

    joined_ncr['ncr_market_potential_rating'] = np.where(
        joined_ncr['Ncr'] >= joined_ncr['Ncr_threshold'], 'High', 'Low')
    ncr_final_potential = joined_ncr.reset_index()

    ncr_final_potential.drop(columns='District_y', inplace=True)
    ncr_final_potential.rename(
        columns={'District_x': 'District'}, inplace=True)
    ncr_final_potential = ncr_final_potential.loc[ncr_final_potential.Product == 'All']

    return ncr_final_potential


def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df


def insert_to_db(df):
    df.columns = df.columns.str.upper()
    df.to_csv('Market_rating_oct_out.csv', index=False)


def district_matrix(market_share,ncr_data, threshold_df, plan_month):
    # now = datetime.now()
    plan_month = plan_month
    last_month = plan_month + dateutil.relativedelta.relativedelta(months=-2) #CHANGE THIS TO -2
    this_month = last_month.month
    this_year = last_month.year
    # plan_month = now.replace(
    #     day=1) + dateutil.relativedelta.relativedelta(months=+1)
    # plan_month = plan_month.strftime('%Y-%m-%d')

    # market_share = pd.read_csv('market_potential.csv')
    market_share.columns = market_share.columns.str.capitalize()
    market_share = convert_data_to_upper(market_share)
    market_share['Month'] = pd.to_datetime(market_share['Month'])

    # market_df = market_share.copy()

    fix_del = True
    if fix_del:
        market_share['District'] = market_share['District'].str.split('/')
        market_share = market_share.explode('District', ignore_index=True)
        market_share['District'] = market_share['District'].str.strip()
        market_share.drop_duplicates(keep='first', inplace=True, subset=[
                                     'State', 'District', 'Brand', 'Month'])

    # ----------------------------------------------------------------
    # FIND NCR POTENTIAL

    # ncr_data = pd.read_csv('ncr_3_year.csv')
    # print(this_month, this_year)
    ncr_data['MONTH'] = pd.to_datetime(ncr_data['MONTH'])
    ncr_avg = ncr_data.loc[(ncr_data.MONTH.dt.month == this_month) &
                           (ncr_data.MONTH.dt.year == this_year)]
    ncr_avg.columns = ncr_avg.columns.str.title()
    ncr_avg.drop(columns=['Sales'], inplace=True, errors='ignore')
    ncr_avg = convert_data_to_upper(ncr_avg)

    # threshold_df = pd.read_csv('ncr_threshold.csv')
    threshold_df = convert_data_to_upper(threshold_df)

    ncr_final_potential = find_ncr_market_potential(ncr_avg, threshold_df)
    ncr_final_potential.replace({'Brand': org_brand_map}, inplace=True)
    # ncr_final_potential.to_csv('ncr_out.csv')
    # -----------------------------------------
    ncr_avg = ncr_data.loc[(ncr_data.MONTH.dt.month == this_month) &
                           (ncr_data.MONTH.dt.year == this_year)]

    ncr_avg.columns = ncr_avg.columns.str.capitalize()
    ncr_avg.replace({'Brand': org_brand_map}, inplace=True)
    # print(ncr_avg)
    ncr_avg['District'] = ncr_avg['District'].str.capitalize()
    ncr_avg['State'] = ncr_avg['State'].str.capitalize()

    ncr_avg['weighted_qty'] = ncr_avg['Ncr'] * ncr_avg['Quantity_invoiced']
    scl = ncr_avg.groupby(['State', 'District', 'Product']
                          ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])
    scl['SCL_Ncr'] = scl['weighted_qty'] / scl['Quantity_invoiced']
    scl = scl.reset_index()
    scl['Brand'] = 'SCL'
    scl.drop(columns=['Ncr'], inplace=True)
    scl.rename(columns={'SCL_Ncr': 'Ncr'}, inplace=True)

    ncr_avg = ncr_avg.append(scl)

    market_share_data = find_market_share(
        market_share, this_month, this_year,  add_scl=False)

    keys = ['State', 'District', 'Brand']
    final_df = market_share_data.merge(ncr_final_potential, on=keys,
                                       how='inner')

    final_market_potential = find_market_potential(final_df)
    market_share_rate = find_market_share_potential(market_share,  this_month, this_year)
    
    print(this_month, this_year)
    delta_market_share_rate = find_market_share_potential(
        market_share_data, this_month, this_year, delta=True)
    print(market_share_rate.columns)
    delta_market_share_rate = delta_market_share_rate[[
        'State', 'District', 'Brand', 'delta', 'delta_market_share_max']]

    keys = ['State', 'District', 'Brand']
    final_market = market_share_rate.merge(delta_market_share_rate, on=keys)
    final_market_potential_req = final_market_potential[['State', 'District', 'Brand', 'Sales',
                                                         'Product', 'Ncr', 'Ncr_market_potential_rating',
                                                         'Prev_month_share_delta', 'Prev_year_share_delta',
                                                         'market_potential_rating']]

    final_market_pot_join = final_market_potential_req.merge(
        final_market, on=keys)

    market_share_rate = find_market_share_rating(
        final_market_pot_join, delta=False)

    delta_market_share_rate = find_market_share_rating(
        market_share_rate, delta=True)

    delta_market_share_rate.drop(
        columns=['Sales_y', 'market_share_perc'], inplace=True)
    delta_market_share_rate['plan_month'] = plan_month
    delta_market_share_rate.rename(columns={'Sales_x': 'Sales'}, inplace=True)
    # delta_market_share_rate.columns = delta_market_share_rate.columns.str.capitalize()
    # market_strategy = get_market_strategy(delta_market_share_rate)
    # market_strategy.to_csv('market_strategy.csv', index=False)
    # insert_to_db(delta_market_share_rate)
    return delta_market_share_rate


if __name__ == '__main__':
    # pass
    plan_month = ''

    market_share = pd.read_csv('market_potential.csv')
    market_share.columns = market_share.columns.str.capitalize()
    market_share = convert_data_to_upper(market_share)
    market_share['Month'] = pd.to_datetime(market_share['Month'])
    ncr_data = pd.read_csv()
    threshold_df = pd.read_csv()
    df = district_matrix(market_share,ncr_data, threshold_df, plan_month)