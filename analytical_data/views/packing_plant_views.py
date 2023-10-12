import json
import logging
from datetime import date as t_date
from datetime import datetime

import pandas as pd
from django.db import transaction
from django.db.models import Count, F, Q, Sum, Value
from django.db.models.functions import Substr
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils import (
    CustomPagination,
    Responses,
    get_workbook_data,
)
from analytical_data.view_helpers import (
    PackingPlantHelper,
    PackingPlantScriptHelper,
    PlantDropdownViewHelper,
)
from analytical_data.views.custom_viewsets import DownloadUploadViewSet

log = logging.getLogger()


class TgtTruckCycleTatAacView(GenericAPIView):
    """
    TGT_TAT_DATA table view - for AAC
    for getting the average duration of the fields for the date and plant selected
    """

    queryset = TgtTruckCycleTat.objects.all()

    def get(self, request):
        plant_name = request.GET.get("plant", "")
        date = request.GET.get("date", "")
        if date != "":
            date = datetime.strptime(date, "%Y-%m-%d")
            date = date.strftime("%d-%b-%Y").upper()

        queryset = self.get_queryset().filter(
            item__in=PackingPlantHelper.items_list_aac,
            plant_name__startswith=plant_name.upper(),
            tax_invoice_date__contains=date,
        )
        serializer = TgtTruckCycleTatSerializer(queryset, many=True)
        if serializer.data:
            response_data = PackingPlantHelper.calculate_average(serializer.data)
            if date != "":
                date = datetime.strptime(date, "%d-%b-%Y").strftime("%Y-%m-%d")
            response_data["date"] = date
        else:
            response_data = {}

        request.session["packing_plant_aac_avg"] = response_data
        log.debug(
            "packing plant aac average values stored in session: %s",
            request.session.session_key,
        )

        return Response(
            {"status": "success", "data": response_data}, status=status.HTTP_200_OK
        )


class TgtTruckCycleTatCementView(GenericAPIView):
    """
    TGT_TAT_DATA table view - for Cement
    for getting the average duration of the fields for the date and plant selected
    """

    queryset = TgtTruckCycleTat.objects.all()

    def get(self, request):
        plant_name = request.GET.get("plant", "")
        _date = request.GET.get("date", "")
        if _date != "":
            date = datetime.strptime(_date, "%Y-%m-%d")
            date = date.strftime("%d-%b-%Y").upper()

        queryset = self.get_queryset().filter(
            item__in=PackingPlantHelper.items_list_cement,
            plant_name__startswith=plant_name.upper(),
            tax_invoice_date__contains=date,
        )
        serializer = TgtTruckCycleTatSerializer(queryset, many=True)
        if serializer.data:
            response_data = PackingPlantHelper.calculate_average(serializer.data)
            response_data["date"] = _date
        else:
            response_data = {}

        return Response(
            {"status": "success", "data": response_data}, status=status.HTTP_200_OK
        )


