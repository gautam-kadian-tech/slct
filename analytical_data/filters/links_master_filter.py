"""Filter class module for links master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LinksMaster


class LinksMasterFilter(FilterSet):
    """Links master filter class."""

    mode = CharInFilter(field_name="mode", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")
    primary_secondary_route = CharInFilter(
        field_name="primary_secondary_route", lookup_expr="in"
    )
    source_name = CharInFilter(field_name="source_name", lookup_expr="in")
    source_district = CharInFilter(field_name="source_district", lookup_expr="in")
    source_state = CharInFilter(field_name="source_state", lookup_expr="in")
    destination_district = CharInFilter(
        field_name="destination_district", lookup_expr="in"
    )
    destination_state = CharInFilter(field_name="destination_state", lookup_expr="in")
    destination_city = CharInFilter(field_name="destination_city", lookup_expr="in")
    plant = CharInFilter(field_name="plant", lookup_expr="in")
    warehouse = CharInFilter(field_name="warehouse", lookup_expr="in")
    freight_type = CharInFilter(field_name="freight_type", lookup_expr="in")
    cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")

    class Meta:
        model = LinksMaster
        fields = ()
