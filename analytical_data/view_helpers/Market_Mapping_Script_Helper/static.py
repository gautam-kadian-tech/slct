threshold = {
    "Haryana": 0.5,
    "Bhiwani": 0.2,
    "Uttar Pradesh": 0.5,
    "Telangana": 0.3,
}


org_brand_map = {102: "SHREE", 103: "BANGUR", 104: "ROCKSTRONG"}

ncr_avg_sql = """select foo."STATE", foo."DISTRICT", foo."BRAND", foo."PRODUCT",
                round(sum(foo."NCR"*foo."QUANTITY_INVOICED")/sum(foo."QUANTITY_INVOICED"),0) as "NCR",
                sum(foo."QUANTITY_INVOICED") as "QUANTITY_INVOICED"
                from(
                select "STATE"
                ,"DISTRICT"
                ,"INVOICE_DATE"
                ,"ORG_ID" as "BRAND"
                ,"PRODUCT"
                , round(AVG("NCR"),0) as "NCR"
                ,sum("QUANTITY_INVOICED") as "QUANTITY_INVOICED"
                from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
                where "INVOICE_DATE" >= '2021-12-01'
                and "QUANTITY_INVOICED" > 0
                and "INVOICE_DATE" < '2022-03-01'
                and "PRODUCT" in ('PPC','OPC_43','OPC_53')
                and "Active" != 0
                group by "STATE", "DISTRICT","INVOICE_DATE", "ORG_ID", "PRODUCT"
                ) as foo
                group by foo."STATE", foo."DISTRICT", foo."BRAND", foo."PRODUCT"
                """

market_pos = {
    "High|High": "Strong",
    "High|Low": "Growing",
    "Low|High": "De-growing",
    "Low|Low": "Weak",
}

market_luc = {
    "High|High": "Highly Lucrative",
    "High|Low": "Profit Driver",
    "Low|High": "Volume Driver",
    "Low|Low": "Not Lucrative",
}


market_growth = {
    "Strong|Highly Lucrative": "Maintain MS",
    "Strong|Profit Driver": "Maintain MS",
    "Strong|Volume Driver": "Maintain MS",
    "Strong|Not Lucrative": "Maintain MS",
    "De-growing|Highly Lucrative": "Grow Aggressively",
    "De-growing|Profit Driver": "Grow Aggressively",
    "De-growing|Volume Driver": "Grow Aggressively",
    "De-growing|Not Lucrative": "Maintain MS",
    "Growing|Highly Lucrative": "Grow Aggressively",
    "Growing|Profit Driver": "Grow Aggressively",
    "Growing|Volume Driver": "Maintain MS",
    "Growing|Not Lucrative": "Maintain MS",
    "Weak|Highly Lucrative": "Grow Aggressively",
    "Weak|Profit Driver": "Grow Aggressively",
    "Weak|Volume Driver": "Grow Aggressively",
    "Weak|Not Lucrative": "Maintain MS",
}

pricing_strategy_map = {
    "Strong|Highly Lucrative": "Assertive",
    "Strong|Profit Driver": "Accommodative",
    "Strong|Volume Driver": "Aggressive",
    "Strong|Not Lucrative": "Aggressive",
    "De-growing|Highly Lucrative": "Accommodative",
    "De-growing|Profit Driver": "Accommodative",
    "De-growing|Volume Driver": "Assertive",
    "De-growing|Not Lucrative": "Assertive",
    "Growing|Highly Lucrative": "Aggressive",
    "Growing|Profit Driver": "Accommodative",
    "Growing|Volume Driver": "Aggressive",
    "Growing|Not Lucrative": "Aggressive",
    "Weak|Highly Lucrative": "Accommodative",
    "Weak|Profit Driver": "Accommodative",
    "Weak|Volume Driver": "Assertive",
    "Weak|Not Lucrative": "Assertive",
}

# ------------------------------------------STATE--------------------------------

market_pos = {
    "High|High": "Strong",
    "High|Low": "Growing",
    "Low|High": "De-growing",
    "Low|Low": "Weak",
}

market_luc = {
    "High|High": "Highly Lucrative",
    "High|Low": "Profit Driver",
    "Low|High": "Volume Driver",
    "Low|Low": "Not Lucrative",
}


