# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 16:06:55 2022

@author: tanay
"""

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
                and "Active" = 1
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
    "De-growing|Volume Driver": "Grow Incrementally",
    "De-growing|Not Lucrative": "Maintain MS",
    "Growing|Highly Lucrative": "Grow Aggressively",
    "Growing|Profit Driver": "Grow Incrementally",
    "Growing|Volume Driver": "Maintain MS",
    "Growing|Not Lucrative": "Maintain MS",
    "Weak|Highly Lucrative": "Grow Aggressively",
    "Weak|Profit Driver": "Grow Aggressively",
    "Weak|Volume Driver": "Grow Incrementally",
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
