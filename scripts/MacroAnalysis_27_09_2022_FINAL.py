from dataclasses import replace
from distutils.log import error
from enum import unique
from tkinter import TRUE
import pandas as pd
import psycopg2
import numpy as np
import psycopg2.extras as extras

# from sqlalchemy import create_engine
if __name__ == "__main__":

    #     server = 'c.hyperdb-slct-dev.postgres.database.azure.com'
    server = "10.20.2.4"
    database = "citus"
    username = "citus"
    password = "Njz2t3rUb9gS"
    cnxn = psycopg2.connect(
        host=server, database=database, user=username, password=password
    )
    df_score_fnl = pd.DataFrame()


# ("--------------------------Urban_Calculation(Done)--------------------------------------")
df_urban_calculation = pd.read_sql(
    """ select * from etl_zone."DF_URBAN_POPULATION_2011" """, cnxn
)
df_rate = pd.read_sql(
    """ select * from etl_zone."DF_ANNUAL_POPULATION_GROWTH_RATE" """, cnxn
)
df_urban_calculation.rename(columns={"IN_%_2011": "IN_%_2011 to URBAN_%"}, inplace=True)
df_urban_calculation["POPULATION_2021"] = None
df_urban_calculation["URBAN_POPULATION_2011"] = (
    df_urban_calculation["IN_%_2011 to URBAN_%"]
    * df_urban_calculation["POPULATION_2011"]
) / 100  # change IN_%_2011 to URBAN_%
df_urban_calculation = pd.merge(df_urban_calculation, df_rate, on="STATE", how="left")
df_annual_urbanization_rate = pd.read_sql(
    """ select * from etl_zone."DF_ANNUAL_URBANIZATION_RATE" """, cnxn
)
df_urban_calculation["POPULATION_2021"] = df_urban_calculation[
    "URBAN_POPULATION_2011"
] * (pow((1 + df_urban_calculation["URBAN_GROWTH_RATE"]), 10))
df_urban_calculation = pd.merge(
    df_urban_calculation, df_annual_urbanization_rate, on=["STATE"], how="left"
)
df_urban_calculation["NEW_URBAN_POPULATION"] = (
    df_urban_calculation["POPULATION_2021"]
    * df_urban_calculation["ANNUAL_URBANIZATION_RATE"]
)  # Change name to NEW_URBAN_POPULATION
df_urban_rural_household = pd.read_sql(
    """ select * from etl_zone."DF_URBAN_RURAL_HOUSEHOLD_SIZE" """, cnxn
)
df_urban_calculation = pd.merge(
    df_urban_calculation, df_urban_rural_household, on=["STATE", "DISTRICT"], how="left"
)
df_urban_calculation["LY_HOUSEHOLDS"] = (
    df_urban_calculation["POPULATION_2021"]
    / df_urban_rural_household["URBAN_HOUSEHOLD_SIZE"]
)
df_urban_calculation["NEW_HOUSEHOLDS"] = (
    df_urban_calculation["NEW_URBAN_POPULATION"]
    / df_urban_rural_household["URBAN_HOUSEHOLD_SIZE"]
)
df_high_rise_low_rise_split = pd.read_sql(
    """ select * from etl_zone."DF_HIGH_RISE_LOW_RISE_SPLIT" """, cnxn
)
df_urban_calculation = pd.merge(
    df_urban_calculation, df_high_rise_low_rise_split, on="STATE", how="left"
)
df_urban_calculation["LOW_RISE %"] = (
    df_urban_calculation["1_FLOOR"]
    + df_urban_calculation["2_FLOOR"]
    + df_urban_calculation["3_TO_5_FLOOR"]
)
df_urban_calculation["HIGH_RISE %"] = (
    df_urban_calculation["5_TO_10_FLOOR"] + df_urban_calculation["10_FLOOR"]
)
df_urban_calculation["LOW_RISE"] = (
    df_urban_calculation["NEW_HOUSEHOLDS"] * df_urban_calculation["LOW_RISE %"]
) / 100
df_urban_calculation["HIGH_RISE"] = (
    df_urban_calculation["NEW_HOUSEHOLDS"] * df_urban_calculation["HIGH_RISE %"]
) / 100
df_urban_calculation = df_urban_calculation[
    [
        "STATE",
        "DISTRICT",
        "POPULATION_2022",
        "POPULATION_2011",
        "IN_%_2011 to URBAN_%",
        "POPULATION_2021",
        "URBAN_POPULATION_2011",
        "RURAL_GROWTH_RATE",
        "URBAN_GROWTH_RATE",
        "ANNUAL_URBANIZATION_RATE",
        "NEW_URBAN_POPULATION",
        "URBAN_HOUSEHOLD_SIZE",
        "RURAL_HOUSEHOLD_SIZE",
        "LY_HOUSEHOLDS",
        "NEW_HOUSEHOLDS",
        "LOW_RISE %",
        "HIGH_RISE %",
        "LOW_RISE",
        "HIGH_RISE",
    ]
]
average_size_of_flat = pd.read_sql(
    """ select * from etl_zone."DF_AVERAGE_FLAT_SIZE" """, cnxn
)
df_urban_calculation = pd.merge(
    df_urban_calculation, average_size_of_flat, on=["STATE", "DISTRICT"], how="left"
)
df_urban_calculation["FLAT_AREA_LOW_RISE"] = (
    df_urban_calculation["LOW_RISE"] * df_urban_calculation["HOUSEHOLD_SIZE_URBAN"]
)
df_urban_calculation["FLAT_AREA_HIGH_RISE"] = (
    df_urban_calculation["HIGH_RISE"] * df_urban_calculation["HOUSEHOLD_SIZE_URBAN"]
)
df_cemnet_consumption_per_sq_ft = pd.read_sql(
    """ select * from etl_zone."DF_CEMENT_CONSUMPTION_PER_SQ_FT" """, cnxn
)
df_urban_calculation = pd.merge(
    df_urban_calculation,
    df_cemnet_consumption_per_sq_ft,
    on=["STATE", "DISTRICT"],
    how="left",
)
df_urban_calculation["CONSUMPTION_OF_CEMENT_LOW_RISE"] = (
    df_urban_calculation["FLAT_AREA_LOW_RISE"]
    * df_urban_calculation["LOW_RISE_CEMENT_CONSUMPTION"]
)
df_urban_calculation["CONSUMPTION_OF_CEMENT_HIGH_RISE"] = (
    df_urban_calculation["FLAT_AREA_HIGH_RISE"]
    * df_urban_calculation["HIGH_RISE_CEMENT_CONSUMPTION"]
)
df_urban_calculation["TOTAL_CONSUMPTION_OF_CEMENT"] = (
    df_urban_calculation["CONSUMPTION_OF_CEMENT_LOW_RISE"]
    + df_urban_calculation["CONSUMPTION_OF_CEMENT_HIGH_RISE"]
)
df_reconstruction_percentage = pd.read_sql(
    """ Select * from etl_zone."DF_RECONSTRUCTION_PERCENTAGE" """, cnxn
)
df_urban_calculation = pd.merge(
    df_urban_calculation,
    df_reconstruction_percentage,
    on=["STATE", "DISTRICT"],
    how="left",
)
df_urban_calculation["RECONSTRUCTION_CONSUMPTION"] = (
    df_urban_calculation["TOTAL_CONSUMPTION_OF_CEMENT"]
    * df_urban_calculation["RECONSTRUCTION_PERCENTAGE_URBAN"]
)  # Change name to Reconstruction Consumption
df_urban_calculation["URBAN_FINAL_CONSUMPTION"] = (
    df_urban_calculation["TOTAL_CONSUMPTION_OF_CEMENT"]
    + df_urban_calculation["RECONSTRUCTION_CONSUMPTION"]
)  # Change name to Urban Final Consumption
for state in df_urban_calculation["STATE"].unique():
    df_urban_calculation["URBAN_TOTAL_CEMENT_DEMAND"] = df_urban_calculation.loc[
        df_urban_calculation["STATE"] == state, "URBAN_FINAL_CONSUMPTION"
    ]
    df_urban_calculation.loc[
        df_urban_calculation["STATE"] == state, "FINAL_URBAN_DEMAND"
    ] = df_urban_calculation["URBAN_TOTAL_CEMENT_DEMAND"].sum()
