"""Filter class module for fact nt sales planning view"""
# pylint: disable=too-few-public-methods
from datetime import date

from django_filters.rest_framework import BooleanFilter, DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    BottomUpNt,
    CrmNthCustCodeCre,
    CrmNthExtendValidity,
    CrmNthLeadForm,
    CrmNthOrderCancAppr,
    CrmNthQuotNcrExcpAppr,
    CrmNthRefuReq,
    CrmNthSoNcrExcpAppr,
    CrmNthSourceChgReq,
    DimProductTest,
    FactNtSalesPlanning,
    MonthlyTargetSetting,
    NonTradeSalesPlanningAccount,
    NonTradeSalesPlanningAccountMonthly,
    NonTradeSalesPlanningDesignation,
    NonTradeSalesPlanningDesignationMonthly,
    NonTradeSalesPlanningMonthlyNcrTarget,
    NonTradeSalesPlanningProduct,
    NonTradeSalesPlanningProductMonthly,
    NonTradeSalesPlanningState,
    NonTradeSalesPlanningStateMonthly,
    NonTradeTopDownMonthlyTarget,
    NtResourceTarget,
    TOebsSclArNcrAdvanceCalcTab,
    TpcCustomerMapping,
)


class DimProductTestFilter(FilterSet):
    """dim product test filterset"""

    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packing_type = CharInFilter(field_name="packing_type", lookup_expr="in")

    class Meta:
        model = DimProductTest
        fields = ()


