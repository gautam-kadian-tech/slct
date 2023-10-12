from datetime import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta as rd

from .connection import connect_db


class TaregtSettingViewHelper:
    def get_targets(cnxn, date):
        date_next = (dt.strptime(date, "%Y-%m-%d") + rd(months=1)).strftime("%Y-%m-%d")

        df_total = pd.read_sql(
            f"""
                select
                tosanact."STATE",
                tosanact."DISTRICT",
                cast(sum("QUANTITY_INVOICED") as int) as "TOTAL_QTY"
                from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" tosanact
                where "INVOICE_DATE" >= '{date}'
                and "INVOICE_DATE" < '{date_next}'
                and "ORDER_CLASSIFICATION" = 'TRADE'
                and "Active" = 1
                and "ORG_ID" in (102,103,104)
                group by
                "STATE","DISTRICT"
            """,
            cnxn,
        )

        df = pd.read_sql(
            f"""
                select
                "STATE",
                "DISTRICT",
                "SALES_TYPE" as "FREIGHT_TYPE"
                ,cast(sum("QUANTITY_INVOICED") as int) as "TARGET"
                from etl_zone."T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB" tosanact
                where "INVOICE_DATE" >= '{date}'
                and "INVOICE_DATE" < '{date_next}'
                and "SALES_TYPE" in ('GD','RD','TP')
                and "ORDER_CLASSIFICATION" = 'TRADE'
                and "Active" = 1
                and "ORG_ID" in (102,103,104)
                group by
                "STATE","DISTRICT","FREIGHT_TYPE"
            """,
            cnxn,
        )

        targets = df.merge(df_total, on=["STATE", "DISTRICT"])

        targets["TARGET"] = round(targets["TARGET"] / targets["TOTAL_QTY"], 2)

        targets.drop(columns=["TOTAL_QTY"], inplace=True)

        return targets

    # if __name__ == "__main__":

    #     cnxn = connect_db()

    #     date = '2023-07-01'

    #     targets = get_targets(cnxn,date)