class PackingPlantAacTatReasonsView(APIView, CustomPagination):
    """
    Packing_Plant_AAC table view
    For storing the reasons
    """

    CustomPagination.page_size = 10

    def get(self, request, id=None):
        if id:
            queryset = PackingPlantAacTatReasons.objects.get(id=id)
            serializer = PackingPlantAacTatReasonsSerializer(queryset)
            request.session["packing_plant_aac_reasons"] = serializer.data
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        plant_name = request.GET.get("plant", "")
        date = request.GET.get("date", "")
        # if date != "":
        # date = datetime.strptime(date, "%Y-%m-%d")
        # date = date.strftime("%Y-%m-%d").upper()
        queryset = PackingPlantAacTatReasons.objects.filter(
            plant__startswith=plant_name.upper(),
            date__icontains=date,
        ).order_by("-id")

        serializer = PackingPlantAacTatReasonsSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data, request)
        return self.get_paginated_response(page)

    def post(self, request):
        serializer = PackingPlantAacTatReasonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                last_updated_by=request.user.id,
                created_by=request.user.id,
                last_update_login=request.user.id,
            )
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, id=None):
        reason = PackingPlantAacTatReasons.objects.get(id=id)
        serializer = PackingPlantAacTatReasonsSerializer(
            reason, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(
                last_updated_by=request.user.id, last_update_login=request.user.id
            )
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PackingPlantAacTatReasonsDownloadView(DownloadUploadViewSet):
    file_name = "truck_movement_pre_filled"

    def download(self, request, *args, **kwargs):
        packing_plant_aac_avg = request.session.get("packing_plant_aac_avg", {})
        packing_plant_aac_reasons = request.session.get("packing_plant_aac_reasons", {})

        data = []
        for key in list(packing_plant_aac_avg.keys())[:10]:
            data.append(
                {
                    "activity": key,
                    "average": packing_plant_aac_avg[key],
                    "reason": packing_plant_aac_reasons[key],
                }
            )
        data.append(
            {
                "activity": packing_plant_aac_reasons["other_activity_name"],
                "average": packing_plant_aac_reasons["other_activity_time"],
                "reason": packing_plant_aac_reasons["other_activity_reason"],
            }
        )
        workbook = get_workbook_data(data, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response


class PackingPlantCementTatReasonsView(APIView, CustomPagination):
    """
    Packing_Plant_Cement table view
    For storing the reasons
    """

    CustomPagination.page_size = 10

    def get(self, request, id=None):
        if id:
            queryset = PackingPlantCementTatReasons.objects.get(id=id)
            serializer = PackingPlantCementTatReasonsSerializer(queryset)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        plant_name = request.GET.get("plant", "")
        date = request.GET.get("date", "")
        # if date != "":
        # date = datetime.strptime(date, "%Y-%m-%d")
        # date = date.strftime("%Y-%m-%d").upper()
        queryset = PackingPlantCementTatReasons.objects.filter(
            plant__startswith=plant_name.upper(),
            date__icontains=date,
        ).order_by("-id")
        serializer = PackingPlantCementTatReasonsSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data, request)
        return self.get_paginated_response(page)

    def post(self, request):
        serializer = PackingPlantCementTatReasonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                last_updated_by=request.user.id,
                created_by=request.user.id,
                last_update_login=request.user.id,
            )
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, id=None):
        reason = PackingPlantCementTatReasons.objects.get(id=id)
        serializer = PackingPlantCementTatReasonsSerializer(
            reason, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(
                last_updated_by=request.user.id, last_update_login=request.user.id
            )
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AacPlantDropdownView(GenericAPIView):
    """Options dropdown API for Plant list."""

    # helper = PlantDropdownViewHelper
    queryset = TgtTruckCycleTat.objects.all()

    def get_demand_dropdown_data(self, items):
        plant_name_data = self.__get_field_values("plant_name", items)
        organization_code_data = self.__get_field_values("organization_code", items)

        options = {
            "plant_name": plant_name_data,
            "organization_code": organization_code_data,
        }
        return options

    def __get_field_values(self, field, items):
        return (
            self.get_queryset()
            .filter(item__in=items)
            .values_list(field, flat=True)
            .annotate(Count(field))
        )

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = self.get_demand_dropdown_data(PackingPlantHelper.items_list_aac)
        return Responses.success_response(
            "AAC Packing Plant name options dropdown.", data=data
        )


class CementPlantDropdownView(GenericAPIView):
    """Options dropdown API for Plant list."""

    queryset = TgtTruckCycleTat.objects.all()

    def get_demand_dropdown_data(self, items):
        plant_name_data = self.__get_field_values("plant_name", items)
        organization_code_data = self.__get_field_values("organization_code", items)

        options = {
            "plant_name": plant_name_data,
            "organization_code": organization_code_data,
        }
        return options

    def __get_field_values(self, field, items):
        return (
            self.get_queryset()
            .filter(item__in=items)
            .values_list(field, flat=True)
            .annotate(Count(field))
        )

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = self.get_demand_dropdown_data(PackingPlantHelper.items_list_cement)
        return Responses.success_response(
            "Cement Packing Plant name options dropdown.", data=data
        )


class PlantStorageView(ModelViewSet):
    """CRUD view set for plant storage."""

    queryset = PlantStorage.objects.all()
    serializer_class = PlantStorageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("plant_name", "product")
    filterset_class = PlantStorageFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class PlantDepoSlaView(ModelViewSet):
    """CRUD view set for plant depots sla."""

    queryset = PlantDepoSla.objects.all()
    serializer_class = PlantDepoSlaSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("plant_name", "product")
    filterset_class = PlantDepoSlaFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class GetPlantDepoSlaPlantAndProductList(ModelViewSet):
    """get plant depots sla product and plant list"""

    def get(self, request):
        plant_list = PlantDepoSlaNew.objects.values_list("plant", flat=True).annotate(
            Count("plant")
        )
        product_list = PlantDepoSlaNew.objects.values_list(
            "product", flat=True
        ).annotate(Count("product"))
        data = {"plant_list": plant_list, "product_list": product_list}
        return Responses.success_response(
            "Plant Depo Sla Plant and Product Dropdown", data=data
        )


class ClinkerDispatchPlanViewSet(ModelViewSet):
    queryset = ClinkerDispatchPlan.objects.all().order_by("-shipping_date")
    serializer_class = ClinkerDispatchPlanSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("shipped_from_plant", "shipped_to_plant")
    filterset_class = ClinkerDispatchPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        dataset = request.data
        dataset["created_by"] = request.user.id
        dataset["last_updated_by"] = request.user.id
        dataset["last_update_login"] = request.user.id
        clinker_dispatch_serializer = ClinkerDispatchPlanSerializer(data=dataset)
        if not clinker_dispatch_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=clinker_dispatch_serializer.errors
            )
        clinker_dispatch_serializer.save()
        clinker_dispatch_data = clinker_dispatch_serializer.data
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, clinker_dispatch_data
        )


