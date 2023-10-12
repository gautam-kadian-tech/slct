import datetime
import json
from datetime import datetime as dt

from dateutil.relativedelta import relativedelta as rd
from django.db import transaction
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters.crm_infl_assist_filter import *
from analytical_data.filters.crm_infl_chg_filter import *
from analytical_data.filters.influencer_manager_filters import (
    AugmentationOutputFilter,
    CrmInflMgrAnnualPlanFilter,
    CrmInflMgrAnnualPlanMonthlyFilter,
    CrmInflMgrMeetPlanFilter,
    CrmInflMgrMeetPlanMonthlyFilter,
    CrmInflMgrSchemeBudgetFilter,
    CrmInflSchemeFilter,
    InfluencerMeetBudgetOutputFilter,
    InfluencerOutputFilter,
)
from analytical_data.filters.state_case_study_filter import *
from analytical_data.models import (
    AugmentationOutputTable,
    CrmInflAssistReq,
    CrmInflChgReq,
    CrmInflGiftMaster,
    CrmInflGiftScheme,
    CrmInflGiftSchemeItemList,
    CrmInflMgrAnnualPlan,
    CrmInflMgrAnnualPlanMonthly,
    CrmInflMgrMeetPlan,
    CrmInflMgrMeetPlanMonthly,
    CrmInflMgrSchemeBudget,
    CrmInflScheme,
    CrmInflSchemeProductPoint,
    InfluencerMeetBudgetOutput,
    InfluencerMeetingOutput,
    InfluencerTechActivityMaster,
    IntendedAudienceStates,
    InternalCaseResources,
    SclCaseStudy,
)
from analytical_data.serializers import (
    AugmentationOutputTableDownloadSerializer,
    AugmentationOutputTableSerializer,
    CrmInflAssistReqSerializer,
    CrmInflChgReqSerializer,
    CrmInflGiftMasterSerializer,
    CrmInflGiftSchemeSerializer,
    CrmInflMgrAnnualPlanDownloadUploadSerializer,
    CrmInflMgrAnnualPlanMonthlySerializer,
    CrmInflMgrAnnualPlanSerializer,
    CrmInflMgrMeetPlanDownloadUploadSerializer,
    CrmInflMgrMeetPlanMonthlySerializer,
    CrmInflMgrMeetPlanSerializer,
    CrmInflMgrSchemeBudgetSerializer,
    CrmInflSchemeSerializer,
    InfluencerMeetBudgetOutputGetSerializer,
    InfluencerMeetBudgetOutputSerializer,
    InfluencerMeetConstrainedRunSerializer,
    InfluencerMeetingOutputSerializer,
    InfluencerOutputSerializer,
    InfluencerTechActivityMasterSerializer,
    IntendedAudienceStatesSerializer,
    InternalCaseResourcesSerializer,
    SclCaseStudySerializer,
)
from analytical_data.utils.pagination import CustomPagination
from analytical_data.utils.responses import Responses
from analytical_data.view_helpers.connection import connect_db
from analytical_data.view_helpers.influencer_check import InfluencerCheckHelper
from analytical_data.view_helpers.so_augmentation import SoAugmentation
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class StateCaseStudyViewSet(ModelViewSet):
    """State case study CRUDs view set class."""

    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request):
        try:
            dataset = request.data
            document = request.FILES.get("related_doc")
            case_study_id = None
            if dataset:
                states_code = json.loads(dataset["state_code"])
                resource_ids = json.loads(dataset["internal_persons_id"])
                case_study_dict = {
                    "case_subject": dataset["subject_line"],
                    "origin_state": dataset["state_of_origin"],
                    "external_persons": dataset["ext_persons"],
                    "description": dataset["case_study_detail"],
                    "case_date": dataset["case_date"],
                    "created_by": request.user.id,
                    "related_doc": document,
                }

                case_study_serializer = SclCaseStudySerializer(data=case_study_dict)
                if not case_study_serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "some issue rise", data=case_study_serializer.errors
                    )
                case_study_serializer.save()
                case_study_data = case_study_serializer.data
                case_study_id = case_study_data["id"]

                for resource in resource_ids:
                    int_case_res_dict = {
                        "case": case_study_id,
                        "resource_id": resource,
                        "created_by": request.user.id,
                    }
                    int_case_res_serializer = InternalCaseResourcesSerializer(
                        data=int_case_res_dict
                    )
                    if not int_case_res_serializer.is_valid(raise_exception=True):
                        return Responses.error_response(
                            "some issue rise", data=int_case_res_serializer.errors
                        )
                    int_case_res_serializer.save()
                for st_code in states_code:
                    intnd_audnce_sts_dict = {
                        "case": case_study_id,
                        "state_code": st_code,
                        "created_by": request.user.id,
                    }
                    intnd_audnce_sts_serializer = IntendedAudienceStatesSerializer(
                        data=intnd_audnce_sts_dict
                    )
                    if not intnd_audnce_sts_serializer.is_valid(raise_exception=True):
                        return Responses.error_response(
                            "some issue rise", data=intnd_audnce_sts_serializer.errors
                        )
                    intnd_audnce_sts_serializer.save()

            return Responses.success_response(
                "data inserted successfully", data=case_study_serializer.data
            )
        except:
            return Responses.error_response(
                "save state case study data failed", data=int_case_res_serializer.errors
            )


