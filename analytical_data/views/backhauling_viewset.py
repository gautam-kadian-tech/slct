import json

from django.db import transaction
from django.db.models import Count, Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import (
    BackhaulingInboundTruckFilter,
    BackhaulingOpportunitiesFilter,
)
from analytical_data.models.backhauling_models import (
    BackhaulingInboundTruck,
    BackhaulingOpportunities,
)
from analytical_data.serializers.backhauling_serializers import (
    BackhaulingInboundTruckSerializer,
    BackhaulingOpportunitiesModelRunSerializer,
    BackhaulingOpportunitiesSerializer,
)
from analytical_data.utils import CustomPagination, Responses
from analytical_data.view_helpers import BackHaulingViewHelper, connect_db
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class BackhaulingOpportunitiesViewSet(ModelViewSet):
    queryset = BackhaulingOpportunities.objects.all()
    serializer_class = BackhaulingOpportunitiesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BackhaulingOpportunitiesFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class BackhaulingOpportunitiesDropdown(ModelViewSet):
    queryset = BackhaulingOpportunities.objects.all()
    serializer_class = BackhaulingOpportunitiesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BackhaulingOpportunitiesFilter

    def __get_backhauling_opportunities_dropdown_query(self, query_string, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(query)
            .values_list(query_string, flat=True)
            .distinct()
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "club_id": self.__get_backhauling_opportunities_dropdown_query(
                "club_id", Q(club_id__isnull=False)
            ),
            "order_master_id": self.__get_backhauling_opportunities_dropdown_query(
                "order_master__id", Q(order_master__id__isnull=False)
            ),
            "truck_number": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__truck_number", Q(inbound__truck_number__isnull=False)
            ),
            "vehicle_type": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__vehicle_type", Q(inbound__vehicle_type__isnull=False)
            ),
            "vehicle_size": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__vehicle_size", Q(inbound__vehicle_size__isnull=False)
            ),
            "plant_id": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__plant_id", Q(inbound__plant_id__isnull=False)
            ),
            "departure_date": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__departure_date__date",
                Q(inbound__departure_date__date__isnull=False),
            ),
            "destination_state": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__destination_state",
                Q(inbound__destination_state__isnull=False),
            ),
            "destination_district": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__destination_district",
                Q(inbound__destination_district__isnull=False),
            ),
            "destination_city": self.__get_backhauling_opportunities_dropdown_query(
                "inbound__destination_city", Q(inbound__destination_city__isnull=False)
            ),
        }
        return Responses.success_response(
            "backhauling opportunities dropdown", data=data
        )


class BackhaulingOpportunitiesCardsViewSet(GenericAPIView):
    queryset = BackhaulingOpportunities.objects.filter(status=True)
    # serializer_class = BackhaulingOpportunitiesSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = BackhaulingOpportunitiesFilter

    def get(self, request):
        first_card = (self.get_queryset()).values().count()
        second_card = (
            (self.get_queryset())
            .values("order_master__order_quantity")
            .annotate(
                order_master__order_quantity_sum=Sum("order_master__order_quantity")
            )
            .values("order_master__order_quantity_sum")
        )
        third_card = (
            (self.get_queryset()).values("inbound__truck_number").distinct()
        ).count()
        data_dict = {
            "first_card": first_card,
            "second_card": second_card,
            "third_card": third_card,
        }
        return Responses.success_response(
            "backhauling opportunities card data", data=data_dict
        )


class BackhaulingInboundTruckViewSet(DownloadUploadViewSet):
    queryset = BackhaulingInboundTruck.objects.all()
    serializer_class = BackhaulingInboundTruckSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BackhaulingInboundTruckFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "backhauling_inbound_truck"


class BackhaulingInboundTruckDropdown(ModelViewSet):
    queryset = BackhaulingInboundTruck.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BackhaulingInboundTruckFilter

    def __get_backhauling_inbound_truck_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant_id": self.__get_backhauling_inbound_truck_query("plant_id"),
            "truck_number": self.__get_backhauling_inbound_truck_query("truck_number"),
            "arrival_date": self.__get_backhauling_inbound_truck_query("arrival_date"),
            "departure_date": self.__get_backhauling_inbound_truck_query(
                "departure_date"
            ),
            "vehicle_type": self.__get_backhauling_inbound_truck_query("vehicle_type"),
            "vehicle_size": self.__get_backhauling_inbound_truck_query("vehicle_size"),
            "destination_state": self.__get_backhauling_inbound_truck_query(
                "destination_state"
            ),
            "destination_district": self.__get_backhauling_inbound_truck_query(
                "destination_district"
            ),
            "destination_city": self.__get_backhauling_inbound_truck_query(
                "destination_city"
            ),
        }
        return Responses.success_response(
            "backhauling-inbound-truck-dropdown", data=data
        )


class BackhaulingRunView(GenericAPIView):
    serializer_class = BackhaulingOpportunitiesModelRunSerializer
    helper = BackHaulingViewHelper

    @transaction.atomic()
    def post(self, request):
        cnxn = connect_db()
        backhauling_df_fnl = self.helper.run_model(cnxn)
        backhauling_df_fnl.columns = backhauling_df_fnl.columns.str.lower()
        backhauling_df_fnl_data = json.loads(
            backhauling_df_fnl.to_json(orient="records")
        )

        backhauling_df_fnl_serializer = BackhaulingOpportunitiesModelRunSerializer(
            data=backhauling_df_fnl_data,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        backhauling_df_fnl_serializer.is_valid(raise_exception=True)
        backhauling_df_fnl_serializer.save()
        return Responses.success_response(" backhauling model run sucessfully", data=[])
