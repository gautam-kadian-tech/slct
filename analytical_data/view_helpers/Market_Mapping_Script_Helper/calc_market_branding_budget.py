import pandas as pd
from datetime import datetime
import dateutil
from .static import org_brand_map

multiplier = {'Maintain MS': 1,
              'Grow Incrementally': 1.25,
              'Grow Aggressively': 1.8}

per_tonne_thres_inr = {'SHREE': 35,
                       'BANGUR': 55,
                       'ROCKSTRONG': 35}

pos_marketing = {'Maintain MS': 0.20,
                 'Grow Incrementally': 0.20,
                 'Grow Aggressively': 0.20}

outdoor_marketing = {'Maintain MS': 0.50,
                     'Grow Incrementally': 0.45,
                     'Grow Aggressively': 0.35}

event_marketing = {'Maintain MS': 0.30,
                   'Grow Incrementally': 0.35,
                   'Grow Aggressively': 0.45}

corporate_marketing = {'SHREE': 0.3,
                       'BANGUR': 0.5,
                       'ROCKSTRONG': 0.3}

org_brand_map = {102: 'SHREE',
                 103: 'BANGUR',
                 104: 'ROCKSTRONG'
                 }


def join_data(market_brand_data, sales_target):
    market_brand_data.rename(columns={'DISTRICTS': 'DISTRICT'}, inplace=True)
    keys = ['STATE', 'DISTRICT', 'BRAND']
    # for key in keys:
    #     market_brand_data[key] = market_brand_data[key].str.capitalize()
    #     sales_target[key] = sales_target[key].str.capitalize()
    # market_brand_data.to_csv('a.csv')
    # sales_target.to_csv('b.csv')
    market_brand_data = market_brand_data.set_index(keys)
    sales_target = sales_target.set_index(keys)

    joined_df = market_brand_data.join(sales_target, how='inner')
    joined_df.reset_index(inplace=True)

    return joined_df


def get_new_cost(df):
    # default_mutliplier = 1

    # return per_tonne_thres_inr.get(df.BRAND), df['PER MT COST'] * multiplier.get(df.MARKET_GROWTH_STRATEGY)
    return df['PER MT COST']* multiplier.get(df.MARKET_GROWTH_STRATEGY)


def get_pos_marketing(df):
    default_mutliplier = 0.35
    return df['budget'] * pos_marketing.get(df.MARKET_GROWTH_STRATEGY, default_mutliplier)


def get_outdoor_marketing(df):
    default_mutliplier = 0.35
    return df['budget'] * outdoor_marketing.get(df.MARKET_GROWTH_STRATEGY, default_mutliplier)


def get_event_marketing(df):
    default_mutliplier = 0.35
    return df['budget'] * event_marketing.get(df.MARKET_GROWTH_STRATEGY, default_mutliplier)


def get_corporate_marketing(df):
    default_mutliplier = 0.3
    return df['budget'] * corporate_marketing.get(df.BRAND, default_mutliplier)

def prepare_data(data):
    cols = data.iloc[0,:]
    data.columns = cols
    data = data.iloc[1:, :]
    df = pd.melt(data, id_vars=['State', 'District'], value_vars=['Budget_Shree', 'Budget_Bangur', 'Budget_Rockstrong'], ignore_index=False)
    df.rename(columns = {0: 'Brand', 'value':'TOT_COST_RS_LAC'}, inplace= True)
    df['Brand'] = df['Brand'].str.replace('Budget_', '')
    # df.to_csv('market_brand_budget2.csv', index=False)
    
    return df


