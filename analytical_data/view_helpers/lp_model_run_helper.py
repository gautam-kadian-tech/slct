import logging
import time

# from connection import connect_db
import warnings
from datetime import datetime as dt

import numpy as np
import pandas as pd
import psycopg2
import pulp as p
from dateutil.relativedelta import relativedelta as rd
from django.conf import settings

from .connection import connect_db

log = logging.getLogger("lp_model_run_helper")

warnings.filterwarnings("ignore")
cnxn = connect_db()


def get_df_rank(df):
    """
    This function is used to get the ranking of the routes basis contribution.

    Parameters
    -------
    df: Pandas Dataframe
        Combination of all routes at a Brand, Grade, Packaging and Customer Category level.

    Returns
    -------
    df_rank: Pandas Dataframe
        Ranking of the routes at DESTINATION_STATE,DESTINATION_DISTRICT,DESTINATION_CITY,BRAND,GRADE,PACKAGING level.

    """

    df_rank = df.copy()

    df_rank = df_rank.sort_values(
        [
            "TO_CITY_ID",
            "DESTINATION_STATE",
            "DESTINATION_DISTRICT",
            "DESTINATION_CITY",
            "BRAND",
            "GRADE",
            "PACKAGING",
            "contribution",
        ],
        ascending=False,
    )

    df_rank["rank"] = (
        df_rank.groupby(
            [
                "TO_CITY_ID",
                "DESTINATION_STATE",
                "DESTINATION_DISTRICT",
                "DESTINATION_CITY",
                "BRAND",
                "GRADE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        ).cumcount()
        + 1
    )

    return df_rank


class LpModelRunViewHelper:
    cnxn = connect_db()

    def get_model_inputs(cnxn):
        """
        This function returns the combination of all routes at a Brand, Grade, Packaging and Customer Category level
        that is fed into the model as an input.

        Parameters
        ----------
        cnxn: connection
            A valid connection to the database

        Returns
        -------
        df_model: Pandas Dataframe

        """

        sql_ = """
            select
            LM."ROUTE_ID"
            ,LM."ROUTE_ID_SECONDARY"
            ,substring(trim(LM."PLANT"),1,3) as "PLANT_ID"
            ,LM."WAREHOUSE"
            ,LM."FROM_CITY_ID"
            ,LM."NODE_CITY_ID"
            ,ADL."CITY" as "NODE_CITY"
            ,ADL."STATE" as "NODE_STATE"
            ,ADL."DISTRICT" as "NODE_DISTRICT"
            ,ADL."TALUKA" as "NODE_TALUKA"
            ,LM."TO_CITY_ID"
            ,LM."MODE"
            ,LM."DISTANCE"
            ,LM."TYPE"
            ,LM."PRIMARY_SECONDARY_ROUTE"
            ,LM."SOURCE_CITY"
            ,LM."SOURCE_DISTRICT"
            ,LM."SOURCE_STATE"
            ,LM."DESTINATION_CITY"
            ,ADL_dest."TALUKA" as "DESTINATION_TALUKA"
            ,LM."DESTINATION_DISTRICT"
            ,LM."DESTINATION_STATE"
            ,LM."AVG_TIME"
            ,LM."CUST_CATEGORY"
            ,LM."PACK_TYPE"
            ,LM."FREIGHT_TYPE"
            ,FM."PRIMARY_FRT"
            ,FM."SECONDARY_FRT"
            ,FM."HANDLING_CHARGES"
            ,FM."RAKE_CHARGES"
            ,FM."DEMURRAGE"
            ,FM."DAMAGES"
            ,FM."NOTIONAL_FREIGHT"
            ,PM."BRAND"
            ,PM."GRADE"
            ,pm."PACKAGING"
            ,PM."PRICE"
            ,PM."HA_COMMISSION"
            ,PM."DISCOUNT"
            ,PM."TAXES"
            ,PM."SP_COMMISSION"
            ,PM."ISP_COMMISSION"
            ,PM."MISC_CHARGES"
            ,LM."IS_EX"
            from etl_zone."LINKS_MASTER" LM
            left join (
            select * from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
            where "Active" = 1
            ) ADL on ADL."CITY_ID" = LM."NODE_CITY_ID"
            left join (
            select * from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
            where "Active" = 1
            ) ADL_dest on ADL_dest."CITY_ID" = LM."TO_CITY_ID"
            inner join (
            select * from etl_zone."FREIGHT_MASTER"
            ) FM on FM."LINK_ID" = LM."ID"
            inner join(
            select distinct on ("DESTINATION","CUST_CATEGORY","BRAND","GRADE","PACKAGING")
            "DESTINATION"
            ,case "CUST_CATEGORY"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "CUST_CATEGORY"
            end as "CUST_CATEGORY"
            ,"PACK_TYPE"
            ,"BRAND"
            ,"GRADE"
            ,"PACKAGING"
            ,"PRICE"
            ,"HA_COMMISSION"
            ,"DISCOUNT"
            ,"TAXES"
            ,"SP_COMMISSION"
            ,"ISP_COMMISSION"
            ,"MISC_CHARGES"
            from etl_zone."PRICE_MASTER"
            where "PRICE" != 0
            ) PM on PM."DESTINATION" = LM."TO_CITY_ID"
            and PM."CUST_CATEGORY" = LM."CUST_CATEGORY"
            and PM."PACK_TYPE" = LM."PACK_TYPE"
            where LM."IS_ACTIVE" = True
            order by LM."ROUTE_ID" asc;
        """
        df_model = pd.read_sql(sql_, cnxn)

        print("DATA READ")

        # Ensure there are no null values
        df_model[
            [
                "AVG_TIME",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "HANDLING_CHARGES",
                "RAKE_CHARGES",
                "DEMURRAGE",
                "DAMAGES",
                "PRICE",
                "HA_COMMISSION",
                "DISCOUNT",
                "TAXES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "MISC_CHARGES",
                "NOTIONAL_FREIGHT",
            ]
        ] = df_model[
            [
                "AVG_TIME",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "HANDLING_CHARGES",
                "RAKE_CHARGES",
                "DEMURRAGE",
                "DAMAGES",
                "PRICE",
                "HA_COMMISSION",
                "DISCOUNT",
                "TAXES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "MISC_CHARGES",
                "NOTIONAL_FREIGHT",
            ]
        ].fillna(
            0
        )
        df_model[
            [
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "HANDLING_CHARGES",
                "RAKE_CHARGES",
                "DEMURRAGE",
                "DAMAGES",
                "PRICE",
                "HA_COMMISSION",
                "DISCOUNT",
                "TAXES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "MISC_CHARGES",
                "NOTIONAL_FREIGHT",
            ]
        ] = df_model[
            [
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "HANDLING_CHARGES",
                "RAKE_CHARGES",
                "DEMURRAGE",
                "DAMAGES",
                "PRICE",
                "HA_COMMISSION",
                "DISCOUNT",
                "TAXES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "MISC_CHARGES",
                "NOTIONAL_FREIGHT",
            ]
        ].astype(
            "int"
        )

        # Replicate routes for plants that do not have routes defined but follow the routes of another plant
        df_model_fgs = df_model[df_model["PLANT_ID"] == "FGS"]
        df_model_fgs["PLANT_ID"] = "FGI"
        df_model_fgg = df_model[df_model["PLANT_ID"] == "FGG"]
        df_model_fgg["PLANT_ID"] = "FGF"
        df_model_fgn = df_model[df_model["PLANT_ID"] == "FGR"]
        df_model_fgn["PLANT_ID"] = "FGN"
        df_model = df_model.append(
            df_model_fgs.append(
                df_model_fgg.append(df_model_fgn, ignore_index=True), ignore_index=True
            ),
            ignore_index=True,
        )

        return df_model

    def get_model_constraints(cnxn, plan_date):
        """
        This function returns multiple datasets that are as constraint for the model.

        Parameters
        ----------
        cnxn: connection
            A valid connection to the database

        Returns
        -------
        ppm: Pandas Dataframe
            Plant product master which contains information about the products being made at a plant along with its
            variable production cost and clinker conversion factor wherever applicable.

        dmnd_model: Pandas Dataframe
            The demand for the month at a city level.

        vehicle_avail: Pandas Dataframe
            Vehicle availability constraint to invalidate certain routes from a plant to a city.

        rake_charges: Pandas Dataframe
            Rake charges to be considered for the planning.

        frt_trgt: Pandas Dataframe
            Freight type targets at a district level for target setting constraint.

        fiscal_benefit: Pandas Dataframe
            Fiscal benefit avaiable at applicable plants

        transit_depots: Pandas Dataframe
            A one time master shared by logistics to exclude routes through certain depots. This would gradually be
            removed as the routes are closed in the ERP.

        handling_charges: Pandas Dataframe
            Master for handling charges

        df_depot: Pandas Dataframe
            Master for depots at node city

        df_packaging: Pandas Dataframe
            Master for packaging cost

        sla: Pandas Dataframe
            Master for SLA at city level.

        packer_constraint: Pandas Dataframe
            Packer capacity for plants

        """
        # Reading depot master
        sql_depot = """
        select
        substring("NAME",1,3) as "DEPOT_ID",
        "STATE" as "NODE_STATE",
        "CITY" as "NODE_CITY",
        "DISTRICT" as "NODE_DISTRICT",
        case substring("NAME",1,1)
            when 'B' then '103'
            when 'S' then '102'
            else '104'
        end as "BRAND"
        from etl_zone."GODOWN_MASTER"
        """
        df_depot = pd.read_sql(sql_depot, cnxn)

        # Reading plant product master
        sql_ppm = """
        SELECT
        "PLANT_ID"
        ,"GRADE"
        ,"QUANTITY"*100000 as "QUANTITY"
        ,"VARIABLE_PRODUCTION_COST"
        ,"CLINKER_CF"
        ,"QUANTITY"*100000*"MAX_CAPACITY_PERC" as "MAX_QUANTITY"
        ,"QUANTITY"*100000*"MIN_CAPACITY_PERC" as "MIN_QUANTITY"
        FROM etl_zone."PLANT_PRODUCTS_MASTER" ppm
        left join (
        select * from etl_zone."LP_MIN_CAPACTIY"
        ) lmc on lmc."PLANT" = ppm."PLANT_ID"
        where "VARIABLE_PRODUCTION_COST" != 0;
        """
        ppm = pd.read_sql(sql_ppm, cnxn)
        ppm["QUANTITY"] *= 100000
        ppm = ppm[ppm["VARIABLE_PRODUCTION_COST"] != 0]
        ppm[["QUANTITY", "VARIABLE_PRODUCTION_COST"]] = ppm[
            ["QUANTITY", "VARIABLE_PRODUCTION_COST"]
        ].fillna(0)
        ppm["ppm_id"] = ppm.index

        # Reading demand for the month
        sql_dmnd_model = f"""
        SELECT
        "DESTINATION"
        ,ADL."STATE"
        ,ADL."DISTRICT"
        ,ADL."CITY"
        ,"BRAND"
        ,"GRADE"
        ,"PACK_TYPE"
        ,"PACKAGING"
        ,case "CUST_CATEGORY"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "CUST_CATEGORY"
        end as "CUST_CATEGORY"
        ,cast("DEMAND_QTY" as int)
        FROM etl_zone."DEMAND" D
        inner join (
        select * from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
        where "ACTIVE" = 'Y'
        and "Active" = 1
        ) ADL on ADL."CITY_ID" = D."DESTINATION"
        where "MONTH" = '{plan_date}';
        """
        dmnd_model = pd.read_sql(sql_dmnd_model, cnxn)
        dmnd_model[["DEMAND_QTY"]] = dmnd_model[["DEMAND_QTY"]].fillna(0)
        dmnd_model["CUST_CATEGORY"] = dmnd_model["CUST_CATEGORY"].str.strip()
        dmnd_model = dmnd_model.groupby(
            [
                "DESTINATION",
                "STATE",
                "DISTRICT",
                "CITY",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        )["DEMAND_QTY"].sum()
        dmnd_model["dmnd_id"] = dmnd_model.index

        # Reading vehicle availability constraints
        vehicle_avail = pd.read_sql(
            """select * from etl_zone."VEHICLE_AVAILABILITY" va """, cnxn
        )

        # Reading rake charges for the month
        # The range of invoice date to be specified to read charges for a specific month
        date_prev = (dt.strptime(plan_date, "%Y-%m-%d") - rd(months=3)).strftime(
            "%Y-%m-01"
        )
        rake_charges = pd.read_sql(
            f"""
        select "DESTINATION_DISTRICT", round("RAKE_CHARGES"/"TOTAL_QTY",0) as "RAKE_CHARGES" from
        (
            select "DISTRICT" as "DESTINATION_DISTRICT" ,
            sum("RAKE_CHARGES"*"QUANTITY_INVOICED") as "RAKE_CHARGES",
            sum("QUANTITY_INVOICED") as "TOTAL_QTY"
            from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" tosanact
            where "INVOICE_DATE" >= '2023-05-01'
            and "INVOICE_DATE" < '2023-08-01'
            and "ORG_ID" != '101'
            and "SALES_TYPE" in ('RK','GD-RK')
            and "Active" = 1
            group by "DISTRICT"
        ) as ad
        where "TOTAL_QTY" > 0
        """,
            cnxn,
        )

        # Reading freight type types targets for target setting constraint
        frt_trgt = pd.read_sql(
            """
        select
        "STATE"
        ,"DISTRICT"
        ,"FREIGHT_TYPE"
        ,"TARGET"
        from etl_zone."LP_TARGET_SETTING" lts
        """,
            cnxn,
        )
        frt_trgt.reset_index(inplace=True, drop=True)
        frt_trgt["TARGET_ID"] = frt_trgt.index
        frt_trgt.columns = [
            "DESTINATION_STATE",
            "DESTINATION_DISTRICT",
            "FREIGHT_TYPE",
            "TARGET",
            "TARGET_ID",
        ]

        # Reading fiscal benefits
        fiscal_benefit = pd.read_sql(
            'select "PLANT_ID",cast("FISCAL_BENEFIT" as float)/100 as "FISCAL_BENEFIT" from etl_zone."PLANT_CONSTRAINTS_MASTER"',
            cnxn,
        )

        # Reading transit depots
        # One time master
        # To be phased out
        transit_depots = pd.read_csv(settings.TRANSIT_DEPOTS_CSV_PATH)[
            ["DEPOT CITY", "DEPOT DISTRICT", "DEPOT STATE"]
        ].drop_duplicates()
        transit_depots["DEPOT CITY"] = transit_depots["DEPOT CITY"].str.replace(
            "\(NT\)-", ""
        )
        transit_depots["DEPOT CITY"] = transit_depots["DEPOT CITY"].str.replace(
            "\(TR\)-", ""
        )
        transit_depots["DEPOT CITY"] = transit_depots["DEPOT CITY"].str.strip()

        # reading handling charges
        sql_handling_charges = """
        select
        "DISTRICT"
        ,"TALUKA"
        ,"CITY"
        ,"PACKING"
        ,"FREIGHT_TYPE"
        ,"HA_COMMISSION"
        from etl_zone."RAIL_HANDLING"
        """
        handling_charges = pd.read_sql(sql_handling_charges, cnxn)
        handling_charges.columns = [
            "NODE_DISTRICT",
            "NODE_TALUKA",
            "NODE_CITY",
            "PACKING",
            "FREIGHT_TYPE",
            "HA_COMMISSION",
        ]
        handling_charges = handling_charges.groupby(
            ["NODE_DISTRICT", "NODE_TALUKA", "NODE_CITY", "PACKING", "FREIGHT_TYPE"],
            as_index=False,
        ).mean()

        # Reading packaging charges
        df_packaging = pd.read_sql(
            """
        select
        "BRAND"::varchar,
        "PRODUCT" as "GRADE",
        "PACKAGING",
        "COST" as "PACKAGING_COST"
        from etl_zone."PACKAGING_MASTER"
        """,
            cnxn,
        )

        # Reading SlA master
        sla = pd.read_sql(
            """
            select
            "DESTINATION" as "TO_CITY_ID"
            ,"SLA"::numeric as sla
            from  etl_zone."SERVICE_LEVEL_SLA"
            """,
            cnxn,
        )

        packer_constraint = pd.read_sql(
            """
            SELECT
            "PLANT_ID",
            "PACKER_NO"::int*"PACKER_CAPACITY"::int*30 as "PACKER_QTY",
            "TRUCK_LOADER_NO"::int*"TL_RATED_OUTPUT"::int*30 as "TL_QTY"
            from etl_zone."PACKER_CONSTRAINTS_MASTER" pcm
            """,
            cnxn,
        )

        return (
            ppm,
            dmnd_model,
            vehicle_avail,
            rake_charges,
            frt_trgt,
            fiscal_benefit,
            transit_depots,
            handling_charges,
            df_depot,
            df_packaging,
            sla,
            packer_constraint,
        )

    def data_prep(
        df,
        ppm,
        dmnd,
        vehicle_avail,
        rake_charges,
        frt_trgt,
        fiscal_benefit,
        transit_depots,
        handling_charges,
        df_depot,
        df_packaging,
        sla,
        constraints,
        cnxn,
    ):
        """
        This function is used to apply business rules to the model inputs and constraints.

        Parameters
        -------
        df: Pandas Dataframe
            Combination of all routes at a Brand, Grade, Packaging and Customer Category level.

        ppm: Pandas Dataframe
            Plant product master which contains information about the products being made at a plant along with its
            variable production cost and clinker conversion factor wherever applicable.

        dmnd_model: Pandas Dataframe
            The demand for the month at a city level.

        vehicle_avail: Pandas Dataframe
            Vehicle availability constraint to invalidate certain routes from a plant to a city.

        rake_charges: Pandas Dataframe
            Rake charges to be considered for the planning.

        frt_trgt: Pandas Dataframe
            Freight type targets at a district level for target setting constraint.

        fiscal_benefit: Pandas Dataframe
            Fiscal benefit avaiable at applicable plants

        transit_depots: Pandas Dataframe
            A one time master shared by logistics to exclude routes through certain depots. This would gradually be
            removed as the routes are closed in the ERP.

        handling_charges: Pandas Dataframe
            Master for handling charges

        df_depot: Pandas Dataframe
            Master for depots at node city

        df_packaging: Pandas Dataframe
            Master for packaging cost

        sla: Pandas Dataframe
            Master for SLA at city level.

        Returns
        -------

        df: Pandas Dataframe
            Final combination of routes to be fed as an input to the model along with contribution calculated
            for each link.

        dmnd: Pandas Dataframe
            Final demand to be fed as an input to the model.

        frt_trgt: Pandas Dataframe
            Final freight type targets at a district level. Used for target setting constraint.

        dmnd_missing: Pandas Dataframe
            Demand that is missed due to unavailability of routes/price. Attached to the output for user's
            reference.

        """

        zone_dict = {
            "Uttar Pradesh": "North",
            "Rajasthan": "North",
            "Gujarat": "North",
            "Haryana": "North",
            "Punjab": "North",
            "Jammu & Kashmir": "North",
            "Maharashtra": "South",
            "Uttranchal": "North",
            "Delhi": "North",
            "Madhya Pradesh": "North",
            "West Bengal": "East",
            "Chandigarh": "North",
            "Himachal Pradesh": "North",
            "Bihar": "East",
            "Jharkhand": "East",
            "Chattisgarh": "East",
            "Odisha": "East",
            "Karnataka": "South",
            "Telangana": "South",
            "Andhra Pradesh": "South",
            "Goa": "South",
        }

        df = df[df["FREIGHT_TYPE"] != "RF"]

        # Add rake charges at a district level for routes with freight type as RK or GD-RK
        df.drop(columns=["RAKE_CHARGES"], inplace=True)
        df = df.merge(rake_charges, how="left", on=["DESTINATION_DISTRICT"])
        df.loc[~df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]), "RAKE_CHARGES"] = 0

        # Map states to the zones
        df["ZONE"] = df["DESTINATION_STATE"].map(zone_dict)

        # Add fiscal benefit for the plants applicable
        # Recompute taxes for the routes where fiscal benefit is applicable
        df = df.merge(fiscal_benefit, how="left", on=["PLANT_ID"])
        df.loc[
            (~df["FISCAL_BENEFIT"].isna())
            & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
            "TAXES",
        ] -= (
            df.loc[
                (~df["FISCAL_BENEFIT"].isna())
                & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
                "TAXES",
            ]
            / 2
        ) * df.loc[
            (~df["FISCAL_BENEFIT"].isna())
            & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
            "FISCAL_BENEFIT",
        ]
        df.loc[
            (~df["FISCAL_BENEFIT"].isna())
            & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
            "FISCAL_BENEFIT_AMT",
        ] = (
            df.loc[
                (~df["FISCAL_BENEFIT"].isna())
                & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
                "TAXES",
            ]
            / 2
        ) * df.loc[
            (~df["FISCAL_BENEFIT"].isna())
            & (df["DESTINATION_STATE"] == df["SOURCE_STATE"]),
            "FISCAL_BENEFIT",
        ]

        # Drop transit depots from the routes
        # df['NODE_CITY'] = df['NODE_CITY'].str.replace('\(NT\)-','')
        # df['NODE_CITY'] = df['NODE_CITY'].str.replace('\(TR\)-','')
        # df = df.loc[~df['NODE_CITY'].isin(transit_depots['DEPOT CITY'])]
        # print(df[(df['TO_CITY_ID']==14221)&(df['PRIMARY_SECONDARY_ROUTE']=='SECONDARY')]['NODE_CITY'].unique())
        df["ROUTE_CHANGED"] = "FALSE"

        # Add variable production cost to the routes
        df = df.merge(
            ppm[["PLANT_ID", "GRADE", "VARIABLE_PRODUCTION_COST", "CLINKER_CF"]],
            how="inner",
            left_on=["PLANT_ID", "GRADE"],
            right_on=["PLANT_ID", "GRADE"],
        )

        # Add handling charges
        df["PACKING"] = df["PACKAGING"].apply(
            lambda x: "PAPER" if x in ["PAPER", "ROOFON"] else "HDPE"
        )
        df.drop(columns=["HA_COMMISSION"], inplace=True)
        df = df.merge(
            handling_charges,
            on=["NODE_DISTRICT", "NODE_TALUKA", "NODE_CITY", "PACKING", "FREIGHT_TYPE"],
            how="left",
        )

        # Add average handling charges for links where handling charges are not available in the master
        df.loc[df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]), "HA_COMMISSION"] = df[
            df["FREIGHT_TYPE"].isin(["RK", "GD-RK"])
        ]["HA_COMMISSION"].replace([np.nan, 0, np.float(0)], 220)
        df.loc[df["FREIGHT_TYPE"].isin(["TP", "GD"]), "HA_COMMISSION"] = df[
            df["FREIGHT_TYPE"].isin(["TP", "GD"])
        ]["HA_COMMISSION"].replace([np.nan, 0, np.float(0)], 90)
        df.loc[df["FREIGHT_TYPE"].isin(["RD"]), "HA_COMMISSION"] = df[
            df["FREIGHT_TYPE"].isin(["RD"])
        ]["HA_COMMISSION"].replace([np.nan, 0, np.float(0)], 45)
        df.loc[df["FREIGHT_TYPE"].isin(["PD"]), "HA_COMMISSION"] = 0

        # Add average demurrage and damages amount
        df.loc[df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]), "DEMURRAGE"] = df[
            df["FREIGHT_TYPE"].isin(["RK", "GD-RK"])
        ]["DEMURRAGE"].replace([np.nan, 0, np.float(0)], 20)
        df.loc[df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]), "DAMAGES"] = df[
            df["FREIGHT_TYPE"].isin(["RK", "GD-RK"])
        ]["DAMAGES"].replace([np.nan, 0, np.float(0)], 40)

        df[
            [
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
            ]
        ] = df[
            [
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
            ]
        ].fillna(
            0
        )

        # Add direct plant discount for trade orders server through primary routes
        df["DIRECT_PLANT_DISCOUNT"] = 0
        df["JHJU_RAIL_DISCOUNT"] = 0
        df.loc[
            (df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY")
            & (df["CUST_CATEGORY"] == "TR"),
            "DIRECT_PLANT_DISCOUNT",
        ] += 120

        df.loc[(df["WAREHOUSE"] == "SCL"), "WAREHOUSE"] = (
            df.loc[(df["WAREHOUSE"] == "SCL"), "WAREHOUSE"]
            + "-"
            + df.loc[(df["WAREHOUSE"] == "SCL"), "NODE_CITY"]
        )

        # Compute avg time taken for delivery
        df.loc[df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY", "avg_time"] = (
            7 + df.loc[df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY", "DISTANCE"] / 25
        )
        df.loc[df["PRIMARY_SECONDARY_ROUTE"] == "SECONDARY", "avg_time"] = (
            2 + df.loc[df["PRIMARY_SECONDARY_ROUTE"] == "SECONDARY", "DISTANCE"] / 25
        )

        # Add packaging cost
        df = df.merge(
            df_packaging.drop_duplicates(),
            how="left",
            on=["BRAND", "GRADE", "PACKAGING"],
        )
        df["PACKAGING_COST"] = df["PACKAGING_COST"].fillna(0)

        # Compute Contribution
        df["contribution"] = (
            df["PRICE"]
            - df["PRIMARY_FRT"]
            - df["SECONDARY_FRT"]
            - df["NOTIONAL_FREIGHT"]
            - df["HA_COMMISSION"]
            - df["RAKE_CHARGES"]
            - df["DEMURRAGE"]
            - df["DAMAGES"]
            - df["DISCOUNT"]
            - df["TAXES"]
            - df["SP_COMMISSION"]
            - df["ISP_COMMISSION"]
            - df["MISC_CHARGES"]
            - df["VARIABLE_PRODUCTION_COST"]
            - df["PACKAGING_COST"]
            - df["DIRECT_PLANT_DISCOUNT"]
        )

        # Remove routes that do not make business sense:
        # Primary routes served through rail.
        # Routes with freight type RK and GD-RK with primary mode as road.
        # Routes with freight type GD with secondary freight as 0.
        # Routes with freight type RD and TP with secondary freight as 0 and distance greater than 60.
        # Primary routes with freight amount 0.
        # Routes with mode rail for other than freight type RK and GD-RK.
        # Primary routes with type as ISO and secondary routes with type as DI.

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["MODE"] == "RAIL")
                    & (df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY")
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["MODE"] == "ROAD")
                    & (df["PRIMARY_SECONDARY_ROUTE"] == "SECONDARY")
                    & (df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]))
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["SECONDARY_FRT"] == 0)
                    & (df["FREIGHT_TYPE"].isin(["GD"]))
                    & (df["IS_EX"] == False)
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["SECONDARY_FRT"] == 0)
                    & (df["DISTANCE"] >= 60)
                    & (df["FREIGHT_TYPE"].isin(["RD", "TP"]))
                    & (df["IS_EX"] == False)
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["PRIMARY_FRT"] == 0)
                    & (df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY")
                    & (df["IS_EX"] == False)
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["MODE"] == "RAIL") & (~df["FREIGHT_TYPE"].isin(["RK", "GD-RK"]))
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[
                    (df["TYPE"] == "ISO") & (df["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY")
                ].index.tolist()
            )
        ]
        df = df.loc[
            ~df.index.isin(
                df[
                    (df["TYPE"] == "DI")
                    & (df["PRIMARY_SECONDARY_ROUTE"] == "SECONDARY")
                ].index.tolist()
            )
        ]

        df = df.loc[
            ~df.index.isin(
                df[(df["MODE"] == "RAIL") & (df["RAKE_CHARGES"] == 0)].index.tolist()
            )
        ]

        # Vehicle avaialbility constraint
        if "vehicle_availability" in constraints:
            vehicle_avail = vehicle_avail.rename(
                columns={"QUANTITY": "TO_DROP", "PACK_TYPE": "PACKING"}
            )[
                [
                    "DISTRICT",
                    "CITY",
                    "GRADE",
                    "CUST_CATEGORY",
                    "PACKING",
                    "PLANT_ID",
                    "TO_DROP",
                ]
            ]
            vehicle_avail.columns = [
                "DESTINATION_DISTRICT",
                "DESTINATION_CITY",
                "GRADE",
                "CUST_CATEGORY",
                "PACK_TYPE",
                "PLANT_ID",
                "TO_DROP",
            ]
            vehicle_avail.drop_duplicates(inplace=True)
            # vehicle_avail['TO_DROP'] = 0
            df1 = df.reset_index().merge(
                vehicle_avail,
                how="inner",
                on=[
                    "DESTINATION_DISTRICT",
                    "DESTINATION_CITY",
                    "GRADE",
                    "CUST_CATEGORY",
                    "PACK_TYPE",
                    "PLANT_ID",
                ],
            )
            # df = df.merge(vehicle_avail,how="left",on=['DESTINATION_DISTRICT','DESTINATION_CITY','GRADE','CUST_CATEGORY','PACK_TYPE','PLANT_ID'])
            # df = df[(df['TO_DROP']!=0)]
            df = df.drop(df1["index"])
            # abc = vehicle_avail[vehicle_avail['DESTINATION_CITY']=='FARIDABAD']
            # df = df.drop(df[
            #     (df['DESTINATION_CITY'].isin(vehicle_avail['DESTINATION_CITY']))
            #     &(df['DESTINATION_DISTRICT'].isin(vehicle_avail['DESTINATION_DISTRICT']))
            #     &(df['GRADE'].isin(vehicle_avail['GRADE']))
            #     &(df['CUST_CATEGORY'].isin(vehicle_avail['CUST_CATEGORY']))
            #     &(df['PACK_TYPE'].isin(vehicle_avail['PACK_TYPE']))
            #     &(df['PLANT_ID'].isin(vehicle_avail['PLANT_ID']))
            #     ].index.tolist())avail['DESTINATION_CITY']=='FARIDABAD']

        # SLA constarint
        if "service_level_sla" in constraints:
            df = df.merge(sla, how="left", on="TO_CITY_ID")
            df["sla"] = df["sla"].fillna(1000)
            df["can_serve"] = df["sla"] - df["avg_time"]

            df_bgp_links = df.groupby(
                [
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
                as_index=False,
            ).size()
            df = df.merge(
                df_bgp_links,
                how="left",
                left_on=[
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
                right_on=[
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
            )

            df_bgp_links_drop = (
                df[df["can_serve"] < 0]
                .groupby(
                    [
                        "TO_CITY_ID",
                        "BRAND",
                        "GRADE",
                        "PACK_TYPE",
                        "PACKAGING",
                        "CUST_CATEGORY",
                    ],
                    as_index=False,
                )
                .size()
            )
            df_bgp_links_drop.rename(columns={"size": "drop_size"}, inplace=True)

            df = df.merge(
                df_bgp_links_drop,
                how="left",
                left_on=[
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
                right_on=[
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
            )
            links_dnd = (
                df[(~df["drop_size"].isna()) & (df["size"] == df["drop_size"])]
                .sort_values("avg_time")
                .drop_duplicates(
                    subset=[
                        "TO_CITY_ID",
                        "BRAND",
                        "GRADE",
                        "PACK_TYPE",
                        "PACKAGING",
                        "CUST_CATEGORY",
                    ]
                )
                .index.tolist()
            )

            links_to_drop = df.loc[
                (~df.index.isin(links_dnd)) & (df["can_serve"] < 0)
            ].index.tolist()

            df = df.loc[~df.index.isin(links_to_drop)]

            NT_drop_list = df[
                (df["CUST_CATEGORY"] == "NT")
                & ((df["PRIMARY_SECONDARY_ROUTE"] == "SECONDARY"))
            ].index.tolist()
            df = df.loc[~df.index.isin(NT_drop_list)]

        # Merge depot master to get depot id for secondary links.
        df = df.merge(
            df_depot,
            how="left",
            on=["NODE_STATE", "NODE_DISTRICT", "NODE_CITY", "BRAND"],
        )
        df.loc[~df["DEPOT_ID"].isna(), "WAREHOUSE"] = df[~df["DEPOT_ID"].isna()][
            "DEPOT_ID"
        ]

        df = df.reset_index(drop=True)
        df["index"] = df.index

        # Remove demand that cannot be served due to unavailability of routes/prices
        dmnd["ZONE"] = dmnd["STATE"].map(zone_dict)
        tmp_df = df.merge(
            dmnd[
                [
                    "DESTINATION",
                    "STATE",
                    "DISTRICT",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "dmnd_id",
                    "DEMAND_QTY",
                ]
            ],
            how="right",
            left_on=[
                "TO_CITY_ID",
                "DESTINATION_STATE",
                "DESTINATION_DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            right_on=[
                "DESTINATION",
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
        )
        dmnd_not_serv = dmnd.loc[
            dmnd.index.isin(tmp_df[tmp_df["ROUTE_ID"].isna()]["dmnd_id"].to_list())
        ]["DEMAND_QTY"].sum()

        dmnd_missing = dmnd.loc[
            dmnd.index.isin(tmp_df[tmp_df["ROUTE_ID"].isna()]["dmnd_id"].to_list())
        ]
        pm = pd.read_sql(
            """
        select distinct on ("DESTINATION","CUST_CATEGORY","BRAND","GRADE","PACKAGING")
        "DESTINATION",
        "BRAND",
        "GRADE",
        "PACKAGING",
        case "CUST_CATEGORY"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "CUST_CATEGORY"
            end as "CUST_CATEGORY",
        true as "PRICE_AVAILABLE" from etl_zone."PRICE_MASTER"
        where "PRICE" != 0
        """,
            cnxn,
        )
        dmnd_missing = dmnd_missing.merge(
            pm,
            how="left",
            on=["DESTINATION", "BRAND", "GRADE", "PACKAGING", "CUST_CATEGORY"],
        )

        dmnd = dmnd.loc[
            ~dmnd.index.isin(tmp_df[tmp_df["ROUTE_ID"].isna()]["dmnd_id"].to_list())
        ]

        print("Demand not served: ", dmnd_not_serv)

        frt_trgt = frt_trgt.merge(
            dmnd[dmnd["CUST_CATEGORY"] == "TR"]
            .groupby(["STATE", "DISTRICT"], as_index=False)["DEMAND_QTY"]
            .sum(),
            left_on=["DESTINATION_STATE", "DESTINATION_DISTRICT"],
            right_on=["STATE", "DISTRICT"],
            how="inner",
        )

        # frt_trgt = (
        #     frt_trgt[~frt_trgt["FREIGHT_TYPE"].isin(["PD", "RK"])]
        #     .dropna()
        #     .reset_index(drop=True)
        # )
        frt_trgt.reset_index(drop=True, inplace=True)
        frt_trgt["TARGET_ID"] = frt_trgt.index

        return df, dmnd, frt_trgt, dmnd_missing

    def run_model(df, ppm, dmnd, frt_trgt, packer_constraint, constraints=[]):
        """
        This function is used to run the LP model.

        Parameters
        -------
        df: Pandas Dataframe
            Combination of all routes at a Brand, Grade, Packaging and Customer Category level.

        ppm: Pandas Dataframe
            Plant product master which contains information about the products being made at a plant along with its
            variable production cost and clinker conversion factor wherever applicable.

        dmnd: Pandas Dataframe
            The demand for the month at a city level.

        frt_trgt: Pandas Dataframe
            Freight type targets at a district level for target setting constraint.

        constaints: array
            List of constraints apllicable for the run.

        Returns
        -------

        df_fnl: Pandas Dataframe
            Model output.

        status: string
            Model run status (Optimal or infeasible)

        df_rank: Pandas Dataframe
            Ranking of the routes at DESTINATION_STATE,DESTINATION_DISTRICT,DESTINATION_CITY,BRAND,GRADE,PACKAGING level.

        """
        start = time.time()

        # 1. initialize problem
        # 2. declare Variables
        # 3. declare Objective Function
        # 4. set objective function in model

        var_names = ["x" + str(i) for i in range(len(df))]
        df["variables"] = pd.Series(var_names)

        lp_prob = p.LpProblem("Maximize_Contribution", p.LpMaximize)
        var_names_model = [
            p.LpVariable(i, lowBound=0, cat="Continuous") for i in var_names
        ]
        cntr = df["contribution"].tolist()

        objective_list = [
            var_names_model[i] * cntr[i] for i in range(len(var_names_model))
        ]
        lp_prob += p.lpSum(objective_list)

        # constraints

        #############################################################################################################################

        # Constraint 1 - Overall Demand
        lp_prob += p.lpSum(var_names_model) <= dmnd["DEMAND_QTY"].sum()

        #############################################################################################################################

        # Constraint 2 - Demand at BGP level for each city
        dmnd_cns = (
            df.merge(
                dmnd[
                    [
                        "DESTINATION",
                        "BRAND",
                        "GRADE",
                        "PACK_TYPE",
                        "PACKAGING",
                        "CUST_CATEGORY",
                        "dmnd_id",
                    ]
                ],
                how="inner",
                left_on=[
                    "TO_CITY_ID",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
                right_on=[
                    "DESTINATION",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
            )
            .groupby("dmnd_id")["index"]
            .apply(list)
        )

        for idx, val in dmnd_cns.items():
            lp_prob += (
                p.lpSum([var_names_model[i] for i in val])
                == dmnd.loc[idx, "DEMAND_QTY"]
            )

        #############################################################################################################################

        # # Constraint 3 - Freight Type Target

        if "target_setting" in constraints:
            dmnd1 = dmnd[dmnd["CUST_CATEGORY"] == "TR"]
            trgt_cns = (
                df.merge(
                    frt_trgt[
                        [
                            "DESTINATION_STATE",
                            "DESTINATION_DISTRICT",
                            "FREIGHT_TYPE",
                            "TARGET_ID",
                        ]
                    ],
                    how="inner",
                    on=["DESTINATION_STATE", "DESTINATION_DISTRICT", "FREIGHT_TYPE"],
                )
                .groupby("TARGET_ID")["index"]
                .apply(list)
            )

            for idx, val in trgt_cns.items():
                if (
                    frt_trgt.loc[idx, "DEMAND_QTY"] * frt_trgt.loc[idx, "TARGET"]
                ) <= dmnd1[
                    dmnd1["DESTINATION"].isin(
                        df[
                            (
                                df["DESTINATION_STATE"]
                                == frt_trgt.loc[idx, "DESTINATION_STATE"]
                            )
                            & (
                                df["DESTINATION_DISTRICT"]
                                == frt_trgt.loc[idx, "DESTINATION_DISTRICT"]
                            )
                            & (df["FREIGHT_TYPE"] == frt_trgt.loc[idx, "FREIGHT_TYPE"])
                        ]["TO_CITY_ID"].unique()
                    )
                ][
                    "DEMAND_QTY"
                ].sum():
                    lp_prob += (
                        p.lpSum([var_names_model[i] for i in val])
                        >= frt_trgt.loc[idx, "DEMAND_QTY"] * frt_trgt.loc[idx, "TARGET"]
                    )

        #############################################################################################################################

        # Constraint 4 - Links where demand do no exist
        dmnd_cns1 = df.merge(
            dmnd[
                [
                    "DESTINATION",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "dmnd_id",
                ]
            ],
            how="left",
            left_on=[
                "TO_CITY_ID",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            right_on=[
                "DESTINATION",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
        )

        dmnd_cns1 = dmnd_cns1[dmnd_cns1["dmnd_id"].isna()]["index"].to_list()

        lp_prob += p.lpSum([var_names_model[i] for i in dmnd_cns1]) == 0

        #############################################################################################################################

        # Constraint 5 - Supply constraint for each plant

        if "plant_constraint_master" in constraints:
            packer_constraint["QTY_PC"] = packer_constraint[
                ["PACKER_QTY", "TL_QTY"]
            ].min(axis=1)
            packer_constraint = packer_constraint[["PLANT_ID", "QTY_PC"]]

            ppm = ppm.merge(packer_constraint, on="PLANT_ID", how="left")
            ppm.loc[~ppm["QTY_PC"].isna(), "QUANTITY"] = ppm.loc[~ppm["QTY_PC"].isna()][
                ["QUANTITY", "QTY_PC"]
            ].min(axis=1)

        ppm_cns = (
            df.merge(
                ppm.drop_duplicates(subset=["PLANT_ID", "QUANTITY"])[
                    ["PLANT_ID", "ppm_id"]
                ],
                how="inner",
                left_on=["PLANT_ID"],
                right_on=["PLANT_ID"],
            )
            .groupby("ppm_id")["index"]
            .apply(list)
        )
        for idx, val in ppm_cns.items():
            lp_prob += (
                p.lpSum([var_names_model[i] for i in val]) <= ppm.loc[idx, "QUANTITY"]
            )

        #############################################################################################################################

        # Constraint 6 - Minimum and Maximum Supply constraint for each plant
        if "plant_min_capacity" in constraints:
            ppm_cns = (
                df.merge(
                    ppm.drop_duplicates(subset=["PLANT_ID", "QUANTITY"])[
                        ["PLANT_ID", "ppm_id"]
                    ],
                    how="inner",
                    left_on=["PLANT_ID"],
                    right_on=["PLANT_ID"],
                )
                .groupby("ppm_id")["index"]
                .apply(list)
            )
            for idx, val in ppm_cns.items():
                lp_prob += (
                    p.lpSum([var_names_model[i] for i in val])
                    >= ppm.loc[idx, "MIN_QUANTITY"]
                )
                lp_prob += (
                    p.lpSum([var_names_model[i] for i in val])
                    <= ppm.loc[idx, "MAX_QUANTITY"]
                )

        print("Time taken to define model =", time.time() - start)
        start = time.time()

        # solve problem
        status = lp_prob.solve()

        print("Status = ", p.LpStatus[status])

        print("TC = ", p.value(lp_prob.objective / 10**7))

        qty = {}
        for i in var_names_model:
            qty[str(i)] = int(p.value(i))

        df["qty"] = df["variables"].apply(lambda x: qty[x])

        print("Time taken to run model=", time.time() - start)

        # Get ranking file
        df_rank = get_df_rank(df)

        # Prepare output
        df_fnl = df[df["qty"] > 0]

        df_fnl["SCENARIO"] = ", ".join(constraints)

        df_fnl["FISCAL_BENEFIT_AMT"] = df_fnl["FISCAL_BENEFIT_AMT"].fillna(0)

        df_fnl["tlc"] = (
            df_fnl["PRIMARY_FRT"]
            + df_fnl["SECONDARY_FRT"]
            + df_fnl["HA_COMMISSION"]
            + df_fnl["RAKE_CHARGES"]
            + df_fnl["DEMURRAGE"]
            + df_fnl["DAMAGES"]
            + df_fnl["DIRECT_PLANT_DISCOUNT"]
            - df_fnl["FISCAL_BENEFIT_AMT"]
        )

        df_fnl.loc[
            df_fnl["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY", "NODE_CITY"
        ] = df_fnl.loc[df_fnl["PRIMARY_SECONDARY_ROUTE"] == "PRIMARY", "PLANT_ID"]

        df_fnl["tlc"] = df_fnl["tlc"] * df_fnl["qty"]

        print("TLC = ", round(df_fnl["tlc"].sum() / 10**7, 2))

        return df_fnl, p.LpStatus[status], df_rank

    def get_clinker_inputs(cnxn):
        """
        This function is used to get the inputs required to run the clinker model.

        Parameters
        -------
        cnxn: connection
            A valid connection to the database

        Returns
        -------

        clinker_links: Pandas Dataframe
            Combination of all routes used to transport clinker from IU to GU.

        ppm: Pandas Dataframe
            Variable production cost for clinker at IU
        """

        # Read plant product master for variable production cost of clinker
        sql_ppm = """
        SELECT
        "PLANT_ID" as "FC_WHSE"
        ,"GRADE"
        ,"QUANTITY"*100000 as "QUANTITY"
        ,"VARIABLE_PRODUCTION_COST"
        ,"CLINKER_CF"
        FROM etl_zone."PLANT_PRODUCTS_MASTER"
        where "VARIABLE_PRODUCTION_COST" != 0
        and "GRADE" = 'CLINKER';
        """

        ppm = pd.read_sql(sql_ppm, cnxn)
        ppm.rename(columns={"PLANT_ID": "FC_WHSE"}, inplace=True)
        ppm["QUANTITY"] *= 100000
        ppm = ppm[ppm["VARIABLE_PRODUCTION_COST"] != 0]
        ppm[["QUANTITY", "VARIABLE_PRODUCTION_COST"]] = ppm[
            ["QUANTITY", "VARIABLE_PRODUCTION_COST"]
        ].fillna(0)
        ppm["ppm_id"] = ppm.index

        # Get bridging cost for plants where applicable
        df_bridging = pd.read_sql(
            """
        select "PLANT_ID","RAILWAY_BRIDGING_COST"
        from etl_zone."PLANT_CONSTRAINTS_MASTER" pcm
        """,
            cnxn,
        )

        # Get all active clinker links
        clinker_links = pd.read_sql(
            """
        select
        left("FG_WHSE",3) as "PLANT_ID",
        left("FC_WHSE",3) as "FC_WHSE",
        "MODE_OF_TRANSPORT" as "MODE",
        "CLINKER_FREIGHT",
        "ROUTE_ID",
        "CLINKER_BRIDGING_LOADING",
        "CLINKER_BRIDGING_UNLOADING",
        "CLINKER_NOTIONAL_FREIGHT"
        from etl_zone."CLINKER_LINKS_MASTER" where "IS_ACTIVE" = true
        """,
            cnxn,
        )

        clinker_links_fgs = clinker_links[clinker_links["PLANT_ID"] == "FGS"]
        clinker_links_fgs["PLANT_ID"] = "FGI"
        clinker_links_fgg = clinker_links[clinker_links["PLANT_ID"] == "FGG"]
        clinker_links_fgg["PLANT_ID"] = "FGF"
        clinker_links = clinker_links.append(
            clinker_links_fgs.append(clinker_links_fgg, ignore_index=True),
            ignore_index=True,
        )

        clinker_links = clinker_links.merge(
            ppm[["FC_WHSE", "VARIABLE_PRODUCTION_COST"]], how="left", on="FC_WHSE"
        )

        clinker_links = clinker_links.merge(df_bridging, how="left", on="PLANT_ID")
        clinker_links["RAILWAY_BRIDGING_COST"] = clinker_links[
            "RAILWAY_BRIDGING_COST"
        ].fillna(0)

        clinker_links["TCC"] = clinker_links[
            [
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
                "RAILWAY_BRIDGING_COST",
                "ROUTE_ID",
                "CLINKER_BRIDGING_LOADING",
                "CLINKER_BRIDGING_UNLOADING",
                "CLINKER_NOTIONAL_FREIGHT",
            ]
        ].sum(axis=1)
        clinker_links["index"] = clinker_links.index

        return clinker_links, ppm

    def run_clinker_model(clinker_links, ppm, df_fnl):
        """
        This function is used to run the LP model for clinker routes.

        Parameters
        -------
        clinker_links: Pandas Dataframe
            Combination of all routes used to transport clinker from IU to GU.

        ppm: Pandas Dataframe
            Variable production cost for clinker at IU

        df_fnl: Pandas Dataframe
            Output of LP model run for routes serving the cities.

        Returns
        -------

        clinker_links: Pandas Dataframe
            Model output.

        """
        # Determine clinker demand at plants basis the model output
        clinker_df = df_fnl[df_fnl["CLINKER_CF"] != 0].copy()
        clinker_df["qty"] = round(clinker_df["qty"] / clinker_df["CLINKER_CF"], 0)
        clinker_df = clinker_df.groupby(["PLANT_ID", "FROM_CITY_ID"], as_index=False)[
            "qty"
        ].sum()
        clinker_df["clinker_dmnd_id"] = clinker_df.index

        run = dt.now().strftime("%Y%m%d_%H%M")
        start = time.time()

        # 1. initialize problem
        # 2. declare Variables
        # 3. declare Objective Function
        # 4. set objective function in model
        var_names = ["x" + str(i) for i in range(len(clinker_links))]
        clinker_links["variables"] = pd.Series(var_names)

        lp_prob = p.LpProblem("Minimize_Contribution", p.LpMinimize)
        var_names_model = [
            p.LpVariable(i, lowBound=0, cat="Continuous") for i in var_names
        ]
        cntr = clinker_links["TCC"].tolist()

        objective_list = [
            var_names_model[i] * cntr[i] for i in range(len(var_names_model))
        ]
        lp_prob += p.lpSum(objective_list)

        # constraints

        #############################################################################################################################

        # Constraint 1 - Overall Demand
        lp_prob += p.lpSum(var_names_model) <= clinker_df["qty"].sum()

        #############################################################################################################################

        # Constraint 2 - Demand at Plant level
        dmnd_cns = (
            clinker_links.merge(
                clinker_df[["PLANT_ID", "clinker_dmnd_id"]],
                how="inner",
                on=["PLANT_ID"],
            )
            .groupby("clinker_dmnd_id")["index"]
            .apply(list)
        )

        for idx, val in dmnd_cns.items():
            lp_prob += (
                p.lpSum([var_names_model[i] for i in val]) == clinker_df.loc[idx, "qty"]
            )

        ##############################################################################################################################

        # Constraint 3 - Supply Constraint at IU

        ppm_cns = (
            clinker_links.merge(
                ppm.drop_duplicates(subset=["FC_WHSE", "QUANTITY"])[
                    ["FC_WHSE", "ppm_id"]
                ],
                how="inner",
                on="FC_WHSE",
            )
            .groupby("ppm_id")["index"]
            .apply(list)
        )
        for idx, val in ppm_cns.items():
            lp_prob += (
                p.lpSum([var_names_model[i] for i in val]) <= ppm.loc[idx, "QUANTITY"]
            )

        print("Time taken to define model =", time.time() - start)
        start = time.time()

        # solve problem
        status = lp_prob.solve()

        print("Status = ", p.LpStatus[status])

        print("TC = ", p.value(lp_prob.objective) / 10**7)

        qty = {}
        for i in var_names_model:
            qty[str(i)] = int(p.value(i))

        clinker_links["CLINKER_DEMAND"] = clinker_links["variables"].apply(
            lambda x: qty[x]
        )

        clinker_links = clinker_links[clinker_links["CLINKER_DEMAND"] > 0]
        clinker_links = clinker_links[
            [
                "PLANT_ID",
                "FC_WHSE",
                "CLINKER_DEMAND",
                "CLINKER_FREIGHT",
                "MODE",
                "RAILWAY_BRIDGING_COST",
                "ROUTE_ID",
                "CLINKER_BRIDGING_LOADING",
                "CLINKER_BRIDGING_UNLOADING",
                "CLINKER_NOTIONAL_FREIGHT",
            ]
        ]

        print("Time taken to run model=", time.time() - start)

        return clinker_links

    # if __name__=='__main__':

    #     start = time.time()

    #     run = dt.now().strftime('%Y%m%d_%H%M')

    #     cnxn = connect_db()

    #     # Get model inputs and constraints
    #     df = get_model_inputs(cnxn)
    #     ppm, dmnd_model, vehicle_avail, rake_charges, frt_trgt, fiscal_benefit, transit_depots, handling_charges, df_depot,df_packaging,sla,packer_constraint = get_model_constraints(cnxn)
    #     ppm_plant = ppm.copy()
    #     pc = packer_constraint.copy()

    #     # uncomment constraints in the list below to consdider them for the model
    #     constraints = [
    #         # "plant_constraint_master",
    #         # "vehicle_availability",
    #         # "service_level_sla",
    #         # "target_setting",
    #         # "plant_min_capacity"
    #     ]

    #     df,dmnd,frt_trgt,dmnd_missing = data_prep(df,ppm, dmnd_model, vehicle_avail, rake_charges, frt_trgt, fiscal_benefit, transit_depots, handling_charges, df_depot,df_packaging,sla,constraints,cnxn)

    #     result,status, df_rank = run_model(df,ppm,dmnd,frt_trgt,packer_constraint,constraints)
    #     clinker_links, ppm = get_clinker_inputs(cnxn)
    #     result_clinker = run_clinker_model(clinker_links,ppm,result)

    #     # # Writing results to file
    #     writer = pd.ExcelWriter(f'output/lp_output_{run}.xlsx', engine='xlsxwriter')

    #     result.to_excel(writer,sheet_name='Model Output',index=False)
    #     result_clinker.to_excel(writer,sheet_name='Model Output Clinker',index=False)
    #     df_rank.to_excel(writer,sheet_name='Rank',index=False)
    #     dmnd_missing.to_excel(writer,sheet_name='Demand Missed',index=False)
    #     if 'service_level_sla' in constraints:
    #         sla.to_excel(writer,sheet_name='Constraint - Service Level',index=False)
    #     if 'target_setting' in constraints:
    #         frt_trgt.to_excel(writer,sheet_name='Constraint - Freight Type',index=False)
    #     if 'plant_min_capacity' in constraints:
    #         ppm_plant.to_excel(writer,sheet_name='Constraint - Plant Utilization',index=False)
    #     if "vehicle_availability" in constraints:
    #         vehicle_avail.to_excel(writer,sheet_name='Constraint - Vehicle',index=False)
    #     if "plant_constraint_master" in constraints:
    #         pc.to_excel(writer,sheet_name='Constraint - Packer',index=False)

    #     writer.save()
    #     writer.close()
    #     writer.handles = None

    #     print('TOTAL TIME TAKEN:',time.time()-start)