class GetStateCaseStudyDataViewSet(ModelViewSet):
    """Get State Case Study Data"""

    queryset = SclCaseStudy.objects.all().order_by("-id")
    serializer_class = SclCaseStudySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SclCaseStudyFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def patch(self, request):
        try:
            id = request.query_params.get("id")
            case_study_obj = SclCaseStudy.objects.get(id=id)
            if id:
                request.data._mutable = True
                dataset = request.data
                document = request.FILES.get("related_doc")
                case_study_dict = {
                    "case_subject": dataset["subject_line"],
                    "origin_state": dataset["state_of_origin"],
                    "external_persons": dataset["ext_persons"],
                    "description": dataset["case_study_detail"],
                    "case_date": dataset["case_date"],
                    "created_by": request.user.id,
                    "related_doc": document,
                }
                case_study_serializer = SclCaseStudySerializer(
                    case_study_obj, data=case_study_dict
                )
                if not case_study_serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "some issue rise", data=case_study_serializer.errors
                    )
                case_study_obj = case_study_serializer.save()
                internal_case_resources_data = InternalCaseResources.objects.filter(
                    case__id=case_study_obj.id
                )
                if internal_case_resources_data:
                    internal_case_resources_data.delete()
                resource_ids = json.loads(dataset["internal_persons_id"])
                for resource in resource_ids:
                    int_case_res_dict = {
                        "case": case_study_obj.id,
                        "resource_id": resource,
                        "created_by": request.user.id,
                    }
                    int_case_res_serializer = InternalCaseResourcesSerializer(
                        data=int_case_res_dict
                    )
                    if not int_case_res_serializer.is_valid(raise_exception=True):
                        return Responses.error_response(
                            "some issue rise", data=int_case_res_serializer.errors
                        )
                    int_case_res_serializer.save()
                intended_audience_state_data = IntendedAudienceStates.objects.filter(
                    case__id=case_study_obj.id
                )
                if intended_audience_state_data:
                    intended_audience_state_data.delete()
                states_code = json.loads(dataset["state_code"])
                for st_code in states_code:
                    intnd_audnce_sts_dict = {
                        "case": case_study_obj.id,
                        "state_code": st_code,
                        "created_by": request.user.id,
                    }
                    intnd_audnce_sts_serializer = IntendedAudienceStatesSerializer(
                        data=intnd_audnce_sts_dict
                    )
                    if not intnd_audnce_sts_serializer.is_valid(raise_exception=True):
                        return Responses.error_response(
                            "some issue rise", data=intnd_audnce_sts_serializer.errors
                        )
                    intnd_audnce_sts_serializer.save()

                return Responses.success_response(
                    "data updated successfully", data=case_study_serializer.data
                )
        except:
            return Responses.error_response(
                "case study data updation failed", data=int_case_res_serializer.errors
            )


class StateCaseStudyDataByIdViewSet(ModelViewSet):
    queryset = SclCaseStudy.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset
        scl_case_study_serializer = SclCaseStudySerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=scl_case_study_serializer.data
        )


