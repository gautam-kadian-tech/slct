"""Filter class module for brand approval."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import FactBrandApproval


class FactBrandApprovalFilter(FilterSet):
    """Brand approval filter class."""

    id = CharInFilter(field_name="id", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    approval_required_by_date = CharInFilter(
        field_name="project_key__approval_required_by_date", lookup_expr="in"
    )
    party_id = CharInFilter(field_name="customer_id__party_id", lookup_expr="in")
    party_name = CharInFilter(field_name="customer_id__party_name", lookup_expr="in")
    project_name = CharInFilter(
        field_name="project_key__project_name", lookup_expr="in"
    )
    approving_authority = CharInFilter(
        field_name="project_key__approving_authority", lookup_expr="in"
    )
    project_location = CharInFilter(
        field_name="project_key__project_location", lookup_expr="in"
    )
    concerned_officer = CharInFilter(
        field_name="project_key__concerned_officer", lookup_expr="in"
    )
    assigned_authority = CharInFilter(
        field_name="assignee_key__resource_name", lookup_expr="in"
    )
    officer_email = CharInFilter(
        field_name="assignee_key__officer_email", lookup_expr="in"
    )
    status = CharInFilter(
         field_name="status", lookup_expr="in"
    )
    party_id = CharInFilter(
        field_name="customer_id__party_id", lookup_expr="in"
    )

    class Meta:
        model = FactBrandApproval
        fields = ()
