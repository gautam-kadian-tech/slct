"""Filter modules for FactNtSalesPlanAnnual  """
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    FactNtSalesPlanAnnual,
    FactNtSalesPlanningMonth,
    FactNtSalesPlanningNcr,
    DimCustomersTest,
)


class FactNtSalesPlanAnnualFilter(FilterSet):
    """FactNtSalesPlanAnnual filter class."""

    year = CharInFilter(field_name="year", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    plan_type = CharInFilter(field_name="plan_type", lookup_expr="in")

    class Meta:
        model = FactNtSalesPlanAnnual
        fields = ()


class FactNtSalesPlanningMonthFilter(FilterSet):
    """FactNtSalesPlanningMonth filter class."""

    year = CharInFilter(field_name="year", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    resource = CharInFilter(field_name="resource", lookup_expr="in")

    class Meta:
        model = FactNtSalesPlanningMonth
        fields = ()


class FactNtSalesPlanningNcrFilter(FilterSet):
    """FactNtSalesPlanningMonth filter class."""

    year = CharInFilter(field_name="year", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    resource = CharInFilter(field_name="resource", lookup_expr="in")

    class Meta:
        model = FactNtSalesPlanningNcr
        fields = ()


class DimCustomersTestFilter(FilterSet):
    """FactNtSalesPlanningMonth filter class."""

    account_number = CharInFilter(field_name="account_number", lookup_expr="in")

    class Meta:
        model = DimCustomersTest
        fields = ()
