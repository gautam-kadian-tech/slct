import json
from datetime import datetime
from datetime import datetime as dt

import pandas as pd
from django.db import transaction
from django.db.models import Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils import CustomPagination, Responses
from analytical_data.view_helpers import PricingHelper
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class CompetitionPriceNewMarketsDownloadUploadViewSet(DownloadUploadViewSet):
    """competition price new market view download"""

    queryset = CompetitionPriceNewMarkets.objects.all()
    serializer_class = CompetitionPriceNewMarketsDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompetitionPriceNewMarketsFilter
    pagination_class = CustomPagination
    sorting_fields = ("id",)
    file_name = "Competition_price_new_market"


class CompetitionPriceNewMarketsViewSet(ModelViewSet):
    """competition price new market viewset"""

    queryset = CompetitionPriceNewMarkets.objects.all()
    serializer_class = CompetitionPriceNewMarketsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompetitionPriceNewMarketsFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class PriceBenchmarksDownloadUploadViewSet(DownloadUploadViewSet):
    """price benchmark view download api"""

    queryset = PriceBenchmarks.objects.all()
    serializer_class = PriceBenchmarksDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PriceBenchmarksFilter
    pagination_class = CustomPagination
    file_name = "Price_Benchmarks_data"
    sorting_fields = ("id",)


class NewPriceComputationViewSet(ModelViewSet):
    queryset = NewPriceComputation.objects.filter(active="Y").order_by("district")
    serializer_class = NewPriceComputationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NewPriceComputationFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        dataset = request.data
        dataset["created_by"] = request.user.id
        dataset["last_updated_by"] = request.user.id
        dataset["last_update_login"] = request.user.id
        new_price_comp_serializer = NewPriceComputationSerializer(data=dataset)
        if not new_price_comp_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=new_price_comp_serializer.errors
            )
        new_price_comp_serializer.save()
        new_price_comp_data = new_price_comp_serializer.data
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, new_price_comp_data
        )

    def update(self, request):
        computation_obj = NewPriceComputation.objects.get(id=request.data["id"])
        if computation_obj:
            dict = {
                "status": "APPROVED",
                "created_by": computation_obj.created_by,
                "last_update_login": computation_obj.last_update_login,
                "last_updated_by": computation_obj.last_updated_by,
            }
            slct_annual_disc_target = NewPriceComputationSerializer(
                computation_obj, data=dict
            )
            if not slct_annual_disc_target.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Updation error",
                    data=slct_annual_disc_target.errors,
                )
            computation_obj = slct_annual_disc_target.save()
        data_list = NewPriceComputation.objects.filter(
            ~Q(status="APPROVED"),
            zone=computation_obj.zone,
            state=computation_obj.state,
            region=computation_obj.region,
            district=computation_obj.district,
            grade=computation_obj.grade,
            business_segment=computation_obj.business_segment,
            date=computation_obj.date,
            active="Y",
        ).values("id", "status")
        if data_list:
            for data in data_list:
                data["status"] = "REJECTED"
                data["created_by"] = request.user.id
                data["last_update_login"] = request.user.id
                data["last_updated_by"] = request.user.id
                computation_obj = NewPriceComputation.objects.get(id=data["id"])
                slct_annual_disc_target = NewPriceComputationSerializer(
                    computation_obj, data=data
                )
                if not slct_annual_disc_target.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "Updation error",
                        data=slct_annual_disc_target.errors,
                    )
                computation_obj = slct_annual_disc_target.save()
        return Responses.success_response(
            "price computation updated successfully", data=slct_annual_disc_target.data
        )


