from datetime import datetime

from django.db import transaction
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters.technical_head_filter import *
from analytical_data.models import (
    CrmAnnualSiteConvPlan,
    CrmAnnualSiteConvPlanMonthly,
    CrmMabRateList,
    CrmMaterialtestCertificate,
    CrmNthActivityPlan,
    CrmNthProductApproval,
    NthBudgetPlan,
    NthBudgetPlanMonthly,
)
from analytical_data.serializers import (
    CrmAnnualSiteConvPlanMonthlySerializer,
    CrmAnnualSiteConvPlanSerializer,
    CrmMabRateListSerializer,
    CrmMaterialtestCertificateSerializer,
    CrmNthActivityPlanSerializer,
    CrmNthProductApprovalSerializer,
    NthBudgetPlanMonthlySerializer,
    NthBudgetPlanSerializer,
)
from analytical_data.utils import (
    CustomPagination,
    CustomPagination12records,
    Responses,
)
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class CrmMaterialtestCertificateViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrmMaterialtestCertificate.objects.all().order_by("-id")
    serializer_class = CrmMaterialtestCertificateSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = CrmMaterialtestCertificatefilter

    @transaction.atomic()
    def post(self, request):
        document = request.FILES.get("upload_doc")
        request.data["upload_doc"] = document
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        crm_mkt_tst_certificates = CrmMaterialtestCertificateSerializer(
            data=request.data
        )
        if not crm_mkt_tst_certificates.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=crm_mkt_tst_certificates.errors
            )
        crm_mkt_tst_certificates.save()
        return Responses.success_response(
            "data inserted successfully", data=crm_mkt_tst_certificates.data
        )


class CrmNthProductApprovalViewSet(ModelViewSet):
    queryset = CrmNthProductApproval.objects.all()
    serializer_class = CrmNthProductApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = CrmNthProductApprovalfilter


class CrmNthActivityPlanView(ModelViewSet):
    queryset = CrmNthActivityPlan.objects.all()
    serializer_class = CrmNthActivityPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = CrmNthActivityPlanfilter
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        for data in request.data:
            data["created_by"] = request.user.id
            data["last_update_date"] = datetime.today()
            data["last_updated_by"] = request.user.id
            data["last_update_login"] = request.user.id
            crm_activity_plan = CrmNthActivityPlanSerializer(data=data)
            print(crm_activity_plan)
            if not crm_activity_plan.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=crm_activity_plan.errors
                )
            crm_activity_plan.save()
        return Responses.success_response("data inserted successfully", data=[])

    @transaction.atomic()
    def patch(self, request):
        for data in request.data:
            data["last_update_date"] = datetime.today()
            data["created_by"] = request.user.id
            data["last_updated_by"] = request.user.id
            data["last_update_login"] = request.user.id
            requested_object = CrmNthActivityPlan.objects.get(id=data["id"])
            crm_activity_plan = CrmNthActivityPlanSerializer(
                requested_object, data=data, partial=True
            )
            if not crm_activity_plan.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=crm_activity_plan.errors
                )
            crm_activity_plan.save()
        return Responses.success_response("data updated successfully")


class CrmNthActivityPlanByIdViewSet(ModelViewSet):
    queryset = CrmNthActivityPlan.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_nth_activity_serializer = CrmNthActivityPlanSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched successfully", data=crm_nth_activity_serializer.data
        )


