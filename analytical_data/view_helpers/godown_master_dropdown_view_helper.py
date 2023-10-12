"""Rail handling view helper module."""
from django.db.models import Count, Q

from analytical_data.models import GodownMaster


class GodownMasterDropdownHelper:
    """Godown Master dropdown view helper."""

    @classmethod
    def __get_godown_master_query(self, query_string, query=Q()):
        return (
            GodownMaster.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    @classmethod
    def _get_dropdown_data(cls, query_params):
        """Returns dropdown data for Godown Master list."""
        return {
            "state": cls.__get_godown_master_query("state"),
            "district": cls.__get_godown_master_query(
                "district", Q(state=query_params.get("state"))
            ),
            "city": cls.__get_godown_master_query(
                "city",
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
        }
