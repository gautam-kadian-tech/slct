"""Rail handling view helper module."""
from django.db.models import Count, Q

from analytical_data.models import RailHandling


class RailHandlingDropdownHelper:
    """Rail handling dropdown view helper."""

    @classmethod
    def __get_rail_handling_query(self, query_string, query=Q()):
        return (
            RailHandling.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    @classmethod
    def _get_dropdown_data(cls, query_params):
        """Returns dropdown data for Rail Handling list."""
        return {
            "state": cls.__get_rail_handling_query("state"),
            "district": cls.__get_rail_handling_query(
                "district", Q(state=query_params.get("state"))
            ),
            # "city": cls.__get_rail_handling_query(
            #     "city",
            #     Q(
            #         state=query_params.get("state"),
            #         district=query_params.get(
            #             "district"
            #         ),
            #     ),
            # ),
            "taluka": cls.__get_rail_handling_query(
                "taluka",
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
            "freight_type": cls.__get_rail_handling_query("freight_type"),
        }
