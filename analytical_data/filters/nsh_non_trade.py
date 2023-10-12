"""Filter class module for nsh non trade sales planning view"""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import NshNonTradeSales


class NshNonTradeSalesFilter(FilterSet):
    """nsh non trade sales filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    field_officer_name = CharInFilter(field_name="field_officer_name", lookup_expr="in")
    invoice_date__year = CharInFilter("invoice_date__year", lookup_expr="in")
    party_name = CharInFilter("channel_partner_name", lookup_expr="in")

    class Meta:
        model = NshNonTradeSales
        fields = ()
