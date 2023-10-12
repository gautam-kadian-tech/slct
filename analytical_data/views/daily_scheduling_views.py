"""Daily scheduling views module."""

import json
from datetime import date, datetime
from decimal import Decimal
from random import randint

import pandas as pd
from django.conf import settings
from django.db import transaction
from django.db.models import (
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    FloatField,
    Max,
    Q,
    Sum,
    functions,
)
from django.db.models.functions import Round
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.custom_mixins import (
    DownloadModelMixin,
    RequestsCountMixin,
)
from analytical_data.enum_classes import (
    ApprovalStatusChoices,
    LpModelDfFnlBrandChoices,
)
from analytical_data.filters import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils import (
    CustomPagination,
    Response,
    Responses,
    dump_to_excel,
)
from analytical_data.view_helpers import *
from analytical_data.view_helpers.connection import connect_db
from analytical_data.view_helpers.get_user_detail import user_details
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class DemandBackhaulingProcessViewSet(ModelViewSet):
    queryset = Demand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DemandFilter
    pagination_class = CustomPagination

    def get(self, request):
        week = request.query_params.get("week")
        weeks = {"w1": 7, "w2": 14, "w3": 21, "w4": 28}
        data = (
            self.filter_queryset(self.get_queryset())
            .values_list("destination__district")
            .annotate(Sum("demand_qty"))
        )
        data_obj = round(weeks[week] / 30 * int(data[0][-1]), 2)
        final_data = {
            "monthly_demand": data[0][-1],
            "pro_rated_fulfilment": data_obj,
            "actual_data": int(data[0][-1]) - int(data_obj),
        }
        return Responses.success_response("Back hauling demand data", data=final_data)


class PackerShiftConstraintViewSet(ModelViewSet):
    """Packer shift constraint CRUDs view set class."""

    queryset = PackerShiftConstraint.objects.all().order_by("-id")
    serializer_class = PackerShiftConstraintSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerShiftConstraintFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        """Patch API"""
        request.data.pop("plant_id", None)
        return super().partial_update(request, *args, **kwargs)


class PackerShiftConstraintListView(ListAPIView):
    """Packer constraints master listing view."""

    queryset = PackerShiftConstraint.objects.all()
    serializer_class = PackerShiftConstraintSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerShiftConstraintFilter
    pagination_class = CustomPagination


class RouteRestrictionsViewSet(ModelViewSet):
    """Route restrictions CRUDs view set class."""

    queryset = RouteRestrictions.objects.all()
    serializer_class = RouteRestrictionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RouteRestrictionsFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class LpSchedulingPackerConstraintView(ModelViewSet):
    """CRUD view set for lp scheduling plant constraint."""

    queryset = LpSchedulingPackerConstraints.objects.order_by(
        "plant", "packer_no", "-id"
    )
    serializer_class = LpSchedulingPackerConstraintSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpSchedulingPackerConstraintFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class LpSchedulingPlantConstraintViewSet(DownloadUploadViewSet):
    """CRUD view set for lp scheduling plant constraint."""

    queryset = LpSchedulingPlantConstraints.objects.all().order_by("-id")
    serializer_class = LpSchedulingPlantConstraintSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpSchedulingPlantConstraintFilter
    sorting_fields = ("date", "plant_id", "grade")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "lp_scheduling_plant_constraint"


# class LpSchedulingPlantConstraintUploadDownloadViewSet(DownloadUploadViewSet):
#     """lp_scheduling_plant_constraint_capacity"""

# queryset = LpSchedulingPlantConstraints.objects.all()
# serializer_class = LpSchedulingPlantConstraintUploadDownloadSerializer
# filter_backends = (DjangoFilterBackend,)


class LpSchedulingVehicleConstraintView(DownloadUploadViewSet):
    """CRUD view set for lp scheduling vehicle constraint."""

    queryset = LpSchedulingVehicleConstraints.objects.all().order_by("-id")
    serializer_class = LpSchedulingVehicleConstraintSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = (
        "date",
        "no_of_vehicles",
        "plant",
        "vehicle_size",
        "vehicle_type",
    )
    filterset_class = LpSchedulingVehicleConstraintFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "lp_scheduling_vehicle_cons"


class LpSchedulingOrderMasterBaseViewSet(ModelViewSet):
    queryset = LpSchedulingOrderMaster.objects.order_by("club_id")
    serializer_class = LpSchedulingOrderMasterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = (
        "order_id",
        "order_header_id",
        "order_line_id",
        "order_date",
        "brand",
        "grade",
        "packaging",
        "pack_type",
        "order_type",
        "order_quantity",
        "ship_state",
        "ship_district",
        "ship_city",
        "customer_code",
        "cust_sub_cat",
        "cust_name",
        "auto_tagged_source",
        "auto_tagged_mode",
        "sales_officer_changed_source",
        "delivery_due_date",
        "dispatch_due_date",
        "order_status",
        "full_truck_load",
        "order_clubbed",
        "club_id",
        "di_generated",
        "order_executable",
        "self_consumption_flag",
        "pp_call",
        "remarks",
        "lp_scheduling_di_details__di_number",
    )
    filterset_class = LpSchedulingOrderMasterFilter
    pagination_class = CustomPagination


