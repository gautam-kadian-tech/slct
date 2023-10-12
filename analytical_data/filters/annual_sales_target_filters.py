"""Filter module for FactNtSalesPlanning."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.non_trade_head_models import FactNtSalesPlanning


class FactNtSalesPlanningFilter(FilterSet):
    """fact nt sales planning filter class."""

    brand = CharInFilter(field_name="brand", lookup_expr="in")
    period_key__year = CharInFilter(field_name="period_key__year", lookup_expr="in")
    so_key = DateFilter(field_name="so_key", lookup_expr="in")
    kam_key = DateFilter(field_name="kam_key", lookup_expr="in")
    product = DateFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = FactNtSalesPlanning
        fields = ()
