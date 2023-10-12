"""Filter class module for plant constraint master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PlantConstraintsMaster


class PlantConstraintFilter(FilterSet):
    """Plant constraint filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    railway_siding_available = CharInFilter(
        field_name="railway_siding_available", lookup_expr="in"
    )
    sididng_inside = CharInFilter(field_name="sididng_inside", lookup_expr="in")
    fiscal_benefit = CharInFilter(field_name="fiscal_benefit", lookup_expr="in")

    class Meta:
        model = PlantConstraintsMaster
        fields = ()
