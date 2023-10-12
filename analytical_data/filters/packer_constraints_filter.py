"""Filter class module for packer constraints master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import PackerConstraintsMaster


class PackerConstraintsFilter(FilterSet):
    """Packer constraints master filter class."""

    plant_id = CharInFilter(field_name="plant_id", lookup_expr="in")
    packer_no = CharInFilter(field_name="packer_no", lookup_expr="in")
    packer_capacity = CharInFilter(field_name="packer_capacity", lookup_expr="in")
    truck_loader_no = CharInFilter(field_name="truck_loader_no", lookup_expr="in")

    class Meta:
        model = PackerConstraintsMaster
        fields = ()