df_urban_calculation = df_urban_calculation.groupby(["STATE"], as_index=False)[
    "FINAL_URBAN_DEMAND"
].mean()
df_urban_calculation.at[7, "STATE"] = "Dadra and Nagar Haveli"
df_urban_calculation.at[8, "STATE"] = "Daman and Diu"


# ("-------------------------------------RURAL CALCULATION----------------------------------")
df_rural_calculation = pd.read_sql(
    """ select * from etl_zone."DF_RURAL_POPULATION_2011" """, cnxn
)
df_rural_calculation["STATE"] = df_rural_calculation["STATE"].replace(
    {
        "Dadra and Nagar Haveli\xa0": "Dadra and Nagar Haveli",
        "Daman and diu": "Daman and Diu",
        "Jammu kashmer": "Jammu Kashmir",
        "Maharashtra\xa0": "Maharashtra",
        "Telangana\xa0": "Telangana",
    }
)
df_kacha_house_percentage = pd.read_sql(
    """ Select * from etl_zone."DF_KACHA_HOUSE_PERCENTAGE" """, cnxn
)
df_rural_calculation = pd.merge(df_rural_calculation, df_rate, on=["STATE"], how="left")

df_rural_calculation = pd.merge(
    df_rural_calculation, df_kacha_house_percentage, on="STATE", how="left"
)
df_rural_calculation["POPULATION_OF_2022"] = df_rural_calculation[
    "RURAL_POPULATION_OF_2011"
] * pow((1 + df_rural_calculation["RURAL_GROWTH_RATE"]), 11)
df_rural_calculation["CHANGE_POPULATION_2022"] = (
    df_rural_calculation["POPULATION_OF_2022"]
    * df_rural_calculation["RURAL_GROWTH_RATE"]
)
df_kacha_pakka_conversation_rate = pd.read_sql(
    """Select * from etl_zone."DF_KACHA_PAKKA_CONVERSION_RATE" """, cnxn
)
df_rural_calculation["STATE"] = df_rural_calculation["STATE"].replace(
    {
        "Dadra and Nagar Haveli\xa0": "Dadra and Nagar Haveli",
        "Daman and diu": "Daman and Diu",
        "Jammu kashmer": "Jammu Kashmir",
        "Maharashtra\xa0": "Maharashtra",
        "Telangana\xa0": "Telangana",
    }
)