# market_growth = {'Strong|Highly Lucrative': 'Maintain MS',
#                  'Strong|Profit Driver': 'Maintain MS',
#                  'Strong|Volume Driver': 'Maintain MS',
#                  'Strong|Not Lucrative': 'Maintain MS',

#                  'De-growing|Highly Lucrative': 'Grow Aggressively',
#                  'De-growing|Profit Driver': 'Grow Aggressively',
#                  'De-growing|Volume Driver': 'Grow Incrementally',
#                  'De-growing|Not Lucrative': 'Maintain MS',

#                  'Growing|Highly Lucrative': 'Grow Aggressively',
#                  'Growing|Profit Driver': 'Grow Incrementally',
#                  'Growing|Volume Driver': 'Maintain MS',
#                  'Growing|Not Lucrative': 'Maintain MS',

#                  'Weak|Highly Lucrative': 'Grow Aggressively',
#                  'Weak|Profit Driver': 'Grow Aggressively',
#                  'Weak|Volume Driver': 'Grow Incrementally',
#                  'Weak|Not Lucrative': 'Maintain MS',

#                  }

growth_potential_sql = """
select
upper(mmgp."STATE") as "STATE",mmgp."MONTH",mmgp."TARGET_TYPE",mmgp."PREVIOUS",mmgp."CURRENT",mmgp."NEXT",upper(shm."ZONE") as "ZONE"
from etl_zone."MARKET_MAPPING_GROWTH_POTENTIAL" mmgp
inner join(
select distinct on ("STATE_SCL","ZONE_SCL") "ZONE_SCL" as "ZONE","STATE_SCL" from etl_zone."SCL_HIERARCHY_MASTER"
) shm on upper(shm."STATE_SCL") = upper(mmgp."STATE")
where "MONTH" = '{month}'
"""

market_potential_sql = f"""
select
mmgp."ID" ,	upper(mmgp."STATE") as "STATE",	upper(mmgp."DISTRICT") as "DISTRICT" ,	mmgp."BRAND" ,	mmgp."MONTH" ,	mmgp."SALES" ,	mmgp."MARKET_POTENTIAL" ,	mmgp."MARKET_SHARE" ,upper(shm."ZONE") as "ZONE",upper(shm."REGION") as "REGION"
from etl_zone."MARKET_MAPPING_MARKET_POTENTIAL" mmgp
inner join(
select distinct on ("STATE_SCL","DISTRICT_SCL","ZONE_SCL","REGION_SCL") "ZONE_SCL" as "ZONE","REGION_SCL" as "REGION","STATE_SCL","DISTRICT_SCL" from etl_zone."SCL_HIERARCHY_MASTER"
) shm on upper(shm."STATE_SCL") = upper(mmgp."STATE") and upper(shm."DISTRICT_SCL") = upper(mmgp."DISTRICT")
"""

ncr_3_year_sql = """
select
upper(shm."ZONE_SCL") as "ZONE",
upper(shm."STATE_SCL") as "STATE",
upper(shm."REGION_SCL") as "REGION",
upper(shm."DISTRICT_SCL") as "DISTRICT",
tosanact."ORG_ID" as "BRAND",
tosanact."PRODUCT",
cast(concat(extract(year from tosanact."INVOICE_DATE"),'-',extract(month from tosanact."INVOICE_DATE"),'-01') as date) as "MONTH",
cast(sum(tosanact."NCR"*tosanact."QUANTITY_INVOICED")/sum(tosanact."QUANTITY_INVOICED") as int) as "NCR",
sum(tosanact."QUANTITY_INVOICED") as "QUANTITY_INVOICED"
from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" tosanact
inner join(
select distinct on ("STATE_ERP","DISTRICT_ERP") * from etl_zone."SCL_HIERARCHY_MASTER" shm
) shm on upper(shm."STATE_ERP") = upper(tosanact."STATE")
and upper(shm."DISTRICT_ERP") = upper(tosanact."DISTRICT")
where "INVOICE_DATE" >= '2019-01-01'
and "INVOICE_DATE" < '{month}'
and "ORG_ID" != 101
and "QUANTITY_INVOICED" > 0
and "Active" != 0
group by
shm."ZONE_SCL",shm."STATE_SCL",shm."REGION_SCL",shm."DISTRICT_SCL",
"BRAND","PRODUCT","MONTH"
"""

