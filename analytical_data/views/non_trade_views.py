"""National non-trade head views module."""
import json
import os
from calendar import monthrange
from datetime import date as datetime_date
from datetime import datetime
from operator import itemgetter

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import Avg, Count, F, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import (
    AdvanceCalcTabFilter,
    CreditLimitFilter,
    CrmNthCustCodeCreFilter,
    CrmNthExtendValidityFilter,
    CrmNthLeadFormFilter,
    CrmNthOrderCancApprFilter,
    CrmNthQuotNcrExcpApprFilter,
    CrmNthRefuReqFilter,
    CrmNthSoNcrExcpApprFilter,
    CrmNthSourceChgReqFilter,
    DimCustomersTestFilter,
    DimProductTestFilter,
    FactBrandApprovalFilter,
    FactNtSalesPlanAnnualFilter,
    FactNtSalesPlanningFilter,
    FactNtSalesPlanningMonthFilter,
    FactNtSalesPlanningNcrFilter,
    MonthlyTargetSettingFilter,
    NonTradeSalesPlanningAccountFilter,
    NonTradeSalesPlanningAccountMonthlyFilter,
    NonTradeSalesPlanningDesignationFilter,
    NonTradeSalesPlanningDesignationMonthlyFilter,
    NonTradeSalesPlanningMonthlyNcrTargetFilter,
    NonTradeSalesPlanningProductFilter,
    NonTradeSalesPlanningProductMonthlyFilter,
    NonTradeSalesPlanningStateFilter,
    NonTradeSalesPlanningStateMonthlyFilter,
    NonTradeTopDownMonthlyTargetFilter,
    NshNonTradeSalesFilter,
    NtAccRelationFilter,
    NtResourceTargetFilter,
    TOebsSclArNcrAdvanceCalcTabFilter,
    TpcCustomerMappingFilter,
)

# from analytical_data.filters.annual_sales_target_filters import (
#     FactNtSalesPlanningFilter,
# )
from analytical_data.models import (
    BottomUpNt,
    ConsensusTarget,
    CrmNthBankGuartAppr,
    CrmNthCustCodeCre,
    CrmNthExtendValidity,
    CrmNthLeadForm,
    CrmNthOrderCancAppr,
    CrmNthQuotNcrExcpAppr,
    CrmNthRefuReq,
    CrmNthSoNcrExcpAppr,
    CrmNthSourceChgReq,
    DimAccountType,
    DimCustomersTest,
    DimPeriod,
    DimProductTest,
    DimResources,
    FactBrandApproval,
    FactNtSalesPlanAnnual,
    FactNtSalesPlanning,
    FactNtSalesPlanningMonth,
    FactNtSalesPlanningNcr,
    MarketMappingMarketPotential,
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
    NshNonTradeSales,
    NtAccRelation,
    NtCommsNotified,
    NtCreditLimit,
    NtMarketTarget,
    NtNcrThreshold,
    NtNotesComms,
    NtResourceTarget,
    PremiumProductsMasterTmp,
    SclHierarchyMaster,
    TgtOrderDataAp,
    TOebsHzCustAccounts,
    TOebsSclArNcrAdvanceCalcTab,
    TpcCustomerMapping,
    VpcHistorical,
    ZoneMappingNew,
)
from analytical_data.serializers import (
    AnnualSalesTargetSerializer,
    BrandApprovalSerializer,
    ConsensusTargetForNtUseSerializer,
    CreditLimitNtSerializer,
    CrmNthBankGuartApprSerializer,
    CrmNthCustCodeCreSerializer,
    CrmNthExtendValiditySerializer,
    CrmNthLeadFormSerializer,
    CrmNthOrderCancApprSerializer,
    CrmNthQuotNcrExcpApprSerializer,
    CrmNthRefuReqSerializer,
    CrmNthSoNcrExcpApprSerializer,
    CrmNthSourceChgReqSerializer,
    DimCustomersSerializer,
    DimCustomersTestSerializer,
    DimResourcesSerializer,
    FactNtSalesPlanAnnualSerializer,
    FactNtSalesPlanningMonthSerializer,
    FactNtSalesPlanningNcrSerializer,
    FactNtSalesPlanningSerializer,
    MonthlyTargetSettingSerializer,
    NonTradeSalesPlanningAccountMonthlySerializer,
    NonTradeSalesPlanningAccountSerializer,
    NonTradeSalesPlanningDesignationMonthlySerializer,
    NonTradeSalesPlanningDesignationSerializer,
    NonTradeSalesPlanningMonthlyNcrTargetSerializer,
    NonTradeSalesPlanningProductMonthlySerializer,
    NonTradeSalesPlanningProductSerializer,
    NonTradeSalesPlanningStateMonthlySerializer,
    NonTradeSalesPlanningStateSerializer,
    NonTradeTopDownMonthlyTargetSerializer,
    NshNonTradeHeadSerializer,
    NshNonTradeSalesForThreeMonthOldSerializer,
    NtAccRelationSerializer,
    NtAccRelationUpdateOrCreateSerializer,
    NtCreditLimitChangeStatusSerializer,
    NtCreditLimitCreateSerializer,
    NtMarketTargettBulkCreateSerializer,
    NtNcrThresholdSerializer,
    NtNotesCommsSerializer,
    NtResourceTargetSerializer,
    TOebsHzCustAccountsSerializer,
    TOebsSclArNcrAdvanceCalcTabDownloadSerializer,
    TOebsSclArNcrAdvanceCalcTabSerializer,
    TpcCustomerMappingSerializer,
    TransferAccountsSerializer,
    TransferOfficersAllAccountsSerializer,
)
from analytical_data.utils import CustomPagination, Responses, dump_to_excel
from analytical_data.view_helpers import (
    NtNcrThresholdHelper,
    TransferAccountsHelper,
)
from analytical_data.view_helpers.get_user_detail import user_details
from analytical_data.views.custom_viewsets import (
    DownloadUploadViewSet,
    FileUploadViewSet,
)


class TOebsHzCustAccountsView(ListAPIView):
    """Customer accounts view class."""

    queryset = TOebsHzCustAccounts.objects.filter(attribute1="NT").select_related(
        "attribute3"
    )
    serializer_class = TOebsHzCustAccountsSerializer
    pagination_class = CustomPagination


class CreditLimitNtView(ModelViewSet):
    """Credit limit non-trade view class."""

    queryset = (
        NtCreditLimit.objects.all().select_related("cust").order_by("-creation_date")
    )
    serializer_class = CreditLimitNtSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CreditLimitFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NtCreditLimitCreateSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "user_id": self.request.user.id,
                "account_type_code": self.request.query_params.get("account_type_code"),
            }
        )
        return context


class CreditLimitNtChangeStatus(GenericAPIView):
    serializer_class = NtCreditLimitChangeStatusSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NtCreditLimit.objects.filter(
            id__in=serializer.validated_data.get("credit_limit_ids")
        ).update(status=serializer.validated_data.get("status"))
        return Responses.success_response("Status updated!")


class NtNcrThresholdView(ListCreateAPIView):
    """NCR threshold view class."""

    queryset = NtNcrThreshold.objects.order_by("-last_update_date")
    serializer_class = NtNcrThresholdSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "product_string",
        "ncr_thresholds",
        "creation_date",
        "state",
        "district",
        "city",
        "account_type",
        "valid_till",
        "type",
        "brand",
    )
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context


class NtNcrMonthlySales(GenericAPIView):
    """Monthly sales view class."""

    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    filterset_class = AdvanceCalcTabFilter
    helper = NtNcrThresholdHelper

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Monthly sales and average ncr_threshold data.",
            data=self.helper._get_monthly_ncr_sales(
                self.filter_queryset(self.get_queryset())
            ),
        )


class BrandApprovalViewSet(FileUploadViewSet):
    """Brand approval view-set class."""

    queryset = FactBrandApproval.objects.order_by("-creation_date")
    serializer_class = BrandApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactBrandApprovalFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_path = settings.BRAND_APPROVAL_PATH

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "attachment": self.file_path + f"{self.request.FILES.get('file_name')}"
                if self.request.FILES.get("file_name")
                else None,
            }
        )
        return context

    def partial_update(self, request, *args, **kwargs):
        if getattr(self.get_object(), "document", None) and request.FILES.get(
            "file_name"
        ):
            os.remove(getattr(self.get_object(), "document"))

        self.file_name = request.FILES.get("file_name")

        dump_file = open(self.file_path + f"{self.file_name}", "bw")

        try:
            dump_file.write(self.file_name.read())
            dump_file.close()
        except AttributeError:
            pass
        return super().partial_update(request, *args, **kwargs)


class BrandApprovalDropdownView(GenericAPIView):
    """Brand approval dropdown api."""

    queryset = FactBrandApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactBrandApprovalFilter

    def __get_brand_approval_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "id": self.__get_brand_approval_query("id"),
            "customer_id": self.__get_brand_approval_query("customer_id__party_id"),
            "customer_name": self.__get_brand_approval_query("customer_id__party_name"),
            "project_name": self.__get_brand_approval_query(
                "project_key__project_name"
            ),
            "approving_authority": self.__get_brand_approval_query(
                "project_key__approving_authority"
            ),
            "project_location": self.__get_brand_approval_query(
                "project_key__project_location"
            ),
            "status": self.__get_brand_approval_query("status"),
            "assigned_to": self.__get_brand_approval_query(
                "assignee_key__resource_name"
            ),
            "product": self.__get_brand_approval_query("product"),
            "brand": self.__get_brand_approval_query("brand"),
            "creation_date": self.__get_brand_approval_query("creation_date"),
            "created_by": self.__get_brand_approval_query("created_by"),
        }
        return Responses.success_response("Brand approval dropdown data.", data=data)


class NtNotesCommsBaseViewSet(FileUploadViewSet):
    """Base view class for communication and notes."""

    serializer_class = NtNotesCommsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("^subject",)
    pagination_class = CustomPagination
    lookup_field = "id"


class NtCommunicationView(NtNotesCommsBaseViewSet):
    """Non-trade communication view class."""

    queryset = NtNotesComms.objects.filter(type="Communication").order_by(
        "-creation_date"
    )
    file_path = settings.NT_NCR_COMMUNICATION_PATH


class NtNotesView(NtNotesCommsBaseViewSet):
    """Non-trade notes view class."""

    queryset = NtNotesComms.objects.filter(type="Note").order_by("-creation_date")
    file_path = settings.NT_NCR_NOTES_PATH


