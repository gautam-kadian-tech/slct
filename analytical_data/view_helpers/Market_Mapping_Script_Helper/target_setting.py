import dateutil.relativedelta
import numpy as np
from .static import market_pos, market_luc, market_growth, org_brand_map
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


def get_market_strategy(df, market_share, this_month, this_year):
    df['market_position'] = df['Delta_market_share_potential_rating'] + \
        '|' + df['Market_share_potential_rating']
    df['market_position'] = df['market_position'].map(market_pos)

    df['market_lucrativeness'] = df['Ncr_market_potential_rating'] + \
        '|' + df['Market_potential_rating']
    df['market_lucrativeness'] = df['market_lucrativeness'].map(market_luc)

    df['market_growth_strategy'] = df['market_position'] + \
        '|' + df['market_lucrativeness']
    df['market_growth_strategy'] = df['market_growth_strategy'].map(
        market_growth)
    
    if this_month == 1:
        this_month_m = 13
        this_year_m = this_year-1
    else:
        this_month_m = this_month
        this_year_m = this_year

    prev_market_share = market_share.loc[(market_share.Month.dt.month < this_month_m) &
                                         (market_share.Month.dt.year == this_year_m)]
    cols = df.columns
    ms = prev_market_share[['Zone', 'Region', 'State',
                            'District', 'Brand']].drop_duplicates()
    ms['prev_ms'] = 1

    # ms.rename(columns={'Market_share': 'prev_ms'}, inplace=True)
    joined_df = df.merge(ms, on=[
                         'Zone', 'Region', 'State', 'District', 'Brand'], how='left')
    print(ms.columns)
    joined_df['market_growth_strategy'] = np.where(joined_df['prev_ms'].isna(
    ), 'Maintain MS', joined_df['market_growth_strategy'])
    
    joined_df = joined_df[cols]
    # print(joined_df.columns)
    # print('---==================-------------')
    return joined_df


def form_market_potential_data(latest_market_df, ncr_avg):

    qty_ncr = ncr_avg.groupby(
        ['District', 'State', 'Brand', 'Month'], as_index=False).sum('Dispatch_Qty')
    # print(latest_market_df)
    key = ['District', 'State', 'Brand', 'Month']

    for k in key:
        if k == 'Month':
            continue

        latest_market_df[k] = latest_market_df[k].str.capitalize()
        latest_market_df[k] = latest_market_df[k].str.strip()
        qty_ncr[k] = qty_ncr[k].str.capitalize()
        qty_ncr[k] = qty_ncr[k].str.strip()

    market_share_ncr = latest_market_df.set_index(
        key).join(qty_ncr.set_index(key), how='inner')

    market_share_ncr.reset_index(inplace=True)

    # print(market_share_ncr.Brand.unique())
    market_share_ncr = market_share_ncr.loc[market_share_ncr.Brand.isin(
        ['Shree', 'Bangur', 'Rockstrong', 'Scl'])]

    market_share_ncr['mark_pot'] = market_share_ncr['Dispatch_Qty'] / \
        market_share_ncr['Market_share']

    # return market_share_ncr
    market_pot = pd.DataFrame()
    states = market_share_ncr.State.unique()
    for state in states:
        state_df = market_share_ncr.loc[market_share_ncr.State == state]
        districts = state_df.District.unique()
        for district in districts:
            df = state_df.loc[state_df.District == district]
            dates = df.Month.unique()
            for date in dates:
                dt_df = df.loc[df.Month == date]
                dt_df['Market_potential'] = dt_df['mark_pot'].max()

                market_pot = market_pot.append(dt_df, ignore_index=False)

    return market_pot


def get_priority_brand(market_potential):
    # take only max one
    market_share_ncr = market_potential.loc[market_potential['Market_share'] != 0]

    market_share_ncr.drop_duplicates(inplace=True)
    market_share_ncr['rank'] = market_share_ncr.sort_values(['Brand'], ascending=False) \
        .groupby(['District', 'State']) \
        .cumcount() + 1
    # print(market_share_ncr)
    market_share_ncr = market_share_ncr.loc[market_share_ncr['rank'] == 1]

    return market_share_ncr


