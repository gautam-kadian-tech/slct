"""Filter class module for packer shift constraints."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PackerShiftConstraint


class PackerShiftConstraintFilter(FilterSet):
    """Packer shift constraints filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    rated_output = CharInFilter(field_name="rated_output", lookup_expr="in")
    shift = CharInFilter(field_name="shift", lookup_expr="in")
    shift_effeciency = CharInFilter(field_name="shift_effeciency", lookup_expr="in")

    class Meta:
        model = PackerShiftConstraint
        fields = ()