df_rural_calculation = pd.merge(
    df_rural_calculation,
    df_kacha_pakka_conversation_rate,
    on=["STATE", "DISTRICT"],
    how="left",
)
df_rural_calculation["STATE"] = df_rural_calculation["STATE"].replace(
    {
        "Dadra and Nagar HaveliÂ ": "Dadra and Nagar Haveli",
        "Daman and diu": "Daman and Diu",
        "Jammu kashmer": "Jammu Kashmir",
        "MaharashtraÂ ": "Maharashtra",
        "TelanganaÂ ": "Telangana",
    }
)


df_rural_calculation["CURRENT KACHA + PAKKA HOUSEHOLDS"] = (
    df_rural_calculation["POPULATION_OF_2022"]
    / df_urban_rural_household["RURAL_HOUSEHOLD_SIZE"]
)
df_rural_calculation = df_rural_calculation[
    [
        "STATE",
        "DISTRICT",
        "RURAL_POPULATION_OF_2011",
        "RURAL_GROWTH_RATE",
        "KACHA_HOUSEHOLD_%",
        "POPULATION_OF_2022",
        "CHANGE_POPULATION_2022",
        "KACHA_PAKKA_CONVERSION_RATE",
        "CURRENT KACHA + PAKKA HOUSEHOLDS",
    ]
]
df_rural_calculation["NEW_HOUSEHOLD"] = (
    df_rural_calculation["POPULATION_OF_2022"]
    * df_rural_calculation["RURAL_GROWTH_RATE"]
    * (1 - df_rural_calculation["KACHA_HOUSEHOLD_%"])
) / df_urban_rural_household[
    "RURAL_HOUSEHOLD_SIZE"
]  # WILL DISCUSS WITH ANSHUL EACH AND EVERY COLUMNS and also discuss the differences as well
df_rural_calculation["KACHA_HOUSEHOLD"] = (
    df_rural_calculation["CURRENT KACHA + PAKKA HOUSEHOLDS"]
    * df_rural_calculation["KACHA_HOUSEHOLD_%"]
)
df_rural_calculation["NEW_PAKKA_HOUSEHOLDS"] = (
    df_rural_calculation["KACHA_HOUSEHOLD"]
    * df_rural_calculation["KACHA_PAKKA_CONVERSION_RATE"]
)
df_rural_calculation["TOTAL_HOUSEHOLD"] = (
    df_rural_calculation["NEW_PAKKA_HOUSEHOLDS"] + df_rural_calculation["NEW_HOUSEHOLD"]
)
df_rural_calculation = pd.merge(
    df_rural_calculation, average_size_of_flat, on=["STATE", "DISTRICT"], how="left"
)
df_rural_calculation = pd.merge(
    df_rural_calculation, df_cemnet_consumption_per_sq_ft, on="DISTRICT", how="left"
)
df_rural_calculation = df_rural_calculation.drop(["STATE_x", "STATE_y"], axis=1)
df_rural_calculation["CONSUMPTION_PER_HOUSEHOLD_KG"] = (
    df_rural_calculation["HOUSEHOLD_SIZE_RURAL"]
    * df_rural_calculation["LOW_RISE_CEMENT_CONSUMPTION"]
)
df_rural_calculation = pd.merge(
    df_rural_calculation, df_reconstruction_percentage, on="DISTRICT", how="left"
)
df_rural_calculation["DEMAND"] = (
    df_rural_calculation["CONSUMPTION_PER_HOUSEHOLD_KG"]
    * df_rural_calculation["TOTAL_HOUSEHOLD"]
)
df_rural_calculation["RECONSTRUCTION_CONSUMPTION"] = (
    df_rural_calculation["DEMAND"]
    * df_rural_calculation["RECONSTRUCTION_PERCENTAGE_RURAL"]
)
df_rural_calculation["TOTAL_DEMAND"] = (
    df_rural_calculation["DEMAND"] + df_rural_calculation["RECONSTRUCTION_CONSUMPTION"]
)
for state in df_rural_calculation["STATE"].unique():
    df_rural_calculation["RURAL_TOTAL_CEMENT_DEMAND"] = df_rural_calculation.loc[
        df_rural_calculation["STATE"] == state, "TOTAL_DEMAND"
    ]
    df_rural_calculation.loc[
        df_rural_calculation["STATE"] == state, "FINAL_RURAL_DEMAND"
    ] = df_rural_calculation["RURAL_TOTAL_CEMENT_DEMAND"].sum()
