from django_filters.rest_framework import BooleanFilter, DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.alerts_models import (
    AlertTransaction,
    CrmApprovalStageGates,
)


class AlertTransactionFilter(FilterSet):
    is_read = CharInFilter(field_name="is_read", lookup_expr="in")
    notification_content = CharInFilter(
        field_name="notification_content", lookup_expr="in"
    )
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")
    is_active = CharInFilter(field_name="is_active", lookup_expr="in")

    class Meta:
        model = AlertTransaction
        fields = ()


class CrmApprovalStageGatesFilter(FilterSet):
    approval_type = CharInFilter(field_name="approval_type", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    record_id = CharInFilter(field_name="record_id", lookup_expr="in")
    is_approved = BooleanFilter(field_name="is_approved")

    class Meta:
        model = CrmApprovalStageGates
        fields = ()
