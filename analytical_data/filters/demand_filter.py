"""Filter class module for demand model data."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import Demand, ZoneMappingNew


class DemandFilter(FilterSet):
    """Demand filter class."""

    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    pack_type = CharInFilter(field_name="pack_type", lookup_expr="in")
    cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")
    demand_qty = CharInFilter(field_name="demand_qty", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    city = CharInFilter(field_name="destination__city", lookup_expr="in")
    district = CharInFilter(field_name="destination__district", lookup_expr="in")
    state = CharInFilter(field_name="destination__state", lookup_expr="in")
    month = CharInFilter(field_name="month__month", lookup_expr="in")
    year = CharInFilter(field_name="month__year", lookup_expr="in")
    system_recommendation_state = CharInFilter(field_name="", method="filter_state")

    class Meta:
        model = Demand
        fields = ()

    def filter_state(self, queryset, name, value):
        districts_list = (
            ZoneMappingNew.objects.filter(state=value[0])
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset.filter(destination__district__in=districts_list)
