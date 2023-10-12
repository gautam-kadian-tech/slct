"""Filter module for packer rated."""
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.packing_plant_models import (
    PackerRatedCapacity,
    PackerShiftLevelStoppages,
)


class PackerRatedFilter(FilterSet):
    """Packer rated filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")

    class Meta:
        model = PackerRatedCapacity
        fields = ()


class PackerShiftLevelStoppagesMainListFilter(FilterSet):
    plant = CharInFilter(field_name="plant", lookup_expr="in")
    shift = CharInFilter(field_name="shift", lookup_expr="in")
    date = DateFilter(field_name="date")

    class Meta:
        model = PackerShiftLevelStoppages
        fields = ()