class PackingPlantBagsStockViewSet(ModelViewSet):
    queryset = PackingPlantBagsStock.objects.all()
    serializer_class = PackingPlantBagsStockSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("plant", "date_of_receipt")
    pagination_class = CustomPagination
    lookup_field = "id"


class PackingPlantBagsStockDropdownView(GenericAPIView):
    """Options dropdown API for Plant list."""

    queryset = PackingPlantBagsStock.objects.all()

    def __get_packing_plant_bags_type_query(self, query_string):
        return (
            self.get_queryset()
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant": self.__get_packing_plant_bags_type_query("plant"),
        }
        return Responses.success_response("packing plant bags type.", data=data)


class PackerBagBurstingDescViewSet(ModelViewSet):
    queryset = PackerBagBurstingDesc.objects.all()
    serializer_class = PackerBagBurstingDescSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerBagBurstingDescFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        dataset = request.data
        dataset["created_by"] = request.user.id
        dataset["last_updated_by"] = request.user.id
        dataset["last_update_login"] = request.user.id
        bag_burst_serializer = PackerBagBurstingDescSerializer(data=dataset)
        if not bag_burst_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=bag_burst_serializer.errors
            )
        bag_burst_serializer.save()
        bag_burst_data = bag_burst_serializer.data
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, bag_burst_data
        )


class PackerBagBurstingDescDataByIdViewSet(ModelViewSet):
    queryset = PackerBagBurstingDesc.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        packer_bag_serializer = PackerBagBurstingDescSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=packer_bag_serializer.data
        )


class PackerShiftLevelStoppagesViewSet(DownloadUploadViewSet):
    queryset = PackerShiftLevelStoppages.objects.order_by("packer_code")
    serializer_class = PackerShiftLevelStoppagesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerShiftLevelStoppagesFilter
    # pagination_class = CustomPagination
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Responses.success_response(
            message="packer shift level stoppages data.", data=response.data
        )


class UpdatePackerShiftLevelStoppagesListViewSet(APIView):
    def post(self, request):
        stoppage_data_list = request.data
        for stoppage_data in stoppage_data_list:
            stoppage_obj = PackerShiftLevelStoppages.objects.get(id=stoppage_data["id"])
            stoppage_data.pop("id")
            stoppage_serializer = PackerShiftLevelStoppagesUpdateSerializer(
                stoppage_obj, data=stoppage_data, partial=True
            )
            if stoppage_serializer.is_valid():
                stoppage_serializer.save(
                    last_updated_by=request.user.id, last_update_login=request.user.id
                )
            else:
                return Response(
                    {"status": "error", "data": stoppage_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"status": "stoppage data updated success", "data": []},
            status=status.HTTP_200_OK,
        )


class PackerShiftLevelStoppagesDropdownView(GenericAPIView):
    """Options dropdown API for Plant and shift list."""

    queryset = PackerShiftLevelStoppages.objects.all()

    def __get_packer_shift_level_type_query(self, query_string):
        return (
            self.get_queryset()
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant": self.__get_packer_shift_level_type_query("plant"),
            "shift": self.__get_packer_shift_level_type_query("shift"),
        }
        return Responses.success_response("packing plant bags type.", data=data)


class ShiftWiseAdhocPercentageViewSet(ModelViewSet):
    queryset = ShiftWiseAdhocPercentage.objects.all()
    serializer_class = ShiftWiseAdhocPercentageSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"


class PpMasterViewSet(ModelViewSet):
    # serializer_class = PpMasterSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request):
        dataset = request.data
        dataset["created_by"] = request.user.id
        dataset["last_updated_by"] = request.user.id
        dataset["last_update_login"] = request.user.id
        dataset["last_update_date"] = t_date.today()
        pp_master_serializer = PpMasterSerializer(data=dataset)
        if not pp_master_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=pp_master_serializer.errors
            )
        pp_master_serializer.save()
        pp_master_data = pp_master_serializer.data
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, pp_master_data
        )


