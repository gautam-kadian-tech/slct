"""Filter class module for packer shift constraints."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PlantProductsMaster


class PlantProductMasterFilter(FilterSet):
    """Plant Product Master filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    quantity = CharInFilter(field_name="quantity", lookup_expr="in")
    variable_production_cost = CharInFilter(
        field_name="variable_production_cost", lookup_expr="in"
    )
    clinker_cf = CharInFilter(field_name="clinker_cf", lookup_expr="in")

    class Meta:
        model = PlantProductsMaster
        fields = ()