class NewPriceComputationGetBenchmarkViewSet(APIView):
    def get(self, request, *args, **kwargs):
        zone = request.query_params.get("zone")
        state = request.query_params.get("state")
        district = request.query_params.get("district")
        region = request.query_params.get("region")
        month = datetime.today().month
        year = datetime.today().year
        try:
            benchmark_data = (
                PriceBenchmarks.objects.filter(
                    zone=zone,
                    state=state,
                    district=district,
                    month__month=month,
                    month__year=year,
                )
                .values("benchmark_name", "price_difference_to_be_maintained")
                .latest("month")
            )
            difference = benchmark_data["price_difference_to_be_maintained"]
            benchmark = benchmark_data["benchmark_name"]

            try:
                new_market_data = (
                    CompetitionPriceNewMarkets.objects.filter(
                        zone=zone,
                        state=state,
                        district=district,
                        brand=benchmark_data["benchmark_name"],
                        price="WSP",
                        region=region,
                        date__month=month,
                        date__year=year,
                    )
                    .values("brand", "value")
                    .latest("date")
                )

                price = new_market_data["value"]
                recommended_price = new_market_data["value"] + difference
            except CompetitionPriceNewMarkets.DoesNotExist:
                price = None
                recommended_price = None
        except PriceBenchmarks.DoesNotExist:
            price = None
            recommended_price = None
            benchmark = None
            difference = None

        data = {
            "benchmark": benchmark,
            "price": price,
            "difference": difference,
            "recommended_price": recommended_price,
        }
        return Responses.success_response("price computation benchmark data", data=data)


class CompetitionPriceNewMarketsDropdown(GenericAPIView):
    queryset = CompetitionPriceNewMarkets.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = (
        "zone",
        "state",
        "district",
        "region",
        "brand",
        "business_segment",
        "grade",
    )

    def __get_competition_price_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_competition_price_dropdown_query("zone"),
            "state": self.__get_competition_price_dropdown_query("state"),
            "district": self.__get_competition_price_dropdown_query("district"),
            "region": self.__get_competition_price_dropdown_query("region"),
            "brand": self.__get_competition_price_dropdown_query("brand"),
            "business_segment": self.__get_competition_price_dropdown_query(
                "business_segment"
            ),
            "grade": self.__get_competition_price_dropdown_query("grade"),
        }
        return Responses.success_response(
            "competition price new market dropdown", data=data
        )


class PriceBenchmarksDropdown(GenericAPIView):
    queryset = PriceBenchmarks.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("zone", "state", "district", "benchmark_name")

    def __get_price_benchmark_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_price_benchmark_dropdown_query("zone"),
            "state": self.__get_price_benchmark_dropdown_query("state"),
            "benchmark_name": self.__get_price_benchmark_dropdown_query(
                "benchmark_name"
            ),
            "district": self.__get_price_benchmark_dropdown_query("district"),
        }
        return Responses.success_response("price benchmark dropdown", data=data)


class NewPriceComputationDropdown(GenericAPIView):
    queryset = NewPriceComputation.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("zone", "state", "district", "region")

    def __get_new_price_comp_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_new_price_comp_query("zone"),
            "state": self.__get_new_price_comp_query("state"),
            "region": self.__get_new_price_comp_query("region"),
            "district": self.__get_new_price_comp_query("district"),
        }
        return Responses.success_response(
            "new price computation price dropdown", data=data
        )


class VpcHistoricalDropdown(GenericAPIView):
    queryset = VpcHistorical.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("plant_id", "grade")

    def __get_vpc_history_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant": self.__get_vpc_history_query("plant_id"),
            "grade": self.__get_vpc_history_query("grade"),
        }
        return Responses.success_response("vpc historical dropdown", data=data)


class GetVpcByPlant(GenericAPIView):
    queryset = VpcHistorical.objects.all()

    def get(self, request, *args, **kwargs):
        plant = request.query_params.get("plant")
        grade = request.query_params.get("grade")
        # month = datetime.today().month
        # year = datetime.today().year

        # month = datetime.today().month
        # year = datetime.today().year
        # try:
        #     avg_vpc = (
        #         VpcHistorical.objects.filter(
        #             plant_id=plant, month__month=month, month__year=year, grade=grade
        #         )
        #         .values_list("vpc", flat=True)
        #         .latest("month")
        #     )
        # except:
        #     avg_vpc = None

        try:
            avg_vpc = (
                self.get_queryset()
                .filter(plant_id=plant, grade=grade)
                .values_list("vpc", flat=True)
                .latest("creation_date")
            )
        except:
            avg_vpc = None

        data = {"avg_vpc": avg_vpc}

        return Responses.success_response("vpc data fetched successfully", data=data)


