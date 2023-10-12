from datetime import datetime as dt
from datetime import timedelta as td

import pandas as pd
from dateutil.relativedelta import relativedelta as rd

from .connection import connect_db


class DemandSplitHelperView:
    def get_trade_dmnd(cnxn, df, date, rerun=False):
        date_prev = (dt.strptime(date, "%Y-%m-%d") - rd(months=1)).strftime("%Y-%m-%d")
        if not rerun:
            df = df[df["CUST_CATEGORY"] == "TR"]
            df = df[df["DEMAND_QTY"] > 0]
            df["BRAND"] = df["BRAND"].astype("str")
            df["PACK_TYPE"] = df["PACK_TYPE"].str.upper()
            df["PACKAGING"] = df["PACKAGING"].str.upper()
            df = df.groupby(
                [
                    "STATE",
                    "DISTRICT",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                ],
                as_index=False,
            ).sum()

            df["STATE"] = df["STATE"].str.strip().str.upper()
            df["DISTRICT"] = df["DISTRICT"].str.strip().str.upper()

            # Uncomment the block below if heirarchy uploaded is new heirarchy
            #################################################################################################################

            sql = """
            select distinct on ("STATE_ERP","DISTRICT_ERP")
            upper("STATE_SCL") as "STATE"
            ,upper("DISTRICT_SCL") as "DISTRICT"
            ,"STATE_ERP",
            "DISTRICT_ERP"
            from etl_zone."SCL_HIERARCHY_MASTER" shm , etl_zone."T_OEBS_SCL_ADDRESS_LINK" tosal
            where
            tosal."CITY_ID" = shm."CITY_ID_ERP"
            and tosal."ACTIVE" = 'Y'
            and tosal."Active" = 1
            and
            (
            tosal."ATTRIBUTE1" is not null
            or tosal."ATTRIBUTE2" is not null
            or tosal."ATTRIBUTE3" is not null
            )
            """

            df_new_h = pd.read_sql(sql, cnxn)

            df_new_h.loc[df_new_h["STATE"] == "Delhi", "DISTRICT"] = "DELHI"

            df_new_h.drop_duplicates(subset=["STATE", "DISTRICT"], inplace=True)

            df = df.merge(df_new_h, how="left", on=["STATE", "DISTRICT"])
            df.loc[~df["STATE_ERP"].isna(), "STATE"] = df.loc[
                ~df["STATE_ERP"].isna(), "STATE_ERP"
            ]
            df.loc[~df["DISTRICT_ERP"].isna(), "DISTRICT"] = df.loc[
                ~df["DISTRICT_ERP"].isna(), "DISTRICT_ERP"
            ]

            # df[df['STATE_ERP'].isna()].to_csv('hierarchy_missing.csv',index=False)
            df_hierarchy_missing = df[df["STATE_ERP"].isna()]
            df = df[~df["STATE_ERP"].isna()]

            df.drop(columns=["STATE_ERP", "DISTRICT_ERP"], inplace=True)

            #################################################################################################################
        else:
            df.drop(columns=["DESTINATION"], inplace=True)

            df_hierarchy_missing = pd.DataFrame()

        add_link = pd.read_sql(
            """
        select "STATE" ,"DISTRICT" ,"CITY" ,"CITY_ID"  from etl_zone."T_OEBS_SCL_ADDRESS_LINK" tosal
        where "ACTIVE" = 'Y'
        and "Active" = 1
        """,
            cnxn,
        )
        add_link["STATE"] = add_link["STATE"].str.strip().str.upper()
        add_link["DISTRICT"] = add_link["DISTRICT"].str.strip().str.upper()
        add_link["CITY"] = add_link["CITY"].str.strip().str.upper()

        sql_dmnd_model = f"""
        select
        ncr."CITY_ID" as "DESTINATION",
        ADL."STATE"
        ,ADL."DISTRICT",
        "ORG_ID"::varchar as "BRAND",
        case "PRODUCT"
            when 'OPC_53_PREMIUM' then 'OPC_53'
            when 'PPC_ROOFON' then 'PPC_PRM'
            when 'PSC' then 'CC'
            else "PRODUCT"
        end as "GRADE",
        "PACKING_TYPE" as "PACK_TYPE",
        case "PACKING_BAG"
            when 'PAPER' then 'PAPER'
            when 'ROOFON' then 'PAPER'
            when 'LOOSE' then 'LOOSE'
            else 'HDPE'
        end as "PACKAGING",
        -- "PACKING_BAG" as "PACKING",
        case "ORDER_CLASSIFICATION"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "ORDER_CLASSIFICATION"
        end as "CUST_CATEGORY",
        sum("QUANTITY_INVOICED") as "DEMAND_QTY"
        from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" ncr
        inner join (
        select "STATE","DISTRICT","CITY_ID" from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
        ) ADL on ADL."CITY_ID" = ncr."CITY_ID"
        where "ORG_ID" != 101
        and "PRODUCT" not in ('RHPC','')
        and "INVOICE_DATE" >= '{date_prev}'
        and "INVOICE_DATE" < '{date}'
        and "QUANTITY_INVOICED" > 0
        and "ORDER_CLASSIFICATION" = 'TRADE'
        and "Active" = 1
        group by
        ADL."STATE"
        ,ADL."DISTRICT",
        "ORG_ID",
        "GRADE",
        "PACKING_TYPE",
        "PACKAGING",
        "ORDER_CLASSIFICATION",
        ncr."CITY_ID";
        """

        dmnd_model = pd.read_sql(sql_dmnd_model, cnxn)
        dmnd_model[["DEMAND_QTY"]] = dmnd_model[["DEMAND_QTY"]].fillna(0)
        dmnd_model = dmnd_model.groupby(
            [
                "DESTINATION",
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        )["DEMAND_QTY"].sum()
        dmnd_model["dmnd_id"] = dmnd_model.index

        dmnd_model_dist = dmnd_model.groupby(
            [
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        )["DEMAND_QTY"].sum()

        dmnd_model_dist.rename(columns={"DEMAND_QTY": "TOTAL"}, inplace=True)

        dmnd_model = dmnd_model.merge(
            dmnd_model_dist,
            on=[
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
        )

        # dmnd_model['perc'] = round(dmnd_model['DEMAND_QTY']/dmnd_model['TOTAL'],3)
        dmnd_model["perc"] = dmnd_model["DEMAND_QTY"] / dmnd_model["TOTAL"]

        dmnd_model = dmnd_model[
            [
                "DESTINATION",
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
                "perc",
            ]
        ]

        df["STATE"] = df["STATE"].str.strip().str.upper()
        df["DISTRICT"] = df["DISTRICT"].str.strip().str.upper()
        df.dropna(subset=["DEMAND_QTY"], inplace=True)
        df = df[df["DEMAND_QTY"] > 0]
        df = df[~df["STATE"].str.contains("TOTAL")]
        df.loc[df["STATE"] == "DELHI", "DISTRICT"] = "DELHI"
        df = df.groupby(
            [
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        ).sum()

        dmnd_model["STATE"] = dmnd_model["STATE"].str.strip().str.upper()
        dmnd_model["DISTRICT"] = dmnd_model["DISTRICT"].str.strip().str.upper()

        df_missing = df.merge(
            dmnd_model,
            how="left",
            on=[
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
        )
        df_missing = df_missing[df_missing["DESTINATION"].isna()]
        df_missing.drop(columns=["DESTINATION", "perc"], inplace=True)

        if rerun:
            df_missing["CITY"] = df_missing["DISTRICT"]

            # Change join to left to get missing demand
            df_missing = df_missing.merge(
                add_link[["STATE", "DISTRICT", "CITY", "CITY_ID"]].drop_duplicates(
                    ["STATE", "DISTRICT", "CITY"]
                ),
                how="left",
                on=["STATE", "DISTRICT", "CITY"],
            )
            df_missing.rename(columns={"CITY_ID": "DESTINATION"}, inplace=True)
        else:
            df_missing["DESTINATION"] = pd.NA

        df_trade_missing = df_missing[df_missing["DESTINATION"].isna()]

        df_missing = df_missing[~df_missing["DESTINATION"].isna()]

        df = df.merge(
            dmnd_model,
            how="inner",
            on=[
                "STATE",
                "DISTRICT",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
        )

        df["DEMAND_QTY"] = df["DEMAND_QTY"] * df["perc"]
        df["DEMAND_QTY"] = round(df["DEMAND_QTY"], 0)

        df = df.append(df_missing, ignore_index=True)

        return (
            df[
                [
                    "DESTINATION",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "DEMAND_QTY",
                ]
            ],
            df_trade_missing,
            df_hierarchy_missing,
            date_prev,
        )

    def get_non_trade_dmnd(cnxn, df, date, rerun=False):
        date_prev = (dt.strptime(date, "%Y-%m-%d") - rd(months=1)).strftime("%Y-%m-%d")
        if not rerun:
            df = df[df["CUST_CATEGORY"] == "NT"]
            df = df[df["DEMAND_QTY"] > 0]
            df["BRAND"] = df["BRAND"].astype("str")
            df["PACK_TYPE"] = df["PACK_TYPE"].str.upper()
            df["PACKAGING"] = df["PACKAGING"].str.upper()
            df = df.groupby(
                ["STATE", "BRAND", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
                as_index=False,
            ).sum()

            df["STATE"] = df["STATE"].str.strip().str.upper()

            # Uncomment the block below if heirarchy uploaded is new heirarchy
            #################################################################################################################

            sql = """
            select distinct on ("STATE_SCL")
            upper("STATE_SCL") as "STATE"
            ,"STATE_ERP"
            from etl_zone."SCL_HIERARCHY_MASTER" shm
            """

            df_new_h = pd.read_sql(sql, cnxn)

            df = df.merge(df_new_h, how="inner", on=["STATE"])
            df.loc[~df["STATE_ERP"].isna(), "STATE"] = df.loc[
                ~df["STATE_ERP"].isna(), "STATE_ERP"
            ]
            df.drop(columns=["STATE_ERP"], inplace=True)

            df = df.groupby(
                ["STATE", "BRAND", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
                as_index=False,
            ).sum()

            #################################################################################################################
            # df.to_excel('test_hier_nt.xlsx',index=False)
        else:
            df.drop(columns=["DESTINATION", "perc"], inplace=True)

        sql_dmnd_model = f"""
        select
        ncr."CITY_ID" as "DESTINATION",
        ADL."STATE",
        case "PRODUCT"
            when 'OPC_53_PREMIUM' then 'OPC_53'
            when 'PPC_ROOFON' then 'PPC_PRM'
            when 'PSC' then 'CC'
            else "PRODUCT"
        end as "GRADE",
        "PACKING_TYPE" as "PACK_TYPE",
        case "PACKING_BAG"
            when 'PAPER' then 'PAPER'
            when 'ROOFON' then 'PAPER'
            when 'LOOSE' then 'LOOSE'
            else 'HDPE'
        end as "PACKAGING",
        case "ORDER_CLASSIFICATION"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "ORDER_CLASSIFICATION"
        end as "CUST_CATEGORY",
        sum("QUANTITY_INVOICED") as "DEMAND_QTY"
        from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" ncr
        inner join (
        select "STATE","DISTRICT","CITY_ID" from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
        where "ACTIVE" = 'Y'
        and "Active" = 1
        ) ADL on ADL."CITY_ID" = ncr."CITY_ID"
        where "ORG_ID" != 101
        and "PRODUCT" not in ('RHPC','')
        and "INVOICE_DATE" >= '{date_prev}'
        and "INVOICE_DATE" < '{date}'
        and "QUANTITY_INVOICED" > 0
        and "ORDER_CLASSIFICATION" = 'NON TRADE'
        and "SALES_TYPE" != 'DM'
        and "CUST_SUBCATEG" != 'ON'
        and "Active" = 1
        group by
        ADL."STATE"
        ,ADL."DISTRICT",
        "ORG_ID",
        "GRADE",
        "PACKING_TYPE",
        "PACKAGING",
        "ORDER_CLASSIFICATION",
        ncr."CITY_ID";
        """

        dmnd_model = pd.read_sql(sql_dmnd_model, cnxn)
        dmnd_model[["DEMAND_QTY"]] = dmnd_model[["DEMAND_QTY"]].fillna(0)
        dmnd_model = dmnd_model.groupby(
            [
                "DESTINATION",
                "STATE",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
            ],
            as_index=False,
        )["DEMAND_QTY"].sum()
        dmnd_model["dmnd_id"] = dmnd_model.index

        dmnd_model_dist = dmnd_model.groupby(
            ["STATE", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
            as_index=False,
        )["DEMAND_QTY"].sum()

        dmnd_model_dist.rename(columns={"DEMAND_QTY": "TOTAL"}, inplace=True)

        dmnd_model = dmnd_model.merge(
            dmnd_model_dist,
            on=["STATE", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
        )

        dmnd_model["perc"] = dmnd_model["DEMAND_QTY"] / dmnd_model["TOTAL"]

        dmnd_model = dmnd_model[
            [
                "DESTINATION",
                "STATE",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
                "perc",
            ]
        ]

        df["STATE"] = df["STATE"].str.strip().str.upper()
        df = df.groupby(
            ["STATE", "BRAND", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
            as_index=False,
        ).sum()

        dmnd_model["STATE"] = dmnd_model["STATE"].str.strip().str.upper()

        #  change join to left and comment line below to get missing demand
        df = df.merge(
            dmnd_model,
            how="left",
            on=["STATE", "GRADE", "PACK_TYPE", "PACKAGING", "CUST_CATEGORY"],
        )
        df_non_trade_missing = df[df["DESTINATION"].isna()]
        df = df[~df["DESTINATION"].isna()]

        df["DEMAND_QTY"] = df["DEMAND_QTY"] * df["perc"]
        df["DEMAND_QTY"] = round(df["DEMAND_QTY"], 0)

        # df[df['DESTINATION'].isna()].to_excel('non_trade_missing.xlsx',index=False)

        return (
            df[
                [
                    "DESTINATION",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "DEMAND_QTY",
                ]
            ],
            df_non_trade_missing,
            date_prev,
        )

    def get_missing_dmnd(cnxn, df):
        add_link = pd.read_sql(
            """
        select "STATE" ,"DISTRICT" ,"CITY" ,"CITY_ID" as "DESTINATION"  from etl_zone."T_OEBS_SCL_ADDRESS_LINK" tosal
        where "ACTIVE" = 'Y'
        and "Active" = 1
        """,
            cnxn,
        )
        add_link["STATE"] = add_link["STATE"].str.strip().str.upper()
        add_link["DISTRICT"] = add_link["DISTRICT"].str.strip().str.upper()
        add_link["CITY"] = add_link["CITY"].str.strip().str.upper()

        df["STATE"] = df["STATE"].str.strip().str.upper()
        df["DISTRICT"] = df["DISTRICT"].str.strip().str.upper()
        df["CITY"] = df["CITY"].str.strip().str.upper()

        df = df.merge(add_link, how="inner", on=["STATE", "DISTRICT", "CITY"])
        df["DEMAND_QTY"] = round(df["DEMAND_QTY"], 0)

        # df[df['DESTINATION'].isna()].to_excel('dmnd_missing_still.xlsx',index=False)

        return df[
            [
                "DESTINATION",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
                "DEMAND_QTY",
            ]
        ]

    def update_missing_prices(cnxn, date_input):
        crsr = cnxn.cursor()
        crsr.execute(
            f"""
                delete from etl_zone."PRICE_MASTER"
                where "PRICE" = 0;

                insert into etl_zone."PRICE_MASTER"
                (
                    "DESTINATION",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "PRICE"
                )
                select
                d."DESTINATION",
                d."BRAND",
                d."GRADE",
                d."PACK_TYPE",
                d."PACKAGING",
                d."CUST_CATEGORY",
                0
                from etl_zone."DEMAND" d
                left join (
                select
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
                from etl_zone."PRICE_MASTER"
                ) pm on pm."DESTINATION" = d."DESTINATION"
                and pm."CUST_CATEGORY" = d."CUST_CATEGORY"
                and pm."BRAND" = d."BRAND"
                and pm."GRADE" = d."GRADE"
                and pm."PACKAGING" = d."PACKAGING"
                where d."MONTH" = '{date_input}'
                and pm."BRAND" is null;
            """
        )
        cnxn.commit()

        return 0

    def upload_price(cnxn, date_input):
        date = dt.now()
        date_now = min(date, dt.strptime(date_input, "%Y-%m-%d") - td(days=1)).strftime(
            "%Y-%m-%d"
        )
        date_prev = (dt.strptime(date_now, "%Y-%m-%d") - td(days=30)).strftime(
            "%Y-%m-%d"
        )

        sql = f"""
            delete from etl_zone."PRICE_MASTER";
            insert into etl_zone."PRICE_MASTER"
            (
                "DESTINATION",
                "BRAND",
                "GRADE",
                "PACK_TYPE",
                "PACKAGING",
                "CUST_CATEGORY",
                "PRICE",
                "TAXES",
                "DISCOUNT",
                "HA_COMMISSION",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "MISC_CHARGES"
            )
            select
            "CITY_ID",
            "ORG_ID" as "BRAND",
            case "PRODUCT"
                when 'OPC_53_PREMIUM' then 'OPC_53'
                when 'PPC_ROOFON' then 'PPC_PRM'
                when 'PSC' then 'CC'
                else "PRODUCT"
            end as "GRADE",
            "PACKING_TYPE",
            case "PACKING_BAG"
                when 'PAPER' then 'PAPER'
                when 'ROOFON' then 'PAPER'
                when 'LOOSE' then 'LOOSE'
                else 'HDPE'
            end as "PACKING",
            case "ORDER_CLASSIFICATION"
            when 'TRADE' then 'TR'
            when 'NON TRADE' then 'NT'
            else "ORDER_CLASSIFICATION"
            end as "CUSTOMER_CATEGORY",
            cast(sum("UNIT_SELLING_PRICE"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "PRICE",
            --cast(sum(("SALES_TAX_PMT" - (
            --((coalesce("SCH2",0)+coalesce("SCH3",0)+coalesce("SCH4",0)+coalesce("SCH5",0)+coalesce("SCH6",0)+coalesce("SCH7",0)+
            --coalesce("SCH8",0)+coalesce("SCH11",0)+coalesce("SCH12",0)+coalesce("SCH13",0)+coalesce("SCH14",0)+coalesce("SCH15",0)+
            --coalesce("SCH16",0)+coalesce("SCH17",0)+coalesce("SCH18",0)+coalesce("SCH19",0)+coalesce("SCH20",0)+coalesce("EXP0",0))*1.28) -
            --(coalesce("SCH2",0)+coalesce("SCH3",0)+coalesce("SCH4",0)+coalesce("SCH5",0)+coalesce("SCH6",0)+coalesce("SCH7",0)+
            --coalesce("SCH8",0)+coalesce("SCH11",0)+coalesce("SCH12",0)+coalesce("SCH13",0)+coalesce("SCH14",0)+coalesce("SCH15",0)+
            --coalesce("SCH16",0)+coalesce("SCH17",0)+coalesce("SCH18",0)+coalesce("SCH19",0)+coalesce("SCH20",0)+coalesce("EXP0",0))
            --))*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "TAXES",
            cast(sum("SALES_TAX_PMT"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "TAXES",
            cast(sum("REBATE_AND_DISCOUNT"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "DISCOUNT",
            cast(sum("HA_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "HA_COMMISSION",
            cast(sum("SP_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "SP_COMMISSION",
            cast(sum("ISP_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "ISP_COMMISSION",
            cast(sum("MISC_CHARGES"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "MISC_CHARGES"
            from
            (
            select
            "CITY_ID",
            "ORG_ID",
            "PRODUCT",
            "PACKING_TYPE",
            "PACKING_BAG",
            "ORDER_CLASSIFICATION",
            "UNIT_SELLING_PRICE",
            "SALES_TAX_PMT",
            case
                when "WAREHOUSE" like 'FG%' then "REBATE_AND_DISCOUNT" - 120
                else "REBATE_AND_DISCOUNT"
            end as "REBATE_AND_DISCOUNT",
            "HA_COMMISSION",
            "SP_COMMISSION",
            "ISP_COMMISSION",
            "MISC_CHARGES",
            "QUANTITY_INVOICED"
            from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
            where "ORG_ID" != 101
            and "PRODUCT" not in ('RHPC','')
            and "INVOICE_DATE" >= '{date_prev}'
            and "INVOICE_DATE" <= '{date_now}'
            and "QUANTITY_INVOICED" > 0
            and "FOB_CODE" not in ('EX_RLWY_SLID')
            and "SALES_TYPE" != 'DM'
            and "Active" = 1
            and not (
                "ORDER_CLASSIFICATION" = 'NON TRADE'
                and "CUST_SUBCATEG" = 'ON'
            )
            ) as ncr
            group by
            "CITY_ID",
            "ORG_ID",
            "GRADE",
            "PACKING_TYPE",
            "PACKING",
            "ORDER_CLASSIFICATION"
            order by "CITY_ID" asc;
        """

        crsr = cnxn.cursor()
        crsr.execute(sql)
        cnxn.commit()

        return 0

    def upload_price_dist(cnxn, date_input):
        date = dt.now()
        date_now = min(date, dt.strptime(date_input, "%Y-%m-%d") - td(days=1)).strftime(
            "%Y-%m-%d"
        )
        date_prev = (dt.strptime(date_now, "%Y-%m-%d") - td(days=30)).strftime(
            "%Y-%m-%d"
        )

        sql = f"""
            CREATE TEMP TABLE price_master_tmp as
            select
                pm."ID",
                pm."DESTINATION",
                pm."CUST_CATEGORY",
                pm."BRAND",
                pm."GRADE",
                pm."PACKAGING",
                sd."PRICE",
                sd."HA_COMMISSION",
                sd."DISCOUNT",
                sd."TAXES",
                sd."SP_COMMISSION",
                sd."ISP_COMMISSION",
                sd."MISC_CHARGES"
                from etl_zone."PRICE_MASTER" pm
                inner join(
                select "CITY_ID","STATE","DISTRICT" from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
                where "ACTIVE" = 'Y'
                and "Active" = 1
                ) tosal on tosal."CITY_ID" = pm."DESTINATION"
                inner join(
                    select
                    "STATE",
                    "DISTRICT",
                    case "PRODUCT"
                        when 'OPC_53_PREMIUM' then 'OPC_53'
                        when 'PPC_ROOFON' then 'PPC_PRM'
                        when 'PSC' then 'CC'
                        else "PRODUCT"
                    end as "GRADE",
                    "PACKING_TYPE",
                    case "PACKING_BAG"
                        when 'PAPER' then 'PAPER'
                        when 'ROOFON' then 'PAPER'
                        when 'LOOSE' then 'LOOSE'
                        else 'HDPE'
                    end as "PACKING",
                    case "ORDER_CLASSIFICATION"
                    when 'TRADE' then 'TR'
                    when 'NON TRADE' then 'NT'
                    else "ORDER_CLASSIFICATION"
                    end as "CUSTOMER_CATEGORY",
                    cast(sum("UNIT_SELLING_PRICE"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "PRICE",
                    cast(sum("SALES_TAX_PMT"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "TAXES",
                    cast(sum("REBATE_AND_DISCOUNT"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "DISCOUNT",
                    cast(sum("HA_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "HA_COMMISSION",
                    cast(sum("SP_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "SP_COMMISSION",
                    cast(sum("ISP_COMMISSION"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "ISP_COMMISSION",
                    cast(sum("MISC_CHARGES"*"QUANTITY_INVOICED")/sum("QUANTITY_INVOICED") as int) as "MISC_CHARGES"
                    from
                    (
                    select
                    "CITY_ID",
                    "STATE",
                    "DISTRICT",
                    "ORG_ID",
                    "PRODUCT",
                    "PACKING_TYPE",
                    "PACKING_BAG",
                    "ORDER_CLASSIFICATION",
                    "UNIT_SELLING_PRICE",
                    "SALES_TAX_PMT",
                    case
                        when "WAREHOUSE" like 'FG%' then "REBATE_AND_DISCOUNT" - 120
                        else "REBATE_AND_DISCOUNT"
                    end as "REBATE_AND_DISCOUNT",
                    "HA_COMMISSION",
                    "SP_COMMISSION",
                    "ISP_COMMISSION",
                    "MISC_CHARGES",
                    "QUANTITY_INVOICED"
                    from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
                    where "ORG_ID" != 101
                    and "PRODUCT" not in ('RHPC','')
                    and "INVOICE_DATE" >= '{date_prev}'
                    and "INVOICE_DATE" <= '{date_now}'
                    and "QUANTITY_INVOICED" > 0
                    and "FOB_CODE" not in ('EX_RLWY_SLID')
                    and "SALES_TYPE" != 'DM'
                    and "Active" = 1
                    and not (
                        "ORDER_CLASSIFICATION" = 'NON TRADE'
                        and "CUST_SUBCATEG" = 'ON'
                    )
                    ) as ncr
                    group by
                    "STATE",
                    "DISTRICT",
                    "GRADE",
                    "PACKING_TYPE",
                    "PACKING",
                    "ORDER_CLASSIFICATION"
                ) sd on sd."STATE" = tosal."STATE"
                and sd."DISTRICT" = tosal."DISTRICT"
                and sd."CUSTOMER_CATEGORY" = pm."CUST_CATEGORY"
                and sd."GRADE" =  pm."GRADE"
                and sd."PACKING" = pm."PACKAGING"
                where pm."PRICE" = 0;

            update etl_zone."PRICE_MASTER" pm1
            set
            "PRICE" = pm2."PRICE",
            "HA_COMMISSION" = pm2."HA_COMMISSION",
            "DISCOUNT" = pm2."DISCOUNT",
            "TAXES" = pm2."TAXES",
            "SP_COMMISSION" = pm2."SP_COMMISSION",
            "ISP_COMMISSION" = pm2."ISP_COMMISSION",
            "MISC_CHARGES" = pm2."MISC_CHARGES"
            from price_master_tmp pm2
            where pm2."ID" = pm1."ID";

            drop table price_master_tmp;

        """

        crsr = cnxn.cursor()
        crsr.execute(sql)
        cnxn.commit()

        return 0

    # if __name__ == '__main__':

    #     cnxn = connect_db()

    #     date_input = '2023-06-01'

    #     ##############################################################################################################

    #     # Importing Main Demand

    #     df_main = pd.read_excel('demand_template Jun-23.xlsx',sheet_name='dmnd')

    #     df_trade, df_trade_missing, df_hierarchy_missing, date_prev = get_trade_dmnd(cnxn,df_main,date_input)
    #     df_trade_prev, df_trade_missing, df_hierarchy_missing_prev, date_prev = get_trade_dmnd(cnxn,df_trade_missing,date_prev,True)
    #     df_trade = df_trade.append(df_trade_prev,ignore_index=True)

    #     df_non_trade, df_non_trade_missing, date_prev = get_non_trade_dmnd(cnxn,df_main,date_input)
    #     df_non_trade_prev, df_non_trade_missing, date_prev = get_non_trade_dmnd(cnxn,df_non_trade_missing,date_prev,True)
    #     df_non_trade = df_non_trade.append(df_non_trade_prev,ignore_index=True)

    #     df = df_trade.dropna().append(df_non_trade.dropna(),ignore_index=True)
    #     df['MONTH'] = date_input
    #     print(df['DEMAND_QTY'].sum())

    #     df_missing = df_trade_missing.append(df_non_trade_missing,ignore_index=True)
    #     df_missing['MONTH'] = date_input
    #     df_missing['CITY'] = None
    #     df_missing = df_missing[["STATE","DISTRICT","CITY","BRAND","GRADE","PACK_TYPE","PACKAGING","CUST_CATEGORY","DEMAND_QTY","MONTH"]]
    #     print(df_missing['DEMAND_QTY'].sum())

    #     print(df_hierarchy_missing['DEMAND_QTY'].sum())

    # df.to_csv('dmnd_h_out.csv',index=False)
    # df_missing.to_csv('dmnd_missing.csv',index=False)
    # df_hierarchy_missing.to_csv('dmnd_h_missing.csv',index=False)

    #################################################################################################################
    # Importing Missing Demand

    # df_main = pd.read_csv('dmnd_missing.csv')

    # df = get_missing_dmnd(cnxn,df_main)
    # df['MONTH'] = date_input

    # print(df['DEMAND_QTY'].sum())
    # df.to_csv('dmnd_missing_out1.csv',index=False)

    ###############################################################################################################

    # cnxn.close()
