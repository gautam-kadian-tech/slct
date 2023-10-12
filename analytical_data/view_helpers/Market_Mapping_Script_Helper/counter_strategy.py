import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def find_counter_strategy(data):
    # data = pd.read_csv('Final_client.csv')
    req_brands_data = ['state', 'district', 'counter_name','counter_id', 'address_block', 'shree_retail_sale',
                       'bangur_retail_sale', 'rockstrong_retail_sale', 'total_retail_sales'] #, 'collected_on']

    counter_data = data[req_brands_data]
    counter_data.dropna(subset=['district'], inplace=True)
    counter_data[['shree_retail_sale','bangur_retail_sale', 'rockstrong_retail_sale', 'total_retail_sales']] = counter_data[['shree_retail_sale','bangur_retail_sale', 'rockstrong_retail_sale', 'total_retail_sales']].fillna(0)
    # ------------------------------------------------------------------------------
    # TAKE AVERAGE FOR EACH MONTH FOR SALES
    # counter_data['month'] = pd.to_datetime(
    #     counter_data['collected_on'], format='%m/%d/%Y').dt.month
    # counter_data = counter_data.groupby(
    #     ['state', 'district', 'counter_name', 'month'], as_index=False).mean()
    # counter_data = counter_data.loc[counter_data.collected_on == counter_data.collected_on.max()]

    # -------------------------------------------------------------------------------------
    # counter_data = counter_data.loc[counter_data.district.str.strip() == 'Hisar']
    counter_data['state'] = counter_data['state'].str.strip()
    counter_data['district'] = counter_data['district'].str.strip()
    counter_data.drop_duplicates(inplace=True)
    # --------------------------------------------------------------------------------
    counter_share = counter_data.groupby(['state', 'district'])[
        'total_retail_sales'].sum()
    counter_share.rename('total_market_sale', inplace=True)
    counter_data = counter_data.set_index(
        ['state', 'district']).join(counter_share).reset_index()

    counter_data['market_sale'] = counter_data['total_retail_sales'] / \
        counter_data['total_market_sale']

    counter_data['shree_counter_share'] = counter_data['shree_retail_sale'] / \
        counter_data['total_retail_sales']

    counter_data['bangur_counter_share'] = counter_data['bangur_retail_sale'] / \
        counter_data['total_retail_sales']

    counter_data['rockstrong_counter_share'] = counter_data['rockstrong_retail_sale'] / \
        counter_data['total_retail_sales']

    # ------------------------------------------------

    # ------------------------------------------------------------------------
    # FIND OUTCOME = ACQUIRE & Oppurtunitistic
    acq_counter_data = counter_data.loc[(counter_data.shree_retail_sale == 0) & (
        counter_data.bangur_retail_sale == 0) & (counter_data.rockstrong_retail_sale == 0)]

    states = acq_counter_data.state.unique()
    acq_opp_final = pd.DataFrame()
    for state in states:
        state_acq = acq_counter_data.loc[acq_counter_data.state == state]
        districts = state_acq.district.unique()
        # print(districts)
        for district in districts:
            district_acq = state_acq.loc[state_acq.district == district]
            perc = np.percentile(district_acq.market_sale, q=75)
            district_acq['shree_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')

            district_acq['bangur_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')

            district_acq['rockstrong_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')
            # print(perc)
            acq_opp_final = acq_opp_final.append(
                district_acq, ignore_index=True)
    # --------------------------------------------------------------------------

    counter_df = counter_data.loc[(counter_data.shree_retail_sale != 0) | (
        counter_data.bangur_retail_sale != 0) | (counter_data.rockstrong_retail_sale != 0)]

    states = counter_df.state.unique()
    others_final = pd.DataFrame()
    for state in states:
        state_data = counter_df.loc[counter_df.state == state]
        districts = state_data.district.unique()

        for district in districts:
            counter_data_n0 = state_data.loc[state_data.district == district]

            shree_market_sale = counter_data_n0.loc[counter_data.shree_retail_sale > 0].market_sale
            counter_share_shree_arr = counter_data_n0.loc[
                counter_data_n0.shree_counter_share != 0].shree_counter_share

            if counter_share_shree_arr.empty:
                counter_data_n0['shree_counter_action'] = '0'
            else:
                shree_counter_share_perc = np.percentile(
                    counter_share_shree_arr, q=75)
                try:
                    market_sale_perc = np.percentile(shree_market_sale, q=75)
                except Exception:
                    market_sale_perc = 0
                # print(market_sale_perc, shree_counter_share_perc)
                counter_data_n0['shree_counter_action'] = np.where(
                    #(counter_data_n0['market_sale'] >= market_sale_perc)
                    (counter_data_n0['shree_counter_share'] >= shree_counter_share_perc), 'Retain',  0)
                a = counter_data_n0

            bangur_market_sale = counter_data_n0.loc[counter_data.bangur_retail_sale > 0].market_sale
            counter_share_bangur_arr = counter_data_n0.loc[
                counter_data_n0.bangur_counter_share != 0].bangur_counter_share
            if counter_share_bangur_arr.empty:
                counter_data_n0['bangur_counter_action'] = '0'
            else:
                bangur_counter_share_perc = np.percentile(
                    counter_share_bangur_arr, q=75)
                try:
                    market_sale_perc = np.percentile(bangur_market_sale, q=75)
                except Exception:
                    market_sale_perc = 0
                counter_data_n0['bangur_counter_action'] = np.where(
                    #(counter_data_n0['market_sale'] >= market_sale_perc)
                     (counter_data_n0['bangur_counter_share'] >= bangur_counter_share_perc), 'Retain',  0)

            rockstrong_market_sale = counter_data_n0.loc[counter_data.rockstrong_retail_sale > 0].market_sale
            counter_share_rockstrong_arr = counter_data_n0.loc[
                counter_data_n0.rockstrong_counter_share != 0].rockstrong_counter_share
            if counter_share_rockstrong_arr.empty:
                counter_data_n0['rockstrong_counter_action'] = '0'
            else:

                rockstrong_counter_share_perc = np.percentile(
                    counter_share_rockstrong_arr, q=75)
                try:
                    market_sale_perc = np.percentile(rockstrong_market_sale, q=75)
                except Exception:
                    market_sale_perc = 0
                counter_data_n0['rockstrong_counter_action'] = np.where(#(counter_data_n0['market_sale'] >= market_sale_perc)
                                                                        (counter_data_n0['rockstrong_counter_share'] >= rockstrong_counter_share_perc), 'Retain', 0)

            # print(counter_data_n0[['shree_counter_action', 'bangur_counter_action', 'rockstrong_counter_action']])

            # -----------------------------------------------------------------------
            counter_data_shree = counter_data_n0[counter_data_n0.shree_counter_action == '0']
            if not counter_data_shree.empty:
                market_sale_perc = np.percentile(
                    counter_data_shree.market_sale, q=10)
                counter_data_shree['shree_counter_action'] = np.where(
                    (counter_data_shree['market_sale'] < market_sale_perc) & (counter_data_shree['shree_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_shree = counter_data_shree[[
                    'state', 'district', 'counter_name','counter_id', 'shree_counter_action']]
            # -----------------------------------------------------------------------
            counter_data_bangur = counter_data_n0[counter_data_n0.bangur_counter_action == '0']
            if not counter_data_bangur.empty:
                market_sale_perc = np.percentile(
                    counter_data_bangur.market_sale, q=10)
                counter_data_bangur['bangur_counter_action'] = np.where(
                    (counter_data_bangur['market_sale'] < market_sale_perc) & (counter_data_bangur['bangur_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_bangur = counter_data_bangur[[
                    'state', 'district', 'counter_name','counter_id', 'bangur_counter_action']]
            # -----------------------------------------------------------------------
            counter_data_rock = counter_data_n0[counter_data_n0.rockstrong_counter_action == '0']
            if not counter_data_rock.empty:
                market_sale_perc = np.percentile(
                    counter_data_rock.market_sale, q=10)
                counter_data_rock['rockstrong_counter_action'] = np.where(
                    (counter_data_rock['market_sale'] < market_sale_perc) & (counter_data_rock['rockstrong_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_rock = counter_data_rock[[
                    'state', 'district', 'counter_name','counter_id', 'rockstrong_counter_action']]

            # ---------------------------------------------------------------------------
            counter_data_leftover = counter_data_n0[(counter_data_n0.rockstrong_counter_action == '0') | (
                counter_data_n0.shree_counter_action == '0') | (counter_data_n0.bangur_counter_action == '0')]
            if not counter_data_leftover.empty:
                counter_data_leftover['shree_counter_action'] = np.where(
                    (counter_data_leftover['shree_counter_share'] > 0) & (counter_data_leftover['shree_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['shree_counter_action'])

                counter_data_leftover['bangur_counter_action'] = np.where(
                    (counter_data_leftover['bangur_counter_share'] > 0) & (counter_data_leftover['bangur_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['bangur_counter_action'])

                counter_data_leftover['rockstrong_counter_action'] = np.where(
                    (counter_data_leftover['rockstrong_counter_share'] > 0) & (counter_data_leftover['rockstrong_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['rockstrong_counter_action'])

            # ---------------------------------------------------------------------------
            # UPDATE VALUES FOR COUNTER ACTION IF IT IS 0 IN counter_data_n0 AND NON ZERO IN 2ND DFS
            counter_data_n0.update(counter_data_shree)
            counter_data_n0.update(counter_data_bangur)
            counter_data_n0.update(counter_data_rock)
            counter_data_n0.update(counter_data_leftover)

            others_final = others_final.append(
                counter_data_n0, ignore_index=True)

    final = others_final.append(acq_opp_final, ignore_index=True)
    final['SCL_retail_sale'] = final['shree_retail_sale'] + \
        final['bangur_retail_sale'] + final['rockstrong_retail_sale']
    final['SCL_counter_share'] = final['SCL_retail_sale'] / \
        final['total_retail_sales']

    # final.to_csv('counter_strat.csv')

    retail_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block',  'total_retail_sales', 'total_market_sale', 'market_sale', 'SCL_retail_sale',
                                      'SCL_counter_share'], value_vars=[
        'shree_retail_sale', 'bangur_retail_sale', 'rockstrong_retail_sale'])  # ,
    retail_melt.rename(
        columns={'variable': 'Brand', 'value': 'retail_sale'}, inplace=True)
    retail_melt['Brand'] = retail_melt['Brand'].apply(
        lambda x: x.split('_')[0])

    # -----------------------------------------------------
    cs_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block'], value_vars=[
        'shree_counter_share', 'bangur_counter_share', 'rockstrong_counter_share'])
    cs_melt.rename(columns={'variable': 'Brand',
                   'value': 'counter_share'}, inplace=True)
    cs_melt['Brand'] = cs_melt['Brand'].apply(lambda x: x.split('_')[0])

    # -----------------------------------------------------
    csa_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block'], value_vars=[
        'shree_counter_action', 'bangur_counter_action', 'rockstrong_counter_action'])
    csa_melt.rename(columns={'variable': 'Brand',
                    'value': 'counter_share_action'}, inplace=True)
    csa_melt['Brand'] = csa_melt['Brand'].apply(lambda x: x.split('_')[0])
    csa_melt = csa_melt.loc[csa_melt.counter_share_action != '0']


    keys = ['state', 'district', 'counter_name','counter_id', 'address_block',  'Brand']
    cs_csa_joined = csa_melt.set_index(keys).join(cs_melt.set_index(keys))
    
    final_melt = cs_csa_joined.join(retail_melt.set_index(keys))
    # final_melt.to_csv('counter_start_melt_oct.csv')
    return final_melt
    
if __name__ == '__main__':
    data = pd.read_csv('Final_client.csv')
    req_brands_data = ['state', 'district', 'counter_name','counter_id', 'address_block', 'shree_retail_sale',
                       'bangur_retail_sale', 'rockstrong_retail_sale', 'total_retail_sales']

    counter_data = data[req_brands_data]
    counter_data.dropna(subset=['district'], inplace=True)
    # ------------------------------------------------------------------------------
    # TAKE AVERAGE FOR EACH MONTH FOR SALES
    # counter_data['month'] = pd.to_datetime(
    #     counter_data['collected_on'], format='%m/%d/%Y').dt.month
    # counter_data = counter_data.groupby(
    #     ['state', 'district', 'counter_name', 'month'], as_index=False).mean()
    # counter_data = counter_data.loc[counter_data.collected_on == counter_data.collected_on.max()]

    # -------------------------------------------------------------------------------------
    # counter_data = counter_data.loc[counter_data.district.str.strip() == 'Hisar']
    counter_data['state'] = counter_data['state'].str.strip()
    counter_data['district'] = counter_data['district'].str.strip()
    counter_data.drop_duplicates(inplace=True)
    # --------------------------------------------------------------------------------
    counter_share = counter_data.groupby(['state', 'district'])[
        'total_retail_sales'].sum()
    counter_share.rename('total_market_sale', inplace=True)
    counter_data = counter_data.set_index(
        ['state', 'district']).join(counter_share).reset_index()

    counter_data['market_sale'] = counter_data['total_retail_sales'] / \
        counter_data['total_market_sale']

    counter_data['shree_counter_share'] = counter_data['shree_retail_sale'] / \
        counter_data['total_retail_sales']

    counter_data['bangur_counter_share'] = counter_data['bangur_retail_sale'] / \
        counter_data['total_retail_sales']

    counter_data['rockstrong_counter_share'] = counter_data['rockstrong_retail_sale'] / \
        counter_data['total_retail_sales']

    # ------------------------------------------------

    # ------------------------------------------------------------------------
    # FIND OUTCOME = ACQUIRE & Oppurtunitistic
    acq_counter_data = counter_data.loc[(counter_data.shree_retail_sale == 0) & (
        counter_data.bangur_retail_sale == 0) & (counter_data.rockstrong_retail_sale == 0)]

    states = acq_counter_data.state.unique()
    acq_opp_final = pd.DataFrame()
    for state in states:
        state_acq = acq_counter_data.loc[acq_counter_data.state == state]
        districts = state_acq.district.unique()
        # print(districts)
        for district in districts:
            district_acq = state_acq.loc[state_acq.district == district]
            perc = np.percentile(district_acq.market_sale, q=75)
            district_acq['shree_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')

            district_acq['bangur_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')

            district_acq['rockstrong_counter_action'] = np.where(
                district_acq['market_sale'] >= perc, 'Acquire',  'Opportunistic')
            print(perc)
            acq_opp_final = acq_opp_final.append(
                district_acq, ignore_index=True)
    # --------------------------------------------------------------------------

    counter_df = counter_data.loc[(counter_data.shree_retail_sale != 0) | (
        counter_data.bangur_retail_sale != 0) | (counter_data.rockstrong_retail_sale != 0)]

    states = counter_df.state.unique()
    others_final = pd.DataFrame()
    for state in states:
        state_data = counter_df.loc[counter_df.state == state]
        districts = state_data.district.unique()

        for district in districts:
            counter_data_n0 = state_data.loc[state_data.district == district]

            shree_market_sale = counter_data_n0.loc[counter_data.shree_retail_sale > 0].market_sale
            counter_share_shree_arr = counter_data_n0.loc[
                counter_data_n0.shree_counter_share != 0].shree_counter_share

            if counter_share_shree_arr.empty:
                counter_data_n0['shree_counter_action'] = '0'
            else:
                shree_counter_share_perc = np.percentile(
                    counter_share_shree_arr, q=75)
                market_sale_perc = np.percentile(shree_market_sale, q=75)
                print(market_sale_perc, shree_counter_share_perc)
                counter_data_n0['shree_counter_action'] = np.where(
                    (counter_data_n0['market_sale'] >= market_sale_perc)
                    & (counter_data_n0['shree_counter_share'] >= shree_counter_share_perc), 'Retain',  0)
                a = counter_data_n0

            bangur_market_sale = counter_data_n0.loc[counter_data.bangur_retail_sale > 0].market_sale
            counter_share_bangur_arr = counter_data_n0.loc[
                counter_data_n0.bangur_counter_share != 0].bangur_counter_share
            if counter_share_bangur_arr.empty:
                counter_data_n0['bangur_counter_action'] = '0'
            else:
                bangur_counter_share_perc = np.percentile(
                    counter_share_bangur_arr, q=75)
                market_sale_perc = np.percentile(bangur_market_sale, q=75)
                counter_data_n0['bangur_counter_action'] = np.where(
                    (counter_data_n0['market_sale'] >= market_sale_perc)
                    & (counter_data_n0['bangur_counter_share'] >= bangur_counter_share_perc), 'Retain',  0)

            rockstrong_market_sale = counter_data_n0.loc[counter_data.rockstrong_retail_sale > 0].market_sale
            counter_share_rockstrong_arr = counter_data_n0.loc[
                counter_data_n0.rockstrong_counter_share != 0].rockstrong_counter_share
            if counter_share_rockstrong_arr.empty:
                counter_data_n0['rockstrong_counter_action'] = '0'
            else:

                rockstrong_counter_share_perc = np.percentile(
                    counter_share_rockstrong_arr, q=75)
                market_sale_perc = np.percentile(rockstrong_market_sale, q=75)
                counter_data_n0['rockstrong_counter_action'] = np.where((counter_data_n0['market_sale'] >= market_sale_perc)
                                                                        & (counter_data_n0['rockstrong_counter_share'] >= rockstrong_counter_share_perc), 'Retain', 0)

            # print(counter_data_n0[['shree_counter_action', 'bangur_counter_action', 'rockstrong_counter_action']])

            # -----------------------------------------------------------------------
            counter_data_shree = counter_data_n0[counter_data_n0.shree_counter_action == '0']
            if not counter_data_shree.empty:
                market_sale_perc = np.percentile(
                    counter_data_shree.market_sale, q=10)
                counter_data_shree['shree_counter_action'] = np.where(
                    (counter_data_shree['market_sale'] < market_sale_perc) & (counter_data_shree['shree_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_shree = counter_data_shree[[
                    'state', 'district', 'counter_name','counter_id', 'shree_counter_action']]
            # -----------------------------------------------------------------------
            counter_data_bangur = counter_data_n0[counter_data_n0.bangur_counter_action == '0']
            if not counter_data_bangur.empty:
                market_sale_perc = np.percentile(
                    counter_data_bangur.market_sale, q=10)
                counter_data_bangur['bangur_counter_action'] = np.where(
                    (counter_data_bangur['market_sale'] < market_sale_perc) & (counter_data_bangur['bangur_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_bangur = counter_data_bangur[[
                    'state', 'district', 'counter_name','counter_id', 'bangur_counter_action']]
            # -----------------------------------------------------------------------
            counter_data_rock = counter_data_n0[counter_data_n0.rockstrong_counter_action == '0']
            if not counter_data_rock.empty:
                market_sale_perc = np.percentile(
                    counter_data_rock.market_sale, q=10)
                counter_data_rock['rockstrong_counter_action'] = np.where(
                    (counter_data_rock['market_sale'] < market_sale_perc) & (counter_data_rock['rockstrong_counter_share'] < 0.05), 'Weed Out',  '0')

                counter_data_rock = counter_data_rock[[
                    'state', 'district', 'counter_name','counter_id', 'rockstrong_counter_action']]

            # ---------------------------------------------------------------------------
            counter_data_leftover = counter_data_n0[(counter_data_n0.rockstrong_counter_action == '0') | (
                counter_data_n0.shree_counter_action == '0') | (counter_data_n0.bangur_counter_action == '0')]
            if not counter_data_leftover.empty:
                counter_data_leftover['shree_counter_action'] = np.where(
                    (counter_data_leftover['shree_counter_share'] > 0) & (counter_data_leftover['shree_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['shree_counter_action'])

                counter_data_leftover['bangur_counter_action'] = np.where(
                    (counter_data_leftover['bangur_counter_share'] > 0) & (counter_data_leftover['bangur_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['bangur_counter_action'])

                counter_data_leftover['rockstrong_counter_action'] = np.where(
                    (counter_data_leftover['rockstrong_counter_share'] > 0) & (counter_data_leftover['rockstrong_counter_action'] == '0'), 'Penetrate',  counter_data_leftover['rockstrong_counter_action'])

            # ---------------------------------------------------------------------------
            # UPDATE VALUES FOR COUNTER ACTION IF IT IS 0 IN counter_data_n0 AND NON ZERO IN 2ND DFS
            counter_data_n0.update(counter_data_shree)
            counter_data_n0.update(counter_data_bangur)
            counter_data_n0.update(counter_data_rock)
            counter_data_n0.update(counter_data_leftover)

            others_final = others_final.append(
                counter_data_n0, ignore_index=True)

    final = others_final.append(acq_opp_final, ignore_index=True)
    final['SCL_retail_sale'] = final['shree_retail_sale'] + \
        final['bangur_retail_sale'] + final['rockstrong_retail_sale']
    final['SCL_counter_share'] = final['SCL_retail_sale'] / \
        final['total_retail_sales']

    final.to_csv('counter_strat.csv')

    retail_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block', 'total_retail_sales', 'total_market_sale', 'market_sale', 'SCL_retail_sale',
                                      'SCL_counter_share'], value_vars=[
        'shree_retail_sale', 'bangur_retail_sale', 'rockstrong_retail_sale'])  # ,
    retail_melt.rename(
        columns={'variable': 'Brand', 'value': 'retail_sale'}, inplace=True)
    retail_melt['Brand'] = retail_melt['Brand'].apply(
        lambda x: x.split('_')[0])

    # -----------------------------------------------------
    cs_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block'], value_vars=[
        'shree_counter_share', 'bangur_counter_share', 'rockstrong_counter_share'])
    cs_melt.rename(columns={'variable': 'Brand',
                   'value': 'counter_share'}, inplace=True)
    cs_melt['Brand'] = cs_melt['Brand'].apply(lambda x: x.split('_')[0])

    # -----------------------------------------------------
    csa_melt = final.melt(id_vars=['state', 'district', 'counter_name','counter_id', 'address_block'], value_vars=[
        'shree_counter_action', 'bangur_counter_action', 'rockstrong_counter_action'])
    csa_melt.rename(columns={'variable': 'Brand',
                    'value': 'counter_share_action'}, inplace=True)
    csa_melt['Brand'] = csa_melt['Brand'].apply(lambda x: x.split('_')[0])
    csa_melt = csa_melt.loc[csa_melt.counter_share_action != '0']


    keys = ['state', 'district', 'counter_name','counter_id', 'address_block',  'Brand']
    cs_csa_joined = csa_melt.set_index(keys).join(cs_melt.set_index(keys))
    
    final_melt = cs_csa_joined.join(retail_melt.set_index(keys))
    final_melt.to_csv('counter_start_melt_oct.csv')
