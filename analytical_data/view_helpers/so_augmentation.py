# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:17:44 2023

@author: tanay
"""

import pandas as pd
from geopy.distance import distance as calc_dist
from .connection import connect_db
from datetime import datetime as dt
import warnings
warnings.filterwarnings('ignore')
# import numpy as np




def convert_data_to_upper(df):
    cols = df.select_dtypes('O')
    for col in cols:
        df[col] = df[col].str.upper()
    return df


# def get_rating(df, col):
#     final_df = pd.DataFrame()
#     districts = df.DISTRICT.unique()
#     for district in districts:
#         df_state = df.loc[df.DISTRICT == district]
#         prerc_50 = 
#         df_state[col+'_SCORE'] = np.where(df_state[col]>= prerc_50, 'High', 'Low')
#         final_df = final_df.append(df_state, ignore_index= True)    
        
#     return final_df
def get_rating(df, avgcol, col):
    if df[col]> 1.3* df[avgcol]:
        return 'High'
    elif (df[col] > 0.7 *df[avgcol]) and (df[col]<= 1.3* df[avgcol]):
        return 'Optimal'
    else:
        return 'Low'
class SoAugmentation:   
    def run_model():
        cnxn = connect_db()
        # data= pd.read_excel('Market-wise SO requirements.xlsx', sheet_name= None)
        # master_df = data.get('Area_Number_Potential (Master)'),
        master_df = pd.read_sql('''select "TALUKA", "COUNTER_CODE", "LAT", "LONG","SO CODE", "COUNTER_POTENTIAL",
        "STATE", "DISTRICT" from target."AUGMENTATION_INPUT_TABLE" where "LAT" is not null ''',cnxn)

        master_df= convert_data_to_upper(master_df)
        master_df.columns = master_df.columns.str.upper()


        so_count = master_df.groupby(['STATE', 'DISTRICT', 'TALUKA'], as_index= False)['SO CODE'].nunique()
        so_count.rename(columns = {'SO CODE': 'SO_COUNT'}, inplace= True)
        market_potential = master_df.groupby(['STATE', 'DISTRICT', 'TALUKA'], as_index= False)['COUNTER_POTENTIAL'].sum()
        joined_df = market_potential.merge(so_count, on = ['STATE', 'DISTRICT', 'TALUKA'])
        joined_df['MP_PER_SO'] = joined_df['COUNTER_POTENTIAL'] / joined_df['SO_COUNT']
        avg_mp = joined_df[['STATE','TALUKA', 'MP_PER_SO','COUNTER_POTENTIAL']].drop_duplicates()
        avg_mp = avg_mp.groupby(['STATE'], as_index= False)['COUNTER_POTENTIAL'].mean()
        avg_mp.rename(columns= {'COUNTER_POTENTIAL':'AVG_MP'}, inplace=True)
        joined_df = joined_df.merge(avg_mp, on=['STATE'])
        print(joined_df)
        
        joined_df['MP_RATING'] = joined_df.apply(get_rating, args= ('AVG_MP', 'MP_PER_SO'), axis = 1)


        talukas = master_df.TALUKA.unique()
        final_df = pd.DataFrame()
        for taluka in talukas:
            taluka_df = master_df.loc[master_df.TALUKA == taluka]
            lat_cntr = taluka_df['LAT'].mean()
            long_cntr = taluka_df['LONG'].mean()
            radius = taluka_df.apply(lambda x: calc_dist((x.LAT,x.LONG),(lat_cntr,long_cntr)).km,axis=1).max()
            area = 3.14*radius*radius
            taluka_df['GEO_SPREAD'] = area
            final_df = final_df.append(taluka_df, ignore_index= True)



        geo_df = final_df.merge(so_count, on=['STATE', 'DISTRICT', 'TALUKA'])
        geo_df['GEO_PER_SO'] = geo_df['GEO_SPREAD'] / geo_df['SO_COUNT']
        # avg_geo['GEO_SPREAD'] = geo_df['GEO_SPREAD']
        avg_geo = geo_df[['STATE', 'TALUKA', 'GEO_PER_SO','GEO_SPREAD']].drop_duplicates()
        avg_geo = avg_geo.groupby(['STATE'], as_index= False)['GEO_SPREAD'].mean()
        avg_geo.rename(columns= {'GEO_SPREAD':'AVG_GEO'}, inplace=True)
        geo_df = geo_df.merge(avg_geo, on=['STATE'])

        geo_df['GEO_ RATING'] = geo_df.apply(get_rating, args= ('AVG_GEO', 'GEO_PER_SO'), axis = 1)
    
        geo_df['BRAND'] = 'SHREE'

        geo_df2 = geo_df[['SO CODE', 'TALUKA', 'DISTRICT', 'STATE', 'BRAND','GEO_SPREAD','GEO_PER_SO', 'AVG_GEO', 'GEO_ RATING']].drop_duplicates()

        # trying
        no_of_counters = master_df.groupby(['STATE', 'DISTRICT', 'TALUKA'], as_index= False)[['COUNTER_CODE']].count()
        no_of_counters_df = no_of_counters.merge(so_count, on = ['STATE', 'DISTRICT', 'TALUKA'])
        no_of_counters_df['COUNTER_PER_SO'] = no_of_counters_df['COUNTER_CODE'] / joined_df['SO_COUNT']
        avg_c = no_of_counters_df[['STATE','TALUKA','COUNTER_CODE', 'COUNTER_PER_SO']].drop_duplicates()
        print(avg_c)
        
        avg_c = avg_c.groupby(['STATE'], as_index= False)['COUNTER_CODE'].mean()
        avg_c.rename(columns= {'COUNTER_CODE':'AVG_C'}, inplace=True)
        no_of_counters_df = no_of_counters_df.merge(avg_c, on=['STATE'])
    
        no_of_counters_df['COUNTER_RATING'] = no_of_counters_df.apply(get_rating, args= ('AVG_C', 'COUNTER_PER_SO'), axis = 1)

        


        final_data = geo_df2.merge(joined_df, on=['STATE', 'DISTRICT', 'TALUKA'])
        final_data = final_data.merge(no_of_counters_df, on=['STATE', 'DISTRICT', 'TALUKA'])
    
        final_data['DATE'] = dt.now().strftime('%Y-%m-%d')
        # final_data.to_csv('final_data_all3.csv')
        final_data.rename(columns= {'SO_COUNT_x':'SO_COUNT','COUNTER_CODE':'COUNTER_CODE_COUNT'}, inplace=True)
        # final_data.drop(["SO_COUNT_y"], axis = 1, inplace = True)
        print(final_data)
        # final_data=pd.read_csv('final_data_all3.csv')
        
        #Additional
        mp_rating_perc=0.30
        counter_rating_perc=0.40
        geo_rating_perc=0.30
        print(final_data)
        print(final_data.columns)
        final_data['GEO_RATING_SCORE']=None
        final_data['GEO_RATING_SCORE_WEIGHTAGE']=None
        final_data['MP_RATING_SCORE']=None
        final_data['MP_RATING_SCORE_WEIGHTAGE']=None
        final_data['COUNTER_RATING_SCORE']=None
        final_data['COUNTER_RATING_SCORE_WEIGHTAGE']=None
        for i in range(0,len(final_data)):
            if (final_data['GEO_ RATING'][i]=='Low'):
                    final_data['GEO_RATING_SCORE'][i]=1
                    final_data['GEO_RATING_SCORE_WEIGHTAGE'][i]=final_data['GEO_RATING_SCORE'][i]*geo_rating_perc
            elif(final_data['GEO_ RATING'][i]=='Optimal'):     
                    final_data['GEO_RATING_SCORE'][i]=3
                    final_data['GEO_RATING_SCORE_WEIGHTAGE'][i]=final_data['GEO_RATING_SCORE'][i]*geo_rating_perc
            elif(final_data['GEO_ RATING'][i]=='High'): 
                    final_data['GEO_RATING_SCORE'][i]=5
                    final_data['GEO_RATING_SCORE_WEIGHTAGE'][i]=final_data['GEO_RATING_SCORE'][i]*geo_rating_perc
                    
            if (final_data['MP_RATING'][i]=='Low'):
                    final_data['MP_RATING_SCORE'][i]=1
                    final_data['MP_RATING_SCORE_WEIGHTAGE'][i]=final_data['MP_RATING_SCORE'][i]*mp_rating_perc
            elif(final_data['MP_RATING'][i]=='Optimal'):     
                    final_data['MP_RATING_SCORE'][i]=3
                    final_data['MP_RATING_SCORE_WEIGHTAGE'][i]=final_data['MP_RATING_SCORE'][i]*mp_rating_perc
            elif(final_data['MP_RATING'][i]=='High'): 
                    final_data['MP_RATING_SCORE'][i]=5
                    final_data['MP_RATING_SCORE_WEIGHTAGE'][i]=final_data['MP_RATING_SCORE'][i]*mp_rating_perc
            
            if (final_data['COUNTER_RATING'][i]=='Low'):
                    final_data['COUNTER_RATING_SCORE'][i]=1
                    final_data['COUNTER_RATING_SCORE_WEIGHTAGE'][i]=final_data['COUNTER_RATING_SCORE'][i]*counter_rating_perc
            elif(final_data['COUNTER_RATING'][i]=='Optimal'):     
                    final_data['COUNTER_RATING_SCORE'][i]=3
                    final_data['COUNTER_RATING_SCORE_WEIGHTAGE'][i]=final_data['COUNTER_RATING_SCORE'][i]*counter_rating_perc
            elif(final_data['COUNTER_RATING'][i]=='High'): 
                    final_data['COUNTER_RATING_SCORE'][i]=5
                    final_data['COUNTER_RATING_SCORE_WEIGHTAGE'][i]=final_data['COUNTER_RATING_SCORE'][i]*counter_rating_perc
        final_data['SUM_ALL_RATING_WEIGHTAGE']=final_data['GEO_RATING_SCORE_WEIGHTAGE']+final_data['MP_RATING_SCORE_WEIGHTAGE']+final_data['COUNTER_RATING_SCORE_WEIGHTAGE']
        final_data.rename(columns= {'SO_COUNT_x':'SO_COUNT','COUNTER_CODE':'COUNTER_CODE_COUNT'}, inplace=True)
        final_data.drop(["SO_COUNT_y"], axis = 1, inplace = True)
        final_data['REMARKS']=None
        for i in range(0, len(final_data)):
            if final_data['SUM_ALL_RATING_WEIGHTAGE'][i]>=4:
                final_data['REMARKS'][i]="Add SOs or divide the Geography"
            elif final_data['SUM_ALL_RATING_WEIGHTAGE'][i]<=2:
                final_data['REMARKS'][i]="SO may be under utilized. Can provide additional responsibility"
            elif (final_data['SUM_ALL_RATING_WEIGHTAGE'][i]>2) and (final_data['SUM_ALL_RATING_WEIGHTAGE'][i]<4):
                final_data['REMARKS'][i]="Optimal size of market and no. of SOs"
        # final_data.to_csv('final_data_try.csv')
        final_data.rename(columns={'SO CODE':'SO_CODE','GEO_ RATING':'GEO_RATING'},inplace=True)
        return final_data

    # if __name__ == '__main__':

    #     final_data = run_model()

        # print(final_data)
        # final_data.to_csv('output.csv', index= False)
