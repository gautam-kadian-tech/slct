"""Filter module for case study master."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.influencer_manager_models import CrmInflChgReq


class CrmInflChgReqFilter(FilterSet):
    """crm infl chq req filter class."""

    status = CharInFilter(field_name="status", lookup_expr="in")
    type_of_change = CharInFilter(field_name="type_of_change", lookup_expr="in")
    request_date = DateFilter(field_name="request_date")
    start_date = DateFilter(field_name="request_date", lookup_expr="gte")
    end_date = DateFilter(field_name="request_date", lookup_expr="lte")
    influencer_type = CharInFilter(field_name="influencer_type", lookup_expr="in")

    class Meta:
        model = CrmInflChgReq
        fields = ()
