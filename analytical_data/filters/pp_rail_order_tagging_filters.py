"""Filter class module for pp_rail_order_tagging model class."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import BooleanFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PpRailOrderTagging


class PpRailOrderTaggingFilter(FilterSet):
    """pp rail order tagging filter class."""

    date = CharInFilter(field_name="run__date", lookup_expr="in")
    shift = CharInFilter(field_name="run__shift", lookup_expr="in")
    plant = CharInFilter(field_name="run__plant", lookup_expr="in")
    run_id = CharInFilter(field_name="run__id", lookup_expr="in")

    class Meta:
        model = PpRailOrderTagging
        fields = ()
