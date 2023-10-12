"""Filter class module for lp schedule plant constraints."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LpSchedulingPlantConstraints


class LpSchedulingPlantConstraintFilter(FilterSet):
    """Lp scheduling plant constraint filter class."""

    grade = CharInFilter(field_name="grade", lookup_expr="in")
    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")

    class Meta:
        model = LpSchedulingPlantConstraints
        fields = ("date",)
