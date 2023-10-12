from datetime import datetime

from django.db import transaction
from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import *
from analytical_data.filters.technical_head_filter import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils.pagination import CustomPagination
from analytical_data.utils.responses import Response, Responses
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class CrmMabBrandingApprViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrmMabBrandingAppr.objects.all()
    serializer_class = CrmMabBrandingApprSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmMabBrandingApprFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmMabBrandingApprByIdViewSet(ModelViewSet):
    queryset = CrmMabBrandingAppr.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_mab_branding_appr = CrmMabBrandingApprSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetch by id successfully ", data=crm_mab_branding_appr.data
        )

    def patch(self, request):
        id = request.query_params.get("id")
        document = request.FILES.get("upload_rev_report")
        request.data["upload_rev_report"] = document
        crmObj = CrmMabBrandingAppr.objects.get(id=id)
        serializer = CrmMabBrandingApprSerializer(
            crmObj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(
                last_updated_by=request.user.id, last_update_login=request.user.id
            )
            return Responses.success_response(
                "data updated by id successfully ", data=serializer.data
            )
        else:
            return Responses.error_response("update failed", data=serializer.errors)


class GetVendorsByStateViewSet(ModelViewSet):
    def get(self, request):
        # id  = request.query_params.get("id")
        state = request.query_params.get("state")

        vendors_by_state = CrmMabBrandingAppr.objects.filter(state=state).values()
        return Responses.success_response(
            "vendors list fetched successfully ", data=vendors_by_state
        )


class GetAllVendorsViewSet(ModelViewSet):
    def get(self, request):
        vendors_data = CrmMabBrandingAppr.objects.all().values()
        return Responses.success_response(
            "vendors list fetched successfully ", data=vendors_data
        )


class CrmMabBtlPlanningViewSet(DownloadUploadViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrmMabBtlPlanning.objects.all()
    serializer_class = CrmMabBtlPlanningSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmMabBtlPlanningFilter
    pagination_class = CustomPagination
    # sorting_field = "id"
    lookup_field = "id"


class CrmMabBtlPlanningByIdViewSet(ModelViewSet):
    queryset = CrmMabBtlPlanning.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_mabbt_planning = CrmMabBtlPlanningGetByIdSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetch by id successfully ", data=crm_mabbt_planning.data
        )


class CrmMabPastRequisitionsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrmMabPastRequisitions.objects.all()
    serializer_class = CrmMabPastRequisitionsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmMabPastRequisitionsFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmMabPastRequisitionsByIdViewSet(ModelViewSet):
    queryset = CrmMabPastRequisitions.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_infl_chg_serializer = CrmMabPastRequisitionsSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=crm_infl_chg_serializer.data
        )


class CrmMabInitReqViewSet(ModelViewSet):
    @transaction.atomic()
    def post(self, request):
        document = request.FILES.get("upload_doc")
        photo_before_brand = request.FILES.get("photo_before_brand")
        request.data["upload_doc"] = document
        request.data["photo_before_brand"] = photo_before_brand
        request.data["created_by"] = request.user.id
        request.data["last_update_date"] = datetime.today()
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        crm_mkt_brnd_init_req_ser = CrmMabInitReqSerializer(data=request.data)
        if not crm_mkt_brnd_init_req_ser.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=crm_mkt_brnd_init_req_ser.errors
            )
        crm_mkt_brnd_init_req_ser.save()
        return Responses.success_response(
            "data inserted successfully", data=crm_mkt_brnd_init_req_ser.data
        )


class VendorDetailMasterDropdown(GenericAPIView):
    queryset = VendorDetailMaster.objects.all()
    serializer_class = VendorDetailMasterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = VendorDetailMasterFilter
    search_fields = ("vendor_name",)

    def __get_vendor_detail_master_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "vendor_name": self.__get_vendor_detail_master_dropdown_query(
                "vendor_name"
            ),
        }
        return Responses.success_response(
            "vendor detail master dropdown data.", data=data
        )


# class CalcTabDealerNameDropdown(GenericAPIView):
#     queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = TOebsSclArNcrAdvanceCalcTabFilter

#     def __get_Calc_Tab_Dealer_Name_dropdown_query(self, query_string):
#         return (
#             self.filter_queryset(self.get_queryset())
#             .values_list(query_string, flat=True)
#             .annotate(Count(query_string))
#             .order_by(query_string)
#         )

