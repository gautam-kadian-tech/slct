"""Filter module for vehicle availability."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import VehicleAvailability


class VehicleAvailabilityFilter(FilterSet):
    """Vehicle availability filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    vehicle_type = CharInFilter(field_name="vehicle_type", lookup_expr="in")
    no_of_vehicles = CharInFilter(field_name="no_of_vehicles", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")

    class Meta:
        model = VehicleAvailability
        fields = ()