class LastYearMeetPlanAvg(GenericAPIView):
    """Get Annual Meet Plan Last Year Average"""

    queryset = CrmInflMgrMeetPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrMeetPlanFilter

    def get_ly_budget_avg(self, prv_yr_data):
        if prv_yr_data:
            lst_yr_budget_avg = int(
                (
                    prv_yr_data["budget_jan"]
                    + prv_yr_data["budget_feb"]
                    + prv_yr_data["budget_mar"]
                    + prv_yr_data["budget_apr"]
                    + prv_yr_data["budget_may"]
                    + prv_yr_data["budget_jun"]
                    + prv_yr_data["budget_jul"]
                    + prv_yr_data["budget_aug"]
                    + prv_yr_data["budget_sep"]
                    + prv_yr_data["budget_oct"]
                    + prv_yr_data["budget_nov"]
                    + prv_yr_data["budget_dec"]
                )
                / 12
            )
        else:
            lst_yr_budget_avg = 0
        return lst_yr_budget_avg

    def get_ly_no_of_meet_avg(self, prv_yr_data):
        if prv_yr_data:
            ly_no_of_meet_avg = int(
                (
                    prv_yr_data["no_of_meets_jan"]
                    + prv_yr_data["no_of_meets_feb"]
                    + prv_yr_data["no_of_meets_mar"]
                    + prv_yr_data["no_of_meets_apr"]
                    + prv_yr_data["no_of_meets_may"]
                    + prv_yr_data["no_of_meets_jun"]
                    + prv_yr_data["no_of_meets_jul"]
                    + prv_yr_data["no_of_meets_aug"]
                    + prv_yr_data["no_of_meets_sep"]
                    + prv_yr_data["no_of_meets_oct"]
                    + prv_yr_data["no_of_meets_nov"]
                    + prv_yr_data["no_of_meets_dec"]
                )
                / 12
            )
        else:
            ly_no_of_meet_avg = 0
        return ly_no_of_meet_avg

    def get(self, request):
        prv_yr = int(request.query_params.get("year")) - 1
        prv_yr_data = (
            self.filter_queryset(self.get_queryset())
            .filter(plan_year=prv_yr)
            .values()
            .first()
        )
        ly_bdgt_avg_data = self.get_ly_budget_avg(prv_yr_data)
        ly_no_of_meet_avg = self.get_ly_no_of_meet_avg(prv_yr_data)

        data = {
            "ly_bdgt_avg_data": ly_bdgt_avg_data,
            "ly_no_of_meet_avg": ly_no_of_meet_avg,
        }
        return Response(data)


class GetCrmInflAssistReqDataViewSet(ModelViewSet):
    """Get CRM Influencer Assistant Request Data ViewSet"""

    queryset = CrmInflAssistReq.objects.all()
    serializer_class = CrmInflAssistReqSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflAssistReqFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflAssistReqDataByIdViewSet(ModelViewSet):
    queryset = CrmInflAssistReq.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_infl_assist_serializer = CrmInflAssistReqSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=crm_infl_assist_serializer.data
        )


class GetCrmInflChgReqDataViewSet(ModelViewSet):
    """Get CRM Influencer Change Request Data ViewSet"""

    queryset = CrmInflChgReq.objects.all()
    serializer_class = CrmInflChgReqSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflChgReqFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflChgReqDataByIdViewSet(ModelViewSet):
    queryset = CrmInflChgReq.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_infl_chg_serializer = CrmInflChgReqSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=crm_infl_chg_serializer.data
        )