class GetPackingPlanOutputViewSet(ModelViewSet):
    """Get Packing Plant Output"""

    queryset = PpOrderTagging.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PpOrderTaggingFilter
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        run_id = request.query_params.get("run_id")
        pp_shift_detail_data = PpShiftDetails.objects.filter(run_id=run_id).values()

        # priority
        pp_order_tagging_data = (
            self.filter_queryset(self.get_queryset())
            .filter(
                run_id=run_id,
            )
            .select_related("order_master_id")
        )

        # mode
        pp_rail_order_tagging_data = PpRailOrderTagging.objects.filter(
            run_id=run_id
        ).values()
        if request.query_params.get("mode"):
            pp_rail_order_tagging_data = pp_rail_order_tagging_data.filter(
                mode=request.query_params.get("mode")
            )

        serializer = PpOrderTaggingViewSerializer(pp_order_tagging_data, many=True)
        data = {
            "pp_shift_detail_data": pp_shift_detail_data,
            "pp_order_tagging_data": serializer.data,
            "pp_rail_order_tagging_data": pp_rail_order_tagging_data,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class PpOrderTaggingDropdown(GenericAPIView):
    queryset = PpOrderTagging.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PpOrderTaggingFilter

    def __get_order_tagging_query(self, query_string, filter_query=Q):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "delivery_id": self.__get_order_tagging_query(
                "order_master_id__delivery_id",
                Q(order_master_id__delivery_id__isnull=False),
            ),
            "token_id": self.__get_order_tagging_query(
                "order_master_id__token_id", Q(order_master_id__token_id__isnull=False)
            ),
            "brand": self.__get_order_tagging_query(
                "order_master_id__brand", Q(order_master_id__brand__isnull=False)
            ),
            "order_line_id": self.__get_order_tagging_query(
                "order_master_id__order_line_id",
                Q(order_master_id__order_line_id__isnull=False),
            ),
            "order_quantity": self.__get_order_tagging_query(
                "order_master_id__order_quantity",
                Q(order_master_id__order_quantity__isnull=False),
            ),
            "pack_type": self.__get_order_tagging_query(
                "order_master_id__pack_type",
                Q(order_master_id__pack_type__isnull=False),
            ),
            "auto_tagged_mode": self.__get_order_tagging_query(
                "order_master_id__auto_tagged_mode",
                Q(order_master_id__auto_tagged_mode__isnull=False),
            ),
            "packer_code": self.__get_order_tagging_query(
                "packer_code", Q(packer_code__isnull=False)
            ),
            "tl_code": self.__get_order_tagging_query(
                "tl_code", Q(tl_code__isnull=False)
            ),
            "mode": PpRailOrderTagging.objects.filter(mode__isnull=False)
            .values_list("mode", flat=True)
            .annotate(Count("mode")),
        }
        return Responses.success_response(
            "packing plant output dropdown data.", data=data
        )


# class PpDowntimeViewSet(ModelViewSet):
#     def post(self, request):
#         request.data["created_by"] = request.user.id
#         request.data["date"] = t_date.today()
#         request.data["last_updated_by"] = request.user.id
#         request.data["last_update_login"] = request.user.id
#         request.data["last_update_date"] = t_date.today()
#         downtime_serializer = PpDowntimeSerializer(data=request.data)
#         if not downtime_serializer.is_valid(raise_exception=True):
#             return Responses.error_response(
#                 "some issue rise", data=downtime_serializer.errors
#             )
#         downtime_serializer.save()
#         return Responses.success_response(
#             "data inserted successfully", data=downtime_serializer.data
#         )


class GetPackerRatedCapacityViewSet(ModelViewSet):
    queryset = PackerRatedCapacity.objects.all()
    serializer_class = PackerRatedCapacitySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerRatedFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class PackingPlantScriptRunModel(GenericAPIView):
    serializer_class = PpMasterSerializer
    helper = PackingPlantScriptHelper

    @transaction.atomic()
    def post(self, request):
        plant_input = request.data["plant"]
        date_input = request.data["date"]
        shift_input = request.data["shift"]

        pp_master_object = {
            "plant": plant_input,
            "date": date_input,
            "shift": shift_input,
            "created_by": request.user.id,
            "last_updated_by": request.user.id,
            "last_update_login": request.user.id,
        }

        model_run_serializer = self.serializer_class(data=pp_master_object)
        model_run_serializer.is_valid(raise_exception=True)
        model_run_object_instance = model_run_serializer.save()
        try:
            (
                shift_details,
                order_details,
                ad_hoc_qty,
                rail_order_details,
            ) = PackingPlantScriptHelper.run_model(plant_input, date_input, shift_input)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        # # shift details saving
        shift_details.columns = shift_details.columns.str.lower()
        shift_details_data = json.loads(shift_details.to_json(orient="records"))

        shift_details_serializer = PpShiftDetailsSerializer(
            data=shift_details_data,
            context={
                "run_id": model_run_object_instance.run_id,
                "request_user": request.user.id,
            },
            many=True,
        )
        shift_details_serializer.is_valid(raise_exception=True)
        shift_details_serializer.save()

        # #order details saving
        order_details.columns = order_details.columns.str.lower()
        order_details["tentative_pp_in_time"] = order_details[
            "tentative_pp_in_time"
        ].astype(str)
        order_details_data = json.loads(order_details.to_json(orient="records"))
        order_details_serializer = PpOrderTaggingSerializer(
            data=order_details_data,
            context={
                "run_id": model_run_object_instance.run_id,
                "request_user": request.user.id,
            },
            many=True,
        )
        order_details_serializer.is_valid(raise_exception=True)
        order_details_serializer.save()

        ###############  rail_order_details ###################
        rail_order_details.columns = rail_order_details.columns.str.lower()
        rail_order_details_data = json.loads(
            rail_order_details.to_json(orient="records")
        )
        rail_order_details_serializer = PpRailOrderTaggingSerializer(
            data=rail_order_details_data,
            context={
                "run_id": model_run_object_instance.run_id,
                "request_user": request.user.id,
            },
            many=True,
        )
        rail_order_details_serializer.is_valid(raise_exception=True)
        rail_order_details_serializer.save()

        return Responses.success_response(
            "Successfully Running Data", data=model_run_object_instance.run_id
        )