class GetPrvYrSelectdMnthCrmNthActivityPlanViewSet(ModelViewSet):
    """Get previous year selected month crm nth activity data"""

    queryset = CrmNthActivityPlan.objects.all()
    serializer_class = CrmNthActivityPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        state = request.query_params.get("state")
        plan_year = int(request.query_params.get("plan_year"))
        service = request.query_params.get("service")
        service_test = request.query_params.get("service_test")
        service_sub_test = request.query_params.get("service_sub_test")
        current_mnth = int(request.query_params.get("month"))
        prv_plan_year = int(request.query_params.get("plan_year")) - 1
        months_list = {
            1: "manual_chg_jan",
            2: "manual_chg_feb",
            3: "manual_chg_mar",
            4: "manual_chg_apr",
            5: "manual_chg_may",
            6: "manual_chg_jun",
            7: "manual_chg_jul",
            8: "manual_chg_aug",
            9: "manual_chg_sep",
            10: "manual_chg_oct",
            11: "manual_chg_nov",
            12: "manual_chg_dec",
        }
        prvs_yr_crnt_mnth_avg = CrmNthActivityPlan.objects.filter(
            state=state,
            service=service,
            service_test=service_test,
            service_sub_test=service_sub_test,
            plan_year=prv_plan_year,
        ).values(months_list[current_mnth], "district", "state", "id")
        current_yr_crnt_mnth_avg = CrmNthActivityPlan.objects.filter(
            state=state,
            service=service,
            service_test=service_test,
            service_sub_test=service_sub_test,
            plan_year=plan_year,
        ).values(months_list[current_mnth], "district", "state", "id")
        data_dict = {
            "prvs_yr_crnt_mnth_avg": prvs_yr_crnt_mnth_avg,
            "current_yr_crnt_mnth_avg": current_yr_crnt_mnth_avg,
        }
        return Responses.success_response("data fetched successfully", data=data_dict)


class NthBudgetPlanViewSet(DownloadUploadViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = NthBudgetPlan.objects.all()
    serializer_class = NthBudgetPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NthBudgetPlanfilter
    pagination_class = CustomPagination12records
    lookup_field = "id"


class GetPrvYrSelectdMnthNthBudgetPlanViewSet(ModelViewSet):
    """Get previous year selected month data"""

    def get(self, request):
        month = int(request.query_params.get("month"))
        prv_plan_year = int(request.query_params.get("plan_year")) - 1

        prvs_yr_crnt_mnth_avg = NthBudgetPlan.objects.filter(
            plan_year=prv_plan_year, month=month
        ).values("budget", "activity_plan")
        return Responses.success_response(
            "data fetched successfully", data=prvs_yr_crnt_mnth_avg
        )


class CrmAnnualSiteConvDropdown(GenericAPIView):
    queryset = CrmAnnualSiteConvPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district")

    def __get_dropdown_query(self, query_str, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(query)
            .values_list(query_str, flat=True)
            .distinct()
        )

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "crm annual site conv plan dropdown",
            data={
                "state": self.__get_dropdown_query("state", Q(state__isnull=False)),
                "district": self.__get_dropdown_query(
                    "district", Q(district__isnull=False)
                ),
            },
        )


class GetLstYrAvgCrmAnnualSiteConvPlanViewSet(ModelViewSet):
    queryset = CrmAnnualSiteConvPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_class = CrmAnnualSiteConvPlanFilter

    def get_lst_yr_target_avg(self, prv_yr_data):
        if prv_yr_data:
            lst_yr_target_avg = int(
                (
                    prv_yr_data["target_jan"]
                    + prv_yr_data["target_feb"]
                    + prv_yr_data["target_mar"]
                    + prv_yr_data["target_apr"]
                    + prv_yr_data["target_may"]
                    + prv_yr_data["target_jun"]
                    + prv_yr_data["target_jul"]
                    + prv_yr_data["target_aug"]
                    + prv_yr_data["target_sep"]
                    + prv_yr_data["target_oct"]
                    + prv_yr_data["target_nov"]
                    + prv_yr_data["target_dec"]
                )
                / 12
            )
        else:
            lst_yr_target_avg = 0
        return lst_yr_target_avg

    def get_ly_volume_gen_avg(self, prv_yr_data):
        if prv_yr_data:
            ly_no_of_meet_avg = int(
                (
                    prv_yr_data["volume_gen_jan"]
                    + prv_yr_data["volume_gen_feb"]
                    + prv_yr_data["volume_gen_mar"]
                    + prv_yr_data["volume_gen_apr"]
                    + prv_yr_data["volume_gen_may"]
                    + prv_yr_data["volume_gen_jun"]
                    + prv_yr_data["volume_gen_jul"]
                    + prv_yr_data["volume_gen_aug"]
                    + prv_yr_data["volume_gen_sep"]
                    + prv_yr_data["volume_gen_oct"]
                    + prv_yr_data["volume_gen_nov"]
                    + prv_yr_data["volume_gen_dec"]
                )
                / 12
            )
        else:
            ly_no_of_meet_avg = 0
        return ly_no_of_meet_avg

    def get(self, request):
        prv_yr = int(request.query_params.get("year")) - 1
        district = request.query_params.get("district")
        prv_yr_data = (
            (
                self.filter_queryset(self.get_queryset()).filter(
                    plan_year=prv_yr, district=district
                )
            )
            .values()
            .first()
        )

        data = {
            "lst_yr_target_avg": self.get_lst_yr_target_avg(prv_yr_data),
            "ly_volume_gen_avg": self.get_ly_volume_gen_avg(prv_yr_data),
        }
        return Response(data)