class NtNcrThresholdDropdownView(GenericAPIView):
    """View class for nt ncr threshold dropdown."""

    helper = NtNcrThresholdHelper

    def __get_scl_hierarchy_master_query(self, request, query, query_string):
        queryset = SclHierarchyMaster.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return (
            queryset.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def __get_advance_calc_tab(self, query_string, request, query=Q()):
        # queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
        # user_email = request.user.email
        # queryset = user_details(user_email, queryset)
        return (
            TOebsSclArNcrAdvanceCalcTab.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def _get_credit_limit_setting_dropdown(self, request):
        # queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
        # user_email = request.user.email
        # queryset = user_details(user_email, queryset)
        return {
            "products": (
                TOebsSclArNcrAdvanceCalcTab.objects.exclude(
                    Q(product__exact=" ") | Q(product__startswith="AAC")
                )
                .values_list("product", flat=True)
                .annotate(Count("product"))
            ),
            "valid_for": [3, 7],
            "state": self.__get_scl_hierarchy_master_query(
                request, Q(state_erp__isnull=False), "state_erp"
            ),
            "key": self.__get_advance_calc_tab("key", request, Q(key__isnull=False)),
            "month": self.__get_advance_calc_tab("creation_date__month", request),
        }

    def get(self, request, *args, **kwargs):
        data = self._get_credit_limit_setting_dropdown(request)
        return Responses.success_response("Nt ncr threshold dropdown data.", data=data)


class NtNcrThresholdDistrictsDropdownView(NtNcrThresholdDropdownView):
    """View class for nt ncr threshold district dropdown."""

    def get(self, request, *args, **kwargs):
        data = self.helper._get_credit_limit_setting_district_dropdown(
            request.query_params
        )
        return Responses.success_response(
            "Nt ncr threshold district dropdown data.", data=data
        )


class NtNcrThresholdCityDropdownView(NtNcrThresholdDropdownView):
    """View class for nt ncr threshold city dropdown."""

    def get(self, request, *args, **kwargs):
        data = self.helper._get_credit_limit_setting_city_dropdown(request.query_params)
        return Responses.success_response(
            "Nt ncr threshold district dropdown data.", data=data
        )


class NonTradeSalesDropdown(GenericAPIView):
    """NSH non-trade sales dropdown view class."""

    queryset = NshNonTradeSales.objects.all()

    def __get_nsh_non_trade_sales_query(self, query_string):
        return (
            self.get_queryset()
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
        )

    def get(self, request, *args, **kwargs):
        data = {
            "brand": self.__get_nsh_non_trade_sales_query("brand"),
            "state": self.__get_nsh_non_trade_sales_query("state"),
            "product": self.__get_nsh_non_trade_sales_query("product"),
        }
        return Responses.success_response(
            "NSH Non-trade sales dropdown data.", data=data
        )


class DimPeriodDropdownBaseView(GenericAPIView):
    """Dim period dropdown base view class."""

    queryset = DimPeriod.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year",)

    def _get_dim_period_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )


class DimPeriodYearsDropdown(DimPeriodDropdownBaseView):
    """Years dropdown from dim period model class."""

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Dim period years dropdown.",
            data={"year": self._get_dim_period_query("year")},
        )


class DimPeriodMonthsDropdown(DimPeriodDropdownBaseView):
    """Months dropdown from dim period model class."""

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Dim period months dropdown.",
            data={"months": self._get_dim_period_query("month")},
        )


class AnnualSalesTargetBaseView(DownloadUploadViewSet):
    """Set annual sales target in non-trade head."""

    queryset = FactNtSalesPlanning.objects.all()
    serializer_class = AnnualSalesTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanningFilter
    sorting_fields = ("brand", "period_key__year")
    pagination_class = CustomPagination

    def get_sorted_data(self, request_data):
        return request_data

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            return super().update(request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset())

        # Sorts list of dicts based on a value of a key in dictionary.
        data = self.get_sorted_data(request.data)

        serializer = self.get_serializer(
            queryset, data, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            self.update_response_message, data=serializer.data
        )


class AnnualSalesTargetStateView(AnnualSalesTargetBaseView):
    """Edit annual sales planning based on states."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.method == "PUT":
            return queryset
        return queryset.filter(
            state__in={data["state"] for data in self.request.data},
            period_key__month__in={data["month"] for data in self.request.data},
        ).order_by("state", *self.sorting_fields, "period_key__month")

    def get_sorted_data(self, request_data):
        return sorted(request_data, key=itemgetter("state", "brand", "year", "month"))

    def list(self, request, *args, **kwargs):
        states = (
            self.filter_queryset(self.get_queryset())
            .filter(state__isnull=False)
            .values(
                "id",
                "state",
                "period_key__year",
                "period_key__month",
                "monthly_sales_target",
                "monthly_ncr_target",
                "quarterly_sales_plan",
                "yearly_sales_plan",
                "brand",
                "grade",
                "packaging",
                "so_key",
                "kam_key",
                "account_key",
                "product",
                "new_customer_target",
                "new_customer_sale_percent",
                "action_by",
                "action_date",
                "action_remark",
                "action_status",
                "created_by",
                "creation_date",
                "last_updated_by",
                "last_update_date",
                "last_update_login",
            )
        )
        df = pd.DataFrame(list(states))

        data = {}
        if not df.empty:
            states = df.state.unique()

            for state in states:
                data[state] = json.loads(
                    df.query(f'state=="{state}"').to_json(orient="records")
                )
        return Response(data)


class AnnualSalesTargetNtsoKamView(AnnualSalesTargetBaseView):
    """Edit annual sales planning based on so_key and kam_key."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.method == "PUT":
            return queryset
        return queryset.filter(
            Q(so_key__in={data["so_key"] for data in self.request.data})
            | Q(kam_key__in={data["so_key"] for data in self.request.data}),
            period_key__month__in={data["month"] for data in self.request.data},
        ).order_by(*self.sorting_fields, "period_key__month", "so_key", "kam_key")

    def get_sorted_data(self, request_data):
        return sorted(
            request_data,
            key=itemgetter(
                *self.sorting_fields, "period_key__month", "so_key", "kam_key"
            ),
        )


class AnnualSalesTargetProductView(AnnualSalesTargetBaseView):
    """Edit annual sales planning based on product."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.method == "PUT":
            return queryset
        return queryset.filter(
            product__in={data["product"] for data in self.request.data},
            period_key__month__in={data["month"] for data in self.request.data},
        ).order_by(*self.sorting_fields, "period_key__month", "product")

    def get_sorted_data(self, request_data):
        return sorted(
            request_data,
            key=itemgetter(*self.sorting_fields, "period_key__month", "product"),
        )


class AnnualSalesTargetAccountView(AnnualSalesTargetBaseView):
    """Edit annual sales planning based on account."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.method == "PUT":
            return queryset
        return queryset.filter(
            account_key__in={data["account_key"] for data in self.request.data},
            period_key__month__in={data["month"] for data in self.request.data},
        ).order_by(*self.sorting_fields, "period_key__month", "account_key")

    def get_sorted_data(self, request_data):
        return sorted(
            request_data,
            key=itemgetter(*self.sorting_fields, "period_key__month", "account_key"),
        )


class DimResourcesListView(ListAPIView):
    """Dim resource base view class."""

    queryset = DimResources.objects.all()
    serializer_class = DimResourcesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("designation", "resource_name")

    # pagination_class = CustomPagination
    def get(self, request, *args, **kwargs):
        querset = self.filter_queryset(self.get_queryset()).values()
        return Responses.success_response("Data Fetched Successfully", data=querset)


class DimResourceDesignationDropdown(DimResourcesListView):
    """Designation dropdown from dim resource view."""

    def _get_dim_resource_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def list(self, request, *args, **kwargs):
        return Responses.success_response(
            "Dim resource designation dropdown.",
            data={"designation": self._get_dim_resource_query("designation")},
        )


class DimResourceDropdown(DimResourcesListView):
    """Resource dropdown from dim resource view."""

    def _get_dim_resource_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def list(self, request, *args, **kwargs):
        return Responses.success_response(
            "Dim resource dropdown.",
            data={"designation": self._get_dim_resource_query("resource_name")},
        )


class DimAccountTypeDropdownBaseView(GenericAPIView):
    """Dim account type dropdown base view class."""

    queryset = DimAccountType.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("account_name",)

    def _get_dim_account_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )


class DimAccountNameDropdown(DimAccountTypeDropdownBaseView):
    """account name dropdown from dim account type model class."""

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Dim account name dropdown.",
            data={"account_name": self._get_dim_account_query("account_name")},
        )


class FactNtSalesPlanningViewSet(ModelViewSet):
    """Fact nt sales planning CRUDs view set class."""

    queryset = FactNtSalesPlanning.objects.select_related("period_key")
    serializer_class = FactNtSalesPlanningSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanningFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class NshNonTradeSalesActualViewSet(ModelViewSet):
    """Fact nt sales planning CRUDs view set class."""

    queryset = (
        NshNonTradeSales.objects.annotate(month=TruncMonth("invoice_date"))
        .values("month")
        .annotate(sum=Count("volume_sales_mt"))
        .order_by()
    )
    serializer_class = NshNonTradeHeadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NshNonTradeSalesFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class SumApi(ModelViewSet):
    def get(self, request):
        query = FactNtSalesPlanning.objects.filter(
            period_key__month__gte=request.GET.get("month", ""),
            period_key__year__gte=request.GET.get("year", ""),
            period_key__month__lte=datetime.now().month,
            period_key__year__lte=datetime.now().year,
        ).aggregate(Sum("yearly_sales_plan"))
        return Responses.success_response(
            "fetch data for your selected year", data=query
        )


