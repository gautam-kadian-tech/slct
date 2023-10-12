"""Filter module for PackerBagBurstingDesc."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet, DateFilter

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.packing_plant_models import PackerBagBurstingDesc


class PackerBagBurstingDescFilter(FilterSet):
    """PackerBagBurstingDesc filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    date = DateFilter(field_name="date")

    class Meta:
        model = PackerBagBurstingDesc
        fields = ()