df_rural_calculation = df_rural_calculation.groupby(["STATE"], as_index=False)[
    "FINAL_RURAL_DEMAND"
].mean()
# ("------------------------Infra Demand-------------------------------------------------------------")
df_infra_calculation = pd.read_sql(
    """ select * from etl_zone."DF_PROJECT_DATABASE" """, cnxn
)
df_infra_calculation["CEMENT_DEMAND"] = (
    df_infra_calculation["CEMENT_VALUE_AS_PERCENTAGE_OF_COST"]
    * df_infra_calculation["COST"]
)
df_infra_calculation["ANNUAL_CEMENT_VAL"] = (
    df_infra_calculation["CEMENT_DEMAND"] / df_infra_calculation["DURATION"]
)
df_infra_calculation["TOTAL_CEMENT_DEMAND"] = (
    (df_infra_calculation["ANNUAL_CEMENT_VAL"] / 300) * 50 * 0.001 * 10000000
)  # kg to MT
for state in df_infra_calculation["STATE"].unique():
    df_infra_calculation["INFRA_TOTAL_CEMENT_DEMAND"] = df_infra_calculation.loc[
        df_infra_calculation["STATE"] == state, "TOTAL_CEMENT_DEMAND"
    ]
    df_infra_calculation.loc[
        df_infra_calculation["STATE"] == state, "FINAL_INFRA_DEMAND"
    ] = df_infra_calculation["INFRA_TOTAL_CEMENT_DEMAND"].sum()
df_infra_calculation = df_infra_calculation.groupby(["STATE"], as_index=False)[
    "FINAL_INFRA_DEMAND"
].mean()
df_infra_calculation.at[0, "STATE"] = "Andaman & Nicobar Islands"
df_infra_calculation.at[15, "STATE"] = "Maharashtra"
df_infra_calculation.at[26, "STATE"] = "Telangana"
df_infra_calculation.at[30, "STATE"] = "West Bengal"
print("-----------------------Macro_Analysis_Output-----------------------------------")
df_macro_output = pd.merge(
    df_urban_calculation, df_rural_calculation, on="STATE", how="left"
)
df_macro_output["RESIDENTIAL_DEMAND"] = (
    df_macro_output["FINAL_URBAN_DEMAND"] + df_macro_output["FINAL_RURAL_DEMAND"]
) / 1000

df_macro_output = pd.merge(
    df_macro_output, df_infra_calculation, on="STATE", how="left"
).fillna(
    0
)  # will ask to anshul regarding 0 value instead of nan value. is it ok?
df_macro_output["TOTAL_DEMAND_VALUE"] = (
    df_macro_output["RESIDENTIAL_DEMAND"] + df_macro_output["FINAL_INFRA_DEMAND"]
) / 0.9  # MATHEMATICAL CALCULATION,will discuss with anshul regarding commercial demand why in commercial column divided by 70?
df_seasonality = pd.read_sql(
    """ select * from etl_zone."DF_SEASONALITY_DEMAND" """, cnxn
)
df_seasonality["STATE"] = df_seasonality["STATE"].replace(
    {
        "chandigarh": "Chandigarh",
        "Chattisgarh": "Chhattisgarh",
        "Jammu & Kashmir": "Jammu Kashmir",
        "Karnataka": "karnataka",
        "Odisha": "Orissa",
        "Uttranchal": "Uttarakhand",
    }
)
df_desired_market_share = pd.read_sql(
    """ select * from etl_zone."DF_DESIRED_MARKET_SHARE" """, cnxn
)
df_desired_market_share["STATE"] = df_desired_market_share["STATE"].replace(
    {
        "Dadra and Nagar Haveli\xa0": "Dadra and Nagar Haveli",
        "Maharashtra\xa0": "Maharashtra",
        "Telangana\xa0": "Telangana",
        "West Bengal\xa0": "West Bengal",
        "Andaman & Nicobar Islands\xa0": "Andaman & Nicobar Islands",
    }
)