class NtCreditLimitDropdown(GenericAPIView):
    """nt credit limit dropdown view class."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CreditLimitFilter

    def __get_nt_credit_limit_query(self, query_string):
        self.filterset_class = CreditLimitFilter
        return (
            self.filter_queryset(NtCreditLimit.objects.all())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def __get_nt_acc_relations_query(self, query_string, filter_query):
        self.filterset_class = NtAccRelationFilter
        return self.filter_queryset(
            NtAccRelation.objects.filter(filter_query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "cust__party_name": self.__get_nt_credit_limit_query("cust__party_name"),
            "cust__party_id": self.__get_nt_credit_limit_query("cust__party_id"),
            "credit_limit": self.__get_nt_credit_limit_query("credit_limit"),
            "creation_date": self.__get_nt_credit_limit_query("creation_date"),
            "comment": self.__get_nt_credit_limit_query("comment"),
            "status": self.__get_nt_credit_limit_query("status"),
            "account_type": self.__get_nt_acc_relations_query(
                "account_type__acct_type_code", Q(cust__credit_limits__isnull=False)
            ),
            "ntso": self.__get_nt_acc_relations_query(
                "resource__resource_name",
                Q(resource__designation="NTSO", cust__credit_limits__isnull=False),
            ),
            "tpc": self.__get_nt_acc_relations_query(
                "resource__resource_name",
                Q(resource__designation="TPC", cust__credit_limits__isnull=False),
            ),
            "ntso_code": self.__get_nt_acc_relations_query(
                "resource__id",
                Q(resource__designation="NTSO", cust__credit_limits__isnull=False),
            ),
            "tpc_code": self.__get_nt_acc_relations_query(
                "resource__id",
                Q(resource__designation="TPC", cust__credit_limits__isnull=False),
            ),
        }

        return Responses.success_response(
            "nt credit limit set dropdown data.", data=data
        )


class DimCustomersView(ListAPIView):
    """Dim customers list view class."""

    queryset = DimCustomersTest.objects.all()
    serializer_class = DimCustomersSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("acc_relations__resource", "cust_cat")
    search_fields = ("^party_name", "^party_id")
    # pagination_class = CustomPagination

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get("acc_relations"):
            return queryset.filter(acc_relations__isnull=False).distinct("id")
        return queryset


class TransferAccounts(ModelViewSet):
    """Transfer accounts view-set class."""

    queryset = NtAccRelation.objects.order_by("-creation_date")
    serializer_class = TransferAccountsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NtAccRelationFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NtAccRelationSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=True, context={"user_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request):
        aac_relation_obj = NtAccRelation.objects.filter(
            cust=request.data["cust"]
        ).first()
        if aac_relation_obj:
            request.data["created_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            acc_relation_serializer = NtAccRelationUpdateOrCreateSerializer(
                instance=aac_relation_obj, data=request.data
            )
            if not acc_relation_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Updation error",
                    data=acc_relation_serializer.errors,
                )
            aac_relation_obj = acc_relation_serializer.save()
            return Responses.success_response(
                "Updated successfully", data=acc_relation_serializer.data
            )
        else:
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            serializer = NtAccRelationUpdateOrCreateSerializer(data=request.data)

            if not serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=serializer.errors
                )
            serializer.save()
            return Responses.success_response(
                "Inserted successfully", data=serializer.data
            )


class TransferOfficersAllAccounts(GenericAPIView):
    """Transfer officer all accounts api."""

    serializer_class = TransferOfficersAllAccountsSerializer
    helper = TransferAccountsHelper

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.helper.background_create(
            request.user.id,
            serializer.validated_data["comments"],
            serializer.validated_data["resource"].id,
            serializer.validated_data["transfer_from"].id,
        )
        return Response({"Accounts transfer status": "Started"})


class ThreeMonthsOldCustomerData(ListAPIView):
    queryset = NshNonTradeSales.objects.all()
    serializer_class = NshNonTradeSalesForThreeMonthOldSerializer
    filterset_class = NshNonTradeSalesFilter
    pagination_class = CustomPagination

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(
            invoice_date__gte=datetime.now() + relativedelta(months=-3)
        )


class GetCustomerBasedOnResource(ModelViewSet):
    serializer_class = DimCustomersSerializer

    def get(self, request):
        queryset = NtAccRelation.objects.filter(
            resource=request.query_params.get("resource_id")
        ).values("cust")
        query_set = DimCustomersTest.objects.filter(id__in=queryset)
        serializer = self.serializer_class(query_set, many=True)
        return Responses.success_response("getting data", data=serializer.data)


class CrmNthQuotNcrExcpApprViewSet(ModelViewSet):
    """CRM Non Trade Head Quotation Ncr Exception Approval Class"""

    queryset = CrmNthQuotNcrExcpAppr.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CrmNthQuotNcrExcpApprSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthQuotNcrExcpApprFilter
    pagination_class = CustomPagination


class CrmNthSoNcrExcpApprViewSet(ModelViewSet):
    """CRM Non Trade Head Source Ncr Exception Approval Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthSoNcrExcpAppr.objects.all()
    serializer_class = CrmNthSoNcrExcpApprSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = CrmNthSoNcrExcpApprFilter


class CrmNthSourceChgReqViewSet(ModelViewSet):
    """CRM Non Trade Head Source Change Request Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthSourceChgReq.objects.all()
    serializer_class = CrmNthSourceChgReqSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthSourceChgReqFilter
    pagination_class = CustomPagination


class CrmNthExtendValidityViewSet(ModelViewSet):
    """CRM Non Trade Extend Validity Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthExtendValidity.objects.all()
    serializer_class = CrmNthExtendValiditySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthExtendValidityFilter
    pagination_class = CustomPagination


class CrmNthBankGuartApprViewSet(ModelViewSet):
    "crm nth bank guart appr class"
    permission_classes = (IsAuthenticated,)
    queryset = CrmNthBankGuartAppr.objects.all()
    serializer_class = CrmNthBankGuartApprSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination


class CrmNthOrderCancApprViewSet(ModelViewSet):
    """CRM Non Trade Head Order Cancel Approval Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthOrderCancAppr.objects.all()
    serializer_class = CrmNthOrderCancApprSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthOrderCancApprFilter
    pagination_class = CustomPagination


class CrmNthLeadFormViewSet(ModelViewSet):
    """CRM Non Trade Head Lead Form Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthLeadForm.objects.order_by("-last_update_date")
    serializer_class = CrmNthLeadFormSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthLeadFormFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        serializer.save()
        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class CrmNthRefuReqViewSet(ModelViewSet):
    """CRM Non Trade Head Refund Request Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthRefuReq.objects.all()
    serializer_class = CrmNthRefuReqSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthRefuReqFilter
    pagination_class = CustomPagination


class CrmNthCustCodeCreViewSet(ModelViewSet):
    """CRM Non Trade Customer Code Cre Class"""

    permission_classes = (IsAuthenticated,)
    queryset = CrmNthCustCodeCre.objects.all()
    serializer_class = CrmNthCustCodeCreSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthCustCodeCreFilter
    pagination_class = CustomPagination


class FactNtSalesPlanAnnualViewSet(ModelViewSet):
    """FactNtSalesPlanAnnual Non Trade Customer Code Cre Class"""

    permission_classes = (IsAuthenticated,)
    queryset = FactNtSalesPlanAnnual.objects.all()
    serializer_class = FactNtSalesPlanAnnualSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanAnnualFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class FactNtSalesPlanningMonthViewSet(ModelViewSet):
    """FactNtSalesPlanMonth Class"""

    permission_classes = (IsAuthenticated,)
    queryset = FactNtSalesPlanningMonth.objects.all()
    serializer_class = FactNtSalesPlanningMonthSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanningMonthFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        serializer.save()
        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class FactNtSalesPlanningMonthGetPreviousMonthDataViewSet(ModelViewSet):
    """FactNtSalesPlanMonth GET PREVIOUS MONTH DATA Class"""

    permission_classes = (IsAuthenticated,)
    queryset = FactNtSalesPlanningMonth.objects.all()
    serializer_class = FactNtSalesPlanningMonthSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanningMonthFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")
        product = request.query_params.get("product")

        prv_year = year - 1
        prv_to_prv_year = prv_year - 1
        prv_mnth = None
        if month == 1:
            mnth = "January"
            prv_mnth = "December"
            year = year - 1
        elif month == 2:
            prv_mnth = "January"
            mnth = "February"
        elif month == 3:
            prv_mnth = "February"
            mnth = "March"
        elif month == 4:
            prv_mnth = "March"
            mnth = "April"
        elif month == 5:
            prv_mnth = "April"
            mnth = "May"
        elif month == 6:
            prv_mnth = "May"
            mnth = "June"
        elif month == 7:
            prv_mnth = "June"
            mnth = "July"
        elif month == 8:
            prv_mnth = "July"
            mnth = "August"
        elif month == 9:
            prv_mnth = "August"
            mnth = "September"
        elif month == 10:
            prv_mnth = "September"
            mnth = "October"
        elif month == 11:
            prv_mnth = "October"
            mnth = "November"
        elif month == 12:
            prv_mnth = "November"
            mnth = "December"
        previous_mnth_qty = (
            FactNtSalesPlanningMonth.objects.filter(
                month=prv_mnth, year=year, product=product, brand=brand, state=state
            )
            .values("monthly_qty")
            .last()
        )
        prv_yr_selctd_mnth_qty = (
            FactNtSalesPlanningMonth.objects.filter(
                month=mnth, year=prv_year, product=product, brand=brand, state=state
            )
            .values("monthly_qty")
            .last()
        )

        prv_to_prv_yr_selctd_mnth_qty = (
            FactNtSalesPlanningMonth.objects.filter(
                month=mnth,
                year=prv_to_prv_year,
                product=product,
                brand=brand,
                state=state,
            )
            .values("monthly_qty")
            .last()
        )
        data_dict = {
            "previous_mnth_qty": previous_mnth_qty,
            "prv_yr_selctd_mnth_qty": prv_yr_selctd_mnth_qty,
            "prv_to_prv_yr_selctd_mnth_qty": prv_to_prv_yr_selctd_mnth_qty,
        }

        return Responses.success_response(
            "Previous month data fetched succesfully", data=data_dict
        )


class FactNtSalesPlanningNcrGetPreviousMonthDataViewSet(ModelViewSet):
    """FactNtSalesPlanNcr Get Previous Month Data Class"""

    def get(self, request):
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")
        product = request.query_params.get("product")

        prv_year = year - 1
        prv_to_prv_year = prv_year - 1
        prv_mnth = None
        if month == 1:
            mnth = "Jan"
            prv_mnth = "Dec"
        elif month == 2:
            prv_mnth = "Jan"
            mnth = "Feb"
        elif month == 3:
            prv_mnth = "Feb"
            mnth = "Mar"
        elif month == 4:
            prv_mnth = "Mar"
            mnth = "Apr"
        elif month == 5:
            prv_mnth = "Apr"
            mnth = "May"
        elif month == 6:
            prv_mnth = "May"
            mnth = "Jun"
        elif month == 7:
            prv_mnth = "Jun"
            mnth = "Jul"
        elif month == 8:
            prv_mnth = "Jul"
            mnth = "Aug"
        elif month == 9:
            prv_mnth = "Aug"
            mnth = "Sep"
        elif month == 10:
            prv_mnth = "Sep"
            mnth = "Oct"
        elif month == 11:
            prv_mnth = "Oct"
            mnth = "Nov"
        elif month == 12:
            prv_mnth = "Nov"
            mnth = "Dec"

        previous_mnth_qty = (
            FactNtSalesPlanningNcr.objects.filter(
                month=prv_mnth,
                year=(year - 1 if prv_mnth == "Dec" else year),
                product=product,
                brand=brand,
                state=state,
            )
            .values("monthly_ncr_target")
            .last()
        )
        prv_yr_selctd_mnth_qty = (
            FactNtSalesPlanningNcr.objects.filter(
                month=mnth, year=prv_year, product=product, brand=brand, state=state
            )
            .values("monthly_ncr_target")
            .last()
        )
        prv_to_prv_yr_selctd_mnth_qty = (
            FactNtSalesPlanningNcr.objects.filter(
                month=mnth,
                year=prv_to_prv_year,
                product=product,
                brand=brand,
                state=state,
            )
            .values("monthly_ncr_target")
            .last()
        )
        data_dict = {
            "previous_mnth_qty": previous_mnth_qty,
            "prv_yr_selctd_mnth_qty": prv_yr_selctd_mnth_qty,
            "prv_to_prv_yr_selctd_mnth_qty": prv_to_prv_yr_selctd_mnth_qty,
        }

        return Responses.success_response(
            "Previous month data fetched succesfully", data=data_dict
        )


class FactNtSalesPlanningNcrViewSet(ModelViewSet):
    """FactNtSalesPlanMonth Class"""

    permission_classes = (IsAuthenticated,)
    queryset = FactNtSalesPlanningNcr.objects.all()
    serializer_class = FactNtSalesPlanningNcrSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FactNtSalesPlanningNcrFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class ConsensusTargetForNtViewSet(ModelViewSet):
    """FactNtSalesPlanAnnual Non Trade Customer Code Cre Class"""

    permission_classes = (IsAuthenticated,)
    queryset = ConsensusTarget.objects.all()
    serializer_class = ConsensusTargetForNtUseSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = ConsensusTargetForNtUseSerializer
    pagination_class = CustomPagination


class ConsensusTargetForNtTargetSumViewSet(ModelViewSet):
    """FactNtSalesPlanAnnual Non Trade Customer Code Cre Class"""

    def get(self, request):
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")

        if month == 1:
            mnth = "January"
        elif month == 2:
            mnth = "February"
        elif month == 3:
            mnth = "March"
        elif month == 4:
            mnth = "April"
        elif month == 5:
            mnth = "May"
        elif month == 6:
            mnth = "June"
        elif month == 7:
            mnth = "July"
        elif month == 8:
            mnth = "August"
        elif month == 9:
            mnth = "September"
        elif month == 10:
            mnth = "October"
        elif month == 11:
            mnth = "November"
        elif month == 12:
            mnth = "December"

        consensus_target_sum = (
            ConsensusTarget.objects.filter(
                brand=brand, state=state, date__year=year, month=mnth
            )
            .values("consensus_target")
            .last()
        )
        return Responses.success_response(
            "consensus target total fetched successfully", data=consensus_target_sum
        )


class SumForAnnualTargetColumnWise(GenericAPIView):
    queryset = FactNtSalesPlanAnnual.objects.all()

    def get(self, request):
        data = {}
        items = self.get_queryset()
        data["fact_nt_jan_sum"] = sum(items.values_list("fact_nt_jan", flat=True))
        data["fact_nt_feb_sum"] = sum(items.values_list("fact_nt_feb", flat=True))
        data["fact_nt_mar_sum"] = sum(items.values_list("fact_nt_mar", flat=True))
        data["fact_nt_apr_sum"] = sum(items.values_list("fact_nt_apr", flat=True))
        data["fact_nt_may_sum"] = sum(items.values_list("fact_nt_may", flat=True))
        data["fact_nt_jun_sum"] = sum(items.values_list("fact_nt_jun", flat=True))
        data["fact_nt_jul_sum"] = sum(items.values_list("fact_nt_jul", flat=True))
        data["fact_nt_aug_sum"] = sum(items.values_list("fact_nt_aug", flat=True))
        data["fact_nt_sep_sum"] = sum(items.values_list("fact_nt_sep", flat=True))
        data["fact_nt_oct_sum"] = sum(items.values_list("fact_nt_oct", flat=True))
        data["fact_nt_nov_sum"] = sum(items.values_list("fact_nt_nov", flat=True))
        data["fact_nt_dec_sum"] = sum(items.values_list("fact_nt_dec", flat=True))
        return Responses.success_response(
            "fetched sum of monthly data for annual year", data=data
        )


class DimProductTestDropdown(GenericAPIView):
    queryset = DimProductTest.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DimProductTestFilter

    def __get_dim_product_test_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "brand": self.__get_dim_product_test_query("brand"),
            "product": self.__get_dim_product_test_query("product"),
            "packing_type": self.__get_dim_product_test_query("packing_type"),
        }
        return Responses.success_response("dim product test dropdown data.", data=data)


class DimCustomersTestViewSet(ModelViewSet):
    """dim customer test Class"""

    permission_classes = (IsAuthenticated,)
    queryset = DimCustomersTest.objects.all()
    serializer_class = DimCustomersTestSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DimCustomersTestFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        data = (self.filter_queryset(self.get_queryset())).last()
        return Responses.success_response("data fetched succesfully", data=data)


class NcrCalculator(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    serializer_class = TOebsSclArNcrAdvanceCalcTabSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "product",
        "packing_type",
        "unloading_by",
        "state",
        "city",
        "district",
        "mode_of_transport",
        "subsidy_lot",
    )
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values(
            "product", "packing_type", "unloading_by", "state", "city", "district", "id"
        ).annotate(
            quantity_invoiced=Avg("quantity_invoiced"),
            misc_charges=Avg("misc_charges"),
            unit_selling_price=Avg("unit_selling_price"),
            unloading_charges=Avg("unloading_charges"),
            demurrages_and_warfages=Avg("demurrages_and_warfages"),
            shortage=Avg("shortage"),
            primary_freight=Avg("primary_freight"),
            secondary_freight=Avg("secondary_freight"),
            rebate_and_discount=Avg("rebate_and_discount"),
            ncr_subsidy=Avg("ncr_subsidy"),
            packing_charges=Avg("packing_charges"),
            rake_charges=Avg("rake_charges"),
        )
        mode_of_transport = (
            queryset.annotate(Count("mode_of_transport"))
            .order_by("-mode_of_transport__count")
            .first()
            .mode_of_transport__count
        )
        uom_code = (
            queryset.annotate(Count("uom_code"))
            .order_by("-uom_code__count")
            .first()
            .uom_code__count
        )
        subsidy_lot = (
            queryset.annotate(Count("subsidy_lot"))
            .order_by("-subsidy_lot__count")
            .first()
            .subsidy_lot__count
        )
        data.first().update(
            {
                "mode_of_transport": mode_of_transport,
                "uom_code": uom_code,
                "subsidy_lot": subsidy_lot,
            }
        )
        return Response(data.first())

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ncr_without_subsidy = (
            serializer.validated_data["unit_selling_price"]
            - serializer.validated_data["incentive"]
            - serializer.validated_data["misc_charges"]
            - serializer.validated_data["third_party"]
            - serializer.validated_data["other_expenses"]
            - serializer.validated_data["sgst_igst"]
            - serializer.validated_data["clinker_avg_freight"]
            - instance.unloading_charges
            - instance.ncr_subsidy
            - instance.rebate_and_discount
            - instance.packing_charges
            - instance.secondary_freight
            - instance.primary_freight
            - instance.shortage
            - instance.demurrages_and_warfages
            - instance.rake_charges
        )

        ncr_with_subsidy = ncr_without_subsidy + instance.ncr_subsidy
        contribution = ncr_without_subsidy - serializer.validated_data["variable_cost"]

        data = {
            "ncr": ncr_without_subsidy,
            "ncr_with_subsidy": ncr_with_subsidy,
            "contribution": contribution,
        }
        return Response(data)


class NcrCalculatorDropdown(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "product",
        "packing_type",
        "unloading_by",
        "state",
        "city",
        "district",
    )

    def __get_ncr_calculated_dropdown_query(self, query_str, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(query)
            .values_list(query_str, flat=True)
            .distinct(query_str)
            .order_by(query_str)
        )

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "ncr calculator dropdown:",
            data={
                "product": self.__get_ncr_calculated_dropdown_query(
                    "product", ~Q(product__startswith="AAC")
                ),
                "packing_type": self.__get_ncr_calculated_dropdown_query(
                    "packing_type"
                ),
                "unloading_by": self.__get_ncr_calculated_dropdown_query(
                    "unloading_by"
                ),
                "state": self.__get_ncr_calculated_dropdown_query("state"),
                "city": self.__get_ncr_calculated_dropdown_query("city"),
                "district": self.__get_ncr_calculated_dropdown_query("district"),
            },
        )


class SchemeProductDropdown(ModelViewSet):
    def get(self, request):
        brand = request.query_params.get("brand")
        grade = request.query_params.get("grade")
        packing_type = request.query_params.get("packing_type")

        queryset = (
            DimProductTest.objects.filter(
                brand=brand, packing_type=packing_type, product__contains=grade
            )
            .values_list("product", flat=True)
            .distinct()
        )
        return Responses.success_response("product data list", data=queryset)


class NonTradeSalesPlanningAdherence(ModelViewSet):
    def get(self, request):
        org_ids = [101, 102, 103]
        invoice_date = datetime.strptime(
            request.query_params.get("invoice_date"), "%Y-%m-%d"
        ).date()
        try:
            sale_data_sum = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                invoice_date__date=invoice_date,
                order_classification="NON TRADE",
                org_id__in=org_ids,
            ).aggregate(quantity_invoiced=Sum("quantity_invoiced"))
        except:
            sale_data_sum = None
        try:
            target_data_sum = ConsensusTarget.objects.aggregate(
                consensus_target=Sum("consensus_target")
            )
        except:
            target_data_sum = None

        return Responses.success_response(
            "sales planing adherence data",
            data=round(
                sale_data_sum["quantity_invoiced"]
                / target_data_sum["consensus_target"],
                2,
            ),
        )


class ResourcesNameDropdown(ModelViewSet):
    def get(self, request):
        resource_name = DimResources.objects.values(
            "resource_id", "resource_name", "designation"
        ).order_by("resource_name")
        return Responses.success_response(
            "dropdown fetched successfully", data=resource_name
        )


class NTInputSPConsensusTarget(GenericAPIView):
    def get(self, request):
        year = request.query_params.get("year")
        brand = request.query_params.get("brand")
        start_date = datetime(int(year), 4, 1)
        end_date = datetime((int(year) + 1), 3, 31)
        state = None
        queryset = (
            ConsensusTarget.objects.filter(
                date__gte=start_date, date__lte=end_date, brand=brand
            )
            .values("state", "month", "date")
            .annotate(Count("state"), Count("month"), Sum("nt_poduct_target"))
            .order_by("state", "month")
        )
        # grouped_data = []
        # for item in queryset:
        #     state = item["state"]
        #     month = item["month"]
        #     date = item["date"]
        #     nt_poduct_target = item["nt_poduct_target__sum"]

        #     if state in grouped_data:
        #         grouped_data[state].append(
        #             {"month": month, "date": date, "nt_poduct_target": nt_poduct_target}
        #         )
        #     else:
        #         grouped_data[state] = [
        #             {"month": month, "date": date, "nt_poduct_target": nt_poduct_target}
        #         ]

        return Responses.success_response("data", data=queryset)


class NTPremiumProductsMasterTmpDropdown(GenericAPIView):
    def get(self, request):
        queryset = (
            PremiumProductsMasterTmp.objects.values("grade", "bag_type")
            .annotate(Count("grade"), Count("bag_type"))
            .order_by("grade")
            .values("grade", "bag_type")
        )
        return Responses.success_response("premium product dropdown", data=queryset)


class NtResourceTargetViewSet(DownloadUploadViewSet):
    """NT Resource Target view set class"""

    queryset = NtResourceTarget.objects.all()
    serializer_class = NtResourceTargetSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NtResourceTargetFilter
    pagination_class = CustomPagination


class NtMarketTargetBulkCreateViewSet(GenericAPIView):
    """NT Market Target Bulk Create Class"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request_data = request.data
        nt_resource_serializer = NtMarketTargettBulkCreateSerializer(
            data=request_data,
            context={
                "created_by": request.user.id,
            },
            many=True,
        )
        nt_resource_serializer.is_valid(raise_exception=True)
        nt_resource_serializer.save()
        return Responses.success_response(
            "created successfully", data=nt_resource_serializer.data
        )


