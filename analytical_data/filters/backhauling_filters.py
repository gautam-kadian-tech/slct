from django.db.models import Q
from django_filters.rest_framework import BooleanFilter, DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    BackhaulingInboundTruck,
    BackhaulingOpportunities,
)


class BackhaulingOpportunitiesFilter(FilterSet):
    """Backhauling Opportunities filter class."""

    club_id = CharInFilter(field_name="club_id", lookup_expr="in")
    order_master_id = CharInFilter(field_name="order_master__id", lookup_expr="in")
    truck_number = CharInFilter(field_name="inbound__truck_number", lookup_expr="in")
    vehicle_type = CharInFilter(field_name="inbound__vehicle_type", lookup_expr="in")
    vehicle_size = CharInFilter(field_name="inbound__vehicle_size", lookup_expr="in")
    plant = CharInFilter(field_name="inbound__plant_id", lookup_expr="in")
    departure_date = CharInFilter(
        field_name="inbound__departure_date__date", lookup_expr="in"
    )
    destination_state = CharInFilter(
        field_name="inbound__destination_state", lookup_expr="in"
    )
    destination_district = CharInFilter(
        field_name="inbound__destination_district", lookup_expr="in"
    )
    destination_city = CharInFilter(
        field_name="inbound__destination_city", lookup_expr="in"
    )
    status = BooleanFilter(field_name="status", method="filter_status")

    class Meta:
        model = BackhaulingOpportunities
        fields = ()

    def filter_status(self, queryset, name, value):
        if value:
            return queryset.filter(status=value)
        return queryset.exclude(status=True)


class BackhaulingInboundTruckFilter(FilterSet):
    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    truck_number = CharInFilter(field_name="truck_number", lookup_expr="in")
    arrival_date = DateFilter(field_name="arrival_date__date")
    departure_date = DateFilter(field_name="departure_date__date")
    vehicle_type = CharInFilter(field_name="vehicle_type", lookup_expr="in")
    vehicle_size = CharInFilter(field_name="vehicle_size", lookup_expr="in")
    destination_state = CharInFilter(field_name="destination_state", lookup_expr="in")
    destination_district = CharInFilter(
        field_name="destination_district", lookup_expr="in"
    )
    destination_city = CharInFilter(field_name="destination_city", lookup_expr="in")

    class Meta:
        model = BackhaulingInboundTruck
        fields = ()