class CreateAnnualInflncrPlnYearly(ModelViewSet):
    """Create Annual Influencer Plan"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        for data in request.data:
            data["created_by"] = request.user.id
            data["plan_year"] = dt.today().year
            data["last_update_date"] = datetime.datetime.now()
            data["last_updated_by"] = request.user.id
            data["last_update_login"] = request.user.id
            crm_in_fl_mgmeetplan = CrmInflMgrAnnualPlanSerializer(data=data)
            if not crm_in_fl_mgmeetplan.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=crm_in_fl_mgmeetplan.errors
                )
            crm_in_fl_mgmeetplan.save()
        return Responses.success_response("data inserted successfully", data=[])


class GetPrvYrSelectdMnthMgrMeetPlanDataViewSet(ModelViewSet):
    """Get previous year selected month data"""

    def get(self, request):
        current_mnth = int(request.query_params.get("month"))
        district = request.query_params.get("district")
        prv_plan_year = int(request.query_params.get("plan_year")) - 1
        months = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]

        get_month = f"budget_{months[current_mnth-1]}"
        no_of_meet = f"no_of_meets_{months[current_mnth-1]}"
        try:
            prvs_yr_crnt_mnth_avg = CrmInflMgrMeetPlan.objects.filter(
                plan_year=prv_plan_year, district=district
            ).values(get_month, no_of_meet, "district")
        except:
            prvs_yr_crnt_mnth_avg = None
        return Responses.success_response(
            "data fetched successfully", data=prvs_yr_crnt_mnth_avg
        )


class GetPrvYrSelectdMnthCrmAnnualPlanViewSet(ModelViewSet):
    """Get previous year selected month data"""

    def get(self, request):
        current_mnth = int(request.query_params.get("month"))
        state = request.query_params.get("state")
        prv_plan_year = int(request.query_params.get("plan_year")) - 1
        month_mapping = {
            1: "jan",
            2: "feb",
            3: "mar",
            4: "apr",
            5: "may",
            6: "jun",
            7: "jul",
            8: "aug",
            9: "sep",
            10: "oct",
            11: "nov",
            12: "dec",
        }

        regt_plan = f"regt_plan_{month_mapping.get(current_mnth)}"
        cont_plan = f"cont_plan_{month_mapping.get(current_mnth)}"
        try:
            prvs_yr_crnt_mnth_avg = (
                CrmInflMgrAnnualPlan.objects.filter(
                    state=state, plan_year=prv_plan_year
                )
                .values(regt_plan, cont_plan)
                .last()
            )
        except:
            prvs_yr_crnt_mnth_avg = None

        return Responses.success_response(
            "data fetched successfully", data=prvs_yr_crnt_mnth_avg
        )


class AnnualInfluencerManagerPLanLastYearAvg(GenericAPIView):
    """Get Annual Influencer Plan Last Year Average Yearly"""

    queryset = CrmInflMgrAnnualPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrAnnualPlanFilter

    def get_ly_regt_plan_avg(self, prv_yr_data):
        if prv_yr_data:
            lst_yr_regt_plan_avg = int(
                (
                    prv_yr_data["regt_plan_jan"]
                    + prv_yr_data["regt_plan_feb"]
                    + prv_yr_data["regt_plan_mar"]
                    + prv_yr_data["regt_plan_apr"]
                    + prv_yr_data["regt_plan_may"]
                    + prv_yr_data["regt_plan_jun"]
                    + prv_yr_data["regt_plan_jul"]
                    + prv_yr_data["regt_plan_aug"]
                    + prv_yr_data["regt_plan_sep"]
                    + prv_yr_data["regt_plan_oct"]
                    + prv_yr_data["regt_plan_nov"]
                    + prv_yr_data["regt_plan_dec"]
                )
                / 12
            )
        else:
            lst_yr_regt_plan_avg = 0
        return lst_yr_regt_plan_avg

    def get_ly_cont_plan_avg(self, prv_yr_data):
        if prv_yr_data:
            ly_cont_plan_avg = int(
                (
                    prv_yr_data["cont_plan_jan"]
                    + prv_yr_data["cont_plan_feb"]
                    + prv_yr_data["cont_plan_mar"]
                    + prv_yr_data["cont_plan_apr"]
                    + prv_yr_data["cont_plan_may"]
                    + prv_yr_data["cont_plan_jun"]
                    + prv_yr_data["cont_plan_jul"]
                    + prv_yr_data["cont_plan_aug"]
                    + prv_yr_data["cont_plan_sep"]
                    + prv_yr_data["cont_plan_oct"]
                    + prv_yr_data["cont_plan_nov"]
                    + prv_yr_data["cont_plan_dec"]
                )
                / 12
            )
        else:
            ly_cont_plan_avg = 0
        return ly_cont_plan_avg

    def get(self, request):
        prv_yr = int(request.query_params.get("year")) - 1
        prv_yr_data = (
            (self.filter_queryset(self.get_queryset()).filter(plan_year=prv_yr))
            .values()
            .first()
        )

        data = {
            "ly_regt_plan_avg": self.get_ly_regt_plan_avg(prv_yr_data),
            "ly_cont_plan_avg": self.get_ly_regt_plan_avg(prv_yr_data),
        }
        return Response(data)


class CreateAnnualMeetPlanYearly(ModelViewSet):
    """Create Annual Meet Plan Data Yearly"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        for data in request.data:
            data["created_by"] = request.user.id
            data["last_update_date"] = datetime.date.today()
            data["last_updated_by"] = request.user.id
            data["last_update_login"] = request.user.id
            crm_in_fl_mgr_meet_plan = CrmInflMgrMeetPlanSerializer(data=data)
            if not crm_in_fl_mgr_meet_plan.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=crm_in_fl_mgr_meet_plan.errors
                )
            crm_in_fl_mgr_meet_plan.save()
        return Responses.success_response("data inserted successfully", data=[])