class NtMonthlySalesPlanNcrData(ModelViewSet):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TOebsSclArNcrAdvanceCalcTabFilter

    def get(self, request, *args, **kwargs):
        try:
            sum_of_quantity_invoice = self.filter_queryset(
                self.get_queryset()
            ).aggregate(quantity_invoice=Sum("quantity_invoiced"))
        except:
            sum_of_quantity_invoice = None

        try:
            sum_ncr = self.filter_queryset(self.get_queryset()).aggregate(
                ncr=Sum(F("ncr") * F("quantity_invoiced"))
            )
        except:
            sum_ncr = None

        try:
            ncr = round(
                ((sum_ncr["ncr"]) / sum_of_quantity_invoice["quantity_invoice"]), 2
            )
        except:
            ncr = None

        return Responses.success_response("ncr fetched successfully", data=ncr)


class MonthlyTargetSettingTargetSum(GenericAPIView):
    queryset = MonthlyTargetSetting.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MonthlyTargetSettingFilter
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return self.get_paginated_response(
            self.paginate_queryset(
                self.filter_queryset(self.get_queryset())
                .values("brand", "state", "packing", "product")
                .annotate(Sum("target"))
            )
        )


class MonthlyTargetSettingViewSet(ModelViewSet):
    queryset = MonthlyTargetSetting.objects.all()
    serializer_class = MonthlyTargetSettingSerializer
    pagination_class = CustomPagination

    def post(self, request):
        monthly_target_serializer_data = MonthlyTargetSettingSerializer(
            data=request.data, context={"request": request}
        )
        monthly_target_serializer_data.is_valid(raise_exception=True)
        monthly_target_serializer_data.save()
        return Responses.success_response(
            "created successfully", data=monthly_target_serializer_data.data
        )


class NtMonthlySalesPlanContributionData(ModelViewSet):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TOebsSclArNcrAdvanceCalcTabFilter

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        try:
            sum_of_quantity_invoice = self.filter_queryset(
                self.get_queryset()
            ).aggregate(quantity_invoice=Sum("quantity_invoiced"))
        except:
            sum_of_quantity_invoice = None
        try:
            sum_ncr = self.filter_queryset(self.get_queryset()).aggregate(
                ncr=Sum(F("ncr") * F("quantity_invoiced"))
            )

            ncr = round(
                ((sum_ncr["ncr"]) / sum_of_quantity_invoice["quantity_invoice"]), 2
            )
        except:
            ncr = None
        try:
            subsidy_lots = (
                self.filter_queryset(self.get_queryset()).values_list(
                    "subsidy_lot", flat=True
                )
            ).distinct()
            sum_vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=subsidy_lots, month__gte=start_date, month__lte=end_date
            ).aggregate(vpc=Sum("vpc"))
            vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=subsidy_lots, month__gte=start_date, month__lte=end_date
            ).values_list("vpc", flat=True)

            avg_vpc = round(
                (sum_vpc_historical_data["vpc"] / len(vpc_historical_data)), 2
            )

        except:
            avg_vpc = None
        try:
            contribution = ncr - avg_vpc
        except:
            contribution = None

        return Responses.success_response(
            "contribution fetched successfully", data=contribution
        )


class PremiumProductsMasterTmpBGPDropdown(GenericAPIView):
    """Brand approval dropdown api."""

    queryset = PremiumProductsMasterTmp.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "org_id",
        "grade",
        "bag_type",
        "revised_name",
        "packaging_condition",
    )

    def __get_branding_approval_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "org_id": self.__get_branding_approval_dropdown_query("org_id"),
            "grade": self.__get_branding_approval_dropdown_query("grade"),
            "bag_type": self.__get_branding_approval_dropdown_query("bag_type"),
            "revised_name": self.__get_branding_approval_dropdown_query("revised_name"),
            "packaging_condition": self.__get_branding_approval_dropdown_query(
                "packaging_condition"
            ),
        }
        return Responses.success_response("Premium product master dropdown", data=data)