#     def get(self, request, *args, **kwargs):
#         data = {
#             "dealer_name": self.__get_Calc_Tab_Dealer_Name_dropdown_query(
#                 "customer_name"
#             ),
#             "dealer_code": self.__get_Calc_Tab_Dealer_Name_dropdown_query(
#                 "customer_number"
#             ),
#         }
#         return Responses.success_response("dealer name dropdown data.", data=data)


class CalcTabDealerNameDropdown(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TOebsSclArNcrAdvanceCalcTabFilter

    def __get_Calc_Tab_Dealer_Name_dropdown_query(self):
        return (
            self.filter_queryset(self.get_queryset())
            .values("customer_name")
            .annotate(
                dealer_name=F("customer_name"),
                dealer_code=F("customer_number"),
            )
            .distinct("customer_name")
            .order_by("customer_name")
        )

    def get(self, request, *args, **kwargs):
        dealer_data = self.__get_Calc_Tab_Dealer_Name_dropdown_query()

        response_data = {
            "message": "dealer name dropdown data.",
            "data": [
                {
                    "dealer_name": dealer["dealer_name"],
                    "dealer_code": dealer["dealer_code"],
                }
                for dealer in dealer_data
            ],
        }

        return Response(response_data)
        # return Responses.success_response("dealer name dropdown data.", data=response_data)


class VendorDetailMasterVendorCodeDropdown(GenericAPIView):
    queryset = VendorDetailMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VendorDetailMasterVendorCodeFilter

    def __get_vendor_detail_master_vendor_code_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        vendor_names = self.__get_vendor_detail_master_vendor_code_dropdown_query(
            "vendor_name"
        )
        vendor_codes = self.__get_vendor_detail_master_vendor_code_dropdown_query(
            "vendor_code"
        )

        data = []
        for vendor_name, vendor_code in zip(vendor_names, vendor_codes):
            data.append({"vendor_name": vendor_name, "vendor_code": vendor_code})

        return Responses.success_response(
            "vendor detail master vendor code dropdown data.", data=data
        )


# class TnmMaterialTransactionDropdown(GenericAPIView):
#     queryset = TNmOmxMaterialTransactionsV.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = TNmOmxMaterialTransactionsVFilter

#     def __get_tnm_material_transaction_dropdown_query(self, type_disp):
#         return self.filter_queryset(
#             self.get_queryset()
#             .filter(transaction_type_disp=type_disp, to_party_name__isnull=False)
#             .values_list("to_party_name", flat=True)
#             .annotate(Count("to_party_name"))
#         )

#     def get(self, request):
#         transaction_type_disp = request.query_params.get("transaction_type_disp")

#         if transaction_type_disp == "Retailer":
#             party_name = self.__get_tnm_material_transaction_dropdown_query("Retailer")

#         else:
#             party_name = self.__get_tnm_material_transaction_dropdown_query("Mitra")

#         data = {"party_name": party_name}

#         return Responses.success_response("party name dropdown data.", data=data)


class TnmMaterialTransactionDropdown(GenericAPIView):
    queryset = TNmOmxMaterialTransactionsV.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TNmOmxMaterialTransactionsVFilter

    def __get_tnm_material_transaction_dropdown_query(self, type_disp):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(transaction_type_disp=type_disp, to_party_name__isnull=False)
            .values("to_party_name")
            .annotate(party_name=F("to_party_name"), party_code=F("to_party_id"))
            .distinct("to_party_name")
            .order_by("to_party_name")
        )

    def get(self, request):
        transaction_type_disp = request.query_params.get("transaction_type_disp")

        if transaction_type_disp == "Retailer":
            party_data = self.__get_tnm_material_transaction_dropdown_query("Retailer")
            response_data = {
                "message": "party name dropdown data.",
                "data": [
                    {
                        "party_name": dealer["party_name"],
                        "party_code": dealer["party_code"],
                    }
                    for dealer in party_data
                ],
            }

        else:
            party_data = self.__get_tnm_material_transaction_dropdown_query("Mitra")
            response_data = {
                "message": "party name dropdown data.",
                "data": [
                    {
                        "party_name": dealer["party_name"],
                        "party_code": dealer["party_code"],
                    }
                    for dealer in party_data
                ],
            }

        return Response(response_data)


