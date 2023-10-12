"""Route restrictions filter module."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import RouteRestrictions


class RouteRestrictionsFilter(FilterSet):
    """Route restrictions filters class."""

    link_id = CharInFilter(field_name="link_id", lookup_expr="in")
    max_size = CharInFilter(field_name="max_size", lookup_expr="in")

    class Meta:
        model = RouteRestrictions
        fields = ()