class CrmMabRateListUploadDownloadAPIView(DownloadUploadViewSet):
    """Crm mab rate list upload and download api."""

    queryset = CrmMabRateList.objects.all()
    serializer_class = CrmMabRateListSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    auto_generated_fields = (
        "id",
        "created_by",
        "creation_date",
        "last_updated_by",
        "last_update_date",
        "last_update_login",
    )
    filterset_fields = ("state", "district", "media")
    file_name = "crm_mab_rate_list"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context


class CrmAnnualSiteConvPlanViewSet(ModelViewSet):
    """crm annual site conv plan get and post api"""

    queryset = CrmAnnualSiteConvPlan.objects.all()
    serializer_class = CrmAnnualSiteConvPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmAnnualSiteConvPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        for data in request.data:
            annual_site_conv_obj = CrmAnnualSiteConvPlan.objects.filter(
                state=data["state"], plan_year=data["plan_year"]
            ).first()
            if annual_site_conv_obj:
                serializer = self.serializer_class(
                    annual_site_conv_obj, data=data, partial=True
                )
                if not serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in crm annual site conv plan",
                        data=serializer.errors,
                    )
                serializer.save(
                    last_updated_by=request.user.id,
                    last_update_login=request.user.id,
                )
            else:
                data["created_by"] = request.user.id
                data["last_updated_by"] = request.user.id
                data["last_update_login"] = request.user.id
                serializer = self.serializer_class(data=data)
                if not serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in crm annual site conv plan",
                        data=serializer.errors,
                    )
                serializer.save()
        return Responses.success_response(
            "annualsite conv data inserted successfully",
            data=serializer.data,
        )


class PreviousYearMonthAnnualSiteConvPlan(GenericAPIView):
    queryset = CrmAnnualSiteConvPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district")

    def get(self, request, *args, **kwargs):
        months_list = {
            "1": "target_jan_nxt_yr",
            "2": "target_feb_nxt_yr",
            "3": "target_mar_nxt_yr",
            "4": "target_apr_cur_yr",
            "5": "target_may_cur_yr",
            "6": "target_jun_cur_yr",
            "7": "target_jul_cur_yr",
            "8": "target_aug_cur_yr",
            "9": "target_sep_cur_yr",
            "10": "target_oct_cur_yr",
            "11": "target_nov_cur_yr",
            "12": "target_dec_cur_yr",
        }
        month = request.query_params.get("month", "1")
        plan_year = request.query_params.get("year", 2021)
        queryset = self.filter_queryset(self.get_queryset())
        current_queryset = queryset.filter(plan_year=plan_year).values(
            months_list[month], "state", "plan", "plan_year", "district"
        )
        previous_queryset = queryset.filter(plan_year=plan_year - 1).values(
            months_list[month], "state", "plan", "plan_year", "district"
        )
        return Response(
            {
                "current_year_data": current_queryset,
                "previous_year_data": previous_queryset,
            }
        )


class CrmNthProductApprovalDropdown(GenericAPIView):
    queryset = CrmNthProductApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("state", "district")

    def __get_product_appr_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_product_appr_query("state"),
            "district": self.__get_product_appr_query("district"),
        }
        return Responses.success_response("nth product approval dropdown", data=data)


class CrmAnnualSiteConvPlanMonthlyViewSet(DownloadUploadViewSet):
    queryset = CrmAnnualSiteConvPlanMonthly.objects.all()
    serializer_class = CrmAnnualSiteConvPlanMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmAnnualSiteConvPlanMonthlyFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "crm_annual_site_conversion_plan_monthly_data"


class NthBudgetPlanMonthlyViewSet(DownloadUploadViewSet):
    queryset = NthBudgetPlanMonthly.objects.all()
    serializer_class = NthBudgetPlanMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NthBudgetPlanMonthlyFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "nth_budget_plan_monthly_data"
