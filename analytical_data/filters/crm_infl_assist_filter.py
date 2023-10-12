"""Filter module for case study master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.influencer_manager_models import CrmInflAssistReq


class CrmInflAssistReqFilter(FilterSet):
    """crm infl assist req filter class."""

    status = CharInFilter(field_name="status", lookup_expr="in")
    request_date = DateFilter(field_name="request_date")
    subject = CharInFilter(field_name="subject", lookup_expr="in")
    start_date = DateFilter(field_name="request_date", lookup_expr="gte")
    end_date = DateFilter(field_name="request_date", lookup_expr="lte")
    subject = CharInFilter(field_name="subject", lookup_expr="in")

    class Meta:
        model = CrmInflAssistReq
        fields = ()