def form_potential_data(market_share, dispatch_df):

    latest_market_df = market_share.loc[(market_share.Month.dt.month == this_month) &
                                        (market_share.Month.dt.year == this_year)]

    ncr_avg = dispatch_df.loc[(dispatch_df.Month.dt.month == this_month) &
                              (dispatch_df.Month.dt.year == this_year)]
    qty_ncr = ncr_avg.groupby(
        ['District', 'State', 'Brand'], as_index=False).sum('Dispatch_Qty')

    key = ['District', 'State', 'Brand']

    for k in key:
        latest_market_df[k] = latest_market_df[k].str.capitalize()
        qty_ncr[k] = qty_ncr[k].str.capitalize()

    market_share_ncr = latest_market_df.set_index(
        key).join(qty_ncr.set_index(key), how='inner')

    # print(market_share_ncr.shape)
    market_share_ncr.reset_index(inplace=True)

    market_share_ncr = market_share_ncr.loc[market_share_ncr.Brand.isin(
        ['Shree', 'Bangur', 'Rockstrong', 'Scl'])]

    market_share_ncr['mark_pot'] = market_share_ncr['Dispatch_Qty'] / \
        market_share_ncr['Market_share']

    market_pot = pd.DataFrame()
    states = market_share_ncr.State.unique()
    for state in states:
        state_df = market_share_ncr.loc[market_share_ncr.State == state]
        districts = state_df.District.unique()
        for district in districts:
            df = state_df.loc[state_df.District == district]
            df['Market_potential'] = df['mark_pot'].max()

            market_pot = market_pot.append(df, ignore_index=False)

    return market_pot


def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df


