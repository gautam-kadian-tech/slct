"""Filter class module for Decision on negative contribution market."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import NshContributionScenario


class NshContributionScenarioFilter(FilterSet):
    """Nsh Contribution scenario  filter class."""

    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    month = CharInFilter(field_name="month__month", lookup_expr="in")
    year = CharInFilter(field_name="month__year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")


    class Meta:
        model = NshContributionScenario
        fields = ()



