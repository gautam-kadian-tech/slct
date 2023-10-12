import numpy as np
import pandas as pd

def read_excel(filename):
    return pd.read_excel(filename, sheet_name= None)


def convert_data(data):
    final_df = pd.DataFrame()
    
    for key in data.keys():
        df = data.get(key)
        df = df.melt(id_vars=["STATE", "ZONE", "DISTRICT", "ORG BRAND"], 
                      var_name="Month", 
                      value_name="SALES")

        df["Month"] = df["Month"].str.replace('JUNE', 'JUN')
        df["Month"] = df["Month"].str.replace('JULY', 'JUL')
        df['Month'] = pd.to_datetime(df['Month'], format="%b'%y")
        # df = df.loc[~df['DISTRICT'].str.upper().str.contains('TOTAL')]
        df.rename(columns= {'ORG BRAND': 'Brand'}, inplace = True)
        final_df = final_df.append(df)
    
    
    # print(final_df)
    
    return final_df



def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df


def insert_to_db(df):
    df.to_csv('Market_Share_test_state_2022_10_01.csv', index= False)
    
if __name__ == '__main__':
    # filename = 'final_df_2022_09_01.xlsx'
    filename = 'Market_Potential_Share_Oct.xlsx'
    df = read_excel(filename)
    df = convert_data(df)
    # insert_to_db(df)

    # final_df = pd.read_csv('final_df_test_state_2022_09_01.csv')
    final_df = df.copy()
    # final_df['SALES'] = final_df['SALES'].str.strip().str.replace('','0').str.replace('0-0','0').str.replace('0.0','0')
    final_df['SALES'] = pd.to_numeric(final_df['SALES'],errors='coerce')
    final_df['SALES'] = final_df['SALES'].fillna(0)

    final_df_tmp = final_df.groupby(['STATE','DISTRICT','Month'],as_index=False)['SALES'].sum()
    final_df_tmp.rename(columns={'SALES':'Market Potential'},inplace=True)
    
    final_df = final_df.merge(final_df_tmp,on=['STATE','DISTRICT','Month'])
    final_df['Market Share'] = round(final_df['SALES']/final_df['Market Potential'],3)

    final_df['Market Share'] = final_df['Market Share'].fillna(0)
    
    final_df_tmp = final_df[final_df['Brand'].isin(
        ['Shree', 'Rockstrong', 'Bangur'])]
    final_df_tmp = final_df_tmp.groupby(['STATE','DISTRICT','Month'], as_index=False).agg({'SALES': np.sum, 'Market Potential': np.mean})
    final_df_tmp['Brand'] = 'SCL'
    final_df = final_df.append(final_df_tmp, ignore_index=True)
    final_df.loc[final_df['Brand'] == 'SCL', 'Market Share'] = round(
        final_df[final_df['Brand'] == 'SCL']['SALES']/final_df[final_df['Brand'] == 'SCL']['Market Potential'], 3)
    final_df.fillna(0, inplace=True)
    final_df.drop_duplicates(inplace=True)
    
    
    hr_map = pd.read_csv('_SCL_HIERARCHY_MASTER__202211111335.csv')
    hr_map_req = hr_map[['STATE_SCL', 'DISTRICT_SCL',
                         'STATE_ERP', 'DISTRICT_ERP']].drop_duplicates()
    hr_map_req = convert_data_to_upper(hr_map_req)
    final_df = convert_data_to_upper(final_df)
    final_df = final_df.merge(hr_map_req, left_on=['STATE', 'DISTRICT'], right_on=[
                            'STATE_SCL', 'DISTRICT_SCL'], how='left')
    
    
    # insert_to_db(final_df)
    
