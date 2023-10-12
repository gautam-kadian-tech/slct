"""Filter class module for plant constraint master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import RailHandling


class RailHandlingFilter(FilterSet):
    """Rail handling filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")

    class Meta:
        model = RailHandling
        fields = ()
