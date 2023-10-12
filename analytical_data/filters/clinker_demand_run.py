"""Filter module for clinker demand run."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import (
    CharInFilter,
    OptionChoiceFilter,
)
from analytical_data.models import ClinkerDemandRun, PlantNameChoices


class ClinkerDemandRunFilter(FilterSet):
    """Clinker demand filter class."""

    plant_id = OptionChoiceFilter(
        field_name="plant_id", choices=PlantNameChoices, method="filter_plant_id"
    )
    fc_whse = OptionChoiceFilter(field_name="fc_whse", choices=PlantNameChoices)
    cement_demand = CharInFilter(field_name="cement_demand", lookup_expr="in")
    clinker_demand = CharInFilter(field_name="clinker_demand", lookup_expr="in")
    clinker_freight = CharInFilter(field_name="clinker_freight", lookup_expr="in")
    mode = CharInFilter(field_name="mode", lookup_expr="in")
    run = CharInFilter(field_name="run", lookup_expr="in")

    class Meta:
        model = ClinkerDemandRun
        fields = ()

    def filter_plant_id(self, queryset, name, value):
        for key, val in PlantNameChoices.choices:
            if value in [key, val]:
                value = "FG" + key[2:]
                return queryset.filter(plant_id=value)
        return queryset
