"""Top down target view helper module."""
from django.db.models import Count

from analytical_data.models import DfTopDownTargets
from analytical_data.view_helpers.kacha_pakka_view_helper import KachaPakkaViewHelper


class TopDownTargetDropdownHelper(KachaPakkaViewHelper):
    """Top down targets view helper class."""

    @classmethod
    def __get_top_down_targets_query(cls, query_string):
        return DfTopDownTargets.objects.values_list(query_string, flat=True).annotate(
            Count(query_string)
        )

    @classmethod
    def _get_dropdown_data(cls, filters):
        return {
            **cls._get_states_cities(filters),
            "brand": cls.__get_top_down_targets_query("brand"),
            "product": cls.__get_top_down_targets_query("product"),
        }
