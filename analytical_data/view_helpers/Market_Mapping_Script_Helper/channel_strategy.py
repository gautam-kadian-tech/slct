import pandas as pd

cs_strategy_map = {'Maintain MS': 'Maintain',
                   'Grow Incrementally': 'Moderate addition',
                   'Grow Aggressively': 'High addition'
                   }


def prepare_row_channel_data(channel_data):

    channel_data['scl_retail_sale'] = channel_data['shree_retail_sale'] + \
        channel_data['bangur_retail_sale'] + \
        channel_data['rockstrong_retail_sale']

    req_brands_data = ['state', 'district', 'shree_retail_sale',
                       'bangur_retail_sale', 'rockstrong_retail_sale', 'scl_retail_sale', 'total_retail_sales']

    brand_channel_data = channel_data[req_brands_data]
    final_channel_brand = pd.DataFrame()

    # print(brand_channel_data.columns)
    total_retail_sale = brand_channel_data.groupby(
        ['state', 'district'], as_index=False)['total_retail_sales'].sum()
    total_retail_sale.rename(
        columns={'total_retail_sales': 'total_sales'}, inplace=True)

    brand_channel_data_shree = brand_channel_data.loc[brand_channel_data.shree_retail_sale != 0].groupby([
        'state', 'district'], as_index=False)['shree_retail_sale', 'total_retail_sales'].sum()
    brand_channel_data_shree['Brand'] = 'SHREE'
    brand_channel_data_shree.rename(
        columns={'shree_retail_sale': 'retail_sale'}, inplace=True)
    brand_channel_data_bangur = brand_channel_data.loc[brand_channel_data.bangur_retail_sale != 0].groupby([
        'state', 'district'], as_index=False)['bangur_retail_sale', 'total_retail_sales'].sum()

    brand_channel_data_bangur['Brand'] = 'BANGUR'
    brand_channel_data_bangur.rename(
        columns={'bangur_retail_sale': 'retail_sale'}, inplace=True)

    brand_channel_data_rockstrong = brand_channel_data.loc[brand_channel_data.rockstrong_retail_sale != 0].groupby([
        'state', 'district'], as_index=False)['rockstrong_retail_sale', 'total_retail_sales'].sum()
    brand_channel_data_rockstrong['Brand'] = 'ROCKSTRONG'
    brand_channel_data_rockstrong.rename(
        columns={'rockstrong_retail_sale': 'retail_sale'}, inplace=True)

    brand_channel_data_scl = brand_channel_data.loc[brand_channel_data.scl_retail_sale != 0].groupby([
        'state', 'district'], as_index=False)['scl_retail_sale', 'total_retail_sales'].sum()
    brand_channel_data_scl['Brand'] = 'SCL'
    brand_channel_data_scl.rename(
        columns={'scl_retail_sale': 'retail_sale'}, inplace=True)

    final_channel_brand = final_channel_brand.append([brand_channel_data_shree, brand_channel_data_bangur,
                                                      brand_channel_data_rockstrong, brand_channel_data_scl], ignore_index=True)

    final_channel_brand['counter_share'] = final_channel_brand['retail_sale'] / \
        final_channel_brand['total_retail_sales']

    keys = ['state', 'district']
    final_channel_brand = final_channel_brand.set_index(
        keys).join(total_retail_sale.set_index(keys))
    final_channel_brand['acv'] = final_channel_brand['total_retail_sales'] / \
        final_channel_brand['total_sales']
    final_channel_brand.reset_index(inplace=True)
    final_channel_brand.columns = final_channel_brand.columns.str.capitalize()
    return final_channel_brand

def find_min_target_acv(df):
    # print(df.columns)
    if df.MARKET_GROWTH_STRATEGY == 'Maintain MS':
        return df.ACV
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Incrementally':
        return df.ACV * 1.05
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Aggressively':
        return df.ACV * 1.1
    else:
        return 0


def find_max_target_acv(df):

    if df.MARKET_GROWTH_STRATEGY == 'Maintain MS':
        return df.ACV * 1.05
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Incrementally':
        return df.ACV * 1.1
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Aggressively':
        return df.ACV * 1.25
    else:
        return 0


def find_counter_share(df):
    if df.MARKET_GROWTH_STRATEGY == 'Maintain MS':
        return df['COUNTER_SHARE']
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Incrementally':
        return df['COUNTER_SHARE'] + df.FUTURE_MARKET_SHARE_THRES
    elif df.MARKET_GROWTH_STRATEGY == 'Grow Aggressively':
        return df['COUNTER_SHARE'] + df.FUTURE_MARKET_SHARE_THRES
    else:
        return 0
