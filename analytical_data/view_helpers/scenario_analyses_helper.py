"""Helper module for LpModelDfFnlScenarioAnalysisView view."""
import numpy as np

from analytical_data.view_helpers.lp_model_output_screen_helper import (
    LpModelOutputScreenViewHelper,
)


class LpModelScenarioAnalysisHelper(LpModelOutputScreenViewHelper):
    """Helper class"""

    @classmethod
    def get_output_data(cls, ncr, df_fnl):
        """Returns scenario analysis data."""
        source_view_ncr = ncr.copy()
        source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].multiply(
            source_view_ncr["QTY"], axis="index"
        )

        source_view_ncr = source_view_ncr.groupby(
            [
                "DESTINATION_CITY",
                "DESTINATION_DISTRICT",
                "DESTINATION_STATE",
                "PLANT_ID",
                "MODE",
                "PRIMARY_SECONDARY_ROUTE",
                "NODE_CITY",
                "GRADE",
            ],
            as_index=False,
        )[
            [
                "QTY",
                "TLC",
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].sum()

        source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].divide(
            source_view_ncr["QTY"], axis="index"
        )

        source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_ncr[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].astype(
            "int"
        )

        source_view_ncr.sort_values(
            [
                "DESTINATION_CITY",
                "DESTINATION_DISTRICT",
                "DESTINATION_STATE",
                "PLANT_ID",
                "MODE",
                "PRIMARY_SECONDARY_ROUTE",
                "NODE_CITY",
                "GRADE",
            ],
            inplace=True,
        )

        source_view_ncr["TLC"] = source_view_ncr["TLC"].astype("int")

        source_view_ncr.set_index(
            ["DESTINATION_CITY", "DESTINATION_DISTRICT", "DESTINATION_STATE", "GRADE"],
            inplace=True,
        )

        source_view_ncr = source_view_ncr.add_suffix("_OUTPUT1")

        source_view_fnl = df_fnl.copy()
        source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].multiply(
            source_view_fnl["QTY"], axis="index"
        )

        source_view_fnl = source_view_fnl.groupby(
            [
                "DESTINATION_CITY",
                "DESTINATION_DISTRICT",
                "DESTINATION_STATE",
                "PLANT_ID",
                "MODE",
                "PRIMARY_SECONDARY_ROUTE",
                "NODE_CITY",
                "GRADE",
            ],
            as_index=False,
        )[
            [
                "QTY",
                "TLC",
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].sum()

        source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].divide(
            source_view_fnl["QTY"], axis="index"
        )

        source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ] = source_view_fnl[
            [
                "PRICE",
                "PRIMARY_FRT",
                "SECONDARY_FRT",
                "DISCOUNT",
                "TAXES",
                "MISC_CHARGES",
                "HA_COMMISSION",
                "DEMURRAGE",
                "DAMAGES",
                "RAKE_CHARGES",
                "SP_COMMISSION",
                "ISP_COMMISSION",
                "CLINKER_FREIGHT",
                "VARIABLE_PRODUCTION_COST",
            ]
        ].astype(
            "int"
        )

        source_view_fnl.sort_values(
            [
                "DESTINATION_CITY",
                "DESTINATION_DISTRICT",
                "DESTINATION_STATE",
                "PLANT_ID",
                "MODE",
                "PRIMARY_SECONDARY_ROUTE",
                "NODE_CITY",
                "GRADE",
            ],
            inplace=True,
        )

        source_view_fnl["TLC"] = source_view_fnl["TLC"].astype("int")

        source_view_fnl.set_index(
            ["DESTINATION_CITY", "DESTINATION_DISTRICT", "DESTINATION_STATE", "GRADE"],
            inplace=True,
        )

        source_view_fnl = source_view_fnl.add_suffix("_OUTPUT2")

        combined = source_view_ncr.merge(
            source_view_fnl, how="outer", left_index=True, right_index=True
        ).reset_index()

        combined.loc[
            combined.duplicated(
                [
                    "DESTINATION_CITY",
                    "DESTINATION_DISTRICT",
                    "DESTINATION_STATE",
                    "GRADE",
                    "PLANT_ID_OUTPUT2",
                    "MODE_OUTPUT2",
                    "PRIMARY_SECONDARY_ROUTE_OUTPUT2",
                    "NODE_CITY_OUTPUT2",
                ]
            ),
            [
                "PLANT_ID_OUTPUT2",
                "MODE_OUTPUT2" "PRIMARY_SECONDARY_ROUTE_OUTPUT2",
                "NODE_CITY_OUTPUT2",
                "QTY_OUTPUT2",
                "TLC_OUTPUT2",
                "PRICE_OUTPUT2",
                "PRIMARY_FRT_OUTPUT2",
                "SECONDARY_FRT_OUTPUT2",
                "DISCOUNT_OUTPUT2",
                "TAXES_OUTPUT2",
                "MISC_CHARGES_OUTPUT2",
                "HA_COMMISSION_OUTPUT2",
                "DEMURRAGE_OUTPUT2",
                "DAMAGES_OUTPUT2",
                "RAKE_CHARGES_OUTPUT2",
                "SP_COMMISSION_OUTPUT2",
                "ISP_COMMISSION_OUTPUT2",
                "CLINKER_FREIGHT_OUTPUT2",
                "VARIABLE_PRODUCTION_COST",
            ],
        ] = 0
        combined.loc[
            combined.duplicated(
                [
                    "DESTINATION_CITY",
                    "DESTINATION_DISTRICT",
                    "DESTINATION_STATE",
                    "GRADE",
                    "PLANT_ID_OUTPUT1",
                    "MODE_OUTPUT1",
                    "PRIMARY_SECONDARY_ROUTE_OUTPUT1",
                    "NODE_CITY_OUTPUT1",
                ]
            ),
            [
                "PLANT_ID_OUTPUT1",
                "MODE_OUTPUT1",
                "PRIMARY_SECONDARY_ROUTE_OUTPUT1",
                "NODE_CITY_OUTPUT1",
                "QTY_OUTPUT1",
                "TLC_OUTPUT1",
                "PRICE_OUTPUT1",
                "PRIMARY_FRT_OUTPUT1",
                "SECONDARY_FRT_OUTPUT1",
                "DISCOUNT_OUTPUT1",
                "TAXES_OUTPUT1",
                "MISC_CHARGES_OUTPUT1",
                "HA_COMMISSION_OUTPUT1",
                "DEMURRAGE_OUTPUT1",
                "DAMAGES_OUTPUT1",
                "RAKE_CHARGES_OUTPUT1",
                "SP_COMMISSION_OUTPUT1",
                "ISP_COMMISSION_OUTPUT1",
                "CLINKER_FREIGHT_OUTPUT1",
                "VARIABLE_PRODUCTION_COST",
            ],
        ] = 0
        combined.set_index(
            ["DESTINATION_CITY", "DESTINATION_DISTRICT", "DESTINATION_STATE", "GRADE"],
            inplace=True,
        )

        columns = [
            "PRICE",
            "PRIMARY_FRT",
            "SECONDARY_FRT",
            "DISCOUNT",
            "TAXES",
            "MISC_CHARGES",
            "HA_COMMISSION",
            "DEMURRAGE",
            "DAMAGES",
            "RAKE_CHARGES",
            "SP_COMMISSION",
            "ISP_COMMISSION",
            "CLINKER_FREIGHT",
            "VARIABLE_PRODUCTION_COST",
        ]
        combined[[f"{column}_OUTPUT2" for column in columns]] = combined[
            [f"{column}_OUTPUT2" for column in columns]
        ].astype("float")
        combined[[f"{column}_OUTPUT1" for column in columns]] = combined[
            [f"{column}_OUTPUT1" for column in columns]
        ].astype("float")
        for column in columns:
            try:
                # combined[f"{column}_OUTPUT2_wt"] = combined.groupby(combined.index).apply(
                #     lambda x: np.average(x[f"{column}_OUTPUT2"], weights=x["QTY_OUTPUT2"])
                # )
                # combined[f"{column}_OUTPUT1_wt"] = combined.groupby(combined.index).apply(
                #     lambda x: np.average(x[f"{column}_OUTPUT1"], weights=x["QTY_OUTPUT1"])
                # )
                combined[f"{column}_OUTPUT2_wt"] = 1
                combined[f"{column}_OUTPUT1_wt"] = 2
            except Exception as e:
                print(e)
                pass
        combined["TLC_OUTPUT2_wt"] = combined.groupby(combined.index)[
            "TLC_OUTPUT2"
        ].sum()
        combined["TLC_OUTPUT1_wt"] = combined.groupby(combined.index)[
            "TLC_OUTPUT1"
        ].sum()

        combined.reset_index(inplace=True)

        combined.loc[
            combined.duplicated([f"{column}_OUTPUT2_wt" for column in columns]),
            [f"{column}_OUTPUT2_wt" for column in columns] + ["TLC_OUTPUT2_wt"],
        ] = np.nan
        combined.loc[
            combined.duplicated([f"{column}_OUTPUT1_wt" for column in columns]),
            [f"{column}_OUTPUT1_wt" for column in columns] + ["TLC_OUTPUT1_wt"],
        ] = np.nan

        return combined.replace(0, np.nan).loc[
            :,
            combined.columns.str.endswith(
                ("OUTPUT1_wt", "OUTPUT1", "OUTPUT2_wt", "OUTPUT2")
            ),
        ]
