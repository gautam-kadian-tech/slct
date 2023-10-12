"""Monthly scheduling views module."""
import json
from datetime import date, datetime
from logging import getLogger

import pandas as pd
import requests
from django.conf import settings
from django.db import transaction
from django.db.models import (
    Case,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
    Sum,
    When,
)
from django.db.models.functions import Substr
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import TgtRlsRoleData
from analytical_data.filters import *
from analytical_data.filters.lp_model_run_filter import (
    GdWharfageRunInputFilter,
)
from analytical_data.models import *
from analytical_data.models.monthly_scheduling_models import (
    LpMinCapacity,
    TOebsHrAllOrganizationUnits,
)
from analytical_data.models.packing_plant_models import PpOrderTagging
from analytical_data.serializers import *
from analytical_data.serializers.monthly_scheduling_serializers import (
    GdWharfageRunInputserializer,
    LpMinCapacitySerializer,
)
from analytical_data.utils import (
    CustomPagination,
    PrefixConversion,
    Response,
    Responses,
    dump_to_excel,
)
from analytical_data.view_helpers import *
from analytical_data.views.custom_viewsets import DownloadUploadViewSet

log = getLogger()
from analytical_data.view_helpers.get_user_detail import user_details


class DemandListView(DownloadUploadViewSet):
    """Demand data listing and download."""

    queryset = (
        Demand.objects.all().select_related("destination").order_by("-month__month")
    )
    serializer_class = DemandSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DemandFilter
    pagination_class = CustomPagination
    file_name = "demand_list"
    lookup_field = "id"


class GetDemandDataByIdViewSet(ModelViewSet):
    queryset = Demand.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        demand_serializer = DemandSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched successfully", data=demand_serializer.data
        )


class DemandDropdownView(GenericAPIView):
    """Options dropdown API for demand list."""

    queryset = Demand.objects.all()

    def _get_demand_dropdown_data(self, query_params):
        destination_state_data = self.__get_field_values("destination__state")
        destination_district_data = self.__get_field_values(
            "destination__district", Q(destination__state=query_params.get("state"))
        )
        destination_city_data = self.__get_field_values(
            "destination__city",
            Q(
                destination__state=query_params.get("state"),
                destination__district=query_params.get("district"),
            ),
        )
        brand_data = self.__get_field_values("brand")
        grade_data = self.__get_field_values("grade")
        cust_category_data = self.__get_field_values("cust_category")
        pack_type_data = self.__get_field_values("pack_type")
        month_data = self.__get_field_values("month__month")

        options = {
            "brand": brand_data,
            "grade": grade_data,
            "cust_category": cust_category_data,
            "pack_type": pack_type_data,
            "month": month_data,
            "destination_state_data": destination_state_data,
            "destination_district": destination_district_data,
            "destination_city": destination_city_data,
        }
        return options

    def __get_field_values(self, field, filter_query=Q()):
        return (
            self.get_queryset()
            .filter(filter_query)
            .values_list(field, flat=True)
            .annotate(Count(field))
        )

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = self._get_demand_dropdown_data(request.query_params)
        return Responses.success_response("Links master options dropdown.", data=data)


# class FreightMasterViewSet(ModelViewSet):
#     """Edit freight master."""

#     queryset = FreightMaster.objects.all()
#     serializer_class = NotionalFreightUpdateSerializer
#     pagination_class = CustomPagination

#     def partial_update(self, request, *args, **kwargs):
#         """Edit notional freight in freight master objects."""
#         demand_object = self.get_object()
#         serializer = self.get_serializer(demand_object, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Responses.success_response(
#             "Notional freight updated.", status.HTTP_200_OK, serializer.data
#         )


# class FreightMasterList(ListAPIView):
#     """Freight master listing"""

#     queryset = FreightMaster.objects.all()
#     serializer_class = FreightMasterSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = FreightMasterFilter
#     pagination_class = CustomPagination


class GodownMasterViewSet(ModelViewSet):
    """Godown master update view."""

    queryset = GodownMaster.objects.all()
    serializer_class = GodownMasterSerializer
    pagination_class = CustomPagination

    def put(self, request, id):
        """Edit godown master data."""
        demand_object = self.get_object()
        serializer = GodownMasterSerializer(
            demand_object, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            "Godown master updated.", data=serializer.data
        )


class GodownMasterListView(DownloadUploadViewSet):
    """Godown master listing view."""

    queryset = GodownMaster.objects.all().order_by("-updated_at")
    serializer_class = GodownMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GodownMasterFilter
    pagination_class = CustomPagination
    file_name = "godown_master"