class LpSchedulingOrderMasterViewSet(LpSchedulingOrderMasterBaseViewSet):
    """Lp scheduling order master data listing."""

    queryset = LpSchedulingOrderMaster.objects.order_by("-order_date")

    def list(self, request, *args, **kwargs):
        active_run_ids = (
            LpModelRun.objects.filter(
                plan_date__month=datetime.now().month, approve_status=1
            )
            .values_list("run_id", flat=True)
            .annotate(Count("run_id"))
        )
        final_demand_plan = LpModelDfFnl.objects.filter(
            run_id__in=list(active_run_ids)
        ).values()
        final_planned_df = pd.DataFrame(final_demand_plan).replace(
            dict(LpModelDfFnlBrandChoices.choices)
        )

        if final_planned_df.empty:
            final_planned_df = pd.DataFrame(
                columns=[
                    "id",
                    "scenario",
                    "run_id",
                    "route_id",
                    "route_id_secondary",
                    "primary_secondary_route",
                    "plant_id",
                    "grade",
                    "node_city",
                    "destination_city",
                    "destination_district",
                    "destination_state",
                    "mode",
                    "cust_category",
                    "brand",
                    "pack_type",
                    "packaging",
                    "freight_type",
                    "price",
                    "primary_frt",
                    "secondary_frt",
                    "discount",
                    "taxes",
                    "misc_charges",
                    "ha_commission",
                    "demurrage",
                    "damages",
                    "rake_charges",
                    "sp_commission",
                    "isp_commission",
                    "variable_production_cost",
                    "clinker_plant",
                    "clinker_mode",
                    "clinker_freight",
                    "route_changed",
                    "clinker_cf",
                    "contribution",
                    "qty",
                    "tlc",
                    "direct_plant_discount",
                    "jhju_rail_discount",
                    "avg_time",
                    "notional_freight",
                    "zone",
                ]
            )

        final_planned_df = (
            final_planned_df.sort_values(
                [
                    "brand",
                    "grade",
                    "destination_state",
                    "destination_district",
                    "destination_city",
                    "qty",
                ],
                ascending=False,
            )
            .drop_duplicates(
                [
                    "brand",
                    "grade",
                    "destination_state",
                    "destination_district",
                    "destination_city",
                ]
            )
            .drop(
                [
                    "scenario",
                    "run_id",
                    "route_id",
                    "route_id_secondary",
                    "primary_secondary_route",
                    "plant_id",
                    "cust_category",
                    "pack_type",
                    "packaging",
                    "price",
                    "primary_frt",
                    "secondary_frt",
                    "discount",
                    "taxes",
                    "misc_charges",
                    "ha_commission",
                    "demurrage",
                    "damages",
                    "rake_charges",
                    "sp_commission",
                    "isp_commission",
                    "variable_production_cost",
                    "clinker_plant",
                    "clinker_mode",
                    "clinker_freight",
                    "route_changed",
                    "clinker_cf",
                    "contribution",
                    "qty",
                    "tlc",
                    "direct_plant_discount",
                    "jhju_rail_discount",
                    "avg_time",
                    "notional_freight",
                    "zone",
                ],
                axis=1,
            )
            .rename(
                columns={
                    "node_city": "planned_node_city",
                    "mode": "planned_mode",
                    "freight_type": "planned_sale_type",
                }
            )
        )

        queryset = self.filter_queryset(self.get_queryset()).values()
        page = self.paginate_queryset(queryset)

        if not page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        order_master_df = pd.DataFrame(page)
        joined_df = order_master_df.merge(
            final_planned_df,
            left_on=["brand", "grade", "ship_state", "ship_district", "ship_city"],
            right_on=[
                "brand",
                "grade",
                "destination_state",
                "destination_district",
                "destination_city",
            ],
            suffixes=("", "_y"),
            how="left",
        ).drop(["id_y"], axis=1)

        joined_df["created_at"] = joined_df["created_at"].apply(
            lambda x: str(x) if x else None
        )
        joined_df["updated_at"] = joined_df["updated_at"].apply(
            lambda x: str(x) if x else None
        )
        joined_df["delivery_due_date"] = joined_df["delivery_due_date"].apply(
            lambda x: str(x) if x else None
        )
        joined_df["dispatch_due_date"] = joined_df["dispatch_due_date"].apply(
            lambda x: str(x) if x else None
        )
        joined_df["dilink_creation_dt"] = joined_df["dilink_creation_dt"].apply(
            lambda x: str(x) if x else None
        )
        joined_df["order_date"] = joined_df["order_date"].apply(
            lambda x: str(x) if x else None
        )

        joined_df["planned_source"] = joined_df["planned_node_city"]

        return self.get_paginated_response(
            json.loads(joined_df.to_json(orient="records"))
        )

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            id__in=[data["id"] for data in request.data]
        )
        queryset.update(updated_at=date.today())
        serializer = self.get_serializer(queryset, request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response("Bulk update success.", data=serializer.data)


class LpSchedulingOrderMasterEditDropdownViewSet(ListAPIView):
    """Lp scheduling order master data edit dropdown listing."""

    active_run_ids = (
        LpModelRun.objects.filter(
            plan_date__month=datetime.now().month, approve_status=1
        )
        .values_list("run_id", flat=True)
        .annotate(Count("run_id"))
    )

    queryset = (
        LpModelDfRank.objects.filter(run_id__in=list(active_run_ids))
        .order_by("qty")
        .annotate(
            tlc=ExpressionWrapper(
                F("primary_frt")
                + F("secondary_frt")
                + F("ha_commission")
                + F("demurrage")
                + F("damages")
                + F("direct_plant_discount")
                + F("fiscal_benefit_amt"),
                output_field=FloatField(),
            )
        )
    )
    serializer_class = LpModelDfRankSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpModelDfFnlOrderMasterEditFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LpSchedulingOrderMasterUpdateView(ModelViewSet):
    queryset = LpSchedulingOrderMaster.objects.all().order_by("club_id")
    serializer_class = LpSchedulingOrderMasterUpdateSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = PackerBagBurstingDescFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class LpSchedulingOrderExecutableView(
    LpSchedulingOrderMasterBaseViewSet, DownloadModelMixin
):
    """Daily scheduling order executable view class."""

    order_executable_ids = LpSchedulingExecutableDtl.objects.values_list(
        "order_master", flat=True
    )
    serializer_class = LpSchedulingOrderExecutableSerializer
    search_fields = ("order_master__order_id",)
    file_name = "order_executable"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "lp_scheduling_crm_checks",
                "lp_scheduling_executable_dtl",
                "lp_scheduling_pp_call_dtl",
            )
            .filter(id__in=self.order_executable_ids)
            .order_by("lp_scheduling_pp_call_dtl__exec_calling_sequence")
        )

    def download(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = json.loads(json.dumps(serializer.data, default=str))
        try:
            df = (
                pd.concat(
                    [
                        pd.json_normalize(
                            data,
                            meta=[
                                "id",
                                "duration",
                                "cost_impact",
                                "order_id",
                                "order_header_id",
                                "order_line_id",
                                "order_date",
                                "brand",
                                "grade",
                                "packaging",
                                "pack_type",
                                "order_type",
                                "order_quantity",
                                "ship_state",
                                "ship_district",
                                "ship_city",
                                "customer_code",
                                "customer_type",
                                "cust_sub_cat",
                                "cust_name",
                                "auto_tagged_source",
                                "auto_tagged_mode",
                                "sales_officer_changed_source",
                                "delivery_due_date",
                                "dispatch_due_date",
                                "order_status",
                                "full_truck_load",
                                "order_clubbed",
                                "club_id",
                                "di_generated",
                                "order_executable",
                                "self_consumption_flag",
                                "pp_call",
                                "remarks",
                                "created_at",
                                "updated_at",
                                "reason",
                                "delivery_id",
                                "delivery_detail_id",
                                "org_id",
                                "organization_id",
                                "inventory_item_id",
                                "dispatched_quantity",
                                "dilink_creation_dt",
                                "tax_invoice_date",
                                "ship_taluka",
                                "full_address",
                                "vehicle_type",
                                "vehicle_number",
                                "plant_name",
                                "ship_from_zone",
                                "warehouse",
                                "ship_to_org_id",
                                "freightterms",
                                "fob",
                                "token_id",
                                "route",
                                "source_location_id",
                                "shipinglocation",
                                "sales_order_type",
                                "changed_source",
                                "changed_mode",
                                "transferred_to_depot",
                                "request_date",
                                "released_date",
                            ],
                            record_path=[value],
                            errors="ignore",
                            record_prefix="_",
                        ).assign(admin_type=value)
                        for value in (
                            "lp_scheduling_crm_checks",
                            "lp_scheduling_executable_dtl",
                            "lp_scheduling_pp_call_dtl",
                        )
                    ]
                )
                .reset_index(drop=True)
                .drop(["_id", "_created_at", "_updated_at", "_order_master"], axis=1)
            )
            df.columns = df.columns.str.lstrip("_")
            df.columns = df.columns.str.replace("_", " ")
            df.columns = df.columns.str.upper()
        except KeyError:
            return Responses.error_response("No data")
        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).distinct()

    def list(self, request, *args, **kwargs):
        # exclude the data for which there is an entry in lp_scheduling_di_dtl
        response = super().list(request, *args, **kwargs)
        self.filterset_class = LpSchedulingOrderExecutableFilter
        total_order_quantity = (
            self.filter_queryset(LpSchedulingExecutableDtl.objects.all())
            .aggregate(Sum("order_master__order_quantity"))
            .get("order_master__order_quantity__sum")
        )
        response.data.get("data").update({"total_order_quantity": total_order_quantity})
        return response

    def patch(self, request):
        id = request.query_params.get("id")
        lpsObj = LpSchedulingExecutableDtl.objects.get(id=id)
        serializer = LpSchedulingExecutableDtlSerializer(
            lpsObj, data=request.data, partial=True
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


class LpSchedulingOrderNonExecutableView(
    LpSchedulingOrderMasterBaseViewSet, DownloadModelMixin
):
    """Daily scheduling order non-executable view class."""

    order_executable_ids = LpSchedulingExecutableDtl.objects.values_list(
        "order_master", flat=True
    )
    serializer_class = LpSchedulingOrderNonExecutableSerializer
    # search_fields = ("order_id", "lp_scheduling_di_details__di_number")
    file_name = "order_non_executable"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "lp_scheduling_crm_checks", "lp_scheduling_executable_dtl"
            )
            .exclude(id__in=self.order_executable_ids)
        )

    def get_serializer_context(self):
        colors = {}
        club_ids = LpSchedulingOrderMaster.objects.values_list(
            "club_id", flat=True
        ).annotate(Count("club_id"))
        get_random_num = lambda: randint(0, 255)
        for club_id in club_ids:
            colors[club_id] = "%02X%02X%02X" % (
                get_random_num(),
                get_random_num(),
                get_random_num(),
            )
        context = super().get_serializer_context()
        context.update({"colors": colors})
        return context

    def download(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = json.loads(json.dumps(serializer.data))
        try:
            df = (
                pd.concat(
                    [
                        pd.json_normalize(
                            data,
                            meta=[
                                "id",
                                "duration",
                                "cost_impact",
                                "order_id",
                                "order_header_id",
                                "order_line_id",
                                "order_date",
                                "brand",
                                "grade",
                                "packaging",
                                "pack_type",
                                "order_type",
                                "order_quantity",
                                "ship_state",
                                "ship_district",
                                "ship_city",
                                "customer_code",
                                "customer_type",
                                "cust_sub_cat",
                                "cust_name",
                                "auto_tagged_source",
                                "auto_tagged_mode",
                                "sales_officer_changed_source",
                                "delivery_due_date",
                                "dispatch_due_date",
                                "order_status",
                                "full_truck_load",
                                "order_clubbed",
                                "club_id",
                                "di_generated",
                                "order_executable",
                                "self_consumption_flag",
                                "pp_call",
                                "remarks",
                                "created_at",
                                "updated_at",
                                "reason",
                                "delivery_id",
                                "delivery_detail_id",
                                "org_id",
                                "organization_id",
                                "inventory_item_id",
                                "dispatched_quantity",
                                "dilink_creation_dt",
                                "tax_invoice_date",
                                "ship_taluka",
                                "full_address",
                                "vehicle_type",
                                "vehicle_number",
                                "plant_name",
                                "ship_from_zone",
                                "warehouse",
                                "ship_to_org_id",
                                "freightterms",
                                "fob",
                                "token_id",
                                "route",
                                "source_location_id",
                                "shipinglocation",
                                "sales_order_type",
                                "changed_source",
                                "changed_mode",
                                "transferred_to_depot",
                                "request_date",
                                "released_date",
                            ],
                            record_path=[value],
                            errors="ignore",
                            record_prefix="_",
                        ).assign(admin_type=value)
                        for value in (
                            "lp_scheduling_crm_checks",
                            "lp_scheduling_executable_dtl",
                            "lp_scheduling_pp_call_dtl",
                        )
                    ]
                )
                .reset_index(drop=True)
                .drop(["_id", "_created_at", "_updated_at", "_order_master"], axis=1)
            )
            df.columns = df.columns.str.lstrip("_")
            df.columns = df.columns.str.replace("_", " ")
            df.columns = df.columns.str.upper()
        except KeyError:
            df = pd.DataFrame()
            # return Responses.error_response("No data")
        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response


class LpSchedulingPpSequenceView(LpSchedulingOrderMasterBaseViewSet):
    """Daily scheduling PP sequence view class."""

    serializer_class = LpSchedulingPpSequenceSerializer
    # search_fields = ("order_id", "lp_scheduling_di_details__di_number")
    filterset_class = PpSequenceFilter
    order_line_ids = (
        PpOrderStatus.objects.filter(status="DI LINKED")
        .distinct("order_line_id")
        .values_list("order_line_id")
    )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "lp_scheduling_di_details",
                "lp_scheduling_pp_call_dtl",
                "pp_order_tagging",
            )
            .filter(
                order_line_id__in=self.order_line_ids,
                pp_call=False,
                lp_scheduling_di_details__di_number__isnull=False,
            )
            .order_by("lp_scheduling_pp_call_dtl__pp_calling_sequence")
        )


