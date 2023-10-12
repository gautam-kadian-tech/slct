"""Lp model df fnl output screen options dropdown api view helper."""
from django.db.models import Count, Q

from analytical_data.models import LpModelDfFnl
from analytical_data.view_helpers.plant_product_master_helper import (
    PlantProductMasterDropdownHelper,
)


class OutputScreenDropdownHelper(PlantProductMasterDropdownHelper):
    """Helper class"""

    @classmethod
    def __get_output_screen_query(self, query_string, query=Q()):
        return (
            LpModelDfFnl.objects.filter(query)
            .values_list(query_string, flat=True)
            .distinct(query_string)
            .order_by(query_string)
        )

    @classmethod
    def _get_dropdown_data(cls, query_params):
        """Returns LpModelDfFnl output screen dropdown data."""
        return {
            "destination_state": cls.__get_output_screen_query("destination_state"),
            "destination_district": cls.__get_output_screen_query(
                "destination_district",
                Q(destination_state=query_params.get("destination_state")),
            ),
            "destination_city": cls.__get_output_screen_query(
                "destination_city",
                Q(
                    destination_state=query_params.get("destination_state"),
                    destination_district=query_params.get("destination_district"),
                ),
            ),
            "plant": super()._get_plant_query("plant_id"),
            "mode": ["RAIL", "ROAD"],
            # "city": cls.__get_df_fnl_output_dropdown_data("destination_city"),
            # "state": cls.__get_df_fnl_output_dropdown_data("destination_state"),
            # "district": cls.__get_df_fnl_output_dropdown_data("destination_district"),
            "primary_secondary_route": ["PRIMARY", "SECONDARY"],
            "brand": cls.__get_df_fnl_output_dropdown_data("brand"),
            "grade": cls.__get_df_fnl_output_dropdown_data("grade"),
        }

    @classmethod
    def __get_df_fnl_output_dropdown_data(cls, query_param):
        """"""
        return LpModelDfFnl.objects.values_list(query_param, flat=True).annotate(
            Count(query_param)
        )