class BrandingActivityViewSet(ModelViewSet):
    queryset = BrandingActivity.objects.all().order_by("date_of_start")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandingActivityFilter
    serializer_class = BrandingActivitySerializer
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        dataset = request.data
        branding_activity_serializer = self.serializer_class(data=dataset)
        if not branding_activity_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise while saving data in branding activity",
                data=branding_activity_serializer.errors,
            )
        branding_activity_serializer.save()
        branding_activity_data = branding_activity_serializer.data
        branding_activity_id = branding_activity_data["id"]
        upload_doc = request.FILES.get("upload_doc")
        photo_before_brand = request.FILES.get("photo_before_brand")
        init_req_data = {
            "branding_activity": branding_activity_id,
            "additional_comment": dataset["additional_comment"],
            "photo_before_brand": photo_before_brand,
            "upload_doc": upload_doc,
            "created_by": request.user.id,
            "last_updated_by": request.user.id,
            "last_update_login": request.user.id,
        }
        crm_mkt_brnd_init_req_ser = CrmMabInitReqSerializer(data=init_req_data)
        if not crm_mkt_brnd_init_req_ser.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=crm_mkt_brnd_init_req_ser.errors
            )
        crm_mkt_brnd_init_req_ser.save()
        return Responses.success_response(
            "data inserted successfully", data=branding_activity_serializer.data
        )

    def update(self, request):
        id = request.query_params.get("id")
        branding_act_id = BrandingActivity.objects.get(id=id)
        if id:
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            branding_activity_ser = self.serializer_class(
                branding_act_id, data=request.data
            )
            additional_comment = request.data.get("additional_comment", "")
            comment_by_cbt = request.data.get("comment_by_cbt", "")
            comment_by_lbt = request.data.get("comment_by_lbt", "")
            comment_by_nsh = request.data.get("comment_by_nsh", "")

            branding_activity_ser = self.serializer_class(
                branding_act_id, data=request.data
            )
            if not branding_activity_ser.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Updation Error in branding activity",
                    branding_activity_ser.errors,
                )
            branding_activity_obj = branding_activity_ser.save()
            mab_init_req_obj = CrmMabInitReq.objects.filter(
                branding_activity__id=branding_activity_obj.id
            )
            if mab_init_req_obj:
                mab_init_req_obj.delete()
            mab_init_req_data = {
                "additional_comment": additional_comment,
                "comment_by_cbt": comment_by_cbt,
                "comment_by_lbt": comment_by_lbt,
                "comment_by_nsh": comment_by_nsh,
                "branding_activity": branding_activity_obj.id,
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
            }
            mab_init_req_ser = CrmMabInitReqSerializer(data=mab_init_req_data)
            if not mab_init_req_ser.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct vol cutter slab based incentive",
                    mab_init_req_ser.errors,
                )
            mab_init_req_ser.save()
        return Responses.success_response(
            "data inserted  in slct vol cutter slab based incentive",
            data=branding_activity_ser.data,
        )


class MarketMappingBrandingBudgetViewSet(ModelViewSet):
    queryset = MarketMappingBrandingBudget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = ("state", "district", "brand")
    filterset_class = MarketMappingBrandingBudgetFilter
    serializer_class = MarketMappingBrandingBudgetSerializer
    pagination_class = CustomPagination
    lookup_field = "id"


class MarketMappingBrandingBudgetViewSet(DownloadUploadViewSet):
    """CRUD view set for lp scheduling vehicle constraint."""

    queryset = MarketMappingBrandingBudget.objects.all().order_by("state")
    serializer_class = MarketMappingBrandingBudgetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MarketMappingBrandingBudgetFilter
    pagination_class = CustomPagination
    # sorting_fields = ("state", "district", "brand")
    lookup_field = "id"
    file_name = "market_mapping_branding_budget"

    # def get_queryset(self):
    #     if self.request.method in ["PATCH", "PUT"] and not isinstance(
    #         self.request.data, dict
    #     ):
    #         return (
    #             super(DownloadUploadViewSet, self)
    #             .get_queryset()
    #             .filter(
    #                 state__in=map(lambda x: x.get("state"), self.data),
    #                 district__in=map(lambda x: x.get("district"), self.data),
    #                 brand__in=map(lambda x: x.get("brand"), self.data),
    #             )
    #         ).order_by(*self.sorting_fields)
    #     return super().get_queryset()