class UniqueValueViewSet(GenericAPIView):
    def get(self, request):
        plant = request.query_params.get("plant")
        shift = request.query_params.get("shift")
        date = request.query_params.get("date")
        run_id = request.query_params.get("run_id")
        data = (
            PpOrderTagging.objects.filter(
                run__plant=plant, run__shift=shift, run__date=date, run__run_id=run_id
            )
            .values(
                "packer_code",
                "tl_code",
                "order_master_id__grade",
                "order_master_id__brand",
            )
            .annotate(
                sum_value_of_order_qty=Sum("order_master_id__order_quantity"),
                sum_of_order_processing_time=Sum("order_processing_time"),
            )
            .order_by()
        )
        return Responses.success_response("data fetched", data=data)


class LpSchedulingDpcDropdownView(GenericAPIView):
    """lp scheduling dpc dropdown api."""

    queryset = LpSchedulingDpc.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = LpSchedulingDpcFilter
    filterset_fields = ("ship_state", "ship_district")

    def __get_lp_scheduling_dpc_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "ship_state": self.__get_lp_scheduling_dpc_query("ship_state"),
            "ship_district": self.__get_lp_scheduling_dpc_query("ship_district"),
        }
        return Responses.success_response("lp scheduling dpc dropdown data.", data=data)


class LpSchedulingDpcViewSet(DownloadUploadViewSet):
    queryset = LpSchedulingDpc.objects.all().order_by("-id")
    serializer_class = LpSchedulingDpcSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpSchedulingDpcFilter
    sorting_fields = ("ship_state", "ship_district", "brand", "plant", "inv_qty")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "lp_scheduling_dpc_data"

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        brands = request.data.get("brand")
        inv_qtys = request.data.get("inv_qty")
        data = []
        for i in range(len(brands)):
            data.append(
                {
                    "ship_state": request.data.get("ship_state"),
                    "ship_district": request.data.get("ship_district"),
                    "brand": brands[i],
                    "plant": request.data.get("plant"),
                    "inv_qty": inv_qtys[i],
                }
            )

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Responses.success_response("data inserted successfully", data=[])


class LpSchedulingDpcByIdViewSet(ModelViewSet):
    queryset = LpSchedulingDpc.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        lp_scheduling_dpc = LpSchedulingDpcSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=lp_scheduling_dpc.data
        )


class PlantDepoSlaNewViewSet(ModelViewSet):
    queryset = PlantDepoSlaNew.objects.all()
    serializer_class = PlantDepoSlaNewSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("plant", "product")
    filterset_class = PlantDepoSlaNewFilter
    lookup_field = "id"


class ShiftWiseAdhocQtyViewSet(ModelViewSet):
    queryset = ShiftwiseAdhocQty.objects.all()
    serializer_class = ShiftWiseAdhocQtySerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = ShiftWiseAdhocQtyFilter
    lookup_field = "id"


