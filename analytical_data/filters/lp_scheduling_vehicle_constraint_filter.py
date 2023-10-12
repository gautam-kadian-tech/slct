"""Filter class module for lp schedule vehicle constraints."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LpSchedulingVehicleConstraints


class LpSchedulingVehicleConstraintFilter(FilterSet):
    """Lp scheduling vehicle constraint filter class."""

    vehicle_type = CharInFilter(field_name="vehicle_type", lookup_expr="in")
    plant = CharInFilter(field_name="plant", lookup_expr="in")

    class Meta:
        model = LpSchedulingVehicleConstraints
        fields = ("date",)