class MarketMappingBrandingBudgetDropDown(GenericAPIView):
    queryset = MarketMappingBrandingBudget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MarketMappingBrandingBudgetFilter

    def __get_Market_Mapping_Branding_Budget_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        state = self.__get_Market_Mapping_Branding_Budget_dropdown_query("state")
        district = self.__get_Market_Mapping_Branding_Budget_dropdown_query("district")
        brand = self.__get_Market_Mapping_Branding_Budget_dropdown_query("brand")

        data = {"state": state, "district": district, "brand": brand}

        return Responses.success_response(
            "market branding budget dropdown data.", data=data
        )


class BrandingActivityDropDown(GenericAPIView):
    queryset = BrandingActivity.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandingActivityFilter

    def __get_Branding_Activity_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .exclude(**{query_string: None})
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        zone = self.__get_Branding_Activity_dropdown_query("zone")
        state = self.__get_Branding_Activity_dropdown_query("state")
        district = self.__get_Branding_Activity_dropdown_query("district")
        brand = self.__get_Branding_Activity_dropdown_query("brand")
        city = self.__get_Branding_Activity_dropdown_query("city")
        vendor_name = self.__get_Branding_Activity_dropdown_query("vendor_name")
        status_of_scheme = self.__get_Branding_Activity_dropdown_query(
            "status_of_scheme"
        )
        status = self.__get_Branding_Activity_dropdown_query("status")
        activity_type = self.__get_Branding_Activity_dropdown_query("activity_type")
        activity_for = self.__get_Branding_Activity_dropdown_query("activity_for")
        activity_category = self.__get_Branding_Activity_dropdown_query(
            "activity_category"
        )
        activity_name = self.__get_Branding_Activity_dropdown_query("activity_name")
        site_type = self.__get_Branding_Activity_dropdown_query("site_type")
        objective_of_activity = self.__get_Branding_Activity_dropdown_query(
            "objective_of_activity"
        )

        data = {
            "zone": zone,
            "state": state,
            "district": district,
            "brand": brand,
            "city": city,
            "vendor_name": vendor_name,
            "status_of_scheme": status_of_scheme,
            "status": status,
            "brand": brand,
            "activity_type": activity_type,
            "activity_for": activity_for,
            "activity_category": activity_category,
            "activity_name": activity_name,
            "site_type": site_type,
            "objective_of_activity": objective_of_activity,
        }

        return Responses.success_response("branding activity dropdown data.", data=data)


# class SponsorshipBudgetViewSet(ModelViewSet):
#     queryset = SponsorshipBudget.objects.all()
#     serializer_class = SponsorshipBudgetSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = SponsorshipBudgetFilter
#     pagination_class = CustomPagination
#     lookup_field = "id"

#     def post(self, request):
#         request.data["created_by"] = request.user.id
#         request.data["last_updated_by"] = request.user.id
#         request.data["last_update_login"] = request.user.id
#         seralizer_obj = SponsorshipBudgetSerializer(data=request.data)
#         if not seralizer_obj.is_valid(raise_exception=True):
#             return Responses.error_response(seralizer_obj.errors, "something wrong")
#         seralizer_obj.save()
#         return Responses.success_response(
#             "Data Inserted Successfully", data=seralizer_obj.data
#         )


class SponsorshipBudgetViewSet(DownloadUploadViewSet):
    """CRUD view set for lp scheduling vehicle constraint."""

    queryset = SponsorshipBudget.objects.all()
    serializer_class = SponsorshipBudgetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SponsorshipBudgetFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "sponsorship_budget"

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        seralizer_obj = SponsorshipBudgetPostSerializer(data=request.data)
        if not seralizer_obj.is_valid(raise_exception=True):
            return Responses.error_response(seralizer_obj.errors, "something wrong")
        seralizer_obj.save()
        return Responses.success_response(
            "Data Inserted Successfully", data=seralizer_obj.data
        )


class NewMarketPricingApprovalViewSet(ModelViewSet):
    queryset = NewMarketPricingApproval.objects.all()
    serializer_class = NewMarketPricingApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = NewMarketPricingApprovalFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        seralizer_obj = NewMarketPricingApprovalSerializer(data=request.data)
        if not seralizer_obj.is_valid(raise_exception=True):
            return Responses.error_response(seralizer_obj.errors, "something wrong")
        seralizer_obj.save()
        return Responses.success_response(
            "Data Inserted Successfully", data=seralizer_obj.data
        )
