"""Filter class module for lp schedule order master."""
# pylint: disable=too-few-public-methods
from datetime import date as datetime_date
from datetime import timedelta

from django.db.models import Q
from django_filters.rest_framework import (
    BooleanFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    LpSchedulingExecutableDtl,
    LpSchedulingOrderMaster,
)


class LpSchedulingOrderMasterFilter(FilterSet):
    """Lp scheduling order master filter class."""

    order_date = CharInFilter(field_name="order_date", lookup_expr="in")
    ship_city = CharInFilter(field_name="ship_city", lookup_expr="in")
    ship_district = CharInFilter(field_name="ship_district", lookup_expr="in")
    ship_state = CharInFilter(field_name="ship_state", lookup_expr="in")
    customer_type = CharInFilter(field_name="customer_type", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    order_type = CharInFilter(field_name="order_type", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    auto_tagged_source = CharInFilter(field_name="auto_tagged_source", lookup_expr="in")
    auto_tagged_mode = CharInFilter(field_name="auto_tagged_mode", lookup_expr="in")
    changed_mode = CharInFilter(field_name="changed_mode", lookup_expr="in")
    changed_source = CharInFilter(field_name="changed_source", lookup_expr="in")
    updated_at = CharInFilter(field_name="updated_at", lookup_expr="in")
    current_source = CharInFilter(field_name="current_source", lookup_expr="in")
    executable_shift = NumberFilter(
        field_name="lp_scheduling_executable_dtl__executable_shift"
    )
    executable_date = DateFilter(
        field_name="lp_scheduling_executable_dtl__executable_date"
    )
    remarks = DateFilter(field_name="lp_scheduling_executable_dtl__remarks")
    reason = DateFilter(field_name="lp_scheduling_executable_dtl__reason")
    is_di_created = BooleanFilter(
        field_name="lp_scheduling_di_details", method="filter_is_di_created"
    )
    is_remark_null = BooleanFilter(
        field_name="lp_scheduling_executable_dtl__remarks",
        method="filter_is_remarks_null",
    )
    is_reason_null = BooleanFilter(
        field_name="lp_scheduling_executable_dtl__reason",
        method="filter_is_reason_null",
    )
    # current_source = CharInFilter(
    #     field_name="auto_tagged_source", method="filter_current_source"
    # )
    transferred_to_depot = BooleanFilter(field_name="transferred_to_depot")
    order_executable = BooleanFilter(field_name="order_executable")
    order_status = CharInFilter(field_name="order_status", lookup_expr="in")
    show_dispatched_order = BooleanFilter(
        field_name="order_status", method="filter_show_dispatched_order"
    )

    class Meta:
        model = LpSchedulingOrderMaster
        fields = ("ship_state", "ship_district")

    def filter_is_di_created(self, queryset, name, value):
        return queryset.filter(lp_scheduling_di_details__isnull=value)

    def filter_show_dispatched_order(self, queryset, name, value):
        end_date = datetime_date.today()
        start_date = end_date - timedelta(days=30)
        if value:
            return queryset.filter(
                order_status="ORDER DISPATCHED",
                updated_at__range=[start_date, end_date],
            )
        return queryset.filter(~Q(order_status="ORDER DISPATCHED"))

    def filter_is_remarks_null(self, queryset, name, value):
        return queryset.filter(lp_scheduling_executable_dtl__remarks__isnull=value)

    def filter_is_reason_null(self, queryset, name, value):
        return queryset.filter(lp_scheduling_executable_dtl__reason__isnull=value)

    def filter_current_source(self, queryset, name, value):
        queryset1 = queryset.filter(
            auto_tagged_source=value[0], changed_source__isnull=True
        )
        queryset2 = queryset.filter(changed_source=value[0])
        return queryset1.union(queryset2)


class LpSchedulingOrderExecutableFilter(FilterSet):
    """Lp scheduling order executable filterset class."""

    order_date = CharInFilter(field_name="order_master__order_date", lookup_expr="in")
    ship_city = CharInFilter(field_name="order_master__ship_city", lookup_expr="in")
    ship_district = CharInFilter(
        field_name="order_master__ship_district", lookup_expr="in"
    )
    ship_state = CharInFilter(field_name="order_master__ship_state", lookup_expr="in")
    customer_type = CharInFilter(
        field_name="order_master__customer_type", lookup_expr="in"
    )
    brand = CharInFilter(field_name="order_master__brand", lookup_expr="in")
    grade = CharInFilter(field_name="order_master__grade", lookup_expr="in")
    order_type = CharInFilter(field_name="order_master__order_type", lookup_expr="in")
    packaging = CharInFilter(field_name="order_master__packaging", lookup_expr="in")
    auto_tagged_source = CharInFilter(
        field_name="order_master__auto_tagged_source", lookup_expr="in"
    )
    current_source = CharInFilter(
        field_name="order_master__current_source", lookup_expr="in"
    )
    executable_date = DateFilter(field_name="executable_date")
    transferred_to_depot = BooleanFilter(
        field_name="order_master__transferred_to_depot"
    )

    class Meta:
        model = LpSchedulingExecutableDtl
        fields = ("executable_shift", "executable_date")


class PpSequenceFilter(LpSchedulingOrderMasterFilter):
    """Lp scheduling pp sequence filter class."""

    prioritized_order = BooleanFilter(
        field_name="lp_scheduling_pp_call_dtl__prioritized_order"
    )
    di_number = CharInFilter(field_name="lp_scheduling_di_details__di_number")