class NmMarketSharePotentialViewSet(DownloadUploadViewSet):
    """nm market share potential view download api"""

    queryset = NmMarketSharePotential.objects.all()
    serializer_class = NmMarketSharePotentialDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NmMarketSharePotentialFilter
    pagination_class = CustomPagination
    file_name = "nm_market_share_potential_data"
    sorting_fields = ("id",)


class NmMarketSharePotentialDropdown(GenericAPIView):
    queryset = NmMarketSharePotential.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("zone", "state", "district", "brand")

    def __get_nm_market_share_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_nm_market_share_query("zone"),
            "state": self.__get_nm_market_share_query("state"),
            "brand": self.__get_nm_market_share_query("brand"),
            "district": self.__get_nm_market_share_query("district"),
        }
        return Responses.success_response(
            "nm market share potential dropdown", data=data
        )


class PricingModelRunView(GenericAPIView):
    helper = PricingHelper

    def post(self, request):
        month = request.data.get("plan_month")
        try:
            matrix_strategy = self.helper.run_model(month)
        except Exception as e:
            return Responses.error_response(
                "ERROR", status_code=status.HTTP_400_BAD_REQUEST, data=str(e)
            )

        matrix_strategy.columns = matrix_strategy.columns.str.lower()
        matrix_strategy["delta"] = matrix_strategy["delta"].round(decimals=2)
        matrix_strategy["ncr"] = matrix_strategy["ncr"].round(decimals=2)
        matrix_strategy["plan_month"] = matrix_strategy["plan_month"].dt.strftime(
            "%Y-%m-%d"
        )
        matrix_strategy["month"] = matrix_strategy["month"].dt.strftime("%Y-%m-%d")
        matrix_strategy_data = json.loads(matrix_strategy.to_json(orient="records"))
        matrix_strategy_data_serializer = NmMarket4X4OutputSaveSerializer(
            data=matrix_strategy_data,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        matrix_strategy_data_serializer.is_valid(raise_exception=True)
        matrix_strategy_data_serializer.save()
        return Responses.success_response("pricing model run successfully", data="")


class NmMarket4X4OutputViewSet(ModelViewSet):
    """nm market 4x4 output viewset"""

    queryset = NmMarket4X4Output.objects.all()
    serializer_class = NmMarket4X4OutputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NmMarket4X4OutputFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class SoLeagueWeightageViewSet(DownloadUploadViewSet):
    """so league weightage get api"""

    queryset = SoLeagueWeightage.objects.order_by("kpi")
    serializer_class = SoLeagueWeightageSerializer
    pagination_class = CustomPagination


class PriceComputationBaseSegmentDropdown(GenericAPIView):
    def __get_dropdown(self, query_string):
        dropdown = CompetitionPriceNewMarkets.objects.values_list(
            query_string, flat=True
        ).distinct()
        return dropdown

    def get(self, request):
        business_segment = self.__get_dropdown("business_segment")
        grade = self.__get_dropdown("grade")
        data = {"business_segment": business_segment, "grade": grade}
        return Responses.success_response("business segment dropdown", data=data)


class PriceChangeReqApproval(DownloadUploadViewSet):
    queryset = PriceChangeRequestApproval.objects.all()
    filterset_class = PriceChangeRequestApprovalFilterset
    serializer_class = PriceChangeRequestApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "crm_annual_site_conversion_plan_monthly_data"


class PriceChangeApprovalGet(GenericAPIView):
    queryset = PricingProposalApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PricingProposalApprovalFilter
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        zone = request.query_params.get("zone")
        state = request.query_params.get("state")
        region = request.query_params.get("region")
        district = request.query_params.get("district")
        product = request.query_params.get("product")
        brand_mapping = {
            "Shree": 102,
            "Bangur": 103,
            "Rockstrong": 104,
        }
        Brands_list = ["Shree", "Bangur", "Rockstrong"]
        data_list = []
        for brand in Brands_list:
            org_id = brand_mapping.get(brand, None)
            productt = (
                (PremiumProductsMasterTmp.objects.filter(org_id=org_id, grade=product))
                .values("revised_name")
                .latest("creation_date")
            )
            try:
                pricing_proposal_df = pd.DataFrame(
                    [
                        (
                            self.filter_queryset(self.get_queryset())
                            .filter(
                                crm_pricing_key__product=productt["revised_name"],
                                crm_pricing_key__district=district,
                                crm_pricing_key__brand=brand,
                            )
                            .annotate(
                                district=F("crm_pricing_key__district"),
                                brand=F("crm_pricing_key__brand"),
                                product=F("crm_pricing_key__product"),
                                pricing_proposal_wsp_price=F("price"),
                                pricing_proposal_rsp_price=F("rsp_price"),
                            )
                            .values(
                                "brand",
                                "district",
                                "product",
                                "pricing_proposal_wsp_price",
                                "pricing_proposal_rsp_price",
                                "status",
                                "comment",
                            )
                            .latest("creation_date")
                        )
                    ]
                )
            except:
                pricing_proposal_df = pd.DataFrame([])

            if pricing_proposal_df.empty:
                return Responses.success_response(
                    "price change request data fetched", data=data_list
                )

            try:
                price_benchmark_df = pd.DataFrame(
                    [
                        (
                            PriceBenchmarks.objects.filter(district=district)
                            .annotate(price_benchmark_id=F("id"))
                            .values(
                                "price_benchmark_id",
                                "district",
                                "benchmark_name",
                                "price_difference_to_be_maintained",
                            )
                            .latest("month")
                        )
                    ]
                )
            except:
                price_benchmark_df = pd.DataFrame([])

            if price_benchmark_df.empty:
                price_benchmark_df = pd.DataFrame(
                    columns=[
                        "district",
                        "benchmark_name",
                        "price_difference_to_be_maintained",
                    ]
                )
            try:
                price_change_req_approval_df = pd.DataFrame(
                    [
                        (
                            PriceChangeRequestApproval.objects.filter(
                                zone=zone,
                                state=state,
                                region=region,
                                district=district,
                                brand=brand,
                                product=product,
                            )
                            .values(
                                "zone",
                                "state",
                                "region",
                                "district",
                                "brand",
                                "product",
                                "wsp_change",
                                "wsp_effective_date",
                                "rsp_change",
                                "rsp_effective_date",
                                "creation_date",
                            )
                            .latest("creation_date")
                        )
                    ]
                )
            except:
                price_change_req_approval_df = pd.DataFrame([])

            if price_change_req_approval_df.empty:
                price_change_req_approval_df = pd.DataFrame(
                    columns=[
                        "zone",
                        "state",
                        "region",
                        "district",
                        "brand",
                        "product",
                        "wsp_change",
                        "wsp_effective_date",
                        "rsp_change",
                        "rsp_effective_date",
                        "creation_date",
                    ]
                )

            pricing_proposal_df = pricing_proposal_df.merge(
                price_benchmark_df, on=["district"], how="left"
            ).merge(
                price_change_req_approval_df,
                on=["district", "brand"],
                how="left",
            )

            data = json.loads(pricing_proposal_df.to_json(orient="records"))
            # data[0]['creation_date'] = datetime(data[0]['creation_date']).strftime('%Y-%m-%d %H:%M:%S')
            # data[0]['rsp_effective_date'] = datetime(data[0]['rsp_effective_date']).strftime('%Y-%m-%d %H:%M:%S')
            # data[0]['wsp_effective_date'] = datetime(data[0]['wsp_effective_date']).strftime('%Y-%m-%d %H:%M:%S')
            data_list.append(data[0])

        return Responses.success_response(
            "price change request data fetched", data=data_list
        )


class PriceChangeRequestApprovalDropdown(GenericAPIView):
    queryset = PriceChangeRequestApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = (
        "zone",
        "state",
        "district",
        "region",
        "status",
        "brand",
        "product",
    )

    def __get_price_change_req_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_price_change_req_dropdown_query("zone"),
            "state": self.__get_price_change_req_dropdown_query("state"),
            "district": self.__get_price_change_req_dropdown_query("district"),
            "region": self.__get_price_change_req_dropdown_query("region"),
            "status": self.__get_price_change_req_dropdown_query("status"),
            "brand": self.__get_price_change_req_dropdown_query("brand"),
            "product": self.__get_price_change_req_dropdown_query("product"),
        }
        return Responses.success_response("price change request dropdown", data=data)
