"""Filter module for clinker links master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import ClinkerLinksMaster


class ClinkerLinksMasterFilter(FilterSet):
    """Clinker links master filter class."""

    mode_of_transport = CharInFilter(field_name="mode_of_transport", lookup_expr="in")
    fc_whse = CharInFilter(field_name="fc_whse", lookup_expr="in")
    fg_whse = CharInFilter(field_name="fg_whse", lookup_expr="in")

    class Meta:
        model = ClinkerLinksMaster
        fields = ()