class NonTradeHeadMonthlySalesData(DownloadUploadViewSet):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.filter(
        ~Q(sales_type="DM"),
        ~Q(org_id=101),
        cust_categ="NT",
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("org_id", "cust_categ", "sales_type", "district", "city")
    serializer_class = TOebsSclArNcrAdvanceCalcTabDownloadSerializer
    pagination_class = CustomPagination
    file_name = "nontrade_head_monthly_sales"

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def bucket_data(self, days, districts_list):
        queryset = (
            self.filter_queryset(
                self.get_queryset().filter(
                    invoice_date__range=days, district__in=districts_list
                )
            )
            .values("state", "district", "org_id", "packing_bag", "product")
            .annotate(
                bucket=Sum("quantity_invoiced"),
            )
        )
        bucket_df = pd.DataFrame(queryset)
        return bucket_df

    def list(self, request, *args, **kwargs):
        try:
            month = int(request.query_params.get("month", datetime.now().month))
            year = int(request.query_params.get("year", datetime.now().year))
            state = request.query_params.get("state")
            districts_list = self.get_districts(state)

            current_month_total_sales = self.bucket_data(
                [
                    datetime_date(day=1, month=month, year=year),
                    datetime_date(
                        day=monthrange(year, month)[1], month=month, year=year
                    ),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_total_sales"})
            current_month_bucket1 = self.bucket_data(
                [
                    datetime_date(day=1, month=month, year=year),
                    datetime_date(day=10, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket1"})
            if current_month_bucket1.empty:
                current_month_bucket1 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket1",
                    ]
                )
            current_month_bucket2 = self.bucket_data(
                [
                    datetime_date(day=11, month=month, year=year),
                    datetime_date(day=20, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket2"})
            if current_month_bucket2.empty:
                current_month_bucket2 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket2",
                    ]
                )
            current_month_bucket3 = self.bucket_data(
                [
                    datetime_date(day=21, month=month, year=year),
                    datetime_date(
                        day=monthrange(year, month)[1], month=month, year=year
                    ),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket3"})
            if current_month_bucket3.empty:
                current_month_bucket3 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket3",
                    ]
                )

            merge_df = pd.merge(
                pd.merge(
                    pd.merge(
                        current_month_bucket1,
                        current_month_bucket2,
                        on=["state", "district", "org_id", "packing_bag", "product"],
                        how="outer",
                    ),
                    current_month_bucket3,
                    on=["state", "district", "org_id", "packing_bag", "product"],
                    how="outer",
                ),
                current_month_total_sales,
                on=["state", "district", "org_id", "packing_bag", "product"],
                how="outer",
            ).fillna(0)

            premium_products_master_data = pd.DataFrame(
                PremiumProductsMasterTmp.objects.filter(
                    org_id__in=merge_df["org_id"].unique(),
                    state__in=merge_df["state"].unique(),
                    grade__in=merge_df["product"].unique(),
                    packaging_condition__in=merge_df["packing_bag"].unique(),
                ).values("org_id", "state", "premium", "grade", "packaging_condition")
            ).rename(columns={"grade": "product", "packaging_condition": "packing_bag"})

            premium_products_merge_df = pd.merge(
                merge_df,
                premium_products_master_data,
                on=["state", "org_id", "packing_bag", "product"],
            )
            premium_products_merge_df = premium_products_merge_df.drop(
                ["product", "org_id", "packing_bag"], axis=1
            )

            premium_products_merge_df = (
                premium_products_merge_df.groupby(["state", "district", "premium"])
                .aggregate(
                    {
                        "current_month_bucket1": "sum",
                        "current_month_bucket2": "sum",
                        "current_month_bucket3": "sum",
                        "current_month_total_sales": "sum",
                    }
                )
                .reset_index()
            )
            premium_products_merge_df["next_month_total_target"] = None
            premium_products_merge_df["next_month_bucket1"] = None
            premium_products_merge_df["next_month_bucket2"] = None
            premium_products_merge_df["next_month_bucket3"] = None

            data = premium_products_merge_df.to_dict(orient="records")
            return Responses.success_response(
                "state head monthly sales data.", data=data
            )
        except:
            return Responses.success_response("No data found", data=[])

    def download(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        data = response.data
        data = data["data"]
        df = pd.DataFrame(data)

        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response


class NonTradeHeadMonthlySalesDropdown(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.filter(
        ~Q(sales_type="DM"),
        ~Q(org_id=101),
        cust_categ="NT",
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def __get_cal_tab_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .distinct(query_string)
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {"state": self.__get_cal_tab_query("state")}
        return Responses.success_response(
            "monthly sales plan state dropdown", data=data
        )


class NTHMarketPotentialAndShareMonthlyViewSet(ModelViewSet):
    def get(self, request, *args, **kwargs):
        state = request.query_params["state"]
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        brands = ["Rockstrong", "Shree", "Bangur"]
        market_potential = MarketMappingMarketPotential.objects.filter(
            month__month=month, month__year=year, state=state, brand__in=brands
        ).aggregate(Avg("market_potential"), Sum("sales"))

        average_market_potential = round(
            market_potential.get("market_potential__avg", 0), 2
        )
        total_sales = market_potential.get("sales__sum", 0)
        if average_market_potential is not None and total_sales is not None:
            market_shares = round((total_sales / average_market_potential), 2)
        else:
            market_shares = 0
        plan = ConsensusTarget.objects.filter(
            date__month=month, date__year=year - 1
        ).aggregate(Sum("consensus_target"))
        sale = (
            TOebsSclArNcrAdvanceCalcTab.objects.filter(
                state=state,
                invoice_date__month=month,
                invoice_date__year=year - 1,
                cust_categ="NT",
            )
            .exclude(Q(org_id=101) | Q(sales_type="DM"))
            .aggregate(Sum("quantity_invoiced"))
        )

        quantity_invoiced_sum = sale.get("quantity_invoiced__sum")
        consensus_target_sum = plan.get("consensus_target__sum")

        if (
            quantity_invoiced_sum is not None
            and consensus_target_sum is not None
            and consensus_target_sum != 0
        ):
            adherence = quantity_invoiced_sum / consensus_target_sum
        else:
            adherence = 0

        data = {
            "market_potential": average_market_potential,
            "market_share": market_shares,
            "plan": plan["consensus_target__sum"],
            "adherence": adherence,
        }
        return Responses.success_response("data fetched ", data=data)


class NTHConsensusTargetMonthlySalesPlan(GenericAPIView):
    queryset = ConsensusTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get(self, request):
        month = int(request.query_params["month"])
        year = request.query_params["year"]
        brand = request.query_params["brand"]
        brand_mapping = {
            "SHREE": "Shree",
            "BANGUR": "Bangur",
            "ROCKSTRONG": "Rockstrong",
        }
        # Assuming 'brand' contains the brand name
        brand = brand_mapping.get(brand, None)
        if month == 1 or month == 2 or month == 3:
            year = int(year) + 1
        data = self.filter_queryset(
            self.get_queryset().filter(brand=brand, date__month=month, date__year=year)
        ).aggregate(
            Sum("premium_product_target"),
            Sum("other_product_target"),
            Sum("nt_poduct_target"),
        )
        final_dict = {
            "premium_product_data": self.format_val(
                data["premium_product_target__sum"]
            ),
            "other_product_data": self.format_val(data["other_product_target__sum"]),
            "nt_product_target": self.format_val(data["nt_poduct_target__sum"]),
        }
        return Responses.success_response("data fetched succesfully", data=final_dict)


class CrmNthLeadFormDropDown(GenericAPIView):
    queryset = CrmNthLeadForm.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmNthLeadFormFilter

    def __get_crm_nth_lead_form_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "customer_name": self.__get_crm_nth_lead_form_dropdown("customer_name"),
            "status": self.__get_crm_nth_lead_form_dropdown("status"),
            "lead_no": self.__get_crm_nth_lead_form_dropdown("lead_no"),
            "lead_by": self.__get_crm_nth_lead_form_dropdown("lead_by"),
            "course_code": self.__get_crm_nth_lead_form_dropdown("course_code"),
            "assigned_to_ntso_kam": self.__get_crm_nth_lead_form_dropdown(
                "assigned_to_ntso_kam"
            ),
            "business_address": self.__get_crm_nth_lead_form_dropdown(
                "business_address"
            ),
            "city": self.__get_crm_nth_lead_form_dropdown("city"),
            "taluka": self.__get_crm_nth_lead_form_dropdown("taluka"),
            "district": self.__get_crm_nth_lead_form_dropdown("district"),
            "state": self.__get_crm_nth_lead_form_dropdown("state"),
            "pin_code": self.__get_crm_nth_lead_form_dropdown("pin_code"),
            "email": self.__get_crm_nth_lead_form_dropdown("email"),
            "project_details": self.__get_crm_nth_lead_form_dropdown("project_details"),
            "contact_number": self.__get_crm_nth_lead_form_dropdown("contact_number"),
            "product": self.__get_crm_nth_lead_form_dropdown("product"),
            "quantity": self.__get_crm_nth_lead_form_dropdown("quantity"),
            "delv_window": self.__get_crm_nth_lead_form_dropdown("delv_window"),
            "delv_address": self.__get_crm_nth_lead_form_dropdown("delv_address"),
            "assigned_to_ntso_kam": self.__get_crm_nth_lead_form_dropdown(
                "assigned_to_ntso_kam"
            ),
        }
        return Responses.success_response("crm nth lead form dropdown.", data=data)


class NtProductTargetByState(GenericAPIView):
    queryset = ConsensusTarget.objects.all()
    # serializer_class = SourceChangeApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("brand",)
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        start_year = request.query_params.get("start_year")
        end_year = int(request.query_params.get("start_year")) + 1
        queryset = (
            self.filter_queryset(self.get_queryset())
            .filter(date__range=[f"{start_year}-04-01", f"{end_year}-03-31"])
            .values(
                "state",
                "month",
                "date",
            )
            .annotate(
                Count("state"),
                target=Sum("nt_poduct_target"),
            )
            .order_by("state")
        )

        return Responses.success_response("Fetched succesfully", data=queryset)


class NonTradeSalesPlanningStateViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningState.objects.all()
    serializer_class = NonTradeSalesPlanningStateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningStateFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_state_data"


class NonTradeSalesPlanningAccountViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningAccount.objects.all()
    serializer_class = NonTradeSalesPlanningAccountSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningAccountFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_account_data"


class NonTradeSalesPlanningDesignationViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningDesignation.objects.all()
    serializer_class = NonTradeSalesPlanningDesignationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningDesignationFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_designation_data"


class NonTradeSalesPlanningProductViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningProduct.objects.all()
    serializer_class = NonTradeSalesPlanningProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningProductFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_product_data"


class NonTradeSalesPlanningStateMonthlyViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningStateMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningStateMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningStateMonthlyFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_state_monthly_data"


class NonTradeSalesPlanningAccountMonthlyViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningAccountMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningAccountMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningAccountMonthlyFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_account_monthly_data"


class NonTradeSalesPlanningDesignationMonthlyViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningDesignationMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningDesignationMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningDesignationMonthlyFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_designation_monthly_data"


class NonTradeSalesPlanningProductMonthlyViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningProductMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningProductMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningProductMonthlyFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_product_monthly_data"


class NtSalesPlanningMonthlyQuantityHistoricalActuals(GenericAPIView):
    """Monthly sales view class."""

    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    helper = NtNcrThresholdHelper

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def get(self, request, *args, **kwargs):
        product = request.query_params.get("product")
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        type = request.query_params.get("type")
        districts_list = self.get_districts(state)
        brand_mapping = {
            "SHREE": 102,
            "BANGUR": 103,
            "ROCKSTRONG": 104,
        }
        # Assuming 'brand' contains the brand name
        org_id = brand_mapping.get(brand, None)

        if type == "AAC":
            product_startswith = None
            if product == "AAC Blocks":
                product_startswith = "AAC"
            elif product == "BlockJoin":
                product_startswith = "Block"
            current_yr_prv_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    org_id=101,
                    district__in=districts_list,
                    product__startswith=product_startswith,
                    invoice_date__date__month=month - 2,
                    invoice_date__date__year=year,
                    active=1,
                )
                .aggregate(quantity=Sum("quantity_invoiced"))
            )
            previous_yr_curr_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    active=1,
                    org_id=101,
                    district__in=districts_list,
                    product__startswith=product_startswith,
                    invoice_date__date__month=month,
                    invoice_date__date__year=year - 1,
                )
                .aggregate(quantity=Sum("quantity_invoiced"))
            )
            annual_plan_current_month_qty = NonTradeSalesPlanningState.objects.filter(
                product=product, month=month, year=year, state=state, type=type
            ).aggregate(Sum("target"))
            monthly_plan_current_month_qty = None
            monthly_plan_current_month_qty_id = None
            monthly_plan_current_month = (
                NonTradeSalesPlanningStateMonthly.objects.filter(
                    product=product, month=month, year=year, state=state, type=type
                )
            )
            if monthly_plan_current_month:
                monthly_plan_current_month_qty_id = monthly_plan_current_month.latest(
                    "id"
                ).id
                monthly_plan_current_month_qty = monthly_plan_current_month.latest(
                    "id"
                ).target

            data_dict = {
                "current_yr_prv_month_qty_invoiced": (
                    current_yr_prv_month_qty_invoiced["quantity"]
                ),
                "previous_yr_curr_month_qty_invoiced": (
                    previous_yr_curr_month_qty_invoiced["quantity"]
                ),
                "annual_plan_current_month_qty": annual_plan_current_month_qty[
                    "target__sum"
                ],
                "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
                "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
            }

        else:
            current_yr_prv_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    active=1,
                    org_id=org_id,
                    district__in=districts_list,
                    product=product,
                    invoice_date__date__month=month - 2,
                    invoice_date__date__year=year,
                )
                .aggregate(quantity=Sum("quantity_invoiced"))
            )
            previous_yr_curr_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    active=1,
                    org_id=org_id,
                    district__in=districts_list,
                    product=product,
                    invoice_date__date__month=month,
                    invoice_date__date__year=year - 1,
                )
                .aggregate(quantity=Sum("quantity_invoiced"))
            )

            annual_plan_current_month_qty = NonTradeSalesPlanningState.objects.filter(
                brand=brand, month=month, year=year, state=state, type=type
            ).aggregate(Sum("target"))
            monthly_plan_current_month_qty = None
            monthly_plan_current_month_qty_id = None
            monthly_plan_current_month = BottomUpNt.objects.filter(
                brand=brand, month=month, year=year, state=state
            )
            if monthly_plan_current_month:
                monthly_plan_current_month_qty_id = monthly_plan_current_month.latest(
                    "id"
                ).id
                monthly_plan_current_month_qty = monthly_plan_current_month.latest(
                    "id"
                ).demand_qty

            data_dict = {
                "current_yr_prv_month_qty_invoiced": (
                    current_yr_prv_month_qty_invoiced["quantity"]
                ),
                "previous_yr_curr_month_qty_invoiced": (
                    previous_yr_curr_month_qty_invoiced["quantity"]
                ),
                "annual_plan_current_month_qty": annual_plan_current_month_qty[
                    "target__sum"
                ],
                "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
                "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
            }

        return Responses.success_response("Fetched Succesfully", data=data_dict)


# class NtSalesPlanningMonthlyNCRMonthActual(GenericAPIView):
#     """Monthly sales view class."""

#     queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()

#     def get_districts(self, state):
#         queryset = (
#             ZoneMappingNew.objects.filter(state=state)
#             .values_list("district", flat=True)
#             .distinct()
#         )
#         return queryset

#     def get(self, request, *args, **kwargs):
#         product = request.query_params.get("product")
#         brand = request.query_params.get("brand")
#         state = request.query_params.get("state")
#         month = int(request.query_params.get("month"))
#         year = int(request.query_params.get("year"))
#         districts_list = self.get_districts(state)
#         brand_mapping = {
#             "SHREE": 102,
#             "BANGUR": 103,
#             "ROCKSTRONG": 104,
#         }

