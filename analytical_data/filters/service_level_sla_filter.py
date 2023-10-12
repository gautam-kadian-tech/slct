"""Filter module for service level sla model."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import ServiceLevelSla


class ServiceLevelSlaFilter(FilterSet):
    """Service level sla filter class."""

    destination = CharInFilter(field_name="destination", lookup_expr="in")
    sla = CharInFilter(field_name="sla", lookup_expr="in")
    city = CharInFilter(field_name="destination__city", lookup_expr="in")
    district = CharInFilter(field_name="destination__district", lookup_expr="in")
    state = CharInFilter(field_name="destination__state", lookup_expr="in")

    class Meta:
        model = ServiceLevelSla
        fields = ()
