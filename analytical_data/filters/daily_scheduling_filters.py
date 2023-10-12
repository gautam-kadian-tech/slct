"""Filter module for daily scheduling"""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    DepotAdditionOutputView,
    LpModelDfRank,
    SourceChangeApproval,
    SourceChangeFreightMaster,
)


class DepotAdditionOutputViewFilter(FilterSet):
    """Clinker links master filter class."""

    run_id = CharInFilter(field_name="run", lookup_expr="in")

    class Meta:
        model = DepotAdditionOutputView
        fields = ()


class LpModelDfRankFilter(FilterSet):
    """Lp model df rank filter class."""

    destination_city = CharInFilter(field_name="destination_city", lookup_expr="in")
    destination_district = CharInFilter(
        field_name="destination_district", lookup_expr="in"
    )
    destination_state = CharInFilter(field_name="destination_state", lookup_expr="in")
    cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    # run_id = CharInFilter(field_name="run_id", lookup_expr="in")

    class Meta:
        model = LpModelDfRank
        fields = ()


class SourceChangeFreightMasterFilter(FilterSet):
    """source change frieght master filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    org_type = CharInFilter(field_name="org_type", lookup_expr="in")

    class Meta:
        model = SourceChangeFreightMaster
        fields = ()


class SourceChangeApprovalFilter(FilterSet):
    auto_tagged_source = CharInFilter(field_name="order__auto_tagged_source")
    auto_tagged_mode = CharInFilter(field_name="order__auto_tagged_mode")
    order_line_id = CharInFilter(field_name="order__order_line_id")
    customer_type = CharInFilter(field_name="order__customer_type")
    dispatch_due_date = CharInFilter(field_name="order__dispatch_due_date")
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")

    class Meta:
        model = SourceChangeApproval
        fields = (
            "changed_source",
            "changed_mode",
            "created_by",
            "creation_date",
            "status",
            "persona",
        )