#         # Assuming 'brand' contains the brand name
#         org_id = brand_mapping.get(brand, None)

#         if state:
#             if month == 1:
#                 prv_year = year - 1
#             else:
#                 prv_year = year
#             current_yr_prv_month_qty_invoiced = (
#                 self.filter_queryset(self.get_queryset())
#                 .filter(
#                     org_id=org_id,
#                     district__in=districts_list,
#                     product=product,
#                     invoice_date__date__month=month - 1,
#                     invoice_date__date__year=prv_year,
#                 )
#                 .aggregate(quantity=Sum("quantity_invoiced"))
#             )
#             current_yr_prv_month_qty_invoiced = current_yr_prv_month_qty_invoiced[
#                 "quantity"
#             ]

#             previous_yr_curr_month_qty_invoiced = (
#                 self.filter_queryset(self.get_queryset())
#                 .filter(
#                     org_id=org_id,
#                     district__in=districts_list,
#                     product=product,
#                     invoice_date__date__month=month,
#                     invoice_date__date__year=year - 1,
#                 )
#                 .aggregate(quantity=Sum("quantity_invoiced"))
#             )
#             previous_yr_curr_month_qty_invoiced = previous_yr_curr_month_qty_invoiced[
#                 "quantity"
#             ]

#             monthly_plan_current_month_qty = (
#                 NonTradeSalesPlanningMonthlyNcrTarget.objects.filter(
#                     brand=brand, month=month, year=year, state=state, product=product
#                 )
#             )
#             if monthly_plan_current_month_qty:
#                 monthly_plan_current_month_qty_id = (
#                     monthly_plan_current_month_qty.latest("id").id
#                 )
#                 monthly_plan_current_month_qty = monthly_plan_current_month_qty.latest(
#                     "id"
#                 ).target
#             else:
#                 monthly_plan_current_month_qty_id = None
#                 monthly_plan_current_month_qty = None

#             data_dict = {
#                 "current_yr_prv_month_qty_invoiced": current_yr_prv_month_qty_invoiced,
#                 "previous_yr_curr_month_qty_invoiced": previous_yr_curr_month_qty_invoiced,
#                 "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
#                 "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
#             }

#             return Responses.success_response("Fetched Succesfully", data=data_dict)


class NtSalesPlanningDesignationActuals(GenericAPIView):
    """Monthly sales view class."""

    queryset = NonTradeSalesPlanningDesignationMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningDesignationMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningDesignationMonthlyFilter

    def get(self, request, *args, **kwargs):
        product = request.query_params.get("product")
        brand = request.query_params.get("brand")
        type = request.query_params.get("type")
        so_key = request.query_params.get("so_key")
        kam_key = request.query_params.get("kam_key")
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if type == "AAC":
            annual_plan_current_month_qty = (
                NonTradeSalesPlanningDesignation.objects.filter(
                    product=product,
                    type=type,
                    so_key=so_key,
                    kam_key=kam_key,
                    year=year,
                    month=month,
                )
            )
            if annual_plan_current_month_qty:
                annual_plan_current_month_qty = annual_plan_current_month_qty.latest(
                    "id"
                ).target
            else:
                annual_plan_current_month_qty = None
        else:
            annual_plan_current_month_qty = (
                NonTradeSalesPlanningDesignation.objects.filter(
                    brand=brand,
                    type=type,
                    so_key=so_key,
                    kam_key=kam_key,
                    year=year,
                    month=month,
                )
            )
            if annual_plan_current_month_qty:
                annual_plan_current_month_qty = annual_plan_current_month_qty.latest(
                    "id"
                ).target
            else:
                annual_plan_current_month_qty = None

        monthly_plan_current_month_qty = self.filter_queryset(self.get_queryset())
        if monthly_plan_current_month_qty:
            monthly_plan_current_month_qty_id = monthly_plan_current_month_qty.latest(
                "id"
            ).id
            monthly_plan_current_month_qty = monthly_plan_current_month_qty.latest(
                "id"
            ).target
        else:
            monthly_plan_current_month_qty_id = None
            monthly_plan_current_month_qty = None

        data_dict = {
            "annual_plan_current_month_qty": annual_plan_current_month_qty,
            "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
            "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
        }

        return Responses.success_response("Fetched Succesfully", data=data_dict)


class NtBottomUpAnnualCards(GenericAPIView):
    def get(self, request):
        start_year = int(request.query_params.get("start_year"))
        end_year = start_year + 1
        type = request.query_params.get("type")
        if type == "AAC":
            try:
                previous_year_plan = NonTradeSalesPlanningState.objects.filter(
                    year=start_year - 1, type="AAC"
                ).aggregate(target=Sum("target"))
                previous_year_plan = annual_sales_plan_total_target["target"]
            except:
                previous_year_plan = 0
            try:
                previous_year_actual_plan = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    invoice_date__date__range=[
                        f"{start_year-1}-04-01",
                        f"{end_year-1}-03-31",
                    ],
                    order_classification="NON TRADE",
                    product__startswith="AAC",
                    active=1,
                ).aggregate(
                    quantity_invoiced=Sum("quantity_invoiced"),
                )
                previous_year_actual_plan = previous_year_actual_plan[
                    "quantity_invoiced"
                ]
            except:
                previous_year_actual_plan = 0
            try:
                annual_sales_plan_total_target = (
                    NonTradeSalesPlanningState.objects.filter(
                        year=start_year, type="AAC"
                    ).aggregate(target=Sum("target"))
                )
                annual_sales_plan_total_target = annual_sales_plan_total_target[
                    "target"
                ]
            except:
                annual_sales_plan_total_target = 0
            data_dict = {
                "previous_year_plan": previous_year_plan,
                "previous_year_actual_plan": previous_year_actual_plan,
                "annual_sales_plan_total_target": annual_sales_plan_total_target,
            }

        else:
            try:
                previous_year_plan = ConsensusTarget.objects.filter(
                    date__range=[f"{start_year}-04-01", f"{end_year}-03-31"]
                ).aggregate(
                    nt_poduct_target=Sum("nt_poduct_target"),
                )
                previous_year_plan = previous_year_plan["nt_poduct_target"]
            except:
                previous_year_plan = 0
            try:
                product_list = PremiumProductsMasterTmp.objects.values_list(
                    "grade", flat=True
                ).distinct()
                previous_year_actual_plan = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    invoice_date__date__range=[
                        f"{start_year-1}-04-01",
                        f"{end_year-1}-03-31",
                    ],
                    order_classification="NON TRADE",
                    product__in=product_list,
                    active=1,
                ).aggregate(
                    quantity_invoiced=Sum("quantity_invoiced"),
                )
                previous_year_actual_plan = previous_year_actual_plan[
                    "quantity_invoiced"
                ]
            except:
                previous_year_actual_plan = 0
            try:
                annual_sales_plan_total_target = (
                    NonTradeSalesPlanningState.objects.filter(
                        year=start_year, type="NT"
                    ).aggregate(target=Sum("target"))
                )
                annual_sales_plan_total_target = annual_sales_plan_total_target[
                    "target"
                ]
            except:
                annual_sales_plan_total_target = 0
            data_dict = {
                "previous_year_plan": previous_year_plan,
                "previous_year_actual_plan": previous_year_actual_plan,
                "annual_sales_plan_total_target": annual_sales_plan_total_target,
            }

        return Responses.success_response("Fetched succesfully", data=data_dict)


class NonTradeTopDownMonthlyTargetViewSet(DownloadUploadViewSet):
    queryset = NonTradeTopDownMonthlyTarget.objects.all()
    serializer_class = NonTradeTopDownMonthlyTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeTopDownMonthlyTargetFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_top_down_monthly_target"


class NonTradeSalesPlanningMonthlyNcrTargetViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningMonthlyNcrTarget.objects.all()
    serializer_class = NonTradeSalesPlanningMonthlyNcrTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningMonthlyNcrTargetFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_monthly_ncr_target"


class NonTradeSalesPlanningSelectedYearTotalMonthTargetsViewSet(DownloadUploadViewSet):
    queryset = NonTradeSalesPlanningState.objects.all()
    serializer_class = NonTradeSalesPlanningStateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningStateFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_state_data"

    def rearrange_fiscal_year(self, data, start_month=4):
        result = {}
        for company, targets in data.items():
            new_targets = sorted(targets, key=lambda x: (x["month"] - start_month) % 12)
            result[company] = new_targets
        return result

    def get(self, request):
        type = request.query_params.get("type")
        if type == "AAC":
            data = (
                self.filter_queryset(self.get_queryset())
                .filter(type="AAC")
                .values("product", "month")
                .annotate(Count("month"), target=Sum("target"))
                .values("product", "month", "target")
            ).order_by("product")

            product_names = ["AAC Blocks", "BlockJoin"]

            grouped_data = {product: [] for product in product_names}

            for entry in data:
                product = entry["product"]
                month = entry["month"]
                target = entry["target"]

                if product not in grouped_data:
                    grouped_data[product] = []

                grouped_data[product].append({"month": month, "target": target})
            grouped_data = self.rearrange_fiscal_year(grouped_data)

        else:
            data = (
                self.filter_queryset(self.get_queryset())
                .filter(type="NT")
                .values("brand", "month")
                .annotate(Count("month"), target=Sum("target"))
                .values("brand", "month", "target")
            ).order_by("brand")

            brand_names = ["SHREE", "BANGUR", "ROCKSTRONG"]

            grouped_data = {brand: [] for brand in brand_names}

            for entry in data:
                brand = entry["brand"]
                month = entry["month"]
                target = entry["target"]

                if brand not in grouped_data:
                    grouped_data[brand] = []

                grouped_data[brand].append({"month": month, "target": target})
            grouped_data = self.rearrange_fiscal_year(grouped_data)

        return Responses.success_response("Fetched succesfully", data=grouped_data)


