"""Filter class module for lp schedule packer constraints."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LpSchedulingPackerConstraints


class LpSchedulingPackerConstraintFilter(FilterSet):
    """Lp scheduling packer constraints filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    packer_no = CharInFilter(field_name="packer_no", lookup_expr="in")

    class Meta:
        model = LpSchedulingPackerConstraints
        fields = ()
