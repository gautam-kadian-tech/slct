"""Filter class module for LP Model."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.enum_classes import LpModelDfFnlBrandChoices
from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LpModelDfFnl, LpModelDfRank


class LpModelDfFnlFilter(FilterSet):
    """LpModelDfFnl filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    mode = CharInFilter(field_name="mode", lookup_expr="in")
    destination_city = CharInFilter(field_name="destination_city", lookup_expr="in")
    destination_state = CharInFilter(field_name="destination_state", lookup_expr="in")
    destination_district = CharInFilter(
        field_name="destination_district", lookup_expr="in"
    )
    primary_secondary_route = CharInFilter(
        field_name="primary_secondary_route", lookup_expr="in"
    )
    route_id = CharInFilter(field_name="route_id", lookup_expr="in")
    node_city = CharInFilter(field_name="node_city", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    freight_type = CharInFilter(field_name="freight_type", lookup_expr="in")

    class Meta:
        model = LpModelDfFnl
        fields = ()


class LpModelDfFnlOrderMasterEditFilter(FilterSet):
    """LpModelDfFnl Order MasterEdit filter class."""

    ship_city = CharInFilter(field_name="destination_city", lookup_expr="in")
    ship_state = CharInFilter(field_name="destination_state", lookup_expr="in")
    ship_district = CharInFilter(field_name="destination_district", lookup_expr="in")
    cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")
    pack_type = CharInFilter(field_name="pack_type", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    brand = CharInFilter(field_name="brand", method="filter_brand")

    class Meta:
        model = LpModelDfRank
        fields = ("brand", "grade")

    def filter_brand(self, queryset, field_name, value):
        """apply custom filtering on farm group name"""
        try:
            filter_value = LpModelDfFnlBrandChoices[value[0]].value
        except KeyError:
            filter_value = None
        return queryset.filter(brand=filter_value)
