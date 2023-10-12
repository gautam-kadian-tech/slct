import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
from datetime import datetime as dt

import psycopg2
import psycopg2.extras as extras
from dateutil.relativedelta import relativedelta as rd
from django.conf import settings

from .connection import connect_db


def no_of_month_active_in_a_year(df):
    if df.NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTHS >= 5:
        return 3
    elif (df.NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTHS >= 3) and (
        df.NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTHS < 5
    ):
        return 2
    else:
        return 1


def premium_product_share(df):
    if df.PREMIUM_PRODUCT_SHARE > 0.70:
        return 3
    elif (df.PREMIUM_PRODUCT_SHARE > 0.40) and (df.PREMIUM_PRODUCT_SHARE <= 0.70):
        return 2
    else:
        return 1


def get_category(df):
    if df.TOTAL_SCORE >= 2.5:
        return "A"
    elif (df.TOTAL_SCORE >= 1.5) and (df.TOTAL_SCORE < 2.5):
        return "B"
    else:
        return "C"


class InfluencerCheckHelper:
    def run_model_free(
        cnxn,
        state,
        district,
        technical_activity_type,
        total_budget,
        budget_per_head,
        average_no_influencers,
        free_run,
    ):
        # database connection

        # Input file
        # data_new_main = pd.read_excel('input_1_16_march.xlsx')
        data_new_main = pd.read_sql(
            f"""
            select * from etl_zone."INFLUENCER_MEET_MAIN_INPUT_FILE"
            where "STATE" = '{state}'
            and "DISTRICT" = '{district}'
        """,
            cnxn,
        )
        data_new_main["CURRENT_STATUS_(ACTIVE/INACTIVE)"] = data_new_main[
            "CURRENT_STATUS_(ACTIVE/INACTIVE)"
        ].str.capitalize()
        # data_new_main['DATE']=
        # meet_details = pd.read_excel('input_2_16_march.xlsx')
        # meet_details=pd.read_sql(f'''
        #     select * from etl_zone."INFLUENCER_MEET_ATTENDEE_INPUT"
        #     where "STATE" = '{state}'
        #     and "DISTRICT" = '{district}'
        #     ''',cnxn)
        meet_details_col = [
            "STATE",
            "DISTRICT",
            "TECHNICAL_ACTIVITY_TYPE",
            "AVG_ATTENDEES_PER_MEETING",
            "MIN_A",
            "MIN_B",
            "MIN_C",
            "BUDEGET_PER_HEAD",
        ]
        meet_details_data = [
            [
                state,
                district,
                technical_activity_type,
                average_no_influencers,
                2,
                1,
                1,
                budget_per_head,
            ]
        ]
        meet_details = pd.DataFrame(columns=meet_details_col, data=meet_details_data)
        # technical_activity_plan=pd.read_excel('TECHNICAL_COMPOSITION.xlsx')
        technical_activity_plan = pd.read_sql(
            f"""
            select * from etl_zone."INFLUENCER_TECH_ACTIVITY_MASTER"
            where "TECHNICAL_ACTIVITY_TYPE" = '{technical_activity_type}' """,
            cnxn,
        )

        data_new_main = data_new_main.merge(
            meet_details, how="left", on=["STATE", "DISTRICT"]
        )

        if len(data_new_main) == 0:
            return pd.DataFrame(), pd.DataFrame()

        data_new_main = data_new_main[
            [
                "STATE",
                "DISTRICT",
                "INFLUENCER_CODE",
                "INFLUENCER_NAME",
                "INFLUENCER_TYPE",
                "LIFTING_PREVIOUS_MONTH_(MT)",
                "CURRENT_STATUS_(ACTIVE/INACTIVE)",
                "NO_OF_SITE_USING_OUR_BRAND",
                "NO_OF_SITES_RUNNING_CURRENTLY",
                "TOTAL_VOLUME_LIFTED_TILL_DATE",
                "NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTHS",
                "PREMIUM_PRODUCT_SHARE",
                "INFLUENCER_POTENTIAL",
                "TIMES_ATTENDED_LAST_MONTH",
                "TECHNICAL_ACTIVITY_TYPE",
            ]
        ]
        data_new = (
            data_new_main.copy()
        )  # creating new dataframe for calculations of all parameters score
        data_new["PARAMETER_1"] = (
            data_new["NO_OF_SITE_USING_OUR_BRAND"]
            / data_new["NO_OF_SITES_RUNNING_CURRENTLY"]
        )
        districts = data_new.DISTRICT.unique()  # unique districts
        influencers = data_new.INFLUENCER_TYPE.unique()  # unique influencers
        final_data_base = pd.DataFrame()  # empty dataframe
        for district in districts:
            for influencer in influencers:
                data = data_new.loc[
                    (data_new.DISTRICT == district)
                    & (data_new.INFLUENCER_TYPE == influencer)
                ]
                parameter_1_50 = data.PARAMETER_1.quantile(0.5)
                parameter_1_20 = data.PARAMETER_1.quantile(0.8)
                parameter_1_30 = data.PARAMETER_1.quantile(0.3)
                conditions = [
                    (data.PARAMETER_1 >= parameter_1_20),
                    (data.PARAMETER_1 >= parameter_1_50)
                    & (data.PARAMETER_1 < parameter_1_20),
                    (data.PARAMETER_1 < parameter_1_50)
                    & (data.PARAMETER_1 >= parameter_1_30),
                    (data.PARAMETER_1 < parameter_1_30),
                ]
                values = [3, 2, 1, 0]
                data["PARAMETER_1_SCORE"] = np.select(conditions, values)

                volume_lifted_till_date_50 = (
                    data.TOTAL_VOLUME_LIFTED_TILL_DATE.quantile(0.5)
                )
                volume_lifted_till_date_20 = (
                    data.TOTAL_VOLUME_LIFTED_TILL_DATE.quantile(0.8)
                )
                volume_lifted_till_date_30 = (
                    data.TOTAL_VOLUME_LIFTED_TILL_DATE.quantile(0.3)
                )

                conditions = [
                    (data.TOTAL_VOLUME_LIFTED_TILL_DATE >= volume_lifted_till_date_20),
                    (data.TOTAL_VOLUME_LIFTED_TILL_DATE >= volume_lifted_till_date_50)
                    & (data.TOTAL_VOLUME_LIFTED_TILL_DATE < volume_lifted_till_date_20),
                    (data.TOTAL_VOLUME_LIFTED_TILL_DATE < volume_lifted_till_date_50)
                    & (
                        data.TOTAL_VOLUME_LIFTED_TILL_DATE >= volume_lifted_till_date_30
                    ),
                    (data.TOTAL_VOLUME_LIFTED_TILL_DATE < volume_lifted_till_date_30),
                ]
                values = [3, 2, 1, 0]

                data["TOTAL_VOLUME_LIFTED_TILL_DATE_SCORE"] = np.select(
                    conditions, values
                )
                data["NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTH_SCORE"] = data.apply(
                    no_of_month_active_in_a_year, axis=1
                )
                data["PREMIUM_PRODUCT_SHARE_SCORE"] = data.apply(
                    premium_product_share, axis=1
                )

                influencer_pot_50 = data.INFLUENCER_POTENTIAL.quantile(0.5)
                influencer_pot_20 = data.INFLUENCER_POTENTIAL.quantile(0.8)
                influencer_pot_30 = data.INFLUENCER_POTENTIAL.quantile(0.3)

                conditions = [
                    (data.INFLUENCER_POTENTIAL >= influencer_pot_20),
                    (data.INFLUENCER_POTENTIAL >= influencer_pot_50)
                    & (data.INFLUENCER_POTENTIAL < influencer_pot_20),
                    (data.INFLUENCER_POTENTIAL < influencer_pot_50)
                    & (data.INFLUENCER_POTENTIAL >= influencer_pot_30),
                    (data.INFLUENCER_POTENTIAL < influencer_pot_30),
                ]
                values = [3, 2, 1, 0]
                data["INFLUENCER_POTENTIAL_SCORE"] = np.select(conditions, values)
                data.loc[
                    data["INFLUENCER_POTENTIAL"] == 0, "INFLUENCER_POTENTIAL_SCORE"
                ] = 0

                final_data_base = final_data_base.append(data, ignore_index=True)
                # data_inactive = data_new.loc[(data_new.DISTRICT == district) & (data_new.INFLUENCER_TYPE == influencer) & (data_new['CURRENT_STATUS_(ACTIVE/INACTIVE)']=='Inactive')]
                # final_data_base = final_data_base.append(data_inactive, ignore_index=True)

        final_data_base["TOTAL_SCORE"] = (
            0.1 * final_data_base["PARAMETER_1_SCORE"]
            + 0.3 * final_data_base["TOTAL_VOLUME_LIFTED_TILL_DATE_SCORE"]
            + 0.1 * final_data_base["NO_OF_MONTHS_ACTIVE_IN_LAST_6_MONTH_SCORE"]
            + 0.4 * final_data_base["PREMIUM_PRODUCT_SHARE_SCORE"]
            + 0.1 * final_data_base["INFLUENCER_POTENTIAL_SCORE"]
        )
        final_data_base["SCORE_CATEGORY"] = final_data_base.apply(get_category, axis=1)
        final_data_base = final_data_base.loc[
            ~(
                (final_data_base["CURRENT_STATUS_(ACTIVE/INACTIVE)"] == "Active")
                & (final_data_base["TOTAL_SCORE"] == "inactive")
            )
        ]

        # score category and total score shoulde be inactive for inactive cases
        for i in range(0, len(final_data_base)):
            if final_data_base["CURRENT_STATUS_(ACTIVE/INACTIVE)"][i] == "Inactive":
                final_data_base["SCORE_CATEGORY"][i] = "Inactive"
                final_data_base["TOTAL_SCORE"][i] = final_data_base[
                    "TOTAL_VOLUME_LIFTED_TILL_DATE"
                ][i]
        final_data_base["TOTAL_SCORE"] = final_data_base["TOTAL_SCORE"].fillna(0)
        # print("final_data_base",final_data_base)#final data base created main file with all active and inactive dealer and it's score
        # final_data_base.to_csv("final_db.csv")
        # print(final_data_base[final_data_base['DISTRICT']=='FARIDABAD'])

        # here new_df_final_product includes remove in active dealer and calculate the active dealer list
        new_df_final_product = final_data_base.copy()
        # new_df_final_product=final_data_base[(final_data_base['DISTRICT']=='MAINPURI')]
        # new_df_final_product=final_data_base[(final_data_base['DISTRICT']==district)]
        # print(new_df_final_product)

        # print(new_df_final_product)
        final_data = pd.DataFrame()
        meet_det_join_final = pd.DataFrame()
        for district in new_df_final_product["DISTRICT"].unique():
            # for influencer_type in new_df_final_product['INFLUENCER_TYPE'].unique():
            new_df_final_product_new = new_df_final_product[
                (new_df_final_product["DISTRICT"] == district)
            ]
            # new_df_final_product_new=(new_df_final_product[(new_df_final_product['INFLUENCER_TYPE']==influencer_type)])
            final_dataframe = pd.merge(
                new_df_final_product_new,
                technical_activity_plan,
                on=["TECHNICAL_ACTIVITY_TYPE", "INFLUENCER_TYPE"],
                how="inner",
            )
            # print(final_dataframe)
            # print(final_dataframe.columns)

            # final_dataframe includes merging both file
            # final_dataframe.to_csv('final_dataframe.csv')
            cat_count = final_dataframe.groupby(
                ["DISTRICT", "SCORE_CATEGORY"], as_index=False
            )["INFLUENCER_CODE"].count()
            cat_count = cat_count.pivot_table(
                "INFLUENCER_CODE", "DISTRICT", "SCORE_CATEGORY"
            )
            cat_count.reset_index(inplace=True, drop=False)
            if "A" not in cat_count.columns:
                cat_count["A"] = np.NaN
            if "B" not in cat_count.columns:
                cat_count["B"] = np.NaN
            if "C" not in cat_count.columns:
                cat_count["C"] = np.NaN
            cat_count.fillna(0, inplace=True)
            meet_det_join = meet_details.merge(cat_count, on="DISTRICT")

            final_dataframe = final_dataframe.merge(
                meet_det_join[["STATE", "DISTRICT", "MIN_A", "MIN_B", "MIN_C"]],
                on=["STATE", "DISTRICT"],
            )
            final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "A", "TIMES_ATTENDED_LAST_MONTH"
            ] = final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "A",
                ["TIMES_ATTENDED_LAST_MONTH", "MIN_A"],
            ].min(
                axis=1
            )
            final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "B", "TIMES_ATTENDED_LAST_MONTH"
            ] = final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "B",
                ["TIMES_ATTENDED_LAST_MONTH", "MIN_A"],
            ].min(
                axis=1
            )
            final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "C", "TIMES_ATTENDED_LAST_MONTH"
            ] = final_dataframe.loc[
                final_dataframe["SCORE_CATEGORY"] == "C",
                ["TIMES_ATTENDED_LAST_MONTH", "MIN_A"],
            ].min(
                axis=1
            )
            # meet_det_join.to_csv('meet_det_join_29_march_check.csv')

            meet_det_join["meetings_A"] = meet_det_join["A"] * meet_det_join["MIN_A"]
            meet_det_join["meetings_B"] = meet_det_join["B"] * meet_det_join["MIN_B"]
            meet_det_join["meetings_C"] = meet_det_join["C"] * meet_det_join["MIN_C"]
            meet_det_join["TOTAL_MEETING"] = (
                meet_det_join["meetings_A"]
                + meet_det_join["meetings_B"]
                + meet_det_join["meetings_C"]
            )
            meet_det_join["NO_MEETINGS"] = meet_det_join["TOTAL_MEETING"] / (
                meet_det_join["AVG_ATTENDEES_PER_MEETING"] * 0.6
            )
            meet_det_join["TOTAL_BUDGET"] = (
                np.ceil(meet_det_join["NO_MEETINGS"])
                * meet_det_join["BUDEGET_PER_HEAD"]
                * meet_det_join["AVG_ATTENDEES_PER_MEETING"]
            )
            if free_run == True:
                meet_det_join["NO_MEETINGS"] = np.ceil(meet_det_join["NO_MEETINGS"])
                meet_det_join["ATTENDEES_PER_MEETING"] = np.ceil(
                    meet_det_join["AVG_ATTENDEES_PER_MEETING"] * 1.2
                )  # 120
            else:
                meet_det_join["NO_MEETINGS"] = total_budget / (
                    budget_per_head * average_no_influencers
                )
                meet_det_join["ATTENDEES_PER_MEETING"] = np.ceil(
                    average_no_influencers * 1.2
                )  # 120

            meet_det_join["INACTIVE_ATTENDEE"] = np.ceil(
                meet_det_join["ATTENDEES_PER_MEETING"] * 0.40
            )  # WILL DISCUSS WITH RASHI WHICH INACTIVE 48
            meet_det_join["CAT_A_ATTENDEE"] = np.ceil(
                meet_det_join["ATTENDEES_PER_MEETING"] * 0.25
            )
            meet_det_join["CAT_B_ATTENDEE"] = np.ceil(
                meet_det_join["ATTENDEES_PER_MEETING"] * 0.20
            )
            meet_det_join["CAT_C_ATTENDEE"] = np.ceil(
                meet_det_join["ATTENDEES_PER_MEETING"] * 0.15
            )
            # print(meet_det_join) #works fine
            # meet_det_join.to_csv('meet_det_join_29_march.csv')

            # print("final_dataframe",final_dataframe) # works fine

            # setting up invitations
            final_data = final_data.append(final_dataframe, ignore_index=True)
            meet_det_join_final = meet_det_join_final.append(
                meet_det_join, ignore_index=False
            )

        final_data["INVITED"] = 0
        final_data["MEETINGS_INVITED"] = ""
        final_data.sort_values(
            ["DISTRICT", "INFLUENCER_TYPE", "TOTAL_SCORE", "INVITED"],
            ascending=[True, True, False, True],
            inplace=True,
        )

        meet_det_join = meet_det_join_final.copy()

        districts = meet_det_join.DISTRICT.unique()
        influencer_type = final_data.INFLUENCER_TYPE.unique()
        new_data = pd.DataFrame()
        # print(technical_activity_plan)
        for district in districts:
            for influencer in final_data[(final_data.DISTRICT == district)][
                "INFLUENCER_TYPE"
            ].unique():
                district_df = final_data[
                    (final_data.DISTRICT == district)
                    & (final_data["INFLUENCER_TYPE"] == influencer)
                ]

                meet_district_count = meet_det_join[
                    meet_det_join.DISTRICT == district
                ].reset_index(drop=True)
                # print(district_df['TECHNICAL_ACTIVITY_TYPE'])
                # print(meet_district_count)

                tc_comp = technical_activity_plan.loc[
                    (
                        technical_activity_plan["TECHNICAL_ACTIVITY_TYPE"]
                        == district_df["TECHNICAL_ACTIVITY_TYPE"].iloc[0]
                    )
                    & (
                        technical_activity_plan["INFLUENCER_TYPE"]
                        == district_df["INFLUENCER_TYPE"].iloc[0]
                    ),
                    "COMPOSITION",
                ].item()

                cat_a = int(meet_district_count.loc[0, "CAT_A_ATTENDEE"]) * tc_comp
                cat_b = int(meet_district_count.loc[0, "CAT_B_ATTENDEE"]) * tc_comp
                cat_c = int(meet_district_count.loc[0, "CAT_C_ATTENDEE"]) * tc_comp

                meetings = int(meet_district_count.loc[0, "NO_MEETINGS"])
                inactive_attendee = (
                    int(meet_district_count.loc[0, "INACTIVE_ATTENDEE"]) * tc_comp
                )

                # print(district_df.iloc[0]['concat_new'])
                # print(cat_a,cat_b,cat_c)

                inactive_attendee = int(np.ceil(inactive_attendee))
                cat_a = int(np.ceil(cat_a))
                cat_b = int(np.ceil(cat_b))
                cat_c = int(np.ceil(cat_c))
                # print(cat_a,cat_b,cat_c)

                district_df["MEETINGS_INVITED"] = ""
                # final_data['MEETINGS_INVITED']=''
                influencer_type = district_df["INFLUENCER_TYPE"].unique()
                # print("final_data",final_data)

                # final_data.to_csv('final_data_10_april.csv')# works perfect
                # meet_district_count.to_csv('meet_det_join_11_april.csv')

                for i in range(meetings):
                    district_df.sort_values(
                        ["DISTRICT", "INVITED", "TOTAL_SCORE"],
                        ascending=[True, True, False],
                        inplace=True,
                    )
                    # print(district_df)
                    idx_upd = district_df.loc[
                        district_df["SCORE_CATEGORY"] == "B"
                    ].head(cat_b)
                    idx_upd = idx_upd.index
                    final_data.loc[idx_upd, "INVITED"] += 1
                    district_df.loc[idx_upd, "INVITED"] += 1
                    final_data.loc[idx_upd, "MEETINGS_INVITED"] += f",{i+1}"

                    idx_upd = district_df.loc[
                        district_df["SCORE_CATEGORY"] == "C"
                    ].head(cat_c)
                    idx_upd = idx_upd.index
                    final_data.loc[idx_upd, "INVITED"] += 1
                    district_df.loc[idx_upd, "INVITED"] += 1
                    final_data.loc[idx_upd, "MEETINGS_INVITED"] += f",{i+1}"

                    idx_upd = district_df.loc[
                        district_df["SCORE_CATEGORY"] == "A"
                    ].head(cat_a)
                    idx_upd = idx_upd.index
                    final_data.loc[idx_upd, "INVITED"] += 1
                    district_df.loc[idx_upd, "INVITED"] += 1
                    final_data.loc[idx_upd, "MEETINGS_INVITED"] += f",{i+1}"

                    idx_upd = district_df.loc[
                        district_df["SCORE_CATEGORY"] == "Inactive"
                    ].head(inactive_attendee)
                    idx_upd = idx_upd.index
                    final_data.loc[idx_upd, "INVITED"] += 1
                    district_df.loc[idx_upd, "INVITED"] += 1
                    final_data.loc[idx_upd, "MEETINGS_INVITED"] += f",{i+1}"
            # print("last_fd",final_data)
            # new_data = new_data.append(final_data, ignore_index= True)
        # new_data=new_data.drop_duplicates()
        # new_data.to_csv("new_data_29_march.csv")
        # print("new_data",new_data)

        # final_data=final_data[['STATE', 'DISTRICT', 'INFLUENCER_CODE', 'INFLUENCER_NAME',
        #    'INFLUENCER_TYPE', 'LIFTING_PREVIOUS_MONTH_(MT)',
        #    'TOTAL_SCORE', 'SCORE_CATEGORY', 'COMPOSITION', 'INVITED',
        #    'MEETINGS_INVITED']]
        final_data.rename(
            {
                "LIFTING_PREVIOUS_MONTH_(MT)": "LIFTING_PREVIOUS_MONTH_MT",
                "MEETINGS_INVITED": "MEETING_INVITED",
            },
            axis=1,
            inplace=True,
        )
        final_data = final_data[
            [
                "STATE",
                "DISTRICT",
                "INFLUENCER_CODE",
                "INFLUENCER_NAME",
                "INFLUENCER_TYPE",
                "SCORE_CATEGORY",
                "LIFTING_PREVIOUS_MONTH_MT",
                "MEETING_INVITED",
                "INVITED",
                "TECHNICAL_ACTIVITY_TYPE",
            ]
        ]
        final_data["DATE"] = (dt.now() + rd(months=1)).strftime("%Y-%m-01")
        final_data["FREE_RUN"] = free_run

        final_output = pd.DataFrame(columns=final_data.columns.tolist())

        for idx, row in final_data.iterrows():
            if row["INVITED"] == 0:
                final_output.loc[len(final_output)] = row
            else:
                meetings = row["MEETING_INVITED"].strip(",").split(",")
                for met in meetings:
                    id = len(final_output)
                    final_output.loc[id] = row
                    final_output.loc[id, "MEETING_INVITED"] = met
        index_names = final_output[final_output["INVITED"] == 0].index
        final_output.drop(index_names, inplace=True)
        return final_output, meet_det_join

    # if __name__ == '__main__':

    #     cnxn = connect_db()

    #     state="Uttar Pradesh"
    #     district="MAINPURI"
    #     technical_activity_type="Mason Meets"
    #     total_budget=500
    #     budget_per_head=200
    #     average_no_influencers=3
    #     free_run = True

    #     output,no_meeting_value=run_model_free(cnxn,state,district,technical_activity_type,total_budget,budget_per_head,average_no_influencers,free_run)

    #     print(output)
    # output.to_csv('output.csv',index=False)
