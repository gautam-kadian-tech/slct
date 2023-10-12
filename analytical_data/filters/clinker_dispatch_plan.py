"""Filter module for clinker dispatch plan."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import OptionChoiceFilter
from analytical_data.models import ClinkerDispatchPlan, PlantNameChoices


class ClinkerDispatchPlanFilter(FilterSet):
    """clinker dispatch plan filter class."""

    shipped_from_plant = OptionChoiceFilter(
        field_name="shipped_from_plant", choices=PlantNameChoices
    )
    shipped_to_plant = OptionChoiceFilter(
        field_name="shipped_to_plant", choices=PlantNameChoices
    )
    shipping_date_month = DateFilter(
        field_name="shipping_date", method="filter_shipping_date_month"
    )

    class Meta:
        model = ClinkerDispatchPlan
        fields = ("shipping_date",)

    def filter_shipping_date_month(self, queryset, name, value):
        return queryset.filter(
            shipping_date__month=value.month, shipping_date__year=value.year
        )