class LpSchedulingOrderExecutableDropdownView(GenericAPIView):
    """Lp scheduling order master executable edit dropdown."""

    # helper = LpSchedulingOrderExecutableDropdownHelper
    queryset = LpSchedulingOrderMaster.objects.all()

    def _get_dropdown_data(self, id):
        BRAND = {
            "Shree": 102,
            "Bangur": 103,
            "Rockstrong": 104,
        }
        order = self.get_queryset().filter(id=id).first()
        df = pd.read_csv(settings.LP_SOURCE_MAPPING_CSV_PATH)
        try:
            df = df.loc[
                (df.ORDER_TYPE == order.order_type)
                & (df.CUST_CATEGORY == order.customer_type)
                & (df.DESTINATION_CITY == order.ship_city)
                & (df.DESTINATION_DISTRICT == order.ship_district)
                & (df.DESTINATION_STATE == order.ship_state)
                & (df.BRAND == BRAND.get(order.brand))
                & (df.GRADE == order.grade)
                & (df.PACKAGING == order.packaging)
            ]
        except ValueError as e:
            print(e)
            return {"changed_source": list(), "changed_mode": list()}
        else:
            return {
                "changed_source": df.SOURCE_ID.tolist(),
                "changed_mode": df.MODE.tolist(),
            }

    def get(self, request, *args, **kwargs):
        """Get edit executable order pool dropdown."""
        return Responses.success_response(
            "Order executable dropdown options.",
            data=self._get_dropdown_data(kwargs.get("id")),
        )