class GetDowntimeDataViewSet(ModelViewSet):
    def get(self, request):
        plant = request.query_params.get("plant")
        date = request.query_params.get("date")
        shift = request.query_params.get("shift")

        packer_shift_level_stoppages_df = pd.DataFrame(
            PackerShiftLevelStoppages.objects.filter(
                plant=plant, date=date, shift=shift
            )
            .values("plant", "date", "shift")
            .annotate(
                tl_downtime_hrs=F("stoppage_hrs"),
                packer=F("packer_code"),
                tl_name=F("tl_code"),
            )
        )

        if PpDowntime.objects.filter(plant=plant, date=date, shift=shift).exists():
            df = pd.DataFrame(
                PpDowntime.objects.filter(plant=plant, date=date, shift=shift).values()
            )
            data_from_table = "downtime"
        else:
            df = pd.DataFrame(
                PackerRatedCapacity.objects.filter(plant=plant)
                .values(
                    "packer",
                    "plant",
                    "packer_rated_capacity_mt_hr",
                    "tl_rated_capacity_mt_hr",
                )
                .annotate(
                    tl_name=F("truck_loader"),
                    date=Value(request.query_params.get("date")),
                    shift=Value(int(request.query_params.get("shift"))),
                )
            )
            data_from_table = "packer_rated"

        df["date"] = df["date"].astype(str)

        if packer_shift_level_stoppages_df.empty:
            df["tl_downtime_hrs"] = 0
            data = {
                "data_from_table": data_from_table,
                "data": df.to_dict(orient="records"),
            }
            return Responses.success_response(
                "Downtime list fetched successfully ", data=data
            )

        packer_shift_level_stoppages_df["date"] = packer_shift_level_stoppages_df[
            "date"
        ].astype(str)

        df = df.merge(
            packer_shift_level_stoppages_df,
            on=["plant", "date", "shift", "packer", "tl_name"],
        ).to_dict(orient="records")

        data = {"data_from_table": data_from_table, "data": df}
        return Responses.success_response(
            "Downtime list fetched successfully ", data=data
        )


# class PpDowntimeEntryViewSet(GenericAPIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         request_data = request.data
#         pp_downtime_serializer = PpDowntimeBulkCreateSerializer(
#             data=request_data,
#             context={
#                 "created_by": request.user.id,
#             },
#             many=True,
#         )
#         pp_downtime_serializer.is_valid(raise_exception=True)
#         pp_downtime_serializer.save()
#         return Responses.success_response(
#             "created successfully", data=pp_downtime_serializer.data
#         )


class ShiftWiseAdhocQtyBulkCreateViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request_data = request.data
        shift_details_serializer = ShiftWiseAdhocQtyBulkCreateSerializer(
            data=request_data,
            context={
                "created_by": request.user.id,
            },
            many=True,
        )
        shift_details_serializer.is_valid(raise_exception=True)
        shift_details_serializer.save()
        return Responses.success_response(
            "created successfully", data=shift_details_serializer.data
        )


class GetAdhocQtyListViewSet(APIView):
    def get(self, request):
        plant = request.query_params.get("plant")
        shift = request.query_params.get("shift")
        date = request.query_params.get("date")

        shift_wise_adhoc_obj = ShiftwiseAdhocQty.objects.filter(
            shift=shift, plant=plant, date=date
        ).values()
        if shift_wise_adhoc_obj:
            data_from_table = "adhoc"
            data_dict = {
                "data_from_table": data_from_table,
                "data": shift_wise_adhoc_obj,
            }
            return Responses.success_response(
                "Adhoc Quantity Fetched Successfully", data=data_dict
            )

        else:
            data_from_table = "executable"
            executable_obj = (
                LpSchedulingExecutableDtl.objects.filter(
                    executable_date=date, executable_shift=shift, original_source=plant
                )
                .values("order_master__brand", "order_master__grade")
                .annotate(
                    Count("order_master__brand"),
                    Count("order_master__grade"),
                    Sum("order_master__order_quantity"),
                )
            )
            # .aggregate(Sum("order_master__order_quantity")).get("order_master__order_quantity__sum")
            data_dict = {"data_from_table": data_from_table, "data": executable_obj}
            return Responses.success_response(
                "Adhoc Quantity Fetched Successfully", data=data_dict
            )


class UpdateAdhocQtyListViewSet(APIView):
    def post(self, request):
        adhoc_data_list = request.data
        for adhoc_data in adhoc_data_list:
            adhoc_obj = ShiftwiseAdhocQty.objects.get(id=adhoc_data["id"])
            adhoc_data.pop("id")
            adhoc_serializer = ShiftWiseAdhocQtySerializer(
                adhoc_obj, data=adhoc_data, partial=True
            )
            if adhoc_serializer.is_valid():
                adhoc_serializer.save(
                    last_updated_by=request.user.id, last_update_login=request.user.id
                )
            else:
                return Response(
                    {"status": "error", "data": adhoc_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"status": "adhoc data updated success", "data": []},
            status=status.HTTP_200_OK,
        )


# class UpdatePpDowntimeListViewSet(APIView):
#     def post(self, request):
#         downtime_data_list = request.data
#         for downtime_data in downtime_data_list:
#             downtime_obj = PpDowntime.objects.get(id=downtime_data["id"])
#             downtime_data.pop("id")
#             downtime_serializer = PpDowntimeSerializer(
#                 downtime_obj, data=downtime_data, partial=True
#             )
#             if downtime_serializer.is_valid():
#                 downtime_serializer.save(
#                     last_updated_by=request.user.id, last_update_login=request.user.id
#                 )

