"""Filter module for godown master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PackagingMaster


class PackagingMasterFilter(FilterSet):
    """Packaging master filter class."""

    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    cost = CharInFilter(field_name="cost", lookup_expr="in")

    class Meta:
        model = PackagingMaster
        fields = ()
