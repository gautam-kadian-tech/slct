"""Filter module for godown master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import GodownMaster


class GodownMasterFilter(FilterSet):
    """Godown master filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    capacity = CharInFilter(field_name="capacity", lookup_expr="in")

    class Meta:
        model = GodownMaster
        fields = ()
