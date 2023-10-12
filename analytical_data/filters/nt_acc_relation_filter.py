"""Filter class module for non-trade account relation view."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import BooleanFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import NtAccRelation


class NtAccRelationFilter(FilterSet):
    """Transfer accounts relation filter class."""

    party_id = CharInFilter(field_name="cust__party_id", lookup_expr="in")
    party_name = CharInFilter(field_name="cust__party_name", lookup_expr="in")
    latest_active_account = BooleanFilter(
        field_name="resource__designation", method="filter_latest_active_account"
    )
    resource_id = CharInFilter(field_name="resource__id", lookup_expr="in")
    designation = CharInFilter(field_name="resource__designation", lookup_expr="in")

    class Meta:
        model = NtAccRelation
        fields = ()

    def filter_latest_active_account(self, queryset, field_name, value):
        """Apply custom filter to return tpc, kam and ntso data for a given customer.

        Args:
            queryset (Queryset): the queryset to apply filter on
            field_name (str): field which will be filtered
            value (str): value

        Returns:
            Queryset: filtered queryset
        """
        # Need to test this part
        if value:
            try:
                return (
                    queryset.filter(resource__designation="TPC")[:1]
                    | queryset.filter(resource__designation="KAM")[:1]
                    | queryset.filter(resource__designation="NTSO")[:1]
                )
            except KeyError:
                return queryset
        return queryset