class CrmInflMgrMeetPlanViewSet(ModelViewSet):
    """Get CRM Influencer Manager Meet Plan Data"""

    queryset = CrmInflMgrMeetPlan.objects.all()
    serializer_class = CrmInflMgrMeetPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrMeetPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflMgrAnnualPlanViewSet(ModelViewSet):
    """Get CRM Influencer Manager Annual Plan Data"""

    queryset = CrmInflMgrAnnualPlan.objects.all()
    serializer_class = CrmInflMgrAnnualPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrAnnualPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflMgrSchemeBudgetViewSet(ModelViewSet):
    """crm influencer manager scheme budget"""

    queryset = CrmInflMgrSchemeBudget.objects.all()
    serializer_class = CrmInflMgrSchemeBudgetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrSchemeBudgetFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        for data in request.data:
            scheme_budget_obj = CrmInflMgrSchemeBudget.objects.filter(
                state=data["state"], plan_year=data["plan_year"]
            ).first()
            if scheme_budget_obj:
                serializer = CrmInflMgrSchemeBudgetSerializer(
                    scheme_budget_obj, data=data, partial=True
                )
                if not serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "some issue rise",
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
                crm_infl_mngr_scheme_budget_serializer = (
                    CrmInflMgrSchemeBudgetSerializer(data=data)
                )
                if not crm_infl_mngr_scheme_budget_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "some issue rise",
                        data=crm_infl_mngr_scheme_budget_serializer.errors,
                    )
                crm_infl_mngr_scheme_budget_serializer.save()
        return Responses.success_response(
            "budget scheme data inserted successfully",
            data=[],
        )


class LstYrBudgetAvgCrmInflMgrSchemeBudgetViewSet(GenericAPIView):
    queryset = CrmInflMgrSchemeBudget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrSchemeBudgetFilter

    def get_ly_bdgt_avg(self, prv_yr_data):
        if prv_yr_data:
            lst_yr_site_conv_avg = int(
                (
                    prv_yr_data["budget_jan_nxt_yr"]
                    + prv_yr_data["budget_feb_nxt_yr"]
                    + prv_yr_data["budget_mar_nxt_yr"]
                    + prv_yr_data["budget_apr_cur_yr"]
                    + prv_yr_data["budget_may_cur_yr"]
                    + prv_yr_data["budget_jun_cur_yr"]
                    + prv_yr_data["budget_jul_cur_yr"]
                    + prv_yr_data["budget_aug_cur_yr"]
                    + prv_yr_data["budget_sep_cur_yr"]
                    + prv_yr_data["budget_oct_cur_yr"]
                    + prv_yr_data["budget_nov_cur_yr"]
                    + prv_yr_data["budget_dec_cur_yr"]
                )
                / 12
            )
        else:
            lst_yr_site_conv_avg = 0
        return lst_yr_site_conv_avg

    def get(self, request):
        prv_yr = int(request.query_params.get("year")) - 1
        prv_yr_data = (
            (self.filter_queryset(self.get_queryset()).filter(plan_year=prv_yr))
            .values()
            .first()
        )

        ly_bdgt_avg_data = self.get_ly_bdgt_avg(prv_yr_data)

        data = {"ly_bdgt_avg_data": ly_bdgt_avg_data}
        return Response(data)


