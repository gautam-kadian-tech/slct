# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:40:35 2022

@author: tanay
"""
import dateutil
import pandas as pd
from static import pricing_strategy_map
from datetime import datetime



def get_pricing_strategy(market_strategy):
    market_strategy['pricing_strategy_driver'] = market_strategy['MARKET_POSITION'] + \
        '|' + market_strategy['MARKET_LUCRATIVENESS']

    market_strategy['pricing_strategy'] = market_strategy['pricing_strategy_driver'].map(
        pricing_strategy_map)

    market_strategy = market_strategy.loc[market_strategy.PRODUCT == 'All']
    market_strategy = market_strategy[[
        'STATE', 'DISTRICT', 'BRAND', 'pricing_strategy']]
    return market_strategy


def read_pricing_data(filename, sheetname=None):
    return pd.read_excel(filename, sheetname, header=None)


def form_pricing_data(pricing_data):
    pricing_data_final = pd.DataFrame()

    for state in pricing_data.keys():
        pricing_state_data = pricing_data.get(state)
        pricing_state_data = pricing_state_data.iloc[4:].reset_index(drop=True)
        pricing_state_data.iloc[0, :] = pricing_state_data.iloc[0, :].fillna(
            method='ffill')
        pricing_state_data.iloc[1,
                                :] = pricing_state_data.iloc[1, :].fillna('')
        pricing_state_data.iloc[1, :] = pricing_state_data.iloc[1, :].astype(
            str).str.split('.').str[0]
        cols = pricing_state_data.iloc[1, :] + '-' + \
            pricing_state_data.iloc[0, :].str.replace("'", "-")
        pricing_state_data.columns = cols
        pricing_state_data = pricing_state_data.iloc[2:].reset_index(drop=True)
        pricing_state_data.drop(columns=['-NO.'], inplace=True)
        pricing_state_data.rename(columns={
                                  '-BRAND': 'Brand', '-DISTRICT': 'District', '-PRICE': 'Price'}, inplace=True)
        pricing_state_data.fillna(method='ffill', axis=0, inplace=True)
        pricing_state_data = pricing_state_data.melt(
            id_vars=["District", "Brand", "Price"], var_name="Month", value_name="MARKET SHARE")
        pricing_state_data["Month"] = pricing_state_data["Month"].str.replace(
            'JUNE', 'JUN', case=False)
        pricing_state_data["Month"] = pricing_state_data["Month"].str.replace(
            'JULY', 'JUL', case=False)
        pricing_state_data["Month"] = pricing_state_data["Month"].str.replace(
            'APRIL', 'APR', case=False)
        pricing_state_data['Date'] = pd.to_datetime(
            pricing_state_data['Month'], format='%d-%b-%Y')
        pricing_state_data['Month'] = pd.DatetimeIndex(
            pricing_state_data['Date']).month
        pricing_state_data['rank'] = pricing_state_data.groupby(
            ['District', 'Month'])['Date'].rank('dense', ascending=False)

        pricing_state_data = pricing_state_data.loc[pricing_state_data['rank'] <= 6]
        pricing_state_data['Date'] = pricing_state_data['Date'].apply(
            lambda x: x.replace(day=1))
        pricing_state_data['State'] = state.title()
        pricing_state_data.drop(columns=['Month', 'rank'], inplace=True)
        cols = ['District', 'Brand']
        for col in cols:
            pricing_state_data[col] = pricing_state_data[col].str.capitalize()
        pricing_data_final = pricing_data_final.append(pricing_state_data)
    # print(pricing_data_final.dtypes)
    pricing_data_final['MARKET SHARE'] = pricing_data_final['MARKET SHARE'].astype(
        float)
    pricing_data_avg = pricing_data_final.groupby(
        ['State', 'District', 'Brand', 'Price', 'Date'], as_index=False)['MARKET SHARE'].mean()
    # pricing_data_avg.to_csv('pricing_data.csv', index=False)
    return pricing_data_avg


def find_wsp_maket_share_diff(pricing_data_final, wsp_rsp):
    pricing_data_wsp = pricing_data_final.loc[pricing_data_final.PRICE.str.upper(
    ) == wsp_rsp]
    max_market_share = pricing_data_wsp.groupby(['STATE', 'DISTRICT', 'DATE'], as_index=False)[
        'MARKET SHARE'].max()

    keys = ['STATE', 'DISTRICT', 'DATE']
    max_market_share_name = max_market_share.rename(
        columns={'MARKET SHARE': 'leader'})
    leader_name = pricing_data_wsp.set_index(keys).join(
        max_market_share_name.set_index(keys))
    leader_name = leader_name.loc[leader_name['MARKET SHARE']
                                  == leader_name['leader']]
    leader_name.drop(columns=['PRICE', 'MARKET SHARE', 'leader'], inplace=True)
    leader_name.rename(columns={'BRAND': 'LEADER_BRAND'}, inplace=True)
    leader_name = leader_name.groupby(['STATE', 'DISTRICT', 'DATE'])[
        'LEADER_BRAND'].last()

    max_market_share.rename(
        columns={'MARKET SHARE': 'max_market_share'}, inplace=True)

    keys = ['STATE', 'DISTRICT', 'DATE']
    wsp_max_joined = pricing_data_wsp.set_index(keys).join(
        max_market_share.set_index(keys), how='inner')
    # print(wsp_max_joined.BRAND.unique()
    req_brand_wsp = wsp_max_joined.loc[wsp_max_joined.BRAND.isin(
        ['SHREE', 'BANGUR', 'ROCKSTRONG'])]
    req_brand_wsp['market_share_diff'] = req_brand_wsp['max_market_share'] - \
        req_brand_wsp['MARKET SHARE']
    req_brand_wsp.reset_index(inplace=True)

    keys = ['STATE', 'DISTRICT', 'DATE']
    req_brand_wsp = req_brand_wsp.set_index(keys).join(leader_name)
    req_brand_wsp.reset_index(inplace=True)

    return req_brand_wsp


def find_min_increase(df):
    max_inc_inr = 10
    if (df.pricing_strategy == 'Accommodative'):
        return 0
    if (df.pricing_strategy == 'Assertive'):
        return min(df.market_share_diff * 0.1, max_inc_inr)
    elif df.pricing_strategy == 'Aggressive':
        return min(df.market_share_diff * 0.2, max_inc_inr)
    else:
        return 0


def find_max_increase(df):
    max_inc_inr = 10
    if df.pricing_strategy == 'Accommodative':
        return min(df.market_share_diff * 0.1, max_inc_inr)
    elif df.pricing_strategy == 'Assertive':
        return min(df.market_share_diff * 0.2, max_inc_inr)
    elif df.pricing_strategy == 'Aggressive':
        return min(df.market_share_diff * 0.3, max_inc_inr)
    else:
        return 0


def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df


def find_pricing_strategy(market_strategy, pricing_data_final, plan_month):
    # market_strategy = pd.read_csv('market_strategy.csv')
    pricing_strategy = get_pricing_strategy(market_strategy)

    # filename = 'pricing_strategy.xlsx'

    # pricing_data = read_pricing_data(filename)
    # pricing_data_final = form_pricing_data(pricing_data)
    pricing_data_final.dropna(inplace=True)
    pricing_data_final.columns = pricing_data_final.columns.str.upper()
    pricing_data_final = convert_data_to_upper(pricing_data_final)
    pricing_data_final['DATE'] = pd.to_datetime(
        pricing_data_final['DATE'], format='%d-%m-%Y')
    pricing_data_final['DATE'] = pricing_data_final['DATE'].apply(
        lambda x: x.replace(day=1))
    # print(pricing_data_final.columns)
    pricing_data_final = pricing_data_final.groupby(
        ['STATE', 'DISTRICT', 'BRAND', 'PRICE', 'DATE'], as_index=False)['MARKET SHARE'].mean()

    # pricing_data_final.to_csv('converted_pricing_data.csv', index= False)
    
    this_month= plan_month + dateutil.relativedelta.relativedelta(months=-1) #CHANGE THIS TO PM -1
    this_year  = this_month.year
    this_month = this_month.month
    
    # if datetime.today().month <3:
    #     this_year = datetime.today().year - 1
    # else:
    #     this_year = datetime.today().year
    # print(this_month, this_year)

    pricing_data_final = pricing_data_final.loc[(pricing_data_final.DATE.dt.month == this_month) &
                                                (pricing_data_final.DATE.dt.year == this_year)]
    # pricing_data_final.to_csv('a.csv')
    req_brand_wsp = find_wsp_maket_share_diff(pricing_data_final, 'WSP')

    keys = ['STATE', 'DISTRICT', 'BRAND']
    # print(req_brand_wsp.columns)
    # print(pricing_strategy.columns)
    # req_brand_wsp.to_csv('a.csv')
    wsp_strat = req_brand_wsp.set_index(keys).join(
        pricing_strategy.set_index(keys), how='inner')
    wsp_strat.reset_index(inplace=True)

    # print(wsp_strat.shape)
    if not wsp_strat.empty:

        wsp_strat['wsp_min_margin'] = wsp_strat.apply(find_min_increase, axis=1)
        wsp_strat['wsp_max_margin'] = wsp_strat.apply(find_max_increase, axis=1)

        wsp_strat.to_csv('pricing_strategy_test.csv', index=False)

    wsp_strat.rename(columns={'MARKET SHARE': 'WSP_PRICE',
                              'max_market_share': 'WSP_LEADER_PRICE',
                              'market_share_diff': 'WSP_LEADER_GAP',
                              'LEADER_BRAND': 'WSP Price Leader'}, inplace=True)
    req_brand_rsp = find_wsp_maket_share_diff(pricing_data_final, 'RSP')
    keys = ['STATE', 'DISTRICT', 'BRAND']

    rsp_strat = req_brand_rsp.set_index(keys).join(
        pricing_strategy.set_index(keys), how='inner')
    rsp_strat.reset_index(inplace=True)

    if not rsp_strat.empty:

        rsp_strat['rsp_min_margin'] = rsp_strat.apply(find_min_increase, axis=1)
        rsp_strat['rsp_max_margin'] = rsp_strat.apply(find_max_increase, axis=1)

        # rsp_strat.to_csv('pricing_strategy_test_rsp.csv', index=False)

    rsp_strat.rename(columns={'MARKET SHARE': 'RSP_PRICE',
                              'max_market_share': 'RSP_LEADER_PRICE',
                              'market_share_diff': 'RSP_LEADER_GAP',
                              'LEADER_BRAND': 'RSP Price Leader'}, inplace=True)
    rsp_strat.drop(columns=['pricing_strategy',
                   'min_margin', 'max_margin', 'PRICE'], inplace=True, errors='ignore')

    keys = ['STATE', 'DISTRICT', 'BRAND', 'DATE']

    joined_data = wsp_strat.set_index(keys).join(rsp_strat.set_index(keys))
    joined_data.drop(columns=['PRICE'], inplace=True)

    # joined_data.to_csv('pricing_output_oct.csv')
    return joined_data


if __name__ == '__main__':
    market_strategy = pd.read_csv('market_strategy.csv')
    pricing_strategy = get_pricing_strategy(market_strategy)

    filename = 'pricing_strategy.xlsx'

    pricing_data = read_pricing_data(filename)
    pricing_data_final = form_pricing_data(pricing_data)
    pricing_data_final.dropna(inplace=True)
    # pricing_data_final.to_csv('converted_pricing_data.csv', index= False)

    # this_month= datetime.today().month -1
    this_month = 2
    this_year = datetime.today().year

    pricing_data_final = pricing_data_final.loc[(pricing_data_final.Date.dt.month == this_month) &
                                                (pricing_data_final.Date.dt.year == this_year)]

    req_brand_wsp = find_wsp_maket_share_diff(pricing_data_final, 'WSP')

    keys = ['State', 'District', 'Brand']

    wsp_strat = req_brand_wsp.set_index(keys).join(
        pricing_strategy.set_index(keys), how='inner')
    wsp_strat.reset_index(inplace=True)

    if not wsp_strat.empty:

        wsp_strat['min_margin'] = wsp_strat.apply(find_min_increase, axis=1)
        wsp_strat['max_margin'] = wsp_strat.apply(find_max_increase, axis=1)

        wsp_strat.to_csv('pricing_strategy_test.csv', index=False)

    wsp_strat.rename(columns={'MARKET SHARE': 'WSP_PRICE',
                              'max_market_share': 'WSP_LEADER_PRICE',
                              'market_share_diff': 'WSP_LEADER_GAP',
                              'Leader_Brand': 'WSP Price Leader'}, inplace=True)
    req_brand_rsp = find_wsp_maket_share_diff(pricing_data_final, 'RSP')
    keys = ['State', 'District', 'Brand']

    rsp_strat = req_brand_rsp.set_index(keys).join(
        pricing_strategy.set_index(keys), how='inner')
    rsp_strat.reset_index(inplace=True)

    if not rsp_strat.empty:

        rsp_strat['min_margin'] = rsp_strat.apply(find_min_increase, axis=1)
        rsp_strat['max_margin'] = rsp_strat.apply(find_max_increase, axis=1)

        rsp_strat.to_csv('pricing_strategy_test_rsp.csv', index=False)

    rsp_strat.rename(columns={'MARKET SHARE': 'RSP_PRICE',
                              'max_market_share': 'RSP_LEADER_PRICE',
                              'market_share_diff': 'RSP_LEADER_GAP',
                              'Leader_Brand': 'RSP Price Leader'}, inplace=True)
    rsp_strat.drop(columns=['pricing_strategy',
                   'min_margin', 'max_margin', 'Price'], inplace=True, errors='ignore')

    keys = ['State', 'District', 'Brand', 'Date']

    joined_data = wsp_strat.set_index(keys).join(rsp_strat.set_index(keys))
    joined_data.drop(columns=['Price'], inplace=True)

    joined_data.to_csv('pricing_output_oct.csv')
