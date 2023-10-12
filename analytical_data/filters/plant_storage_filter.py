"""Filter module for plant storage filter."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.packing_plant_models import PlantDepoSla, PlantStorage


class PlantStorageFilter(FilterSet):
    """Plant Storage filter class."""

    plant_name = CharInFilter(field_name="plant_name", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = PlantStorage
        fields = ()


class PlantDepoSlaFilter(FilterSet):
    """Plant Depo sla filter class."""

    plant_name = CharInFilter(field_name="plant_name", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = PlantDepoSla
        fields = ()
