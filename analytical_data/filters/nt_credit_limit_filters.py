"""Filter class module for nt credit limit planning view"""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import BooleanFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import NtCreditLimit


class CreditLimitFilter(FilterSet):
    """Non-trade credit limit filter class."""

    status = BooleanFilter(field_name="status")
    party_name = CharInFilter(field_name="cust__party_name", lookup_expr="in")
    party_id = CharInFilter(field_name="cust__party_id", lookup_expr="in")
    account_type = CharInFilter(lookup_expr="in", method="filter_account_type")
    ntso = CharInFilter(lookup_expr="in", method="filter_ntso")
    tpc = CharInFilter(lookup_expr="in", method="filter_tpc")
    resource_id = CharInFilter(field_name="resource__id", method="filter_resource_id")

    class Meta:
        model = NtCreditLimit
        fields = (
            "credit_limit",
            "creation_date",
            "comment",
        )

    def filter_account_type(self, queryset, name, value):
        return queryset.filter(
            cust__acc_relations__account_type__acct_type_code=value[0]
        )

    def filter_ntso(self, queryset, name, value):
        return queryset.filter(
            cust__acc_relations__resource__designation="NTSO",
            cust__acc_relations__resource__resource_name=value[0],
        )

    def filter_tpc(self, queryset, name, value):
        return queryset.filter(
            cust__acc_relations__resource__designation="TPC",
            cust__acc_relations__resource__resource_name=value[0],
        )

    def filter_resource_id(self, queryset, name, value):
        return queryset.filter(
            cust__acc_relations__resource__id=value[0],
        )