class NtSalesPlanningMonthlyNCRMonthActual(GenericAPIView):
    """Monthly sales view class."""

    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def get(self, request, *args, **kwargs):
        product = request.query_params.get("product")
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        type = request.query_params.get("type")
        districts_list = self.get_districts(state)
        brand_mapping = {
            "SHREE": 102,
            "BANGUR": 103,
            "ROCKSTRONG": 104,
        }

        # Assuming 'brand' contains the brand name
        org_id = brand_mapping.get(brand, None)

        if month == 1:
            prv_year = year - 1
        else:
            prv_year = year
        if type == "AAC":
            product_startswith = None
            if product == "AAC Blocks":
                product_startswith = "AAC"
            elif product == "BlockJoin":
                product_startswith = "Block"
            current_yr_prv_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    active=1,
                    org_id=101,
                    district__in=districts_list,
                    product__startswith=product_startswith,
                    invoice_date__date__month=month - 2,
                    invoice_date__date__year=prv_year,
                )
                .aggregate(
                    ncr_sum=Sum(F("ncr") * F("quantity_invoiced")),
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                current_yr_prv_month_qty_invoiced = (
                    current_yr_prv_month_qty_invoiced["ncr_sum"]
                    / current_yr_prv_month_qty_invoiced["quantity_sum"]
                )
                current_yr_prv_month_qty_invoiced = round(
                    current_yr_prv_month_qty_invoiced, 2
                )
            except:
                current_yr_prv_month_qty_invoiced = None

            previous_yr_curr_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    active=1,
                    org_id=101,
                    district__in=districts_list,
                    product__startswith=product_startswith,
                    invoice_date__date__month=month,
                    invoice_date__date__year=year - 1,
                )
                .aggregate(
                    ncr_total=Sum(F("ncr") * F("quantity_invoiced")),
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                previous_yr_curr_month_qty_invoiced = (
                    previous_yr_curr_month_qty_invoiced["ncr_total"]
                    / previous_yr_curr_month_qty_invoiced["quantity_sum"]
                )
                previous_yr_curr_month_qty_invoiced = round(
                    previous_yr_curr_month_qty_invoiced, 2
                )
            except:
                previous_yr_curr_month_qty_invoiced = None

            monthly_plan_current_month_qty = (
                NonTradeSalesPlanningMonthlyNcrTarget.objects.filter(
                    month=month, year=year, state=state, product=product, type=type
                )
            )
            if monthly_plan_current_month_qty:
                monthly_plan_current_month_qty_id = (
                    monthly_plan_current_month_qty.latest("id").id
                )
                monthly_plan_current_month_qty = monthly_plan_current_month_qty.latest(
                    "id"
                ).target
            else:
                monthly_plan_current_month_qty_id = None
                monthly_plan_current_month_qty = None

        if type == "NT":
            current_yr_prv_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    org_id=org_id,
                    district__in=districts_list,
                    product=product,
                    invoice_date__date__month=month - 2,
                    invoice_date__date__year=prv_year,
                    active=1,
                )
                .aggregate(
                    ncr_sum=Sum(F("ncr") * F("quantity_invoiced")),
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                current_yr_prv_month_qty_invoiced = (
                    current_yr_prv_month_qty_invoiced["ncr_sum"]
                    / current_yr_prv_month_qty_invoiced["quantity_sum"]
                )
                current_yr_prv_month_qty_invoiced = round(
                    current_yr_prv_month_qty_invoiced, 2
                )
            except:
                current_yr_prv_month_qty_invoiced = None

            previous_yr_curr_month_qty_invoiced = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    ~Q(sales_type="DM"),
                    org_id=org_id,
                    district__in=districts_list,
                    product__startswith=product,
                    invoice_date__date__month=month,
                    invoice_date__date__year=year - 1,
                    active=1,
                )
                .aggregate(
                    ncr_total=Sum(F("ncr") * F("quantity_invoiced")),
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                previous_yr_curr_month_qty_invoiced = (
                    previous_yr_curr_month_qty_invoiced["ncr_total"]
                    / previous_yr_curr_month_qty_invoiced["quantity_sum"]
                )
                previous_yr_curr_month_qty_invoiced = round(
                    previous_yr_curr_month_qty_invoiced, 2
                )
            except:
                previous_yr_curr_month_qty_invoiced = None
            monthly_plan_current_month_qty = (
                NonTradeSalesPlanningMonthlyNcrTarget.objects.filter(
                    brand=brand,
                    month=month,
                    year=year,
                    state=state,
                    product=product,
                    type=type,
                )
            )
            if monthly_plan_current_month_qty:
                monthly_plan_current_month_qty_id = (
                    monthly_plan_current_month_qty.latest("id").id
                )
                monthly_plan_current_month_qty = monthly_plan_current_month_qty.latest(
                    "id"
                ).target
            else:
                monthly_plan_current_month_qty_id = None
                monthly_plan_current_month_qty = None

        data_dict = {
            "current_yr_prv_month_qty_invoiced": current_yr_prv_month_qty_invoiced,
            "previous_yr_curr_month_qty_invoiced": previous_yr_curr_month_qty_invoiced,
            "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
            "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
        }

        return Responses.success_response("Fetched Succesfully", data=data_dict)


class NTTopDownMonthProductActual(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def get(self, request, *args, **kwargs):
        product = request.query_params.get("product")
        brand = request.query_params.get("brand")
        state = request.query_params.get("state")
        month = int(request.query_params.get("month"))
        year = int(request.query_params.get("year"))
        districts_list = self.get_districts(state)
        brand_mapping = {
            "SHREE": 102,
            "BANGUR": 103,
            "ROCKSTRONG": 104,
        }
        org_id = brand_mapping.get(brand, None)

        if month == 1:
            year = year - 1
        prv_to_prv_month_qty_invoiced = (
            self.filter_queryset(self.get_queryset())
            .filter(
                ~Q(sales_type="DM"),
                org_id=org_id,
                district__in=districts_list,
                product=product,
                invoice_date__date__month=month - 2,
                invoice_date__date__year=year,
                active=1,
            )
            .aggregate(
                quantity_sum=Sum("quantity_invoiced"),
            )
        )
        try:
            prv_to_prv_month_qty_invoiced = round(
                prv_to_prv_month_qty_invoiced["quantity_sum"], 2
            )
        except:
            prv_to_prv_month_qty_invoiced = None

        monthly_plan_current_month_qty = NonTradeTopDownMonthlyTarget.objects.filter(
            brand=brand,
            month=month,
            year=year,
            state=state,
            product=product,
        )
        if monthly_plan_current_month_qty:
            monthly_plan_current_month_qty_id = monthly_plan_current_month_qty.latest(
                "id"
            ).id
            monthly_plan_current_month_qty = monthly_plan_current_month_qty.latest(
                "id"
            ).target
        else:
            monthly_plan_current_month_qty_id = None
            monthly_plan_current_month_qty = None

        data_dict = {
            "prv_to_prv_month_qty_invoiced": prv_to_prv_month_qty_invoiced,
            "monthly_plan_current_month_qty": monthly_plan_current_month_qty,
            "monthly_plan_current_month_qty_id": monthly_plan_current_month_qty_id,
        }

        return Responses.success_response("Fetched Succesfully", data=data_dict)


class TpcCustomerMappingViewSet(ModelViewSet):
    queryset = TpcCustomerMapping.objects.order_by("-creation_date")
    serializer_class = TpcCustomerMappingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TpcCustomerMappingFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def update(self, request):
        tpc_relation_obj = TpcCustomerMapping.objects.filter(
            customer_name=request.data["customer_name"]
        ).first()
        if tpc_relation_obj:
            request.data["created_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            tpc_relation_serializer = TpcCustomerMappingSerializer(
                instance=tpc_relation_obj, data=request.data
            )
            if not tpc_relation_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Updation error",
                    data=tpc_relation_serializer.errors,
                )
            tpc_relation_obj = tpc_relation_serializer.save()
            return Responses.success_response(
                "Updated successfully", data=tpc_relation_serializer.data
            )
        else:
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            serializer = TpcCustomerMappingSerializer(data=request.data)

            if not serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=serializer.errors
                )
            serializer.save()
            return Responses.success_response(
                "Inserted successfully", data=serializer.data
            )


class TgtOrderDataApCustomerAndTPCDropdown(GenericAPIView):
    """Brand approval dropdown api."""

    queryset = TgtOrderDataAp.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    filter_backends = (SearchFilter,)
    search_fields = ("customer_name", "customer_code")

    def __get_tgt_order_query(self, query1, query2, filter_query=Q):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values(query1, query2)
            .distinct()
        )

    def get(self, request, *args, **kwargs):
        data = {
            "customer_list": self.__get_tgt_order_query(
                "customer_name", "customer_code", Q(customer_name__isnull=False)
            ),
            # "tpc_list": self.__get_tgt_order_query(
            #     "mm_name", "mm_code", Q(mm_name__isnull=False)
            # ),
        }
        return Responses.success_response("tgt order data dropdown", data=data)


class NonTradeSalesPlanningSelectedYearSelectedMonthTotalMonthTargetsViewSet(
    DownloadUploadViewSet
):
    queryset = NonTradeSalesPlanningStateMonthly.objects.all()
    serializer_class = NonTradeSalesPlanningStateMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NonTradeSalesPlanningStateMonthlyFilter
    # pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "non_trade_sales_planning_state_monthly_data"

    def rearrange_fiscal_year(self, data, start_month=4):
        result = {}
        for company, targets in data.items():
            new_targets = sorted(targets, key=lambda x: (x["month"] - start_month) % 12)
            result[company] = new_targets
        return result

    def get(self, request):
        type = request.query_params.get("type")
        if type == "AAC":
            data = (
                self.filter_queryset(self.get_queryset())
                .filter(type="AAC")
                .values("product", "month")
                .annotate(Count("month"), target=Sum("target"))
                .values("product", "month", "target")
            ).order_by("product")

            product_names = ["AAC Blocks", "BlockJoin"]

            grouped_data = {product: [] for product in product_names}

            for entry in data:
                product = entry["product"]
                month = entry["month"]
                target = entry["target"]

                if product not in grouped_data:
                    grouped_data[product] = []

                grouped_data[product].append({"month": month, "target": target})
            grouped_data = self.rearrange_fiscal_year(grouped_data)

        else:
            data = (
                self.filter_queryset(self.get_queryset())
                .filter(type="NT")
                .values("brand", "month")
                .annotate(Count("month"), target=Sum("target"))
                .values("brand", "month", "target")
            ).order_by("brand")

            brand_names = ["SHREE", "BANGUR", "ROCKSTRONG"]

            grouped_data = {brand: [] for brand in brand_names}

            for entry in data:
                brand = entry["brand"]
                month = entry["month"]
                target = entry["target"]

                if brand not in grouped_data:
                    grouped_data[brand] = []

                grouped_data[brand].append({"month": month, "target": target})
            grouped_data = self.rearrange_fiscal_year(grouped_data)

        return Responses.success_response("Fetched succesfully", data=grouped_data)


class TgtOrderDataApTPCDropdown(GenericAPIView):
    """Brand approval dropdown api."""

    queryset = TgtOrderDataAp.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("mm_name", "mm_code")

    def __get_tgt_order_query(self, query1, query2, filter_query=Q):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values(query1, query2)
            .distinct()
        )

    def get(self, request, *args, **kwargs):
        data = {
            "tpc_list": self.__get_tgt_order_query(
                "mm_name", "mm_code", Q(mm_name__isnull=False)
            ),
        }
        return Responses.success_response("tgt order data dropdown", data=data)