class InfluencerMeetFreeRunInputView(GenericAPIView):
    helper = InfluencerCheckHelper
    serializer_class = InfluencerMeetConstrainedRunSerializer

    def post(self, request):
        cnxn = connect_db()
        state = request.data.get("state")
        district = request.data.get("district")
        technical_activity_type = request.data.get("technical_activity_type")
        monthly_budget = request.data.get("monthly_budget")
        budget_per_head = request.data.get("budget_per_head")
        average_no_of_influencer_per_meet = request.data.get(
            "average_no_of_influencers_per_meet"
        )
        free_run = request.data.get("Free_run")
        try:
            output, no_meeting_value = self.helper.run_model_free(
                cnxn,
                state,
                district,
                technical_activity_type,
                monthly_budget,
                budget_per_head,
                average_no_of_influencer_per_meet,
                free_run,
            )
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        if len(output) == 0:
            return Responses.error_response("No Data For Selected Inputs")
        output.columns = output.columns.str.lower()
        output.rename(
            columns={"lifting_previous_month_(mt)": "lifting_previous_month_mt"},
            inplace=True,
        )
        existing_data = InfluencerMeetingOutput.objects.filter(
            state__in=output["state"],
            district__in=output["district"],
            technical_activity_type__in=output["technical_activity_type"],
            date__in=output["date"],
        )
        if existing_data.exists():
            existing_data.delete()
        output = json.loads(output.to_json(orient="records"))
        influencer_data_serializer = InfluencerMeetingOutputSerializer(
            data=output,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        influencer_data_serializer.is_valid(raise_exception=True)
        influencer_data_serializer.save()

        # no of meetings
        no_meeting_value.columns = no_meeting_value.columns.str.lower()
        no_meeting_value = json.loads(no_meeting_value.to_json(orient="records"))
        existing_data = InfluencerMeetBudgetOutput.objects.filter(
            state=no_meeting_value[0]["state"],
            district=no_meeting_value[0]["district"],
            technical_activity_type=no_meeting_value[0]["technical_activity_type"],
        )
        if existing_data.exists():
            existing_data.delete()
        no_meeting_value_serializer = InfluencerMeetBudgetOutputSerializer(
            data=no_meeting_value,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        no_meeting_value_serializer.is_valid(raise_exception=True)
        no_meeting_value_serializer.save()
        return Responses.success_response("model run successfully", data="")
        # # no of meetings
        # no_meeting_value.columns = no_meeting_value.columns.str.lower()
        # no_meeting_value = json.loads(no_meeting_value.to_json(orient="records"))
        # no_meeting_value_serializer = InfluencerMeetBudgetOutputSerializer(
        #     data=no_meeting_value,
        #     context={
        #         "request_user": request.user.id,
        #     },
        #     many=True,
        # )
        # no_meeting_value_serializer.is_valid(raise_exception=True)
        # no_meeting_value_serializer.save()
        return Responses.success_response("model run successfully", data="")


class InfluencerTechActivityMasterDropdown(ModelViewSet):
    def get(self, request):
        queryset = InfluencerTechActivityMaster.objects.distinct().values_list(
            "technical_activity_type", flat=True
        )
        return Responses.success_response(
            "technical activity type data fetched successfully", data=queryset
        )


class InfluencerOutputViewSet(ModelViewSet):
    """Get CRM Influencer Output Data"""

    def get(self, request):
        run_id = request.query_params.get("run_id")
        data = InfluencerMeetingOutput.objects.filter(run_id=run_id).values()
        return Responses.success_response("crm influencer output data", data=data)


class InfluencerOutputView(DownloadUploadViewSet):
    """influencer output view"""

    plan_date = (dt.now() + rd(months=1)).strftime("%Y-%m-01")
    queryset = InfluencerMeetingOutput.objects.filter(date=plan_date)
    serializer_class = InfluencerOutputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InfluencerOutputFilter
    pagination_class = CustomPagination
    file_name = "InfluencerOutput"
    lookup_field = "id"


class InfluencerMeetBudgetOutputAPIView(ListAPIView):
    queryset = InfluencerMeetBudgetOutput.objects.all()
    serializer_class = InfluencerMeetBudgetOutputGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InfluencerMeetBudgetOutputFilter
    pagination_class = CustomPagination


class InfluencerMeetingOutputViewSet(ModelViewSet):
    """influencer meeting output view"""

    plan_date = (dt.now() + rd(months=1)).strftime("%Y-%m-01")
    queryset = InfluencerMeetingOutput.objects.filter(date=plan_date).order_by(
        "meeting_invited"
    )
    serializer_class = InfluencerOutputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InfluencerOutputFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class SoAugmentationRunView(GenericAPIView):
    helper = SoAugmentation
    serializer_class = AugmentationOutputTableSerializer

    def post(self, request):
        try:
            final_data = self.helper.run_model()
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        final_data.columns = final_data.columns.str.lower()
        final_data = json.loads(final_data.to_json(orient="records"))
        final_data_serializer = self.serializer_class(
            data=final_data,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        final_data_serializer.is_valid(raise_exception=True)
        final_data_serializer.save()
        return Responses.success_response("model run successfully", data="")


class AugmentationOutputTableDownloadAPIView(DownloadUploadViewSet):
    queryset = AugmentationOutputTable.objects.all()
    serializer_class = AugmentationOutputTableDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AugmentationOutputFilter
    pagination_class = CustomPagination
    file_name = "augmentation_output_table"


class InfluencerTechActivityMasterViewSet(ModelViewSet):
    """influencer meeting output view"""

    queryset = InfluencerTechActivityMaster.objects.all()
    serializer_class = InfluencerTechActivityMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = InfluencerOutputFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflChgReqDropdown(GenericAPIView):
    queryset = CrmInflChgReq.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = (
        "type_of_change",
        "state",
        "district",
        "influencer_type",
    )

    def __get_crm_infl_chg_req_dropdown_query(self, query_string, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "type_of_change": self.__get_crm_infl_chg_req_dropdown_query(
                "type_of_change", Q(type_of_change__isnull=False)
            ),
            "influencer_type": self.__get_crm_infl_chg_req_dropdown_query(
                "influencer_type", Q(influencer_type__isnull=False)
            ),
        }
        return Responses.success_response(
            "influencer change request dropdown", data=data
        )


class CrmInflAssistReqDropdown(GenericAPIView):
    queryset = CrmInflAssistReq.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("subject",)

    def __get_crm_infl_assist_req_dropdown_query(self, query_string, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "subject": self.__get_crm_infl_assist_req_dropdown_query(
                "subject", Q(subject__isnull=False)
            ),
        }
        return Responses.success_response(
            "influencer assist request dropdown", data=data
        )


class CrmInflSchemeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrmInflScheme.objects.all()
    serializer_class = CrmInflSchemeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflSchemeFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmInflGiftSchemeviewset(viewsets.ModelViewSet):
    queryset = CrmInflGiftScheme.objects.all()
    serializer_class = CrmInflGiftSchemeSerializer

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        crm_in_fl_mgr_meet_plan = CrmInflGiftSchemeSerializer(data=request.data)
        if not crm_in_fl_mgr_meet_plan.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=crm_in_fl_mgr_meet_plan.errors
            )
        crm_in_fl_mgr_meet_plan.save()
        return Responses.success_response("data inserted successfully", data=[])


class CrmInflMgrMeetPlanMonthlyViewSet(DownloadUploadViewSet):
    queryset = CrmInflMgrMeetPlanMonthly.objects.all()
    serializer_class = CrmInflMgrMeetPlanMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrMeetPlanMonthlyFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "crm_infl_mgr_meet_plan_monthly"


class CrmInflMgrAnnualPlanMonthlyViewSet(DownloadUploadViewSet):
    queryset = CrmInflMgrAnnualPlanMonthly.objects.all()
    serializer_class = CrmInflMgrAnnualPlanMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrAnnualPlanMonthlyFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "crm_influencer_manager_annual_plan_monthly_data"


class CrmInflMgrMeetPlanDownloadUploadViewset(DownloadUploadViewSet):
    queryset = CrmInflMgrMeetPlan.objects.all()
    serializer_class = CrmInflMgrMeetPlanDownloadUploadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrMeetPlanFilter
    pagination_class = CustomPagination
    file_name = "crm_infl_mngr_meet_plan"
    lookup_field = "id"


class CrmInflMgrAnnualPlanDownloadUploadViewset(DownloadUploadViewSet):
    queryset = CrmInflMgrAnnualPlan.objects.all()
    serializer_class = CrmInflMgrAnnualPlanDownloadUploadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmInflMgrAnnualPlanFilter
    pagination_class = CustomPagination
    file_name = "crm_infl_mgr_annual_plan"
    lookup_field = "id"