def target_setting(district_classifier, market_share, ncr_avg, target_setting_change, plan_month):
    # now = datetime.now()
    last_month = plan_month + dateutil.relativedelta.relativedelta(months=-2) #CHANGE THIS TO -2
    this_month = last_month.month
    this_year = last_month.year
    prev_year = this_year - 1
    # plan_month = 

    # ---------------------------------------------------------
    # df = pd.read_csv('Market_rating_oct_out.csv')

    district_classifier.columns = district_classifier.columns.str.capitalize()
    district_classifier['Month'] = pd.to_datetime(district_classifier['Month'])
    df = district_classifier.copy()

    market_share.columns = market_share.columns.str.capitalize()
    market_share['Month'] = pd.to_datetime(
        market_share['Month'])
    market_share = convert_data_to_upper(market_share)
    market_df = market_share.copy()

    market_strategy = get_market_strategy(
        district_classifier, market_share, this_month, this_year)
    market_strategy_val = market_strategy.copy()
    df = df.drop(columns=['Market_share'])
    # ---------------------------------------------------------
    # READ NCR DATA AND Market_share DATA TO FORM Market_potential DATA
    # market_share = pd.read_csv('market_potential.csv')

    # market_share.drop(columns=['Zone'], inplace=True, errors='ignore')

    market_share_tmp = market_share[market_share['Brand'].isin(
        ['Shree', 'Rockstrong', 'Bangur'])]
    # market_share_tmp = market_share_tmp.groupby(['State', 'District', 'Month'], as_index=False).agg({
    #     'Sales': np.sum, 'Market_potential': np.mean})
    # market_share_tmp['Brand'] = 'SCL'
    # market_share = market_share.append(market_share_tmp, ignore_index=True)
    # market_share.loc[market_share['Brand'] == 'SCL', 'Market_share'] = round(
    #     market_share[market_share['Brand'] == 'SCL']['Sales']/market_share[market_share['Brand'] == 'SCL']['Market_potential'], 3)
    # market_share.fillna(0, inplace=True)

    # ncr_avg = pd.read_excel('NCR_3_Year_Data_Sep.xlsx')
    # ncr_avg = pd.read_csv('ncr_3_year.csv')

    ncr_avg.columns = ncr_avg.columns.str.capitalize()

    # ----------------------------------------------------------------------
    # ADDING SCL DATA TO NCR
    # ncr_avg['weighted_qty'] = ncr_avg['Ncr'] * ncr_avg['Quantity_invoiced']
    # scl = ncr_avg.groupby(['State', 'District', 'Month', 'Product']
    #                       ).sum(['Ncr', 'Quantity_Invoiced', 'weighted_qty'])
    # scl['SCL_Ncr'] = scl['weighted_qty'] / scl['Quantity_invoiced']
    # scl = scl.reset_index()
    # scl['Brand'] = 'Scl'
    # scl.drop(columns=['Ncr'], inplace=True)
    # scl.rename(columns={'SCL_Ncr': 'Ncr'}, inplace=True)

    # ncr_avg = ncr_avg.append(scl)

    # market_share.columns = market_share.columns.str.capitalize()

    ncr_avg.replace({'Brand': org_brand_map}, inplace=True)

    market_share['Month'] = pd.to_datetime(
        market_share['Month'], errors='coerce')  # , format='%Y-%m-%d')
    ncr_avg['Month'] = pd.to_datetime(
        ncr_avg['Month'], format='%Y-%m-%d')

    fix_del = False
    if fix_del:
        market_share['District'] = market_share['District'].str.split('/')
        market_share = market_share.explode('District', ignore_index=True)
        market_share['District'] = market_share['District'].str.strip()
        market_share.drop_duplicates(keep='first', inplace=True, subset=[
                                     'State', 'District', 'Brand', 'Month'])

    latest_market_df = market_share.loc[(market_share.Month.dt.month == this_month) &
                                        (market_share.Month.dt.year.isin([this_year, prev_year]))]

    market_potential = market_df.copy()

    end_year = this_year - 3
    market_potential = market_potential.loc[(market_potential.Month.dt.month == this_month) &
                                            ((market_potential.Month.dt.year >= end_year) & (market_potential.Month.dt.year <= this_year))]

    market_potential['prev_market_potential'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                                 .groupby(['State', 'District', 'Brand'])['Market_potential'].shift(-1))

    market_potential['prev_market_share'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                             .groupby(['State', 'District', 'Brand'])['Market_share'].shift(-1))

    market_potential.dropna(inplace=True)
    market_potential['market_potential_diff'] = (1 + ((market_potential['Market_potential'] -
                                                       market_potential['prev_market_potential']) / market_potential['prev_market_potential']))
    market_potential['market_potential_diff'] = np.where(
        market_potential['market_potential_diff'] < 1, 1, market_potential['market_potential_diff'])

    # --------------------------------NEW CODE TO FETCH FUTURE Market_potential
    # target_setting_change = pd.read_csv('growth_potential.csv')
    target_setting_change.drop(columns=[np.nan], inplace=True, errors='ignore')
    target_setting_change.columns = target_setting_change.columns.str.capitalize()
    target_setting_change = convert_data_to_upper(target_setting_change)
    # target_setting_change['State'] = target_setting_change['State'].str.upper()

    curr_market_share = market_share.loc[(market_share.Month.dt.month == this_month) &
                                         (market_share.Month.dt.year == this_year)]
    curr_market_share = curr_market_share[[
        'State', 'District', 'Market_potential']].drop_duplicates()
    future_mp = target_setting_change.merge(curr_market_share, on='State')
    future_mp.columns = future_mp.columns.str.strip()
    future_mp['curr_market_potential'] = future_mp['Market_potential'] * \
        (1 + future_mp['Current']/100)
    future_mp['future_market_potential'] = future_mp['curr_market_potential'] * \
        (1 + future_mp['Next']/100)

    future_mp = future_mp[['State', 'District',
                           'future_market_potential', 'Next']]
    market_potential = market_potential.merge(
        future_mp, on=['State', 'District'])

    market_strategy_all = market_strategy.loc[market_strategy.Product == 'All']
    market_strategy_all.drop(
        columns=['Market_potential', 'Market_share'], inplace=True)

    keys = ['Zone', 'Region', 'State', 'District', 'Brand', 'Month']
    market_strategy_all.drop_duplicates(inplace=True)
    market_potential_strategy = market_strategy_all.merge(
        market_potential, on=keys, how='inner')
    market_potential_strategy = market_potential_strategy.loc[market_potential_strategy.Brand != 'SCL']
    # ---------------------------------------------------------------
    # FIND TARGET WHERE STRATEGY IS TO MAINTAIN MS
    maintain_target = market_potential_strategy.loc[
        market_potential_strategy.market_growth_strategy == 'Maintain MS']
    # maintain_target = maintain_target.loc[maintain_target.Month]
    maintain_target['future_market_share'] = maintain_target['Market_share']
    maintain_target['target_sales'] = maintain_target['Market_share'] * \
        maintain_target['future_market_potential']

    # ---------------------------------------------------------------
    # FIND TARGET WHERE MARKET STRATEGY IS TO GROW INCREMENTALLY

    grow_inc_target = market_potential_strategy.loc[
        market_potential_strategy.market_growth_strategy == 'Grow Incrementally']
    thres = 0.5
    grow_inc_target['future_market_share_thres'] = abs(
        grow_inc_target['Market_share'] - grow_inc_target['prev_market_share'])

    grow_inc_target['future_market_share_thres'] = (thres *
                                                    grow_inc_target['future_market_share_thres']) / 6

    grow_inc_target['future_market_share'] = grow_inc_target['future_market_share_thres'] + \
        grow_inc_target['Market_share']

    grow_inc_target['target_sales'] = grow_inc_target['future_market_potential'] * \
        grow_inc_target['future_market_share']

    # ----------------------------------------------------------------------
    # FIND GROW AGRESSIVELY
    end_year = this_year - 3
    latest_market_df = market_share.loc[(market_share.Month.dt.month == this_month) &
                                        ((market_share.Month.dt.year >= end_year) & (market_share.Month.dt.year <= this_year))]
    market_potential = market_df.copy()

    market_potential['prev_market_potential'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                                 .groupby(['State', 'District', 'Brand'])['Market_potential'].shift(-1))

    market_potential['prev_market_share'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                             .groupby(['State', 'District', 'Brand'])['Market_share'].shift(-1))
    market_potential['prev_market_share2'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                              .groupby(['State', 'District', 'Brand'])['Market_share'].shift(-2))

    market_potential['prev_market_share3'] = (market_potential.sort_values(by=['Month'], ascending=False)
                                              .groupby(['State', 'District', 'Brand'])['Market_share'].shift(-3))
    market_potential.fillna(0, inplace=True)
    market_potential['Month'] = pd.to_datetime(
        market_potential['Month'], errors='coerce')
    market_potential_priority = market_potential.loc[(
        market_potential.Month.dt.year == this_year) & (market_potential.Month.dt.month == this_month)]

    market_potential_priority['curr_prev'] = market_potential_priority['Market_share'] - \
        market_potential_priority['prev_market_share']
    market_potential_priority['curr_prev'] = np.maximum(
        market_potential_priority['curr_prev'], 0)
    # print(market_potential_priority['curr_prev'])
    market_potential_priority['prev_prev2'] = market_potential_priority['prev_market_share'] - \
        market_potential_priority['prev_market_share2']

    market_potential_priority['prev_prev2'] = np.maximum(
        market_potential_priority['prev_prev2'], 0)

    market_potential_priority['prev2_prev3'] = market_potential_priority['prev_market_share2'] - \
        market_potential_priority['prev_market_share3']
    market_potential_priority['prev2_prev3'] = np.maximum(
        market_potential_priority['prev2_prev3'], 0)

    cols = ['curr_prev', 'prev_prev2', 'prev2_prev3']
    market_potential_priority['max_market_share'] = market_potential_priority[cols].max(
        axis=1)
    market_strategy_all_agr = market_strategy_all.loc[
        market_strategy_all.market_growth_strategy == 'Grow Aggressively']

    keys = ['Zone', 'Region', 'State', 'District', 'Brand']
    # print(market_strategy_all_agr.dtypes)
    # print(market_potential_priority.dtypes)
    grow_aggr = market_strategy_all_agr.merge(
        market_potential_priority, on=keys, how='inner')

    grow_aggr['future_market_share_thres'] = (0.5 *
                                              grow_aggr['max_market_share']) / 6

    grow_aggr['future_market_share'] = grow_aggr[
        'future_market_share_thres'] + grow_aggr['Market_share']

    keys = ['State', 'District']
    grow_aggr = grow_aggr.merge(
        future_mp, on=keys)

    grow_aggr['target_sales'] = grow_aggr['future_market_share'] * \
        grow_aggr['future_market_potential']

    grow_aggr.drop(columns=['Month_y'], inplace=True)
    grow_aggr.rename(columns={'Month_x': 'Month'}, inplace=True)
    final_data = grow_aggr.append(
        [grow_inc_target, maintain_target], ignore_index=True)

    final_data = final_data.loc[(final_data.Month.dt.month == this_month) & (
        final_data.Month.dt.year == this_year)]
    final_data.drop_duplicates(inplace=True)

    final_data = final_data.drop_duplicates(subset=['State', 'District', 'Brand', 'Product', 'Ncr_market_potential_rating', 'Market_potential_rating', 'Month', 'Market leader',
                                            'Market_share_potential_rating', 'Delta_market_share_potential_rating', 'Zone', 'Region', 'market_position', 'market_lucrativeness', 'market_growth_strategy'])
    final_data.drop(columns=['Id_x', 'Id_y', 'Sales_y'], inplace=True)
    final_data.rename(columns={'Sales_x': 'Sales'}, inplace=True)
    # final_data.to_csv('sales_target_oct.csv', index=False)

    prod_sales = ncr_avg.loc[(ncr_avg.Month.dt.year == this_year) & (
        ncr_avg.Month.dt.month == this_month)]
    brand_sales_sum = prod_sales.groupby(
        ['State', 'District', 'Brand'], as_index=False)['Quantity_invoiced'].sum()
    brand_sales_sum.rename(
        columns={'Quantity_invoiced': 'total_brand_sales'}, inplace=True)

    keys = ['State', 'District', 'Brand']

    total_prod_sales = prod_sales.set_index(keys).join(
        brand_sales_sum.set_index(keys), on=keys)
    total_prod_sales['sales_ratio'] = total_prod_sales['Quantity_invoiced'] / \
        total_prod_sales['total_brand_sales']

    total_prod_sales.reset_index(inplace=True)
    req_final = final_data[['State', 'District',
                            'Brand', 'Next', 'target_sales']]

    prod_sales_target = total_prod_sales.set_index(
        keys).join(req_final.set_index(keys), how='inner')
    prod_sales_target['prod_sales_target'] = prod_sales_target['target_sales'] * \
        prod_sales_target['sales_ratio']
    prod_sales_target.reset_index(inplace=True)
    # prod_sales_target.to_csv('product_target_sales_oct.csv')

    market_strategy.columns = market_strategy.columns.str.upper()
    final_data.columns = final_data.columns.str.upper()
    prod_sales_target.columns = prod_sales_target.columns.str.upper()
    
    final_data = final_data.loc[final_data.BRAND != 'SCL']
    return market_strategy, final_data, prod_sales_target


if __name__ == '__main__':
    plan_month = ''
    district_classifier = pd.read_csv()
    market_share = pd.read_csv()
    ncr_avg = pd.read_csv()
    target_setting_change = pd.read_csv()
    df = target_setting(district_classifier, market_share, ncr_avg, target_setting_change, plan_month)