class FactNtSalesPlanningFilter(FilterSet):
    """fact nontrade sales planning filter class."""

    year = CharInFilter(field_name="period_key__year", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    account_name = CharInFilter(
        field_name="account_key__account_name", lookup_expr="in"
    )
    so_key = CharInFilter(field_name="so_key", lookup_expr="in")
    kam_key = CharInFilter(field_name="kam_key", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")

    class Meta:
        model = FactNtSalesPlanning
        fields = ()


class CrmNthQuotNcrExcpApprFilter(FilterSet):
    """Crm nontrade quotncr excep appr filter class."""

    customer_name = CharInFilter(field_name="customer_name", lookup_expr="in")
    customer_type = CharInFilter(field_name="customer_type", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")

    class Meta:
        model = CrmNthQuotNcrExcpAppr
        fields = ()


class CrmNthSoNcrExcpApprFilter(FilterSet):
    """crm nontrade so ncr exception approval  filter class."""

    customer_name = CharInFilter(field_name="customer_name", lookup_expr="in")
    customer_type = CharInFilter(field_name="customer_type", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")

    class Meta:
        model = CrmNthSoNcrExcpAppr
        fields = ()


class CrmNthSourceChgReqFilter(FilterSet):
    """crm non trade head source change filter class."""

    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")
    request_date = DateFilter(field_name="request_date", lookup_expr="in")

    class Meta:
        model = CrmNthSourceChgReq
        fields = ()


class CrmNthExtendValidityFilter(FilterSet):
    """crm non trade extend validity filter class."""

    # ntso_name = CharInFilter(
    #     field_name="ntso_name", lookup_expr="in"
    # )
    # request_date = DateFilter(field_name="request_date", lookup_expr="in")

    class Meta:
        model = CrmNthExtendValidity
        fields = ()


class CrmNthOrderCancApprFilter(FilterSet):
    """crm non trade head source change filter class."""

    customer_name = CharInFilter(field_name="customer_name", lookup_expr="in")
    customer_type = CharInFilter(field_name="customer_type", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")

    class Meta:
        model = CrmNthOrderCancAppr
        fields = ()


class CrmNthLeadFormFilter(FilterSet):
    """crm non trade head lead form class."""

    creation_date = CharInFilter(field_name="creation_date", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = CrmNthLeadForm
        fields = ()


class CrmNthRefuReqFilter(FilterSet):
    """crm non trade head refund req filter class."""

    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")
    creation_date = CharInFilter(field_name="creation_date", lookup_expr="in")

    class Meta:
        model = CrmNthRefuReq
        fields = ()


class CrmNthCustCodeCreFilter(FilterSet):
    """crm non trade head customer code cre filter class."""

    ntso_name = CharInFilter(field_name="ntso_name", lookup_expr="in")
    creation_date = CharInFilter(field_name="creation_date", lookup_expr="in")

    class Meta:
        model = CrmNthCustCodeCre
        fields = ()


class NtResourceTargetFilter(FilterSet):
    fiscal_year = CharInFilter(
        field_name="creation_date__year", method="filter_fiscal_year"
    )

    class Meta:
        model = NtResourceTarget
        fields = ()

    def filter_fiscal_year(self, queryset, name, value):
        year = int(value[0])
        return queryset.filter(
            creation_date__date__range=[date(year, 4, 1), date(year + 1, 3, 31)]
        )


class MonthlyTargetSettingFilter(FilterSet):
    """Monthly Target Filter Class."""

    date = DateFilter(field_name="date", method="filter_date")
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = DateFilter(field_name="date__year", lookup_expr="in")

    class Meta:
        model = MonthlyTargetSetting
        fields = ()

    def filter_date(self, queryset, name, value):
        return queryset.filter(date__range=[value, date.today()])


class NonTradeSalesPlanningStateFilter(FilterSet):
    """crm non trade head refund req filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningState
        fields = ()


class NonTradeSalesPlanningAccountFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    account_key = CharInFilter(field_name="account_key", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningAccount
        fields = ()


class NonTradeSalesPlanningDesignationFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    kam_key = CharInFilter(field_name="kam_key", lookup_expr="in")
    so_key = CharInFilter(field_name="so_key", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningDesignation
        fields = ()


class NonTradeSalesPlanningProductFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningProduct
        fields = ()


class BottomUpNtFilter(FilterSet):
    """crm non trade head refund req filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    date = DateFilter(field_name="date", lookup_expr="in")

    class Meta:
        model = BottomUpNt
        fields = ()


class NonTradeSalesPlanningStateMonthlyFilter(FilterSet):
    """crm non trade head refund req filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningStateMonthly
        fields = ()


class NonTradeSalesPlanningAccountMonthlyFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    account_key = CharInFilter(field_name="account_key", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningAccountMonthly
        fields = ()


class NonTradeSalesPlanningDesignationMonthlyFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    kam_key = CharInFilter(field_name="kam_key", lookup_expr="in")
    so_key = CharInFilter(field_name="so_key", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningDesignationMonthly
        fields = ()


class NonTradeSalesPlanningProductMonthlyFilter(FilterSet):
    """crm non trade head refund req filter class."""

    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningProductMonthly
        fields = ()


class NonTradeTopDownMonthlyTargetFilter(FilterSet):
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    account_type = CharInFilter(field_name="account_type", lookup_expr="in")
    ntso_or_kam_type = CharInFilter(field_name="ntso_or_kam_type", lookup_expr="in")
    ntso_or_kam = CharInFilter(field_name="ntso_or_kam", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    ntso_or_kam_is_not_null = BooleanFilter(
        field_name="", method="filter_ntso_or_kam_is_not_null"
    )
    account_type_is_not_null = BooleanFilter(
        field_name="", method="filter_account_type_is_not_null"
    )
    product_is_not_null = BooleanFilter(
        field_name="", method="filter_product_is_not_null"
    )

    class Meta:
        model = NonTradeTopDownMonthlyTarget
        fields = ()

    def filter_ntso_or_kam_is_not_null(self, queryset, name, value):
        if value:
            return queryset.filter(ntso_or_kam__isnull=False)

    def filter_account_type_is_not_null(self, queryset, name, value):
        if value:
            return queryset.filter(account_type__isnull=False)

    def filter_product_is_not_null(self, queryset, name, value):
        if value:
            return queryset.filter(product__isnull=False)


class NonTradeSalesPlanningMonthlyNcrTargetFilter(FilterSet):
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    target = CharInFilter(field_name="target", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    packing_type = CharInFilter(field_name="packing_type", lookup_expr="in")

    class Meta:
        model = NonTradeSalesPlanningMonthlyNcrTarget
        fields = ()


class TpcCustomerMappingFilter(FilterSet):
    """crm non trade head refund req filter class."""

    tpc_code = CharInFilter(field_name="tpc_code", lookup_expr="in")
    tpc_name = CharInFilter(field_name="tpc_name", lookup_expr="in")
    customer_code = CharInFilter(field_name="customer_code", lookup_expr="in")
    customer_name = CharInFilter(field_name="customer_name", lookup_expr="in")

    class Meta:
        model = TpcCustomerMapping
        fields = ()