class LpSchedulingPpSequenceDropdown(APIView):
    """PP Sequence filters dropdown api."""

    helper = PpSequenceDropdownHelper

    def get(self, request, *args, **kwargs):
        """Get API"""
        return Responses.success_response(
            "PP Sequence filters dropdown API.", data=self.helper._get_dropdown_data()
        )


class OrderExecutableQuantitySumView(ModelViewSet):
    """Order executable quantity sum and total quantity sum API."""

    queryset = LpSchedulingOrderMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpSchedulingOrderMasterFilter

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        """Get API"""

        order_t = request.query_params.get("order_type")
        plant_name = request.query_params.get("current_source")
        executable_date = request.query_params.get("executable_date")

        if request.query_params.get("order_type"):
            order_type = order_t
        else:
            order_type = "DI"
        total_order_qty = (
            self.get_queryset()
            .filter(
                ~Q(order_status="ORDER DISPATCHED"),
                ~Q(order_status="CANCELLED"),
                order_type=order_type,
                current_source=plant_name,
            )
            .aggregate(Sum("order_quantity"))
            .get("order_quantity__sum")
        )
        order_executable_qty_sum = (
            LpSchedulingExecutableDtl.objects.filter(
                ~Q(order_master__order_status="ORDER DISPATCHED"),
                ~Q(order_master__order_status="CANCELLED"),
                order_master__order_type=order_type,
                order_master__current_source=plant_name,
                executable_date=executable_date,
            )
            .aggregate(
                order_quantity__sum=functions.Coalesce(
                    Sum("order_master__order_quantity"), 0, output_field=DecimalField()
                )
            )
            .get("order_quantity__sum")
        )
        order_non_executable_qty = (
            self.get_queryset()
            .filter(
                ~Q(order_status="ORDER DISPATCHED"),
                ~Q(order_status="CANCELLED"),
                order_executable=False,
                current_source=plant_name,
                order_type=order_type,
            )
            .aggregate(non_executable_qty_sum=Sum("order_quantity"))
            .get("non_executable_qty_sum")
        )
        clubbed_order_qty = (
            self.filter_queryset(self.get_queryset())
            .filter(~Q(club_id=0))
            .aggregate(Sum("order_quantity"))
            .get("order_quantity__sum")
        )

        pp_call = (
            LpSchedulingPpCallDtl.objects.filter(
                pp_call_date__isnull=False, order_master__current_source=plant_name
            )
            .aggregate(
                order_quantity__sum=functions.Coalesce(
                    Sum("order_master__order_quantity"), 0, output_field=DecimalField()
                )
            )
            .get("order_quantity__sum")
        )

        data = {
            "order_pool": total_order_qty,
            "order_executable": order_executable_qty_sum,
            "order_non_executable": order_non_executable_qty,
            "pp_call": pp_call,
            "order_per_club_id": clubbed_order_qty,
        }
        return Responses.success_response("Order executable quantity data.", data=data)