class GodownMasterDropdownView(GenericAPIView):
    """Options dropdown API for vehicle availability list."""

    # helper = GodownMasterDropdownHelper
    queryset = GodownMaster.objects.all()

    def __get_godown_master_query(self, query_string, query=Q()):
        return (
            self.get_queryset()
            .filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def _get_dropdown_data(self, query_params):
        """Returns dropdown data for Godown Master list."""
        return {
            "state": self.__get_godown_master_query("state"),
            "district": self.__get_godown_master_query(
                "district", Q(state=query_params.get("state"))
            ),
            "city": self.__get_godown_master_query(
                "city",
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
        }

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        return Responses.success_response(
            "Godown Master options dropdown.",
            data=self._get_dropdown_data(request.query_params),
        )


class LinksMasterViewSet(DownloadUploadViewSet):
    """Links master objects operations view set class."""

    queryset = LinksMaster.objects.all().select_related("freight_master")
    serializer_class = LinksMasterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = LinksMasterFilter
    search_fields = ("^route_id",)
    pagination_class = CustomPagination
    file_name = "links_master"
    sorting_fields = ("id",)

    def partial_update(self, request, *args, **kwargs):
        """Activate or deactivate links master"""
        response = super().partial_update(request, *args, **kwargs)
        return Responses.success_response(
            "LinksMaster object activated/deactivated.",
            response.status_code,
            data=response.data,
        )


class GetLastUpdatedDate(APIView):
    MASTER_TYPES = {
        "LinksMaster": LinksMaster,
        "GodownMaster": GodownMaster,
        "PackagingMaster": PackagingMaster,
        "PlantProductsMaster": PlantProductsMaster,
        "ClinkerLinksMaster": ClinkerLinksMaster,
        "RailHandling": RailHandling,
        "PlantConstraintsMaster": PlantConstraintsMaster,
    }

    def __get_latest_record(self, master_type):
        if master_type == ClinkerLinksMaster or master_type == RailHandling:
            latest_record = (
                master_type.objects.filter(last_update_date__isnull=False)
                .order_by("-last_update_date")
                .first()
            )
            return (
                {"last_updated": latest_record.last_update_date}
                if latest_record
                else {"last_updated": None}
            )
        else:
            latest_record = (
                master_type.objects.filter(updated_at__isnull=False)
                .order_by("-updated_at")
                .first()
            )
            return (
                {"last_updated": latest_record.updated_at}
                if latest_record
                else {"last_updated": None}
            )

    def get(self, request):
        master_type = request.query_params.get("master_type")
        master_type_cls = self.MASTER_TYPES.get(master_type)
        if master_type_cls:
            return Response(self.__get_latest_record(master_type_cls))
        else:
            return Response({"last_updated": None})


class LinksMasterDropdownView(GenericAPIView):
    """Options dropdown API for links master list."""

    # helper = LinksMasterDropdownViewHelper
    queryset = LinksMaster.objects.all()

    def get_links_master_dropdown_data(self):
        plant = self.__get_field_values("plant")
        freight_type = self.__get_field_values("freight_type")
        # destination_district = self.__get_field_values("destination_district")
        destination_state = self.__get_field_values("destination_state")
        warehouse = self.__get_field_values("warehouse")

        options = {
            "plant": plant,
            "cust_category": ["NT", "TR"],
            "freight_type": freight_type,
            "mode": ["ROAD", "RAIL"],
            # "destination_district": destination_district,
            "destination_state": destination_state,
            "primary_secondary_route": ["PRIMARY", "SECONDARY"],
            "warehouse": warehouse,
        }
        return options

    def __get_field_values(self, field):
        return (
            self.get_queryset()
            .values_list(field, flat=True)
            .annotate(Count(field))
            .order_by(field)
        )

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = self.get_links_master_dropdown_data()
        return Responses.success_response("Links master options dropdown.", data=data)


class StateViewSet(ModelViewSet):
    """Destination district, city, state list view."""

    def __get_links_master_query(self, query_string, query=Q()):
        return (
            LinksMaster.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "destination_state": self.__get_links_master_query("destination_state"),
            "destination_district": self.__get_links_master_query(
                "destination_district",
                Q(destination_state=request.query_params.get("destination_state")),
            ),
            "destination_city": self.__get_links_master_query(
                "destination_city",
                Q(
                    destination_state=request.query_params.get("destination_state"),
                    destination_district=request.query_params.get(
                        "destination_district"
                    ),
                ),
            ),
        }
        return Response(data=data, status=status.HTTP_200_OK)


class PackagingMasterViewSet(DownloadUploadViewSet):
    """Packaging master update and list view set class."""

    queryset = PackagingMaster.objects.all()
    serializer_class = PackagingMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackagingMasterFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "packaging_master"
    sorting_fields = ("id",)


class PackagingMasterDropdownView(GenericAPIView):
    """Options dropdown API for packaging master list."""

    # helper = PackagingMasterDropdownViewHelper
    queryset = PackagingMaster.objects.all()

    def get_packaging_master_dropdown_data(self):
        brand_data = self.__get_field_values("brand")
        product_data = self.__get_field_values("product")
        packaging_data = self.__get_field_values("packaging")

        options = {
            "brand": brand_data,
            "product": product_data,
            "packaging": packaging_data,
        }
        return options

    def __get_field_values(self, field):
        return (
            self.get_queryset()
            .values_list(field, flat=True)
            .annotate(Count(field))
            .order_by(field)
        )

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = self.get_packaging_master_dropdown_data()
        return Responses.success_response(
            "Packaging master options dropdown.", data=data
        )


class PackerConstraintsMViewSet(ModelViewSet):
    """Packer constraints master CRUDs view set class."""

    queryset = PackerConstraintsMaster.objects.all()
    serializer_class = PackerConstraintsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackerConstraintsFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        """Patch API"""
        request.data.pop("plant_id", None)
        return super().partial_update(request, *args, **kwargs)


class PlantConstraintsMViewSet(ModelViewSet):
    """Plant constraints master CRUDs view set class."""

    queryset = PlantConstraintsMaster.objects.all()
    serializer_class = PlantConstraintsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlantConstraintFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        request.data.pop("plant_id", None)
        return super().partial_update(request, *args, **kwargs)


class PlantProductsMasterViewSet(DownloadUploadViewSet):
    """Edit variable_production_cost field in PlantProductsMaster."""

    queryset = PlantProductsMaster.objects.all()
    serializer_class = PlantProductsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = PlantProductMasterFilter
    search_fields = ("plant_id", "grade")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "plant_products_master"

    def upload_update(self, request, *args, **kwargs):
        response = super().upload_update(request, *args, **kwargs)
        background_update_vpc_history(response.data.get("data"), request.user.id)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        background_update_vpc_history(response.data, request.user.id)
        return Responses.success_response(
            "Plant product master updated.", response.status_code, response.data
        )


class PlantProductMasterDropdownView(GenericAPIView):
    """Options dropdown API for plant product master list."""

    queryset = PlantProductsMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("plant_id", "grade")

    def __get_plant_query(self, query_string):
        """Pass query string and get the dropdown data associated with
        string."""
        filter_kwargs = {}
        if query_string == "plant_id":
            filter_kwargs[f"{query_string}__startswith"] = "FG"
        return (
            self.filter_queryset(self.get_queryset())
            # .filter(**{f"{query_string}__startswith": "FG"})
            .filter(**filter_kwargs)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant_id": self.__get_plant_query("plant_id"),
            "grade": self.__get_plant_query("grade"),
        }
        return Responses.success_response(
            "Plant products master options dropdown.", data=data
        )


class PriceMasterViewSet(DownloadUploadViewSet):
    """Price master list view."""

    queryset = PriceMaster.objects.all().select_related("destination")
    serializer_class = PriceMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PriceMasterFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "price_master"
    sorting_fields = ("id",)


class ServiceLevelSlaViewSet(DownloadUploadViewSet):
    """Service level sla CRUDs view set class."""

    queryset = ServiceLevelSla.objects.all().select_related("destination")
    serializer_class = ServiceLevelSlaSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceLevelSlaFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "service_level_sla"
    sorting_fields = ("id",)

    def partial_update(self, request, *args, **kwargs):
        """Patch API"""
        request.data.pop("plant_id", None)
        return super().partial_update(request, *args, **kwargs)


class ServiceLevelSlaDropdownView(GenericAPIView):
    """Options dropdown API for service level sla list."""

    queryset = ServiceLevelSla.objects.all()

    def __get_service_level_sla_query(self, query_string, query=Q()):
        return (
            self.get_queryset()
            .filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_service_level_sla_query("destination__state"),
            "district": self.__get_service_level_sla_query(
                "destination__district",
                Q(destination__state=request.query_params.get("state")),
            ),
            "city": self.__get_service_level_sla_query(
                "destination__city",
                Q(
                    destination__state=request.query_params.get("state"),
                    destination__district=request.query_params.get("district"),
                ),
            ),
        }
        return Response(data=data, status=status.HTTP_200_OK)


class VehicleAvailabilityViewSet(DownloadUploadViewSet):
    """Vehicle availability CRUDs view set class."""

    queryset = VehicleAvailability.objects.all()
    serializer_class = VehicleAvailabilitySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VehicleAvailabilityFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "vehicle_availability"
    sorting_fields = ("id",)


class VehicleAvailabilityDropdownView(GenericAPIView):
    """Options dropdown API for vehicle availability list."""

    # helper = VehicleAvailabilityDropdownHelper

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

    def __get_vehicle_type(self, request):
        """Returns total distinct vehicle types present in db."""
        queryset = VehicleAvailability.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return (
            queryset.exclude(vehicle_type=None)
            .values_list("vehicle_type", flat=True)
            .annotate(Count("vehicle_type"))
        )

    def __get_vehicle_availability_query(self, query_string, request, query=Q()):
        queryset = VehicleAvailability.objects.all()
        user_email = request.user.email
        queryset = user_details(user_email, queryset)
        return (
            queryset.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get_dropdown_data(self, query_params, request):
        """Returns dropdown data for vehicle availability list."""
        return {
            "state": self.__get_vehicle_availability_query("state", request),
            "district": self.__get_vehicle_availability_query(
                "district", request, Q(state=query_params.get("state"))
            ),
            "city": self.__get_vehicle_availability_query(
                "city",
                request,
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
            "plant_id": self._get_plant_query("plant_id", request),
            "vehicle_type": self.__get_vehicle_type(request),
        }

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        return Responses.success_response(
            "Vehicle Availability options dropdown.",
            data=self.get_dropdown_data(request.query_params, request),
        )


class RouteRestrictionDropdownView(GenericAPIView):
    """Options dropdown API for route restriction list."""

    queryset = RouteRestrictions.objects.all()

    def get(self, request, *args, **kwargs):
        """Get options dropdown."""
        data = (
            self.get_queryset()
            .values_list("link_id", flat=True)
            .annotate(Count("link_id"))
        )
        return Responses.success_response("Links master options dropdown.", data=data)


class LpModelRunListView(ListAPIView):
    """Lp model run list view."""

    queryset = LpModelRun.objects.all()
    serializer_class = LpModelRunSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpModelRunFilter
    pagination_class = CustomPagination


class GdWarfhageRunListView(ListAPIView):
    """Gdmodel run list view."""

    queryset = GdWharfageRunInput.objects.all()
    serializer_class = GdWharfageRunInputserializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GdWharfageRunInputFilter
    pagination_class = CustomPagination


class LpModelDfFnlView(GenericAPIView):
    """View class to create entries in LpModelDfFnl"""

    serializer_class = LpModelDfFnlSerializer
    helper = LpModelRunViewHelper

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """Insert data into LPModelRun."""
        is_force = request.data.get("is_force", None)
        if is_force is True:
            pass
        else:
            if PriceMaster.objects.filter(price=0):
                return Responses.error_response("price not set here")
            else:
                pass

        constraints = request.data.get("constraints")
        model_run_data = {
            "user": 100,
            "run_type": "Constraint run" if constraints else "Free run",
            "run_status": "Running",
            "contribution": 0,
            "plan_date": request.data.get("plan_date"),
            "run_date": date.today(),
        }
        plan_date = request.data.get("plan_date")
        model_run_serializer = LpModelRunSerializer(data=model_run_data)
        model_run_serializer.is_valid(raise_exception=True)
        model_run_instance = model_run_serializer.save()
        try:
            cnxn = self.helper.cnxn
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        try:
            df = self.helper.get_model_inputs(cnxn)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        try:
            (
                ppm,
                dmnd_model,
                vehicle_avail,
                rake_charges,
                frt_trgt,
                fiscal_benefit,
                transit_depots,
                handling_charges,
                df_depot,
                df_packaging,
                sla,
                packer_constraint,
            ) = self.helper.get_model_constraints(cnxn, plan_date)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        ppm_plant = ppm.copy()
        try:
            df, dmnd, frt_trgt, dmnd_missing = self.helper.data_prep(
                df,
                ppm,
                dmnd_model,
                vehicle_avail,
                rake_charges,
                frt_trgt,
                fiscal_benefit,
                transit_depots,
                handling_charges,
                df_depot,
                df_packaging,
                sla,
                constraints,
                cnxn,
            )
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        try:
            dataframe, run_status, df_rank = self.helper.run_model(
                df, ppm, dmnd, frt_trgt, packer_constraint, constraints
            )
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        try:
            clinker_links, ppm = self.helper.get_clinker_inputs(cnxn)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        try:
            result_clinker = self.helper.run_clinker_model(
                clinker_links, ppm, dataframe
            )
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        result_clinker.columns = result_clinker.columns.str.lower()
        data = json.loads(result_clinker.to_json(orient="records"))
        print("data", data)

        dataframe.columns = dataframe.columns.str.lower()
        dataframe["route_changed"] = dataframe["route_changed"].replace(False, "0")
        dataframe["primary_frt"] = dataframe["primary_frt"].round(decimals=2)
        dataframe["ha_commission"] = dataframe["ha_commission"].round(decimals=2)
        dataframe["sp_commission"] = dataframe["sp_commission"].round(decimals=2)
        dataframe["secondary_frt"] = dataframe["secondary_frt"].round(decimals=2)
        dataframe["demurrage"] = dataframe["demurrage"].round(decimals=2)
        dataframe["damages"] = dataframe["damages"].round(decimals=2)
        dataframe["rake_charges"] = dataframe["rake_charges"].round(decimals=2)
        dataframe["isp_commission"] = dataframe["isp_commission"].round(decimals=2)
        dataframe["taxes"] = dataframe["taxes"].round(decimals=2)
        dataframe["contribution"] = dataframe["contribution"].round(decimals=2)
        dataframe["tlc"] = dataframe["tlc"].round(decimals=2)
        # dataframe["clinker_freight"] = dataframe["clinker_freight"].round(decimals=2)

        dataframe = dataframe.loc[:, ~dataframe.columns.duplicated()].copy()
        # if request.data.get("constraints") == []:
        #     pass
        # else:
        #     dataframe['scenario'] = cons_str
        # list_cons = request.data.get("constraints")
        # cons_str = ''
        # for i in list_cons:
        #     cons_str += i + ', '
        # cons_str.strip(',')
        # extracting excel based on the run _id

        writer = pd.ExcelWriter(
            # f"output/lp_output_{model_run_instance.run_id}.xlsx", engine="xlsxwriter"
            settings.LP_MODEL_RUN_FILE_PATH
            + f"lp_output_{model_run_instance.run_id}.xlsx",
            engine="xlsxwriter",
        )

        dataframe.to_excel(writer, sheet_name="Model Output", index=False)
        result_clinker.to_excel(writer, sheet_name="Model Output Clinker", index=False)
        df_rank.to_excel(writer, sheet_name="Rank", index=False)
        dmnd_missing.to_excel(writer, sheet_name="Demand Missed", index=False)
        if "service_level_sla" in constraints:
            sla.to_excel(writer, sheet_name="Constraint - Service Level", index=False)
        if "target_setting" in constraints:
            frt_trgt.to_excel(
                writer, sheet_name="Constraint - Freight Type", index=False
            )
        if "plant_min_capacity" in constraints:
            ppm_plant.to_excel(
                writer, sheet_name="Constraint - Plant Utilization", index=False
            )
        if "vehicle_availability" in constraints:
            vehicle_avail.to_excel(
                writer, sheet_name="Constraint - Vehicle", index=False
            )

        writer.save()
        writer.close()
        writer.handles = None

        clinker_demand_serializer = ClinkerDemandRunSerializer(
            data=data, context={"run_id": model_run_instance.run_id}, many=True
        )
        clinker_demand_serializer.is_valid(raise_exception=True)
        clinker_demand_serializer.save()

        dataframe = json.loads(dataframe.to_json(orient="records"))

        serializer = self.get_serializer(
            data=dataframe, context={"run_id": model_run_instance.run_id}, many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        model_run_instance.run_status = run_status
        model_run_instance.save()
        data = {
            "run_status": model_run_instance.run_status,
            "run_id": model_run_instance.run_id,
        }
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, data
        )


class LpModelDfFnlBaseListAPIView(ListAPIView):
    """LP Model Df Fnl base and listing API view."""

    queryset = LpModelDfFnl.objects.all()
    serializer_class = LpModelDfFnlSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpModelDfFnlFilter
    pagination_class = CustomPagination
    helper = LpModelOutputScreenViewHelper

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(run_id=self.kwargs.get("run_id"))
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        self.total_quantity = queryset.aggregate(total_qty=Sum("qty")).get("total_qty")
        return queryset


class RakeTransferDetails(LpModelDfFnlBaseListAPIView):
    """Rake transfer details api."""

    serializer_class = RakeTransferSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .values("node_city", "cust_category", "mode", "route_id", "plant_id")
            .annotate(total_qty=Sum("qty"))
            .order_by("-total_qty")
        )


# class OutputScreenDropdown(GenericAPIView):
#     """Dropdown API for lp model df fnl output screen."""

#     helper = OutputScreenDropdownHelper

#     def _get_plant_query(self, query_string, request):
#         """Pass query string and get the dropdown data associated with
#         string."""
#         queryset = PlantProductsMaster.objects.all()
#         user_email = request.user.email
#         queryset = user_details(user_email, queryset)
#         return (
#             queryset.values_list(query_string, flat=True)
#             .annotate(Count(query_string))
#             .order_by(query_string)
#         )

#     def __get_output_screen_query(self, query_string, request, query=Q()):
#         queryset = LpModelDfFnl.objects.all()
#         user_email = request.user.email
#         queryset = user_details(user_email, queryset)
#         return (
#             queryset.filter(query)
#             .values_list(query_string, flat=True)
#             .distinct(query_string)
#             .order_by(query_string)
#         )

#     def _get_dropdown_data(self, query_params, request):
#         """Returns LpModelDfFnl output screen dropdown data."""
#         return {
#             "destination_state": self.__get_output_screen_query(
#                 "destination_state", request
#             ),
#             "destination_district": self.__get_output_screen_query(
#                 "destination_district",
#                 request,
#                 Q(destination_state=query_params.get("destination_state")),
#             ),
#             "destination_city": self.__get_output_screen_query(
#                 "destination_city",
#                 request,
#                 Q(
#                     destination_state=query_params.get("destination_state"),
#                     destination_district=query_params.get("destination_district"),
#                 ),
#             ),
#             "plant": self._get_plant_query("plant_id", request),
#             "mode": ["RAIL", "ROAD"],
#             # "city": self.__get_df_fnl_output_dropdown_data("destination_city"),
#             # "state": self.__get_df_fnl_output_dropdown_data("destination_state"),
#             # "district": self.__get_df_fnl_output_dropdown_data("destination_district"),
#             "primary_secondary_route": ["PRIMARY", "SECONDARY"],
#             "brand": self.__get_df_fnl_output_dropdown_data("brand", request),
#             "grade": self.__get_df_fnl_output_dropdown_data("grade", request),
#         }

#     def __get_df_fnl_output_dropdown_data(self, query_param, request):
#         queryset = LpModelDfFnl.objects.all()
#         user_email = request.user.email
#         queryset = user_details(user_email, queryset)
#         return queryset.values_list(query_param, flat=True).annotate(Count(query_param))

#     def get(self, request, *args, **kwargs):
#         """Get API"""
#         return Responses.success_response(
#             "Output screen filter drop down.",
#             data=self.helper._get_dropdown_data(request.query_params),
#         )


class OutputScreenDropdown(GenericAPIView):
    """Dropdown API for lp model df fnl output screen."""

    helper = OutputScreenDropdownHelper

    def _get_data(self, request):
        """Fetch data needed for dropdowns."""
        user_email = request.user.email

        # Fetch Plant Products Master data
        plant_queryset = user_details(user_email, PlantProductsMaster.objects.all())
        plant_data = (
            plant_queryset.values_list("plant_id", flat=True)
            .annotate(Count("plant_id"))
            .order_by("plant_id")
        )

        # Fetch Lp Model Df Fnl data
        lp_model_queryset = LpModelDfFnl.objects.all()
        brand_data = lp_model_queryset.values_list("brand", flat=True).annotate(
            Count("brand")
        )
        grade_data = lp_model_queryset.values_list("grade", flat=True).annotate(
            Count("grade")
        )

        return {
            "plant_data": plant_data,
            "brand_data": brand_data,
            "grade_data": grade_data,
        }

    def _get_output_screen_query(self, query_string, request, query=Q()):
        lp_model_queryset = LpModelDfFnl.objects.all()
        return (
            lp_model_queryset.filter(query)
            .values_list(query_string, flat=True)
            .distinct(query_string)
            .order_by(query_string)
        )

    def _get_dropdown_data(self, query_params, request):
        """Generate dropdown data."""
        data = self._get_data(request)

        return {
            "plant": data["plant_data"],
            "mode": ["RAIL", "ROAD"],
            # "city": self._get_df_fnl_output_dropdown_data("destination_city"),
            # "state": self._get_df_fnl_output_dropdown_data("destination_state"),
            # "district": self._get_df_fnl_output_dropdown_data("destination_district"),
            "primary_secondary_route": ["PRIMARY", "SECONDARY"],
            "brand": data["brand_data"],
            "grade": data["grade_data"],
            "destination_state": self._get_output_screen_query(
                "destination_state", request
            ),
            "destination_district": self._get_output_screen_query(
                "destination_district",
                request,
                Q(destination_state=query_params.get("destination_state")),
            ),
            "destination_city": self._get_output_screen_query(
                "destination_city",
                request,
                Q(
                    destination_state=query_params.get("destination_state"),
                    destination_district=query_params.get("destination_district"),
                ),
            ),
        }

    def get(self, request, *args, **kwargs):
        """Get API"""
        return Responses.success_response(
            "Output screen filter dropdown.",
            data=self._get_dropdown_data(request.query_params, request),
        )


class RoadVsRakeView(LpModelDfFnlBaseListAPIView):
    """Road Vs Rake LP Model output screen pie chart API view."""

    def get(self, request, *args, **kwargs):
        """Get Road and Rake comparison data."""
        filtered_data = self.filter_queryset(self.get_queryset())
        data = self.helper.get_road_vs_rake_data(filtered_data, self.total_quantity)
        return Responses.success_response("Road Vs Rake Data.", data=data)


class DispatchAPIView(LpModelDfFnlBaseListAPIView):
    """Dispatches LP Model output screen pie chart API view."""

    def get(self, request, *args, **kwargs):
        """Get direct and indirect dispatch data."""
        filtered_data = self.filter_queryset(self.get_queryset())
        data = self.helper.get_dispatches_data(filtered_data, self.total_quantity)
        return Responses.success_response("Dispatches Data.", data=data)


class FreightBasedQuantity(LpModelDfFnlBaseListAPIView):
    """LpModelDfFnl quantity data based on freight type."""

    def get(self, request, *args, **kwargs):
        """Get Quantity breakup data based on freight type."""
        filtered_data = self.filter_queryset(self.get_queryset())
        data = self.helper.get_freight_based_quantity(
            filtered_data, self.total_quantity
        )
        return Responses.success_response(
            "Quantity data based on freight type.", data=data
        )


class TLCBreakupView(LpModelDfFnlBaseListAPIView):
    """API view class for TLC Breakup data."""

    def get(self, request, *args, **kwargs):
        """Get TLC Breakup data."""

        data = self.helper.get_tlc_breakup_data(self)
        return Responses.success_response("TLC breakup data.", data=data)


class ExportToExcelView(LpModelDfFnlBaseListAPIView):
    """Export lp model df fnl dataset to excel sheet."""

    def get(self, request, *args, **kwargs):
        """API to export data to excel sheet."""
        run_id = kwargs.get("run_id")
        if LpModelRun.objects.filter(run_id=run_id).exists():
            with open(
                f"analytical_data/files/monthly_scheduling/run_model_output/lp_output_{run_id}.xlsx",
                "rb",
            ) as excel:
                workbook = excel.read()

            content_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response = HttpResponse(workbook, content_type=content_type)
            response[
                "Content-Disposition"
            ] = f"attachment; filename=lp_output_{run_id}.xlsx"

            return response

        return Responses.error_response("No runs found for given run_id.")


class PlantDispatchPlan(LpModelDfFnlBaseListAPIView):
    """Plant and grade wise quantity and capacity sum."""

    serializer_class = PlantDispatchPlanSerializer

    def get(self, request, *args, **kwargs):
        """Get quantity dispatched utilization data."""
        queryset = self.filter_queryset(self.get_queryset())
        data = self.helper.get_plant_dispatch_data(queryset)
        serializer = self.get_serializer(data, many=True)
        return Responses.success_response(
            "Plant dispatch plan data.", data=serializer.data
        )


class PlantDispatchPlanAnalysis(LpModelDfFnlBaseListAPIView):
    """Plant dispatch plan analysis output screen view."""

    serializer_class = PlantDispatchPlanSerializer

    def get(self, request, *args, **kwargs):
        """Get plant dispatch plan scenario analysis data associated with
        two run ids."""
        queryset1 = self.filter_queryset(
            LpModelDfFnl.objects.filter(run_id=self.kwargs.get("run_id1"))
        )
        queryset2 = self.filter_queryset(
            LpModelDfFnl.objects.filter(run_id=self.kwargs.get("run_id2"))
        )

        data1 = self.helper.get_plant_dispatch_data(queryset1)
        data2 = self.helper.get_plant_dispatch_data(queryset2)

        serializer1 = self.get_serializer(data1, many=True)
        serializer2 = self.get_serializer(data2, many=True)

        data = {"output1": serializer1.data, "output2": serializer2.data}
        return Responses.success_response(
            "Plant dispatch plan analysis data.", data=data
        )


# class ClinkerALlocation(LpModelDfFnlBaseListAPIView):
#     """Clinker Allocation api for output screen."""

#     serializer_class = ClinkerALlocationSerializer

#     def get(self, request, *args, **kwargs):
#         """Get API"""
#         queryset = self.filter_queryset(self.get_queryset())
#         data = self.helper.get_clinker_allocation_data(queryset)
#         serializer = self.get_serializer(data, many=True)
#         return Responses.success_response(
#             "Clinker allocation data.", data=serializer.data
#         )


class LpModelDfFnlScenarioAnalysisView(GenericAPIView):
    """Lp model df fnl scenario analysis"""

    pagination_class = CustomPagination
    helper = LpModelScenarioAnalysisHelper

    def get(self, request, *args, **kwargs):
        """Export data to excel."""
        queryset1 = LpModelDfFnl.objects.filter(
            run_id=request.query_params.get("run_id_1")
        ).values()
        queryset2 = LpModelDfFnl.objects.filter(
            run_id=request.query_params.get("run_id_2")
        ).values()

        run_id_1_data = pd.DataFrame(list(queryset1))[:25]
        run_id_1_data.columns = run_id_1_data.columns.str.upper()
        run_id_2_data = pd.DataFrame(list(queryset2))[:25]
        run_id_2_data.columns = run_id_2_data.columns.str.upper()

        try:
            data = self.helper.get_output_data(run_id_1_data, run_id_2_data)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        data = json.loads(data.to_json(orient="records"))
        request.session["scenario_analysis_data"] = data

        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)


class LpModelScenarioAnalysisExportView(GenericAPIView):
    """Export LpModelDfFnl scenario analysis data."""

    helper = LpModelScenarioAnalysisHelper

    def get(self, request, *args, **kwargs):
        """Export data to excel."""
        dataframe = pd.read_json(json.dumps(request.session["scenario_analysis_data"]))
        data = dump_to_excel(dataframe, "scenario_analysis")
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(data, content_type=content_type)
        response["Content-Disposition"] = "attachment; filename=scenario_analysis.xlsx"
        return response


class CLinkerLinksMasterViewSet(DownloadUploadViewSet):
    """View set class for clinker links master."""

    queryset = ClinkerLinksMaster.objects.all()
    serializer_class = ClinkerLinksMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClinkerLinksMasterFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "clinker_links_master"
    sorting_fields = ("id",)


class ClinkerLinksMasterDropDownView(GenericAPIView):
    """Clinker links master filters dropdown."""

    queryset = ClinkerLinksMaster.objects.all()

    def get(self, request, *args, **kwargs):
        """Get dropdown data."""
        data = {
            "fg_whse": self.get_queryset()
            .values_list("fg_whse", flat=True)
            .annotate(Count("fg_whse")),
            "fc_whse": self.get_queryset()
            .values_list("fc_whse", flat=True)
            .annotate(Count("fg_whse")),
            "mode_of_transport": ["ROAD", "RAIL"],
        }
        return Responses.success_response(
            "Clinker links master filters dropdown data.", data=data
        )


class DjpCounterScoreViewSet(ListAPIView):
    """View set class for djp counter score."""

    queryset = DjpCounterScore.objects.all()
    serializer_class = DjpCounterScoreSerializer
    pagination_class = CustomPagination
    lookup_field = "id"


class DjpRouteScoreViewSet(ListAPIView):
    """View set class for djp route score."""

    queryset = DjpRouteScore.objects.all()
    serializer_class = DjpRouteScoreSerializer
    pagination_class = CustomPagination
    lookup_field = "id"


class DjpRunViewSet(ListAPIView):
    """View set class for djp run."""

    queryset = DjpRun.objects.all().prefetch_related(
        "djp_route_score", "djp_counter_score"
    )
    serializer_class = DjpRunSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DjpRunFilter


class RouteUpdateView(APIView):
    """Route update third party api calling view class."""

    def post(self, request, *args, **kwargs):
        """Post API"""
        response = requests.post(
            "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/SCL_ROUTE_UPDATE/Routeupdate/",
            json=request.data,
        )
        response_data = json.loads(response._content.decode())
        return Responses.success_response(
            response_data.get("P_ERROR_CODE"),
            data=response_data.get("P_ERROR_MESSAGE"),
        )


class DeliveryCreationView(APIView):
    """Delivery creation third party api calling view class."""

    def post(self, request, *args, **kwargs):
        """Post API"""
        response = requests.post(
            "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/DICreation/Delivery_SLCT",
            json=request.data,
        )

        response_data = json.loads(response._content.decode())
        if response_data.get("STATUS") == "E":
            return Responses.success_response(
                response_data.pop("STATUS"),
                data=response_data,
            )
        di_dtl = LpSchedulingDiDetails(
            **{
                "order_master": LpSchedulingOrderMaster.objects.filter(
                    order_id=request.data.get("data", {}).get("SALES_ORDER_NUMBER")
                ).first(),
                "di_number": response_data.get("DELIVERY_ID"),
                "remarks": request.data.get("data", {}).get("REMARKS"),
                "di_quantity": request.data.get("data", {}).get("_DELIVERY_QUANTITY"),
                "order_line_id": request.data.get("data", {}).get("LINE_ID"),
                "order_id": request.data.get("data", {}).get("SALES_ORDER_NUMBER"),
            }
        )
        di_dtl.save()
        lp_scheduling_ids = LpSchedulingOrderMaster.objects.filter(
            order_line_id=request.data.get("data", {}).get("LINE_ID")
        )
        for lp_id in lp_scheduling_ids:
            lp_id.order_status = "DI GENERATED"
            lp_id.save()

        return Responses.success_response(
            response_data.pop("STATUS"),
            data=response_data,
        )


class PpCallView(APIView):
    """PP Call third party api calling view class."""

    def post(self, request, *args, **kwargs):
        """Post API"""
        # try:
        #     emp_code = TgtRlsRoleData.objects.get(email=request.user.email)
        #     request.data["USERNAME"] = str(emp_code.emp_id)
        # except Exception as e:
        #     return Responses.error_response(
        #         "cannot find the employee code or some issue arrise", data=e
        #     )
        # try:
        #     tl_code = PpOrderTagging.objects.get(token_no=request.data["TOKEN_ID"])
        #     request.data["TL_NO"] = tl_code.tl_code
        # except Exception as e:
        #     return Responses.error_response(
        #         "cannot find the tl_code or some issue arrise", data=e
        #     )

        response = requests.post(
            "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/PPCall/PPCall",
            json=request.data,
        )
        response_data = json.loads(response._content.decode())

        if response_data["STATUS"] == "S":
            lp_scheduling_ids = LpSchedulingOrderMaster.objects.filter(
                token_id=request.data["data"]["TOKEN_ID"]
            )
            for lp_id in lp_scheduling_ids:
                lp_id.pp_call = True
                lp_id.order_executable = True
                lp_id.save()

        return Responses.success_response(
            response_data.pop("STATUS"),
            data=response_data,
        )


class OrderUpdateView(APIView):
    """Order Update third party api calling view class."""

    def post(self, request, *args, **kwargs):
        response = requests.post(
            "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/OrderUpdate/OrderUpdate/",
            json=request.data,
        )
        print("orderupdatejson", response)
        response_data = json.loads(response._content.decode())
        return Responses.success_response(
            response_data.pop("STATUS"),
            data=response_data,
        )


class LpTargetSettingView(DownloadUploadViewSet):
    """LpTargetSetting listing view class."""

    queryset = LpTargetSetting.objects.all()
    serializer_class = LpTargetSettingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LpTargetSettingFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "target_settings"
    sorting_fields = ("id",)


class LpTargetSettingsDropdownViewSet(ModelViewSet):
    """LpTargetSetting district, state list view."""

    def __get_target_settings_query(self, query_string, query=Q()):
        return (
            LpTargetSetting.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_target_settings_query("state"),
            "district": self.__get_target_settings_query(
                "district",
                Q(state=request.query_params.get("state")),
            ),
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ClinkerDemandRunView(ListAPIView):
    """Clinker demand run listing view class."""

    queryset = ClinkerDemandRun.objects.all()
    serializer_class = ClinkerDemandRunSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClinkerDemandRunFilter
    # pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Responses.success_response("Lp target setting data.", data=response.data)


class ClinkerALlocationAnalysis(ClinkerDemandRunView):
    """Clinker allocation analysis output screen view."""

    def get(self, request, *args, **kwargs):
        """Get clinker allocation scenario analysis data associated with
        two run ids."""
        queryset1 = self.filter_queryset(
            self.get_queryset().filter(run=self.kwargs.get("run_id1"))
        )
        queryset2 = self.filter_queryset(
            self.get_queryset().filter(run=self.kwargs.get("run_id2"))
        )

        serializer1 = self.get_serializer(queryset1, many=True)
        serializer2 = self.get_serializer(queryset2, many=True)

        data = {"output1": serializer1.data, "output2": serializer2.data}
        return Responses.success_response(
            "Clinker allocation analysis data.", data=data
        )


class RailHandlingView(DownloadUploadViewSet):
    """Rail handling listing view class."""

    queryset = RailHandling.objects.all()
    serializer_class = RailHandlingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RailHandlingFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "handling"
    sorting_fields = ("id",)

    def read_file_get_json(self, file):
        try:
            df = pd.read_excel(file.read())
            df.columns = df.columns.str.lower()
            df = df.drop(self.auto_generated_fields, axis=1, errors="ignore")
            df = df.round(decimals=2)
            if "ha_commission" in df.columns:
                df["ha_commission"] = round(df["ha_commission"], 0).astype("int")
            for column in df.columns:
                if df[column].dtype == "datetime64[ns]":
                    df[column] = df[column].astype(str)
        except Exception as e:
            log.error("FileError: %s", e)
            return Responses.error_response("FileError: Unable to read file.")
        return json.loads(df.to_json(orient="records"))


class RailHandlingDownView(GenericAPIView):
    """Rail handling dropdown api."""

    # helper = RailHandlingDropdownHelper
    queryset = RailHandling.objects.all()

    def __get_rail_handling_query(self, query_string, query=Q()):
        return (
            self.get_queryset()
            .filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def _get_dropdown_data(self, query_params):
        """Returns dropdown data for Rail Handling list."""
        return {
            "state": self.__get_rail_handling_query("state"),
            "district": self.__get_rail_handling_query(
                "district", Q(state=query_params.get("state"))
            ),
            "taluka": self.__get_rail_handling_query(
                "taluka",
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
            "freight_type": self.__get_rail_handling_query("freight_type"),
        }

    def get(self, request, *args, **kwargs):
        """Get api."""
        return Responses.success_response(
            "Rail handling dropdown.",
            data=self._get_dropdown_data(request.query_params),
        )


class LpModelRunUpdate(APIView):
    def insert_into_database(self, cnxn, df, table):
        cols_dt = df.select_dtypes("datetime64").columns.tolist()

        for col_dt in cols_dt:
            df[col_dt] = df[col_dt].apply(lambda x: x.strftime("%Y-%m-%d"))

        df.columns = df.columns.str.upper()
        df = df.drop(
            [
                "IS_EX",
                "JHJU_RAIL_DISCOUNT",
                "SP_COMMISSION",
                "TAXES",
                "INDEX",
                "PACKAGING_COST",
                "FISCAL_BENEFIT",
                "CLINKER_CF",
                "ROUTE_CHANGED",
                "MISC_CHARGES",
                "VARIABLES",
                "DISCOUNT",
                "AVG_TIME",
                "PRICE",
                "ISP_COMMISSION",
            ],
            axis=1,
            errors="ignore",
        )
        df = df.to_dict("split")
        val = ",".join(str(tuple(i)) for i in df["data"])
        col = ",".join(f'"{i}"' for i in df["columns"])
        sql = f"""Insert into etl_zone."{table}" ({col}) values{val}"""
        sql = sql.replace("None", "NULL")
        sql = sql.replace("nan", "NULL")

        crsr = cnxn.cursor()
        crsr.execute(sql)
        cnxn.commit()
        return

    def patch(self, request):
        run_id = request.data.get("run_id")
        data_object = LpModelRun.objects.filter(run_id=run_id).first()
        serializer = LpModelRunSerializer(data_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        df = pd.read_excel(
            settings.LP_MODEL_RUN_FILE_PATH + f"lp_output_{run_id}.xlsx",
            sheet_name="Rank",
        )
        df.columns = df.columns.str.lower()
        df = df.loc[:, ~df.columns.duplicated()].copy()
        df = df.round(decimals=2).fillna(0)
        df["run_id"] = request.data.get("run_id")
        decimal_columns = [
            "route_id",
            "route_id_secondary",
            "from_city_id",
            "node_city_id",
            "to_city_id",
            "brand",
            "rank",
            "rake_charges",
        ]
        df[decimal_columns] = df[decimal_columns].astype(int)

        data = json.loads(df.to_json(orient="records"))
        model_rank_ser = LpModelDfRankCreateSerializer(data=data, many=True)
        model_rank_ser.is_valid(raise_exception=True)

        self.insert_into_database(connect_db(), df, "LP_MODEL_DF_RANK")
        return Responses.success_response("data updated.", data=serializer.data)


class LpMinCapacityViewSet(ModelViewSet):
    """View set class for lp min capacity"""

    queryset = LpMinCapacity.objects.all()
    serializer_class = LpMinCapacitySerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"


class GetCLinkerDemandRunDataViewSet(GenericAPIView):
    """Lp scheduling order master data listing."""

    queryset = ClinkerDemandRun.objects.all()
    serializer_class = GetClinkerDemandRunDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClinkerDemandRunFilter

    def get(self, request, *args, **kwargs):
        date = datetime.strptime((request.query_params.get("date")), "%Y-%m-%d")
        month = date.month
        year = date.year
        active_run_ids = (
            LpModelRun.objects.filter(
                plan_date__month=month, plan_date__year=year, approve_status=1
            )
            .values_list("run_id", flat=True)
            .annotate(Count("run_id"))
        )

        clinker_demand_run_data = self.filter_queryset(
            self.get_queryset().filter(run__run_id__in=list(active_run_ids))
        ).annotate(
            plant_id_1=Case(
                When(
                    plant_id__startswith="FG",
                    then=PrefixConversion("RM", F("plant_id"), 3),
                )
            )
        )

        serializer = self.get_serializer(clinker_demand_run_data, many=True)
        return Responses.success_response(
            "demand run data fetched successfully", data=serializer.data
        )


class ClinkerDispatchGUPlantDropdown(ListAPIView):
    queryset = TgtPlantLookup.objects.all()
    serializer_class = TgtPlantLookupSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TgtPlantLookupFilter

    # below requirement changed by lakshya.
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset().filter(
    #         Q(name__startswith="FC") | Q(name__startswith="RM")
    #     ).annotate(plant_name=Substr("name", 1, 3)).values("plant_name")
    # return Responses.success_response(
    #     "plant dropdown fetched successfully", data=queryset
    # )

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Responses.success_response(
            "plant dropdown fetched successfully",
            data=serializer.data,
        )


class MonthlyNthBudget(ListAPIView):
    """Monthly projected budget."""

    queryset = Demand.objects.values("month__month", "month__year").annotate(
        Count("month__month"),
        Count("month__year"),
        monthly_budget=ExpressionWrapper(
            Sum("demand_qty") * 1.2, output_field=DecimalField()
        ),
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("destination__state",)

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Monthly nth budget data.", data=self.filter_queryset(self.get_queryset())
        )


class SampleDownloadView(APIView):
    def get(self, request, format=None):
        extension = ".xlsx"
        file_path = request.query_params.get("url")
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/ms-excel")
            response["Content-Disposition"] = "attachment; filename={}{}".format(
                "sample_file", extension
            )

        return response


class TOebsSclAddressLinkDropdown(GenericAPIView):
    queryset = TOebsSclAddressLink.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "city", "region", "taluka")

    def __get_address_link_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_address_link_dropdown_query("state"),
            "city": self.__get_address_link_dropdown_query("city"),
            "district": self.__get_address_link_dropdown_query("district"),
            "region": self.__get_address_link_dropdown_query("region"),
            "taluka": self.__get_address_link_dropdown_query("taluka"),
        }
        return Responses.success_response(
            "toebs scl address link dropdown data.", data=data
        )


class VpcHistoricalPlantDropdown(GenericAPIView):
    queryset = TOebsHrAllOrganizationUnits.objects.all()

    def get(self, request):
        plant_dropdown = (
            self.get_queryset()
            .filter(Q(name__startswith="FG"))
            .values_list("name", flat=True)
            .distinct()
        )

        return Responses.success_response(
            "plant dropdown fetched successfully", data=plant_dropdown
        )


class SidingCodeMappingDropdown(GenericAPIView):
    queryset = SidingCodeMapping.objects.filter(rake_point_type="Plant")
    filter_backends = (DjangoFilterBackend,)

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "siding code mapping dropdown",
            data=(
                self.filter_queryset(self.get_queryset())
                .values(
                    "rake_point",
                    "rake_point_code",
                )
                .distinct()
                .order_by("rake_point", "rake_point_code")
            ),
        )


class RakeTypesDropdown(GenericAPIView):
    queryset = RakeTypes.objects.all()
    filter_backends = (DjangoFilterBackend,)

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "rake type dropdown",
            data=(
                self.filter_queryset(self.get_queryset())
                .values_list("rake_types", flat=True)
                .distinct()
                .order_by("rake_types")
            ),
        )