ncr_threshold_sql = """
select foo."ZONE",foo."STATE",foo."REGION", upper(foo."DISTRICT") as "DISTRICT", foo."BRAND", foo."PRODUCT",
round(sum(foo."NCR"*foo."QUANTITY_INVOICED")/sum(foo."QUANTITY_INVOICED"),0) as "NCR",
sum(foo."QUANTITY_INVOICED") as "QUANTITY_INVOICED"
from(
select
upper(shm."ZONE_SCL") as "ZONE",
upper(shm."STATE_SCL") as "STATE",
upper(shm."REGION_SCL") as "REGION",
upper(shm."DISTRICT_SCL") as "DISTRICT",
tosanact."ORG_ID" as "BRAND",
tosanact."PRODUCT",
cast(concat(extract(year from tosanact."INVOICE_DATE"),'-',extract(month from tosanact."INVOICE_DATE"),'-01') as date) as "MONTH",
cast(sum(tosanact."NCR"*tosanact."QUANTITY_INVOICED")/sum(tosanact."QUANTITY_INVOICED") as int) as "NCR",
sum(tosanact."QUANTITY_INVOICED") as "QUANTITY_INVOICED"
from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" tosanact
inner join(
select distinct on ("STATE_ERP","DISTRICT_ERP") * from etl_zone."SCL_HIERARCHY_MASTER" shm
) shm on upper(shm."STATE_ERP") = upper(tosanact."STATE")
and upper(shm."DISTRICT_ERP") = upper(tosanact."DISTRICT")
where "INVOICE_DATE" >= '{month_start}'
and "INVOICE_DATE" < '{month}'
and "ORG_ID" != 101
and "QUANTITY_INVOICED" > 0
and "Active" != 0
group by shm."ZONE_SCL",shm."STATE_SCL",shm."REGION_SCL",shm."DISTRICT_SCL","BRAND","PRODUCT","MONTH"
) as foo
group by foo."ZONE",foo."STATE",foo."REGION", foo."DISTRICT", foo."BRAND", foo."PRODUCT"
"""

channel_data_sql = """
select
"BRAND"
,"STATE"
,"TALUKA"
,"DISTRICT"
,"ADDRESS_BLOCK"
,"ERP_CUSTOMER_NUMBER" as "COUNTER_CODE"
,"COUNTER_NAME"
,case "COUNTER_TYPE"
	when 'D' then 'Dealer'
	when 'R' then 'Retailer'
	else "COUNTER_TYPE"
end as "COUNTER_TYPE"
,"LATITUDE" as "LAT"
,"LONGITUDE" as "LONG"
,"ROUTE"
,"TOTAL_RETAIL_SALE" as "TOTAL_RETAIL_SALES"
,"TOTAL_WHOLE_SALE" as "TOTAL_WHOLESALE"
,"SHREE_WHOLESALE"
,"SHREE_RETAIL" as "SHREE_RETAIL_SALE"
,"BANGUR_WHOLESALE"
,"BANGUR_RETAIL" as "BANGUR_RETAIL_SALE"
,"ROCKSTRONG_WHOLESALE"
,"ROCKSTRONG_RETAIL" as "ROCKSTRONG_RETAIL_SALE"
,"COUNTER_ID"
from etl_zone."SCL_CUSTOMER_MARKET_MAPPING" scmm
"""

price_data_sql = """
select
"ZONE"
,pitai."STATE"
,"REGION"
,pitai."DISTRICT"
,"BRAND"
,"PRICE_TYPE" as "PRICE"
,"DATE"
,"PRICE" as "MARKET SHARE"
from etl_zone."PRICING_INPUT_TEMPLATE_ALL_INDIA" pitai
inner join(
select distinct on ("STATE_SCL","DISTRICT_SCL","ZONE_SCL","REGION_SCL") "ZONE_SCL" as "ZONE","REGION_SCL" as "REGION","STATE_SCL","DISTRICT_SCL" from etl_zone."SCL_HIERARCHY_MASTER"
) shm on shm."STATE_SCL" = pitai."STATE" and shm."DISTRICT_SCL" = pitai."DISTRICT"
"""

branding_budget_sql = """
select
"STATE" as "State",
"DISTRICT" as "District",
"BRAND" as "Brand",
"TOT_COST_RS_LAC" as "TOT_COST_RS_LAC"
from etl_zone."MARKET_MAPPING_BRANDING_BUDGET"
"""