class LpSchedulingVehicleConstraintDropdownView(GenericAPIView):
    """Lp scheduling vehicle constraint dropdown view."""

    # helper = LpSchedulingVehicleConstraintsHelper
    def _get_plant_query(self, query_string, request):
        """Pass query string and get the dropdown data associated with
        string."""
        queryset = PlantProductsMaster.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return (
            queryset.values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def _get_dropdown_data(self, request):
        """Returns Lp scheduling packer constraints dropdown data."""
        queryset = LpSchedulingVehicleConstraints.objects.filter(
            vehicle_type__isnull=False
        )
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return {
            "plant_id": self._get_plant_query("plant_id", request),
            "vehicle_type": (
                queryset.values_list("vehicle_type", flat=True).annotate(
                    Count("vehicle_type")
                )
            ),
        }

    def get(self, request, *args, **kwargs):
        """Get scheduling dropdown api."""
        return Responses.success_response(
            "Lp scheduling vehicle constraint dropdown.",
            data=self._get_dropdown_data(request),
        )


class LpSchedulingPlantConstraintDropdownView(GenericAPIView):
    """Lp scheduling plant constraint dropdown view."""

    # helper = PlantProductMasterDropdownHelper
    queryset = PlantProductsMaster.objects.all()

    def _get_plant_query(self, query_string):
        """Pass query string and get the dropdown data associated with
        string."""
        return (
            self.get_queryset()
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        """Get filter dropdown."""
        data = {
            "plant_id": self._get_plant_query("plant_id"),
            "grade": self._get_plant_query("grade"),
        }
        return Responses.success_response(
            "Lp scheduling plant constraint dropdown data.", data=data
        )


class LpSchedulingPackerConstraintDropdownView(GenericAPIView):
    """Lp scheduling packer constraint dropdown view."""

    # helper = LpSchedulingPackerConstraintsDropdownHelper
    def _get_plant_query(self, query_string, request):
        queryset = PlantProductsMaster.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return (
            queryset.values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def _get_dropdown_data(self, request):
        queryset = LpSchedulingPackerConstraints.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return {
            "plant_id": self._get_plant_query("plant_id", request),
            "packer": queryset.values_list("packer_no", flat=True).annotate(
                Count("packer_no")
            ),
        }

    def get(self, request, *args, **kwargs):
        """Get dropdown data."""
        return Responses.success_response(
            "Lp scheduling packer constraint dropdown data.",
            data=self._get_dropdown_data(request),
        )


class LpSchedulingOrderMasterDropdownView(ModelViewSet):
    """Lp scheduling order master dropdown view."""

    queryset = LpSchedulingOrderMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("ship_state", "ship_district", "ship_city")
    helper = LpSchedulingOrderMasterDropdownHelper

    def get(self, request, *args, **kwargs):
        """Get API."""
        return Responses.success_response(
            "Lp scheduling order master dropdown data.",
            data=self.helper._get_dropdown_data(
                self.filter_queryset(self.get_queryset())
            ),
        )


class LpSchedulingOrderMasterDistrictDropdownView(GenericAPIView):
    """Lp scheduling order master dropdown view."""

    queryset = LpSchedulingOrderMaster.objects.all()
    helper = LpSchedulingOrderMasterDropdownHelper

    def get(self, request, *args, **kwargs):
        """Get API."""
        return Responses.success_response(
            "Lp scheduling order master dropdown data.",
            data=self.helper._get_districts(self.get_queryset(), request.query_params),
        )


class LpSchedulingOrderMasterCityDropdownView(GenericAPIView):
    """Lp scheduling order master dropdown view."""

    queryset = LpSchedulingOrderMaster.objects.all()
    helper = LpSchedulingOrderMasterDropdownHelper

    def get(self, request, *args, **kwargs):
        """Get API."""
        return Responses.success_response(
            "Lp scheduling order master dropdown data.",
            data=self.helper._get_cities(self.get_queryset(), request.query_params),
        )


class LpScriptViewSet(GenericAPIView):
    def post(self, request):
        plant_input = request.data["plant_name"]
        cnxn = connect_db()
        run_pp_call_model(cnxn)
        run_executable_model(cnxn, plant_input)
        return Responses.success_response("Script compiled Successfully")


class LpSchedulingDiDtlViewSet(ListAPIView):
    queryset = LpSchedulingDiDetails.objects.all()
    serializer_class = LpSchedulingDiDetailsReadOnlySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = (
        "order_master__order_id",
        "created_at",
        "order_master__order_line_id",
        "order_line_id",
        "order_id",
    )
    search_fields = ("order_master__order_id", "order_master__order_line_id")
    pagination_class = CustomPagination


class LpSchedulingDiDtlDropdownViewSet(GenericAPIView):
    queryset = LpSchedulingDiDetails.objects.all()

    def get(self, request, *args, **kwargs):
        data = {
            "order_id": self.filter_queryset(self.get_queryset())
            .values_list("order_master__order_id", flat=True)
            .annotate(Count("order_master__order_id"))
        }
        return Responses.success_response(
            "lp scheduling di details dropdown: ", data=data
        )


class BackhaulingProcessDropdownViewSet(ModelViewSet):
    queryset = BackhaulingProcess.objects.all()
    serializer_class = BackhaulingProcessSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_fields = ("inbound_plant", "source_state", "source_district", "product")

    def __get_backhualing_process_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "inbound_plant": self.__get_backhualing_process_dropdown_query(
                "inbound_plant"
            ),
            "source_state": self.__get_backhualing_process_dropdown_query(
                "source_state"
            ),
            "source_district": self.__get_backhualing_process_dropdown_query(
                "source_district"
            ),
            "product": self.__get_backhualing_process_dropdown_query("product"),
        }
        return Responses.success_response(
            "backhualing_process_dropdown_list", data=data
        )

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        seralizer_obj = BackhaulingProcessSerializer(data=request.data)
        if not seralizer_obj.is_valid(raise_exception=True):
            return Responses.error_response(seralizer_obj.errors, "something wrong")
        seralizer_obj.save()
        return Responses.success_response(
            "data save in backhauling table", data=seralizer_obj.data
        )


class DepotAdditionOutputRunView(GenericAPIView):
    helper = DepotAdditionRunHelper
    serializer_class = DepotAdditionRunSerializer

    @transaction.atomic()
    def post(self, request):
        model_run_data = {
            "run_date": date.today(),
            "brand": request.data.get("brand"),
            "depot_cost": request.data.get("depot_cost"),
            "max_taluka_per_depot": request.data.get("max_taluka_per_depot"),
            "created_by": request.user.id,
            "last_updated_by": request.user.id,
            "last_update_login": request.user.id,
        }
        model_run_serializer = self.serializer_class(data=model_run_data)
        model_run_serializer.is_valid(raise_exception=True)
        model_run_instance = model_run_serializer.save()
        try:
            output = self.helper.get_optimal_depots(
                request.data.get("brand"),
                request.data.get("depot_cost"),
                request.data.get("max_taluka_per_depot"),
            )
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        output.columns = output.columns.str.lower()

        output["recommended_depo_lead"] = output["recommended_depo_lead"].round(
            decimals=2
        )
        output["lat"] = output["lat"].round(decimals=2)
        output["long"] = output["long"].round(decimals=2)
        output["depot_lat"] = output["depot_lat"].round(decimals=2)
        output["depot_long"] = output["depot_long"].round(decimals=2)
        output["brand"] = request.data.get("brand")
        output["depot_opening_cost"] = request.data.get("depot_cost")
        output["no_of_taluka"] = request.data.get("max_taluka_per_depot")

        data = json.loads(output.to_json(orient="records"))

        depot_addition_serializer = DepotAdditionOutputViewOutputSerializer(
            data=data,
            context={
                "run_id": model_run_instance.run_id,
                "request_user": request.user.id,
            },
            many=True,
        )
        depot_addition_serializer.is_valid(raise_exception=True)
        depot_addition_serializer.save()
        return Responses.success_response(
            "model run successfully", data=model_run_instance.run_id
        )


class DepotAdditionOutputViewViewSet(ModelViewSet):
    """Packer constraints master listing view."""

    queryset = DepotAdditionOutputView.objects.all()
    serializer_class = DepotAdditionOutputViewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DepotAdditionOutputViewFilter
    pagination_class = CustomPagination


class OrderPoolSourceChangeDropdown(GenericAPIView):
    run_id = LpModelDfRank.objects.aggregate(Max("run_id"))
    queryset = (
        LpModelDfRank.objects.filter(run_id=run_id["run_id__max"])
        .values(
            "id",
            "run_id",
            "plant_id",
            "warehouse",
            "mode",
            "rank",
            "route_id",
            "route_id_secondary",
            "primary_secondary_route",
        )
        .order_by("rank")
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpModelDfRankFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data_list = []
        for data in queryset:
            party_code = None
            route_code = None
            if data["primary_secondary_route"] == "PRIMARY":
                party_code = data["plant_id"]
                route_code = data["route_id"]
            else:
                party_code = data["warehouse"]
                route_code = data["route_id_secondary"]

            data_dict = {
                "source": party_code,
                "mode": data["mode"],
                "route_id": route_code,
                "rank": data["rank"],
                "primary_secondary_route": data["primary_secondary_route"],
                "run_id": data["run_id"],
                "id": data["id"],
            }

            data_list.append(data_dict)

        return Responses.success_response("fetched successfully", data=data_list)


class SourceChangeFreightMasterViewSet(ModelViewSet):
    queryset = SourceChangeFreightMaster.objects.all()
    serializer_class = SourceChangeFreightMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SourceChangeFreightMasterFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        state = request.query_params.get("state")
        brand = request.query_params.get("brand")
        district = request.query_params.get("district")
        org_type = request.query_params.get("org_type")
        freight_master_data = SourceChangeFreightMaster.objects.filter(
            state=state, brand=brand, district=district, org_type=org_type
        ).values("incoterm", "freight_term")

        return Responses.success_response(
            "freight master data fetched successfully", data=freight_master_data
        )


class GetWarehouseId(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            w_house = request.query_params.get("w_house")
            warehouse_obj = TOebsHrAllOrganizationUnits.objects.filter(
                name__startswith=w_house
            ).first()
            warehouse_id = warehouse_obj.organization_id
        except:
            warehouse_id = None

        data_dict = {"warehouse_id": warehouse_id}

        return Responses.success_response(
            "warehouse id fetched successfully ", data=data_dict
        )


class LpSchedulingOrderMasterSourceChange(ModelViewSet):
    def patch(self, request):
        id = request.query_params.get("id")
        request.data["source_change_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        lpsObj = LpSchedulingOrderMaster.objects.get(id=id)
        serializer = LpSchedulingOrderMasterUpdateSerializer(
            lpsObj, data=request.data, partial=True
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


class SourceChangeContributionDifference(GenericAPIView):
    run_id = LpModelDfRank.objects.aggregate(Max("run_id"))
    queryset = LpModelDfRank.objects.filter(run_id=run_id["run_id__max"]).values(
        "contribution"
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpModelDfRankFilter

    def get(self, request):
        auto_tagged_source_contribution = (
            self.filter_queryset(self.get_queryset()).filter(
                plant_id=(request.query_params.get("auto_tagged_source")),
                primary_secondary_route="PRIMARY",
            )
        ).first()
        changed_source_contribution = (
            self.filter_queryset(self.get_queryset()).filter(
                rank=(request.query_params.get("rank"))
            )
        ).first()
        try:
            contribution_difference = (
                changed_source_contribution["contribution"]
                - auto_tagged_source_contribution["contribution"]
            )
        except:
            contribution_difference = 0
        return Responses.success_response(
            "contribution difference", data=contribution_difference
        )


class ChangeSourceApprovalRequest(DownloadUploadViewSet, RequestsCountMixin):
    queryset = SourceChangeApproval.objects.all().order_by("id")
    serializer_class = SourceChangeApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SourceChangeApprovalFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def __get_dropdown_query(self, query_str):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_str, flat=True)
            .distinct()
        )

    def dropdown(self, request, *args, **kwargs):
        data = {
            "auto_tagged_source": self.__get_dropdown_query(
                "order__auto_tagged_source"
            ),
            "auto_tagged_mode": self.__get_dropdown_query("order__auto_tagged_mode"),
            "changed_source": self.__get_dropdown_query("changed_source"),
            "changed_mode": self.__get_dropdown_query("changed_mode"),
            "order_line_id": self.__get_dropdown_query("order__order_line_id"),
            "ship_state": self.__get_dropdown_query("order__ship_state"),
            "ship_district": self.__get_dropdown_query("order__ship_district"),
            "ship_city": self.__get_dropdown_query("order__ship_city"),
            "customer_type": self.__get_dropdown_query("order__customer_type"),
            "dispatch_due_date": self.__get_dropdown_query("order__dispatch_due_date"),
        }
        return Responses.success_response("change source dropdown data.", data=data)


# class SourceChangeModeTotalImpact(GenericAPIView):
#     queryset = SourceChangeApproval.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = SourceChangeApprovalFilter
#     pagination_class = CustomPagination

#     def get(self, request, *args, **kwargs):
#         queryset = self.paginate_queryset(
#             self.filter_queryset(self.get_queryset())
#             .values(
#                 "order__auto_tagged_source",
#                 "order__auto_tagged_mode",
#                 "changed_source",
#                 "changed_mode",
#             )
#             .distinct()
#         )
#         return self.get_paginated_response(queryset)


class SystemRecommendationTechicalActivities(GenericAPIView):
    queryset = Demand.objects.all()
    # serializer_class = SourceChangeApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DemandFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def get(self, request):
        service = request.query_params.get("service")
        start_year = int(request.query_params.get("start_year"))
        end_year = start_year + 1

        if service == "Concrete Test":
            queryset = (
                self.filter_queryset(self.get_queryset())
                .filter(month__range=[f"{start_year}-04-01", f"{end_year}-03-31"])
                .values(
                    "destination__district",
                    "month__month",
                )
                .annotate(
                    Count("destination__district"),
                    total_services=Round(
                        Sum("demand_qty") * Decimal(1.2),
                        output_field=DecimalField(decimal_places=2),
                    ),
                )
            ).order_by("destination__district")
        else:
            queryset = (
                self.filter_queryset(self.get_queryset())
                .filter(month__range=[f"{start_year}-04-01", f"{end_year}-03-31"])
                .values(
                    "destination__district",
                    "month__month",
                )
                .annotate(
                    Count("destination__district"),
                    total_services=Round(
                        Sum("demand_qty") * Decimal(0.015),
                        output_field=DecimalField(decimal_places=2),
                    ),
                )
            ).order_by("destination__district")

        return Responses.success_response("Fetched succesfully", data=queryset)


class TaregtSettingDownload(GenericAPIView):
    helper = TaregtSettingViewHelper
    parser_classes = (MultiPartParser, JSONParser)
    file_name = "target_setting_file"

    def get(self, request):
        cnxn = connect_db()
        date = request.query_params.get("date")
        targets = self.helper.get_targets(cnxn, date)
        workbook = dump_to_excel(targets, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response[
            "Content-Disposition"
        ] = f"attachment; filename=target_settings_file.xlsx"
        return response


class OrderExecutableDetailUpdateOrCreate(GenericAPIView):
    def delete(self, request):
        order_master_id = request.query_params.get("order_master_id")
        lpsObj = LpSchedulingExecutableDtl.objects.filter(
            order_master__id=order_master_id
        )
        if lpsObj:
            lpsObj.latest("id").delete()
            return Responses.success_response(
                "deleted data by order master id successfully ", data=[]
            )
        return Responses.success_response("No data found", data=[])

    def patch(self, request):
        order_master_id = request.query_params.get("order_master_id")
        lpsObj = LpSchedulingExecutableDtl.objects.filter(
            order_master__id=order_master_id
        )
        if lpsObj:
            lpsObj = lpsObj.latest("id")
            serializer = LpSchedulingExecutableDtlSerializer(
                lpsObj, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(
                    last_updated_by=request.user.id, last_update_login=request.user.id
                )
                return Responses.success_response(
                    "data updated by order master id successfully ",
                    data=serializer.data,
                )
            else:
                return Responses.error_response("update failed", data=serializer.errors)
        else:
            request.data["order_master"] = order_master_id
            seralizer_obj = LpSchedulingExecutableDtlSerializer(data=request.data)
            if not seralizer_obj.is_valid(raise_exception=True):
                return Responses.error_response(seralizer_obj.errors, "something wrong")
            seralizer_obj.save()
            return Responses.success_response(
                "Created Succesfully", data=seralizer_obj.data
            )


class DepoAdditionRunListViewSet(ModelViewSet):
    def get(self, request):
        queryset = DepotAdditionRun.objects.filter(
            run_date=request.query_params.get("run_date")
        ).values_list("run_id", flat=True)
        return Responses.success_response(
            "dropdown data of addition run ", data=queryset
        )


class PackerRatedCapacityDropdown(GenericAPIView):
    """packer rated dropdown api."""

    queryset = PackerRatedCapacity.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("plant",)

    def __get_packer_rated_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .distinct(query_string)
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "truck_loader": self.__get_packer_rated_query("truck_loader"),
        }
        return Responses.success_response("packer rated capacity dropdown", data=data)
