import datetime

import numpy as np
import pandas as pd


class PackingPlantHelper:
    """
    Packing Plant AAC View Helper
    for calculation of datetime difference and it's average
    and keeping all the items list needed to filter
    """

    # list of items need to filter
    items_list_aac = [
        "AACB_625200075",
        "AACB_215100075",
        "AACB_600200200",
        "AACB_625240200",
        "AACB_625240100",
        "AACB_625250300",
        "AACB_625200100",
        "AACB_625250225",
        "AACB_625250200",
        "AACB_625250150",
        "AACB_625250125",
        "AACB_625250100",
        "AACB_625240115",
        "AACB_625230200",
        "AACB_150075050",
        "AACB_625200115",
        "AACB_625240150",
        "AACB_600200300",
        "AACB_625250230",
        "AACB_625250090",
        "AACB_600250225",
        "AACB_600250150",
        "AACB_600250100",
        "AACB_600250200",
        "AACB_625250115",
        "RUBBLE.",
        "AACB_625200225",
        "AACB_625200200",
        "AACB_625200150",
        "AACB_625200125",
        "BLOCKJOIN40",
    ]

    items_list_cement = [
        "OPC_43",
        "OPC_53",
        "PPC",
        "PSC",
        "SSC",
        "CC",
        "PPC_ROOFON",
        "OPC_53_PREMIUM",
        "PPC_S",
    ]

    def calculate_average(data):
        """
        Function to calculate the difference and average datetime
        """
        response_data = {}
        # converting the serializer's data to pandas dataframe
        df = pd.DataFrame(data)

        # converting all the datetimes from string to Pandas DateTime Format
        df["tare"] = pd.to_datetime(df["tare"], format="%d-%b-%Y %X")
        df["sec_in"] = pd.to_datetime(df["sec_in"], format="%d-%b-%Y %X")
        df["pp_in"] = pd.to_datetime(df["pp_in"], format="%d-%b-%Y %X")
        df["pp_out"] = pd.to_datetime(df["pp_out"], format="%d-%b-%Y %X")
        df["tax_invoice_date"] = pd.to_datetime(
            df["tax_invoice_date"], format="%d-%b-%Y %X"
        )
        df["dilink"] = pd.to_datetime(df["dilink"], format="%d-%b-%Y %X")
        df["gate_entry_time"] = pd.to_datetime(
            df["gate_entry_time"], format="%d-%b-%Y %X"
        )
        df["ppcal_in"] = pd.to_datetime(df["ppcal_in"], format="%d-%b-%Y %X")
        df["ppcal_out"] = pd.to_datetime(df["ppcal_out"], format="%d-%b-%Y %X")
        df["gate_exit_time"] = pd.to_datetime(
            df["gate_exit_time"], format="%d-%b-%Y %X"
        )
        df["gross_wt_time"] = pd.to_datetime(df["gross_wt_time"], format="%d-%b-%Y %X")
        df["sec_out"] = pd.to_datetime(df["sec_out"], format="%d-%b-%Y %X")

        # calculating date difference in new dataframe (dividing with 60 for getting minutes)

        df_out = pd.DataFrame()

        df_out["yard_reg_to_di_link_reason"] = (
            df["dilink"] - df["gate_entry_time"]
        ) / 60
        df_out["di_link_to_pp_call_reason"] = (df["ppcal_in"] - df["dilink"]) / 60
        df_out["pp_call_to_sec_in_time_reason"] = (df["sec_in"] - df["ppcal_in"]) / 60
        df_out["sec_in_to_tare_reason"] = (df["tare"] - df["sec_in"]) / 60
        df_out["tare_to_pp_in_reason"] = (df["pp_in"] - df["tare"]) / 60
        df_out["pp_in_to_pp_out_reason"] = (df["pp_out"] - df["pp_in"]) / 60
        df_out["pp_out_to_invoice_reason"] = (
            df["tax_invoice_date"] - df["pp_out"]
        ) / 60
        df_out["invoice_to_gross_wt_reason"] = (
            (df["gross_wt_time"] - df["tax_invoice_date"]) / 60
        ).abs()
        df_out["gross_wt_to_sec_out_reason"] = (
            df["sec_out"] - df["gross_wt_time"]
        ) / 60
        df_out["sec_out_to_plant_out_reason"] = (
            df["gate_exit_time"] - df["sec_out"]
        ) / 60

        df_out["total_ard_time"] = (
            df_out["yard_reg_to_di_link_reason"]
            + df_out["di_link_to_pp_call_reason"]
            + df_out["pp_call_to_sec_in_time_reason"]
        )

        df_out["plant_time"] = (
            df_out["sec_in_to_tare_reason"]
            + df_out["tare_to_pp_in_reason"]
            + df_out["pp_in_to_pp_out_reason"]
            + df_out["pp_out_to_invoice_reason"]
            + df_out["gross_wt_to_sec_out_reason"]
            + df_out["invoice_to_gross_wt_reason"]
            + df_out["sec_out_to_plant_out_reason"]
        )

        # averaging non negative values
        for element in df_out.columns.to_list():
            response_data[element] = str(
                round(
                    float(
                        df_out.loc[
                            df_out[element] >= datetime.timedelta(minutes=0), element
                        ]
                        .mean()
                        .total_seconds()
                    ),
                    2,
                )
            )

        response_data["plant_name"] = df["plant_name"][0]
        response_data["organization_code"] = df["organization_code"][0]

        return response_data