df_geographical_presence = pd.read_sql(
    """select * from etl_zone."DF_GEOGRAPHICAL_PRESENCE" """, cnxn
)
df_geographical_presence["STATE"] = df_geographical_presence["STATE"].replace(
    {
        "Dadra and Nagar Haveli\xa0": "Dadra and Nagar Haveli",
        "Maharashtra\xa0": "Maharashtra",
        "Telangana\xa0": "Telangana",
        "West Bengal\xa0": "West Bengal",
        "Andaman & Nicobar Islands\xa0": "Andaman & Nicobar Islands",
    }
)
df_seasonality = pd.merge(
    df_seasonality, df_desired_market_share, on="STATE", how="left"
)
df_seasonality = pd.merge(
    df_seasonality, df_geographical_presence, on="STATE", how="left"
)
df_macro_output = pd.merge(df_seasonality, df_macro_output, on="STATE", how="left")

df_macro_output["STATE_TARGET"] = (
    df_macro_output["TOTAL_DEMAND_VALUE"]
    * df_macro_output["DESIRED_MARKET_SHARE"]
    * df_macro_output["DESIRED_MARKET_SHARE"]
)
df_macro_output["FINAL_RESULT"] = df_macro_output["STATE_TARGET"] * (
    df_macro_output["PERCENTAGE"] / 100
)
df_macro_output["INVOICE_DATE_MONTH"] = df_macro_output["INVOICE_DATE_MONTH"].replace(
    {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    }
)
df_macro_output["ORG_ID"] = df_macro_output["ORG_ID"].replace(
    {102: "SHREE", 103: "BANGUR", 104: "ROCKSTRONG"}
)
df_macro_output.drop(
    df_macro_output[df_macro_output["ORG_ID"] == 101].index, inplace=True
)
df_macro_output["INDIVIDUAL_STATE_PERCENTAGE"] = df_macro_output["PERCENTAGE"]
df_macro_output["BRAND"] = df_macro_output["ORG_ID"]
df_macro_output["INVOICE_MONTH"] = df_macro_output["INVOICE_DATE_MONTH"]
df_macro_output["FINAL_DEMAND"] = df_macro_output["FINAL_RESULT"]
df_macro_output["DATE"] = df_macro_output["INVOICE_DATE_MONTH"]
df_macro_output["DATE"] = df_macro_output["DATE"].replace(
    {
        "JAN": "01-01-2023",
        "FEB": "01-02-2023",
        "MAR": "01-03-2023",
        "APR": "01-04-2022",
        "MAY": "01-05-2022",
        "JUN": "01-06-2022",
        "JUL": "01-07-2022",
        "AUG": "01-08-2022",
        "SEP": "01-09-2022",
        "OCT": "01-10-2022",
        "NOV": "01-11-2022",
        "DEC": "01-12-2022",
    }
)

df_macro_output = df_macro_output[
    [
        "STATE",
        "BRAND",
        "INVOICE_MONTH",
        "STATE_TARGET",
        "INDIVIDUAL_STATE_PERCENTAGE",
        "FINAL_DEMAND",
        "DATE",
    ]
]
print(df_macro_output)
print("insert_part")


def execute_values(cnxn, df_macro_output, DF_MACRO_OUTPUT_FINAL):
    print(df_macro_output.columns)
    tuples = [tuple(x) for x in df_macro_output.to_numpy()]
    col = " "
    for i in list(df_macro_output.columns):
        col += '"{0}"'.format(i) + ","
    col = col.strip(",")
    query = "INSERT INTO %s(%s) VALUES %%s" % ('etl_zone."DF_MACRO_OUTPUT_FINAL"', col)
    cursor = cnxn.cursor()

    try:
        extras.execute_values(cursor, query, tuples)
        cnxn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cnxn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


# df_macro_output.to_csv("DF_MACRO_OUTPUT_FINAL.csv")
execute_values(cnxn, df_macro_output, "DF_MACRO_OUTPUT_FINAL")
