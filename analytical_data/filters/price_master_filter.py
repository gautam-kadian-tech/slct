"""Filter class module for plant constraint master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PriceMaster


class PriceMasterFilter(FilterSet):
    """Price master filter class."""

    cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    price = CharInFilter(field_name="price", lookup_expr="in")
    city = CharInFilter(field_name="destination__city", lookup_expr="in")
    district = CharInFilter(field_name="destination__district", lookup_expr="in")
    state = CharInFilter(field_name="destination__state", lookup_expr="in")

    class Meta:
        model = PriceMaster
        fields = ("pack_type",)
