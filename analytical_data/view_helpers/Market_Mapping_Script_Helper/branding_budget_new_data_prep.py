import pandas as pd


data= pd.read_excel('Branding_Budget_Dummy.xlsx')

cols = data.iloc[0,:]
data.columns = cols
data = data.iloc[1:, :]


df = pd.melt(data, id_vars=['State', 'District'], value_vars=['Budget_Shree', 'Budget_Bangur', 'Budget_Rockstrong'], ignore_index=False)

df.rename(columns = {0: 'Brand', 'value':'TOT_COST_RS_LAC'}, inplace= True)

df['Brand'] = df['Brand'].str.replace('Budget_', '')
df.to_csv('market_brand_budget2.csv', index=False)