#             else:
#                 return Response(
#                     {"status": "error", "data": downtime_serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         return Response(
#             {"status": "pp downtime data updated success", "data": []},
#             status=status.HTTP_200_OK,
#         )


class PpRailOrderTaggingValueViewSet(GenericAPIView):
    queryset = PpRailOrderTagging.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PpRailOrderTaggingFilter

    def get(self, request):
        plant = request.query_params.get("plant")
        shift = request.query_params.get("shift")
        date = request.query_params.get("date")
        run_id = request.query_params.get("run_id")

        data = (
            PpRailOrderTagging.objects.filter(
                run__run_id=run_id, run__plant=plant, run__shift=shift, run__date=date
            )
            .values(
                "packer_code",
                "tl_code",
                "grade",
                "brand",
            )
            .annotate(
                sum_value_of_order_qty=Sum("quantity"),
                sum_of_order_processing_time=Sum("order_processing_time"),
            )
            .order_by()
        )
        return Responses.success_response("data fetched", data=data)


class MvPendingReasonsForDelayViewSet(ModelViewSet):
    queryset = MvPendingReasonsForDelay.objects.all().order_by("-delay")
    serializer_class = MvPendingReasonsForDelaySerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MvPendingReasonsForDelayFilter
    lookup_field = "delivery_detail_id"


class MvPendingReasonsForDelayDropdown(GenericAPIView):
    queryset = MvPendingReasonsForDelay.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MvPendingReasonsForDelayFilter

    def __get_reason_for_delay_query(self, query_string, filter_query=Q):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "source_line_id": self.__get_reason_for_delay_query(
                "source_line_id", Q(source_line_id__isnull=False)
            ),
            "status": self.__get_reason_for_delay_query(
                "status", Q(status__isnull=False)
            ),
            "packing_type": self.__get_reason_for_delay_query(
                "packing_type", Q(packing_type__isnull=False)
            ),
            "segment": self.__get_reason_for_delay_query(
                "segment", Q(segment__isnull=False)
            ),
            "ship_to_state": self.__get_reason_for_delay_query(
                "ship_to_state", Q(ship_to_state__isnull=False)
            ),
            "ship_to_district": self.__get_reason_for_delay_query(
                "ship_to_district", Q(ship_to_district__isnull=False)
            ),
            "ship_to_city": self.__get_reason_for_delay_query(
                "ship_to_city", Q(ship_to_city__isnull=False)
            ),
            "brand": self.__get_reason_for_delay_query("brand", Q(brand__isnull=False)),
            "product": self.__get_reason_for_delay_query(
                "product", Q(product__isnull=False)
            ),
            "delivery_id": self.__get_reason_for_delay_query(
                "delivery_id", Q(delivery_id__isnull=False)
            ),
            "plant": self.filter_queryset(self.get_queryset())
            .values_list("plant")
            .annotate(Count("plant"), plant_name=Substr("plant", pos=1, length=3))
            .values_list("plant_name", flat=True),
        }

        return Responses.success_response("reason for delay dropdown data.", data=data)


class TgtBridgingCostViewSet(ModelViewSet):
    queryset = TgtBridgingCost.objects.order_by("-effective_start_date")
    serializer_class = TgtBridgingCostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "active_flag",
        "route_id",
        "to_org",
    )
    pagination_class = CustomPagination
    lookup_field = "id"


class TgtBridgingCostAPIView(GenericAPIView):
    queryset = TOebsSclRouteMaster.objects.filter(
        route_id__isnull=False, active_flag="Y"
    )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    # filterset_fields = ("route_id", "mode_of_transport", "active_flag")
    filterset_class = TOebsSclRouteMasterFilter
    search_fields = ("route_id",)

    def __get_bridging_cost_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "route_id": self.__get_bridging_cost_query("route_id"),
            "to_org": self.__get_bridging_cost_query("to_city"),
        }
        return Responses.success_response("bridging cost dropdown data", data=data)


class GetStoppageDescriptionList(ModelViewSet):
    queryset = PackerRatedCapacity.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerRatedFilter

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .order_by("packer")
            .values("packer", "truck_loader")
            .annotate(
                Count("packer"),
                Count("truck_loader"),
            )
        )
        return Responses.success_response("stoppage description list data", data=data)


class PackerShiftLevelStoppagesMainListViewSet(ModelViewSet):
    queryset = PackerShiftLevelStoppages.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerShiftLevelStoppagesMainListFilter

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .values("plant", "shift", "date")
            .annotate(
                Count("plant"),
                Count("shift"),
                Count("date"),
            )
        )
        return Responses.success_response("stoppage description list data", data=data)


class BackUnloadingEnrouteMarketsMasterViewSet(ModelViewSet):
    queryset = BackUnloadingEnrouteMarketsMaster.objects.all()
    serializer_class = BackUnloadingEnrouteMarketsMasterSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "source_state",
        "source_district",
        "destination_state",
        "destination_district",
        "passing_district",
        "passing_state",
    )
    lookup_field = "id"