def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
        df[col] = df[col].str.strip()
    return df

def find_channel_stretegy(channel_data, market_strategy, sales_target):
    # channel_data = pd.read_csv('Final_client.csv')
    channel_data = convert_data_to_upper(channel_data)    
    # market_strategy = pd.read_csv('market_strategy.csv')
    market_strategy_all = market_strategy.loc[market_strategy.PRODUCT == 'All']
    req_cols = ['STATE', 'DISTRICT', 'BRAND', 'MARKET_GROWTH_STRATEGY']
    market_strategy_all = market_strategy_all[req_cols]

    # data_keys = ['STATE', 'DISTRICT']
    # for key in data_keys:
    #     channel_data[key] = channel_data[key].str.strip()

    final_brand_channel = prepare_row_channel_data(channel_data)
    final_brand_channel.columns = final_brand_channel.columns.str.upper()
    # final_brand_channel.to_csv('channel_conv.csv')
    keys = ['STATE', 'DISTRICT', 'BRAND']

    # for key in keys:
    #     final_brand_channel[key] = final_brand_channel[key].str.capitalize()
    #     market_strategy_all[key] = market_strategy_all[key].str.capitalize()

    brand_market = final_brand_channel.set_index(keys).join(
        market_strategy_all.set_index(keys), how='inner')

    if not brand_market.empty:
        # print(brand_market.columns)
        brand_market['min_target_acv'] = brand_market.apply(
            find_min_target_acv, axis=1)
        brand_market['max_target_acv'] = brand_market.apply(
            find_max_target_acv, axis=1)
    else:
        print('Empty dataframe, cannot find ACV values.')

    # sales_target = pd.read_csv('sales_target_oct.csv')
    # print(sales_target.columns)
    sales_target = sales_target[[
        'STATE', 'DISTRICT', 'BRAND', 'FUTURE_MARKET_SHARE', 'FUTURE_MARKET_SHARE_THRES']]

    # brand_market.to_csv('ACV_output.csv')

    brand_market = brand_market.join(sales_target.set_index(keys), how='left')
    brand_market.fillna(0, inplace=True)
    if not brand_market.empty:
        # print(brand_market.columns)
        brand_market['counter_share_target'] = brand_market.apply(
            find_counter_share, axis=1)

        brand_market['counter_share_strategy'] = brand_market['MARKET_GROWTH_STRATEGY'].map(
            cs_strategy_map)
    
    return brand_market

if __name__ == '__main__':
    channel_data = pd.read_csv('Final_client.csv')
    channel_data = convert_data_to_upper(channel_data)
    channel_data.columns = channel_data.columns.str.upper()
    
    market_strategy = pd.read_csv('market_strategy.csv')
    market_strategy_all = market_strategy.loc[market_strategy.PRODUCT == 'All']
    req_cols = ['STATE', 'DISTRICT', 'BRAND', 'MARKET_GROWTH_STRATEGY']
    market_strategy_all = market_strategy_all[req_cols]

    # data_keys = ['STATE', 'DISTRICT']
    # for key in data_keys:
    #     channel_data[key] = channel_data[key].str.strip()

    final_brand_channel = prepare_row_channel_data(channel_data)

    keys = ['STATE', 'DISTRICT', 'BRAND']

    # for key in keys:
    #     final_brand_channel[key] = final_brand_channel[key].str.capitalize()
    #     market_strategy_all[key] = market_strategy_all[key].str.capitalize()

    brand_market = final_brand_channel.set_index(keys).join(
        market_strategy_all.set_index(keys), how='inner')

    if not brand_market.empty:
        brand_market['min_target_acv'] = brand_market.apply(
            find_min_target_acv, axis=1)
        brand_market['max_target_acv'] = brand_market.apply(
            find_max_target_acv, axis=1)
    else:
        print('Empty dataframe, cannot find ACV values.')

    sales_target = pd.read_csv('sales_target_oct.csv')
    sales_target = sales_target[[
        'STATE', 'DISTRICT', 'BRAND', 'future_market_share', 'future_market_share_thres']]

    brand_market.to_csv('ACV_output.csv')

    brand_market = brand_market.join(sales_target.set_index(keys), how='left')
    brand_market.fillna(0, inplace=True)
    if not brand_market.empty:
        brand_market['counter_share_target'] = brand_market.apply(
            find_counter_share, axis=1)

        brand_market['counter_share_strategy'] = brand_market['MARKET_GROWTH_STRATEGY'].map(
            cs_strategy_map)

        brand_market.to_csv('ounter_share_target_oct.csv')