def calculate_brand_budget(sales_target_data, market_brand_data, ncr_data, plan_month):
    # this_month = datetime.now().month
    # if this_month ==1:
    #     this_month = 12
    # else:
    #     this_month = this_month - 1
    this_month= plan_month + dateutil.relativedelta.relativedelta(months=-1)
    this_year = this_month.year
    this_month = this_month.month
    
    
    
    # market_brand_data = pd.read_csv('market_BRAND_budget2.csv')
    # market_brand_data = pd.read_excel('Branding_Budget_Dummy.xlsx')
    # market_brand_data = prepare_data(market_brand_data)
    # market_brand_data.to_csv('branding_converted.csv')
    market_brand_data['TOT_COST_RS_LAC'] = market_brand_data['TOT_COST_RS_LAC'].astype('float')
    market_brand_data.columns = market_brand_data.columns.str.upper()
    market_brand_data = convert_data_to_upper(market_brand_data)
    # sales_target_data = pd.read_csv('sales_target_test.csv')
    # ncr_data = pd.read_csv('ncr_3_year.csv') # we only fetch the ncr data for req month 
    ncr_data = convert_data_to_upper(ncr_data)
    ncr_data['MONTH'] = pd.to_datetime(ncr_data['MONTH'],  format='%Y-%m-%d')
    
    ncr_monthly = ncr_data.loc[(ncr_data.MONTH.dt.month == this_month) &
                                        (ncr_data.MONTH.dt.year == this_year)]
    
    # ncr_monthly.columns = ncr_monthly.columns.str.capitalize()
    ncr_monthly.replace({'BRAND': org_brand_map}, inplace=True)
    # print(ncr_mon)
    ncr_brand = ncr_monthly.groupby(['STATE', 'DISTRICT', 'BRAND'], as_index= False)['QUANTITY_INVOICED'].sum()
    
    # --------------------------------------------------------
    # DATA PROCESSING TO JOIN SUCCESSFULLY   
    
    sales_target = sales_target_data[[
        'STATE', 'DISTRICT', 'BRAND', 'MARKET_GROWTH_STRATEGY', 'MARKET_LUCRATIVENESS', 'MARKET_POSITION', 'TARGET_SALES']]
    # cols = ['STATE', 'DISTRICT']
    # for col in cols:
    #     sales_target[col] = sales_target[col].str.upper()
    #     ncr_brand[col] = ncr_brand[col].str.upper()

    # -----------------------------------------------------------
    # keys = ['STATE', 'DISTRICT']
    # market_brand_data = market_brand_data.set_index(keys).join(ncr_brand)
    ncr_brand.replace({'Brand': org_brand_map}, inplace=True)
    market_brand_data = join_data(market_brand_data, ncr_brand) # JOINING NCR AND MARKET BRAND DATA
    
    # print(market_brand_data)
    # market_brand_data['STATE'] = market_brand_data['STATE'].str.replace('Haryana', 'Hr')
    # print(market_brand_data.shape, sales_target.shape)
    joined_df = join_data(market_brand_data, sales_target)
    print('----------------------------------------')
    
    # -----------------------------------------------------------
    # CALCULATING PER MT COST AT MONTH LEVEL
    joined_df.drop(columns = ['PER MT COST'], inplace = True, errors='ignore')
    joined_df['PER MT COST'] = ((joined_df['TOT_COST_RS_LAC'] * 100000)/ 12) / joined_df['QUANTITY_INVOICED']
    
    # -----------------------------------------------------------------------
    if joined_df.empty:
        print('empty joined df')
    else:
        print(joined_df.columns)
        joined_df['new_cost'] = joined_df.apply(get_new_cost, axis=1)
        joined_df['multiplier'] = joined_df['MARKET_GROWTH_STRATEGY'].map(multiplier)
        joined_df['budget'] = joined_df['TARGET_SALES'] * joined_df['new_cost']
    
        joined_df['pos_budget'] = joined_df.apply(get_pos_marketing, axis=1)
        joined_df['outdoor_budget'] = joined_df.apply(
            get_outdoor_marketing, axis=1)
        joined_df['event_budget'] = joined_df.apply(get_event_marketing, axis=1)
        joined_df['corporate_budget'] = joined_df.apply(
            get_corporate_marketing, axis=1)
        joined_df['total_budget'] = joined_df['corporate_budget'] + \
            joined_df['budget']
    
        joined_df.dropna(inplace=True)
        
    return joined_df

def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df
        
if __name__ == '__main__':
    plan_month = ''
    market_brand_data = pd.read_csv('market_brand_budget2.csv')
    sales_target_data = pd.read_csv('sales_target_test.csv')
    ncr_data = pd.read_csv('ncr_3_year.csv') # we only fetch the ncr data for req month 
    
    df = calculate_brand_budget(sales_target_data, market_brand_data, ncr_data, plan_month)
