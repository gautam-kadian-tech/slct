import pandas as pd

data = pd.read_excel('Combined_data_v2_cleaned.xlsx')

data.rename(columns={'Wholesale (MT) / MONTH': 'whole_sale', 'Retail Sale (MT) / MONTH': 'retail_sale',
                     'Retail_Wholesale': 'total_sale', 'Counter Name':'counter_name', 'Address, Block': 'address_block'}, inplace=True)
data.drop(columns=['total_sale'], inplace=True)


df = data.pivot_table(['whole_sale', 'retail_sale'], ['Zone', 'State', 'District', 'Taluka', 'counter_name',
                                                      'address_block', 'Location tag (Latitude)', 'Location tag (Longitude)',
                                                      'Is this a SCL counter?', 'Dealer Or Retailer ?'], 'Brand')


df.columns = ['{}_{}'.format(j, i) for i, j in df.columns]
df.reset_index(inplace=True, drop=False)
df.fillna(0, inplace=True)
df['rockstrong_retail_sale'] = 0
df['rockstrong_whole_sale'] = 0
df.columns = df.columns.str.lower()
retail_cols = [c for c in df.columns if 'retail' in c]
df['total_retail_sales'] = df[retail_cols].sum(axis=1)

df.to_csv('final_client_new.csv', index= False)