class BackUnloadingEnrouteMarketsMasterDropdownView(GenericAPIView):
    queryset = BackUnloadingEnrouteMarketsMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "source_state",
        "source_district",
        "destination_state",
        "destination_district",
        "passing_district",
        "passing_state",
    )

    def __get_back_unloading_query(self, query_str):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_str, flat=True)
            .annotate(Count(query_str))
        )

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "back unloading en route market master dropdown data!",
            data={
                "source_state": self.__get_back_unloading_query("source_state"),
                "source_district": self.__get_back_unloading_query("source_district"),
                "destination_state": self.__get_back_unloading_query(
                    "destination_state"
                ),
                "destination_district": self.__get_back_unloading_query(
                    "destination_district"
                ),
                "passing_district": self.__get_back_unloading_query("passing_district"),
                "passing_state": self.__get_back_unloading_query("passing_state"),
            },
        )


class BagBurstDispatchQty(GenericAPIView):
    def get(self, request):
        plant = request.query_params.get("plant")
        date = request.query_params.get("date")
        data = TgtPlantDispatchData.objects.filter(
            excise_invoice_no__startswith=plant, tax_invoice_date__date=date
        ).aggregate(Sum("shipped_qty"))
        return Responses.success_response("tgt plant dispatch qty data", data=data)


class TOebsSclRouteMasterViewSet(ModelViewSet):
    queryset = TOebsSclRouteMaster.objects.filter(active_flag="Y")
    serializer_class = TOebsSclRouteMasterSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TOebsSclRouteMasterFilter
    lookup_field = "id"


class L1SourceMappingRouteIdDropdown(GenericAPIView):
    queryset = L1SourceMapping.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("route_id",)

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .values_list("route_id", flat=True)
            .distinct()
        )

        return Responses.success_response("source mapping route id dropdown", data=data)


class L1SourceMappingViewSet(ModelViewSet):
    queryset = L1SourceMapping.objects.filter(order_type="SO", priority=1)
    serializer_class = L1SourceMappingSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = L1SourceMappingFilter
    lookup_field = "id"


# class SourceChangeModeTotalImpact(GenericAPIView):
#     queryset = SourceChangeMode.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = (
#         "auto_tagged_source",
#         "auto_tagged_mode",
#         "changed_source",
#         "changed_mode",
#         "created_by__name",
#     )

#     def get(self, request, *args, **kwargs):
#         data = (
#             self.filter_queryset(self.get_queryset())
#             .values(
#                 "auto_tagged_source",
#                 "auto_tagged_mode",
#                 "changed_source",
#                 "changed_mode",
#                 "created_by__name",
#             )
#             .annotate(total_impact=Sum(F("changed_sla") - F("original_sla")))
#         )
#         return Responses.success_response(
#             "total impact of change source mode approvals data", data=data
#         )


class SourceChangeModeViewSet(ModelViewSet):
    queryset = SourceChangeMode.objects.all()
    serializer_class = SourceChangeModeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "auto_tagged_source",
        "auto_tagged_mode",
        "changed_source",
        "changed_mode",
    )


class TOebsApSuppliersViewSet(ModelViewSet):
    def get(self, request):
        data = TOebsApSuppliers.objects.filter(vendor_type_lookup_code="PP BAG").values(
            "vendor_id", "vendor_name"
        )
        return Responses.success_response("data", data=data)


class DemurrageAndWharfageForecastViewSet(GenericAPIView):
    queryset = LogisticsForecastRunDtl.objects.all()
    serializer_class = LogisticsForecastRunDtlSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("source",)
    # filterset_class = LogisticsForecastRunDtlFilter
    lookup_field = "id"

    def __get_run_id(self, month, year, type):
        try:
            data = (
                LogisticsForecastRun.objects.filter(
                    forecast_month__month=month,
                    forecast_month__year=year,
                    run_type=type,
                )
                .values("run_id")
                .latest("run_id")
            )
            return data["run_id"]
        except:
            return None

    def get(self, request, *args, **kwargs):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        siding_type = request.query_params.get("siding_type")

        if siding_type:
            plant_run_id = self.__get_run_id(month, year, siding_type)
            depot_run_id = None
        else:
            plant_run_id = self.__get_run_id(month, year, "PLANT")
            depot_run_id = self.__get_run_id(month, year, "Rake Point")

        data = self.filter_queryset(
            self.get_queryset().filter(
                Q(run__run_id=plant_run_id) | Q(run__run_id=depot_run_id)
            )
        ).values()
        ser_data = self.get_serializer(data, many=True)

        return Responses.success_response(
            "Demurrage and wharfage forecast data", data=ser_data.data
        )
