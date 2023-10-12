"""Sales planning views module."""
import json
import os
from datetime import date, datetime
from functools import reduce
from operator import itemgetter

import pandas as pd
from django.db import transaction
from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
    Sum,
    Value,
)
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import (
    BottomUpNtFilter,
    ExistingDepotLocationsFilter,
)
from analytical_data.models import *

# from analytical_data.models.sales_planning_models import DfMacroOutputFinal
from analytical_data.serializers import *
from analytical_data.utils import (
    CustomPagination,
    Response,
    Responses,
    dump_to_excel,
    get_zip_file,
)
from analytical_data.view_helpers import (
    DemandSplitHelperView,
    KachaPakkaViewHelper,
    MarketMappingViewHelper,
    TopDownTargetDropdownHelper,
    connect_db,
)
from analytical_data.view_helpers.Market_Mapping_Script_Helper.district_cls_excel import (
    DistrictClassificationHelper,
)
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class KachaPakkaConversionRateViewSet(DownloadUploadViewSet):
    """Kacha pakka conversion rate view set."""

    queryset = DfKachaPakkaConversionRate.objects.all()
    serializer_class = KachaPakkaConversionRateSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state", "district")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "kacha_pakka_conversion_rate"


class AnnualUrbanizationRateViewSet(DownloadUploadViewSet):
    """Annual urbanization rate view set."""

    queryset = DfAnnualUrbanizationRate.objects.all()
    serializer_class = AnnualUrbanizationRateSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "annual_urbanization_rate"


class AverageFlatSizeViewSet(DownloadUploadViewSet):
    """Average flat size view set."""

    queryset = DfAverageFlatSize.objects.all()
    serializer_class = AverageFlatSizeSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state", "district")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "average_flat_size"


class UrbanRuralHouseholdSizeViewSet(DownloadUploadViewSet):
    """Urban rural household size view set."""

    queryset = DfUrbanRuralHouseholdSize.objects.all()
    serializer_class = UrbanRuralHouseholdSizeSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state", "district")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "urban_rural_household"


class CementConsumptionViewSet(DownloadUploadViewSet):
    """Cement consumption per square foot view set."""

    queryset = DfCementConsumptionPerSqFt.objects.all()
    serializer_class = CementConsumptionSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state", "district")
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "cement_consumption"


class ProjectDbViewSet(DownloadUploadViewSet):
    """Project database view set."""

    queryset = DfProjectDatabase.objects.all()
    serializer_class = ProjectDbSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "project_db"


class DesiredMarketShareViewSet(DownloadUploadViewSet):
    """Desired market share view set."""

    queryset = DfDesiredMarketShare.objects.all()
    serializer_class = DesiredMarketShareSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "desired_market_share"


class GetDesiredMarketShareStatesViewSet(GenericAPIView):
    queryset = DfDesiredMarketShare.objects.all()
    """Desired market share view set."""

    def get(self, request):
        desired_market_states = (
            self.get_queryset()
            .filter(state__isnull=False)
            .values_list("state", flat=True)
            .annotate(Count("state"))
            .order_by("state")
        )

        return Responses.success_response(
            "Desired market states fetched successfully",
            data=desired_market_states,
        )


class GeographicalPresenceViewSet(DownloadUploadViewSet):
    """Geographical presence view set."""

    queryset = DfGeographicalPresence.objects.all()
    serializer_class = GeographicalPresenceSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "geographical_presence"


class GetGeographicalPresenceStatesViewSet(GenericAPIView):
    """Get Geographical presence states ."""

    queryset = DfGeographicalPresence.objects.all()

    def get(self, request):
        geographical_presence__states = (
            self.get_queryset().values_list("state", flat=True).annotate(Count("state"))
        )

        return Responses.success_response(
            "Geographical presence states data  fetched successfully",
            data=geographical_presence__states,
        )


class SeasonalityViewSet(DownloadUploadViewSet):
    """Seasonality view set."""

    queryset = DfSeasonality.objects.all()
    serializer_class = SeasonalitySerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "seasonality"


class HighRiseLowRiseSplitViewSet(DownloadUploadViewSet):
    """High rise low rise split view set."""

    queryset = DfHighRiseLowRiseSplit.objects.all()
    serializer_class = HighRiseLowRiseSplitSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "high_rise_low_rise_split"


class StatesCities(APIView):
    """List api for cities and states list."""

    helper = KachaPakkaViewHelper

    def get(self, request, *args, **kwargs):
        """Get states and cities list."""

        return Responses.success_response(
            "States, cities data.",
            data=self.helper._get_states_cities(request.query_params),
        )


class DemandForecastRunViewSet(DownloadUploadViewSet):
    """Demand forecast run detail view set."""

    queryset = DemandForecastRunDtl.objects.all()
    serializer_class = DemandForecastRunDtlSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = ("state", "district")
    filterset_fields = ("state", "district", "forecast_month")
    pagination_class = CustomPagination
    file_name = "demand_forecast_run_details"


class DfMacroOutputFinalViewSet(DownloadUploadViewSet):
    """Macro output final detail view set."""

    queryset = DfMacroOutputFinal.objects.all()
    serializer_class = DfMacroOutputFinalSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    file_name = "df_macro_output_final"


class TopDownTargetsViewSet(DownloadUploadViewSet):
    """Top down targets detail view set."""

    queryset = DfTopDownTargets.objects.all()
    serializer_class = DfTopDownTargetsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "brand", "product", "date")
    pagination_class = CustomPagination
    file_name = "top_down_target"


class TopDownTargetsDropdownView(APIView):
    """Kacha pakka dropdown view class."""

    helper = TopDownTargetDropdownHelper

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "Kacha pakka dropdown data.",
            data=self.helper._get_dropdown_data(request.query_params),
        )


class ConsensusTargetViewSet(ListAPIView):
    """Consensus target list view class."""

    queryset = (
        ConsensusTarget.objects.filter()
        .values("state", "zone")
        .annotate(
            Count("state"),
            Count("zone"),
            Sum("consensus_target"),
            Sum("premium_product_target"),
            Sum("other_product_target"),
            Sum("nt_poduct_target"),
        )
    )
    serializer_class = ConsensusTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "zone", "date")
    # sorting_fields = ("state",)
    # file_name = "consensus_target"

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            consensus_target_df = pd.read_json(json.dumps(response.data))
            consensus_target_df["state"] = consensus_target_df["state"].str.upper()

            if consensus_target_df.empty:
                return Responses.success_response("Consensus target data!", data=[])
            month = datetime.strptime(
                request.query_params.get("date"), "%Y-%m-%d"
            ).month
            if month:
                bottom_up_target_qs = (
                    DfBottomUpTargetsMonthly2.objects.filter(date__month=month)
                    .values("zone", "state")
                    .annotate(
                        Count("zone"),
                        Count("state"),
                        bottom_up_target=Sum("bottom_up_retailer_targets"),
                    )
                )
            else:
                bottom_up_target_qs = (
                    DfBottomUpTargetsMonthly2.objects.filter()
                    .values("zone", "state")
                    .annotate(
                        Count("zone"),
                        Count("state"),
                        bottom_up_target=Sum("bottom_up_retailer_targets"),
                    )
                )
            bottom_up_target_ser = BottomUpTargetsMonthly2Serializer(
                bottom_up_target_qs, many=True
            )
            bottom_up_target_df = pd.read_json(
                json.dumps(list(bottom_up_target_ser.data))
            )[["zone", "state", "bottom_up_target"]]
            bottom_up_target_df["state"] = bottom_up_target_df["state"].str.upper()

            if month:
                statistical_forecast_qs = (
                    DemandForecastRunDtl.objects.filter(forecast_month__month=month)
                    .values("state")
                    .annotate(Count("state"), statistical_forecast=Sum("forecast"))
                )
            else:
                statistical_forecast_qs = (
                    DemandForecastRunDtl.objects.filter()
                    .values("state")
                    .annotate(Count("state"), statistical_forecast=Sum("forecast"))
                )

            statistical_forecast_ser = DemandForecastRunDtlSerializer(
                statistical_forecast_qs, many=True
            )
            statistical_forecast_df = pd.read_json(
                json.dumps(list(statistical_forecast_ser.data))
            )[["state", "statistical_forecast"]]
            statistical_forecast_df["state"] = statistical_forecast_df[
                "state"
            ].str.upper()

            if month:
                macro_analysis_output_qs = (
                    DfMacroOutputFinal.objects.filter(date__month=month)
                    .values("state")
                    .annotate(Count("state"), macro_analysis_output=Sum("final_demand"))
                )
            else:
                macro_analysis_output_qs = (
                    DfMacroOutputFinal.objects.filter()
                    .values("state")
                    .annotate(Count("state"), macro_analysis_output=Sum("final_demand"))
                )
            macro_analysis_output_ser = DfMacroOutputFinalSerializer(
                macro_analysis_output_qs, many=True
            )
            macro_analysis_output_df = pd.read_json(
                json.dumps(list(macro_analysis_output_ser.data))
            )[["macro_analysis_output", "state"]]

            macro_analysis_output_df["state"] = macro_analysis_output_df[
                "state"
            ].str.upper()

            # top_down_targets_qs = (
            #     DfTopDownTargets.objects.filter(date__month=month)
            #     .values("state", "zone")
            #     .annotate(
            #         Count("state"), Count("zone"), top_down_target=Sum("top_down_target")
            #     )
            # )
            # top_down_targets_ser = DfTopDownTargetsSerializer(
            #     top_down_targets_qs, many=True
            # )
            # top_down_targets_df = pd.read_json(json.dumps(list(top_down_targets_ser.data)))[
            #     ["state", "zone", "top_down_target"]
            # ]
            # top_down_targets_df['state']=top_down_targets_df['state'].str.upper()
            if month:
                run_id = (
                    MarketMappingRun.objects.filter(plan_month__month=month)
                    .order_by("-run_id")
                    .first()
                    .run_id
                )
                top_down_targets_qs = (
                    MarketMappingSalesTarget.objects.filter(run__run_id=run_id)
                    .values("state", "zone")
                    .annotate(
                        Count("state"),
                        Count("zone"),
                        top_down_target=Sum("target_sales"),
                        sales_target=Value(0),
                    )
                )
            else:
                top_down_targets_qs = (
                    MarketMappingSalesTarget.objects.filter()
                    .values("state", "zone")
                    .annotate(
                        Count("state"),
                        Count("zone"),
                        top_down_target=Sum("target_sales"),
                        sales_target=Value(0),
                    )
                )
            top_down_targets_ser = MarketMappingSalesTargetSerializer(
                top_down_targets_qs, many=True
            )
            top_down_targets_df = pd.read_json(
                json.dumps(list(top_down_targets_ser.data))
            )
            top_down_targets_df["state"] = top_down_targets_df["state"].str.upper()
            # if month:
            #     sales_target_qs = (
            #         SalesTargetMonthly.objects.filter(plan_month__month=month)
            #         .values("state", "zone")
            #         .annotate(
            #             Count("state"),
            #             Count("zone"),
            #             sales_target=Sum("target_sales"),
            #             top_down_target=Value(0),
            #         )
            #     )
            # else:
            #     sales_target_qs = (
            #         SalesTargetMonthly.objects.filter()
            #         .values("state", "zone")
            #         .annotate(
            #             Count("state"),
            #             Count("zone"),
            #             sales_target=Sum("target_sales"),
            #             top_down_target=Value(0),
            #         )
            #     )
            # sales_target_ser = SalesTargetMonthlySerializer(sales_target_qs, many=True)
            # sales_target_df = pd.read_json(json.dumps(list(sales_target_ser.data)))
            # sales_target_df["state"] = sales_target_df["state"].str.upper()
            dataframe_list = [
                bottom_up_target_df,
                statistical_forecast_df,
                macro_analysis_output_df,
                top_down_targets_df,
                # sales_target_df,
            ]
            merged_data = reduce(
                lambda left_df, right_df: pd.merge(
                    left_df, right_df, on="state", how="outer"
                ),
                dataframe_list,
            )
            if (
                "sales_target_y" in merged_data.columns
                and "top_down_target_x" in merged_data.columns
            ):
                merged_data.rename(
                    columns={
                        "sales_target_y": "sales_target",
                        "top_down_target_x": "top_down_target",
                    },
                    inplace=True,
                )
            merged_data.rename(
                columns={"target_sales": "top_down_target"}, inplace=True
            )
            data = pd.merge(
                consensus_target_df,
                merged_data,
                on="state",
                how="left",
                suffixes=("", "_y"),
            )[
                [
                    "state",
                    "zone",
                    "consensus_target__sum",
                    "bottom_up_target",
                    "statistical_forecast",
                    "macro_analysis_output",
                    "top_down_target",
                    # "sales_target",
                    "premium_product_target__sum",
                    "other_product_target__sum",
                    "nt_poduct_target",
                ]
            ]
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Consensus target data!",
                        "data": json.loads(data.to_json(orient="records")),
                    }
                )
            )
        except:
            return Responses.success_response(
                "selected month data doesn't exist in database", data=[]
            )


class ConsensusTargetUpdateDownloadViewSet(DownloadUploadViewSet):
    """Consensus target download, upload and update api view-set."""

    sorting_fields = ("state", "brand")
    queryset = ConsensusTarget.objects.order_by(*sorting_fields)
    # Month filter made dynamic instead of static value on backend.
    # queryset = ConsensusTarget.objects.filter(month="December").order_by(
    #     *sorting_fields
    # )
    serializer_class = ConsensusTargetUpdateDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("date", "month")
    file_name = "consensus_target"

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            state__in=[data["state"] for data in request.data],
            brand__in=[data["brand"] for data in request.data],
        )
        # Sorts list of dicts based on a value of a key in dictionary.
        data = sorted(request.data, key=itemgetter(*self.sorting_fields))

        serializer = self.get_serializer(
            queryset,
            data[: len(queryset)],
            partial=kwargs.pop("partial", None),
            many=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            self.update_response_message, data=serializer.data
        )


class ConsensusTargetDropdownView(GenericAPIView):
    """Consensus target dropdown view class."""

    queryset = ConsensusTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "zone", "brand")

    def __get_consensus_target_query(self, query_string, filter_query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_consensus_target_query("zone", Q(zone__isnull=False)),
            "brand": self.__get_consensus_target_query("brand", Q(brand__isnull=False)),
            "states": self.__get_consensus_target_query(
                "state", Q(state__isnull=False)
            ),
        }
        return Responses.success_response("Consensus target dropdown data.", data=data)


class TdtMultiplierViewSet(DownloadUploadViewSet):
    """tdt multiplier  view set."""

    queryset = TdtMultiplier.objects.all()
    serializer_class = TdtMultiplierSerializer
    filter_backends = (DjangoFilterBackend,)
    sorting_fields = filterset_fields = ("state",)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "tdt-multiplier-data"


class TdtMultiplierBaseView(GenericAPIView):
    """Tdt Multiplier dropdown base view class."""

    queryset = TdtMultiplier.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def _get_tdt_multiplier_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )


class TdtMultiplierDropdown(TdtMultiplierBaseView):
    """state name dropdown from tdt multiplier data."""

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "state dropdown data",
            data={"state": self._get_tdt_multiplier_query("state")},
        )


class MacroAnalysisScriptRunView(APIView):
    """Run macro analysis script view class."""

    def get(self, request, *args, **kwargs):
        os.system("python3 scripts/MacroAnalysis_27_09_2022_FINAL.py")
        return Response()


class MarketMappingMarketPotentialViewSet(DownloadUploadViewSet):
    """Market mapping market potential view-set class."""

    sorting_fields = filterset_fields = ("state", "district", "brand", "month")
    queryset = MarketMappingMarketPotential.objects.order_by(*sorting_fields)
    serializer_class = MarketMappingMarketPotentialSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    file_name = "market_mapping_market_potential"


class MarketMappingMarketPotentialDropdown(GenericAPIView):
    queryset = MarketMappingMarketPotential.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "brand", "month")

    def __get_market_potential_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_market_potential_query("state"),
            "district": self.__get_market_potential_query("district"),
            "brand": self.__get_market_potential_query("brand"),
            "month": self.__get_market_potential_query("month"),
        }
        return Responses.success_response(
            "market mapping market potential dropdown data.", data=data
        )


class MarketMappingGrowthPotentialViewSet(DownloadUploadViewSet):
    """Market mapping growth potential view-set class."""

    sorting_fields = filterset_fields = ("state", "month")
    queryset = MarketMappingGrowthPotential.objects.order_by(*sorting_fields)
    serializer_class = MarketMappingGrowthPotentialSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    file_name = "market_mapping_growth_potential"


class MarketMappingGrowthPotentialDropdown(GenericAPIView):
    queryset = MarketMappingGrowthPotential.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "month")

    def __get_market_mapping_growth_potential_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_market_mapping_growth_potential_query("state"),
            "month": self.__get_market_mapping_growth_potential_query("month"),
        }
        return Responses.success_response(
            "market mapping growth potential dropdown data.", data=data
        )


class MarketMappingRunRunModel(GenericAPIView):
    serializer_class = MarketMappingRunSerializer
    helper = MarketMappingViewHelper

    @transaction.atomic()
    def post(self, request):
        date_input = request.data.get("date_input")

        markrt_mapping_run_obj = {
            "run_type": "Monthly",
            "run_date": date.today(),
            "plan_month": date_input,
        }

        model_run_serializer = self.serializer_class(data=markrt_mapping_run_obj)
        model_run_serializer.is_valid(raise_exception=True)
        model_run_object_instance = model_run_serializer.save()
        try:
            (
                district_clsf,
                sales_target,
                state_clsf,
                channel_strat,
                counter_strat,
                brand_budget,
                pricing_strategy,
            ) = self.helper.run_model(date_input)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))

        # # state_clsf saving
        ##################################### state classification ##################################
        state_clsf.columns = state_clsf.columns.str.lower()
        state_clsf_data = json.loads(state_clsf.to_json(orient="records"))

        state_clsf_seralizer = MarketMappingStateClassificationSerializer(
            data=state_clsf_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        state_clsf_seralizer.is_valid(raise_exception=True)
        state_clsf_seralizer.save()

        ##################################### districts classification ##################################
        district_clsf.columns = district_clsf.columns.str.lower()
        district_clsf_data = json.loads(district_clsf.to_json(orient="records"))

        district_clsf_serializer = MarketMappingDistrictClassificationSerializer(
            data=district_clsf_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        district_clsf_serializer.is_valid(raise_exception=True)
        district_clsf_serializer.save()

        ##################################### sales target ##################################
        sales_target.columns = sales_target.columns.str.lower()
        sales_target_data = json.loads(sales_target.to_json(orient="records"))

        sales_target_serializer = MarketMappingSalesTargetSerializer(
            data=sales_target_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        sales_target_serializer.is_valid(raise_exception=True)
        sales_target_serializer.save()

        ##################################### channel strategy ##################################
        channel_strat.columns = channel_strat.columns.str.lower()
        channel_strat["total_sales"] = channel_strat["total_sales"].astype(int)
        channel_strat_data = json.loads(channel_strat.to_json(orient="records"))

        channel_strat_serializer = MarketMappingChannelStrategySerializer(
            data=channel_strat_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        channel_strat_serializer.is_valid(raise_exception=True)
        channel_strat_serializer.save()

        #####################################counter_strat ##################################
        counter_strat.columns = counter_strat.columns.str.lower()
        counter_strat_data = json.loads(counter_strat.to_json(orient="records"))

        counter_strat_serializer = MarketMappingCounterStrategySerializer(
            data=counter_strat_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        counter_strat_serializer.is_valid(raise_exception=True)
        counter_strat_serializer.save()

        # ##################################### branding output ##################################
        brand_budget.columns = brand_budget.columns.str.lower()
        brand_budget_data = json.loads(brand_budget.to_json(orient="records"))

        brand_budget_serializer = MarketMappingBrandingOuputSerializer(
            data=brand_budget_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        brand_budget_serializer.is_valid(raise_exception=True)
        brand_budget_serializer.save()

        #  ##################################### pricing_strategy ##################################
        pricing_strategy.columns = pricing_strategy.columns.str.lower()
        pricing_strategy_data = json.loads(pricing_strategy.to_json(orient="records"))

        pricing_strategy_data_serializer = MarketMappingPricingOuputSerializer(
            data=pricing_strategy_data,
            context={
                "run_id": model_run_object_instance.run_id,
            },
            many=True,
        )
        pricing_strategy_data_serializer.is_valid(raise_exception=True)
        pricing_strategy_data_serializer.save()

        return Responses.success_response(
            "successfully Running Data", data=model_run_object_instance.run_id
        )


class DemandSplitView(GenericAPIView):
    serializer_class = DemandForMarketMappingCreateSerializer
    helper = DemandSplitHelperView
    parser_classes = (MultiPartParser, JSONParser)
    file_name = "df_missing"

    # @transaction.atomic()
    def post(self, request):
        excel = request.FILES["file_name"]
        date_input = request.query_params["plan_date"]
        cnxn = connect_db()
        df_flag = request.query_params.get("flag")
        try:
            if df_flag == "true":
                df_main = pd.read_excel(excel, sheet_name="dmnd")
            else:
                df_main = pd.read_excel(excel, sheet_name="df_hierarchy_missing")
            try:
                (
                    df_trade,
                    df_trade_missing,
                    df_hierarchy_missing,
                    date_prev,
                ) = self.helper.get_trade_dmnd(
                    # cnxn, df_main, date_input
                    cnxn,
                    df_main,
                    date_input,
                )
                (
                    df_trade_prev,
                    df_trade_missing,
                    df_hierarchy_missing_prev,
                    date_prev,
                ) = self.helper.get_trade_dmnd(cnxn, df_trade_missing, date_prev, True)
                df_trade = df_trade.append(df_trade_prev, ignore_index=True)
            except Exception as e:
                return Responses.error_response("ERROR", data=str(e))
            try:
                (
                    df_non_trade,
                    df_non_trade_missing,
                    date_prev,
                ) = self.helper.get_non_trade_dmnd(cnxn, df_main, date_input)
                (
                    df_non_trade_prev,
                    df_non_trade_missing,
                    date_prev,
                ) = self.helper.get_non_trade_dmnd(
                    cnxn, df_non_trade_missing, date_prev, True
                )
                df_non_trade = df_non_trade.append(df_non_trade_prev, ignore_index=True)
            except Exception as e:
                return Responses.error_response("ERROR", data=str(e))
            df = df_trade.dropna().append(df_non_trade.dropna(), ignore_index=True)
            df["MONTH"] = date_input
            df_missing = df_trade_missing.append(
                df_non_trade_missing, ignore_index=True
            )
            df_missing["MONTH"] = date_input
            df_missing["CITY"] = None
            df_missing = df_missing[
                [
                    "STATE",
                    "DISTRICT",
                    "CITY",
                    "BRAND",
                    "GRADE",
                    "PACK_TYPE",
                    "PACKAGING",
                    "CUST_CATEGORY",
                    "DEMAND_QTY",
                    "MONTH",
                ]
            ]

        except Exception as e:
            print(e)
            return Responses.error_response("Some issue arrise")

        df.columns = df.columns.str.lower()
        if df_flag == "true":
            Demand.objects.filter(month__in=df["month"]).delete()
        df["destination"] = df["destination"].round(decimals=2)
        # df["demand_qty"] = df["demand_qty"].round(decimals=2)
        demand_data = json.loads(df.to_json(orient="records"))
        df_missing.to_csv("demand.csv", index=False)
        sales_target_serializer = self.get_serializer(data=demand_data, many=True)
        sales_target_serializer.is_valid(raise_exception=True)
        sales_target_serializer.save()
        workbook1 = dump_to_excel(df_missing, self.file_name)
        workbook2 = dump_to_excel(df_hierarchy_missing, "df_hierarchy_missing")
        self.helper.upload_price(cnxn, date_input)
        self.helper.update_missing_prices(cnxn, date_input)
        self.helper.upload_price_dist(cnxn, date_input)
        zip_file = get_zip_file(
            {"df_missing.xlsx": workbook1, "df_hierarchy_missing.xlsx": workbook2}
        )

        content_type = (
            # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            "application/force-download"
        )
        response = HttpResponse(zip_file, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename=demand_split_run.zip"
        return response


class MarketMappingPricingOutputViewSet(DownloadUploadViewSet):
    queryset = MarketMappingPricingOuput.objects.all()
    serializer_class = MarketMappingPricingOuputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "market_mapping_pricing_output"


class MarketMappingSalesTargetViewSet(DownloadUploadViewSet):
    queryset = MarketMappingSalesTarget.objects.all()
    serializer_class = MarketMappingSalesTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "market_mapping_sales_target"


class MarketMappingBrandingOuputViewSet(DownloadUploadViewSet):
    queryset = MarketMappingBrandingOuput.objects.all()
    serializer_class = MarketMappingBrandingOuputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "market_mapping_branding_output"


class MarketMappingChannelStrategyViewSet(DownloadUploadViewSet):
    queryset = MarketMappingChannelStrategy.objects.all()
    serializer_class = MarketMappingChannelStrategySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "market_mapping_channel_strategy"


class MarketMappingCounterStrategyViewSet(DownloadUploadViewSet):
    queryset = MarketMappingCounterStrategy.objects.all()
    serializer_class = MarketMappingCounterStrategySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "market_mapping_channel_strategy"


class MarketMappingStateClassificationViewSet(DownloadUploadViewSet):
    queryset = MarketMappingStateClassification.objects.all()
    serializer_class = MarketMappingStateClassificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "mm_state_classification"


class MarketMappingDistrictClassificationViewSet(DownloadUploadViewSet):
    queryset = MarketMappingDistrictClassification.objects.all()
    serializer_class = MarketMappingDistrictClassificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("run__plan_month",)
    file_name = "mm_district_classification"


class DfBottomUpTargetsMonthly2ViewSet(DownloadUploadViewSet):
    queryset = DfBottomUpTargetsMonthly2.objects.all()
    serializer_class = BottomUpTargetsMonthly2CreateSerializer
    file_name = "bottom_up_monthly_2"
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("date",)


class BottomUpNtViewSet(DownloadUploadViewSet):
    queryset = BottomUpNt.objects.all()
    serializer_class = BottomUpNtSerializer
    file_name = "bottom_up_nt"
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BottomUpNtFilter


class DemandSplitMissingView(GenericAPIView):
    serializer_class = DemandForMarketMappingCreateSerializer
    helper = DemandSplitHelperView

    # @transaction.atomic()
    def post(self, request):
        csv = request.FILES["file_name"]
        date_input = request.query_params["plan_date"]
        cnxn = connect_db()
        df_main = pd.read_excel(csv)
        try:
            df = self.helper.get_missing_dmnd(cnxn, df_main)
        except Exception as e:
            return Responses.error_response("ERROR", data=str(e))
        df["MONTH"] = date_input
        df.columns = df.columns.str.lower()
        df["demand_qty"] = df["demand_qty"].round(decimals=2)
        df["destination"] = df["destination"].round(decimals=2)
        demand_data = json.loads(df.to_json(orient="records"))

        sales_target_serializer = self.get_serializer(data=demand_data, many=True)
        sales_target_serializer.is_valid(raise_exception=True)
        sales_target_serializer.save()
        self.helper.upload_price(cnxn, date_input)
        self.helper.update_missing_prices(cnxn, date_input)
        self.helper.upload_price_dist(cnxn, date_input)
        return Responses.success_response("Successfully Running Data", data="")


class DistrictClassification(GenericAPIView):
    helper = DistrictClassificationHelper

    def post(self, request):
        try:
            cnxn = connect_db()
            date_input = request.data.get("date_input")
            run_dtl = self.helper.get_run_dtl(cnxn, date_input)
            df = self.helper.get_data(cnxn, run_dtl.loc[0, "RUN_ID"])
            self.helper.get_file(df, date_input)
            with open(
                f"analytical_data/district_cls_data/district_cls_out_65.xlsx",
                "rb",
            ) as excel:
                workbook = excel.read()
                content_type = (
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                response = HttpResponse(workbook, content_type=content_type)
                response[
                    "Content-Disposition"
                ] = f"attachment; filename=district_cls_out_65.xlsx"
                return response
        except Exception as e:
            return Responses.error_response("some issue occurred", data=e)


# class DepotAdditionMasterViewSet(ModelViewSet):
#     queryset = DepotAdditionMaster.objects.all()
#     serializer_class = DepotAdditionMasterSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = (
#         "state",
#         "district",
#         "taluka",
#     )
#     pagination_class = CustomPagination
#     lookup_field = "id"


class DepotAdditionMasterViewSet(DownloadUploadViewSet):
    """Depot Addition Master View"""

    queryset = DepotAdditionMaster.objects.all()
    serializer_class = DepotAdditionMasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "state",
        "district",
        "taluka",
    )
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "Depot_addition_master"


class IFramesUrlMapping(ListAPIView):
    queryset = UrlMapping.objects.all()
    serializer_class = UrlMappingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)


class DepotAdditionMasterDropdownViewSet(GenericAPIView):
    queryset = DepotAdditionMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "state",
        "district",
        "taluka",
    )

    def __get_depot_addition_master_query(self, query_str):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_str, flat=True)
            .annotate(Count(query_str))
        )

    def get(self, request, *args, **kwargs):
        return Responses.success_response(
            "dropdown data",
            data={
                "state": self.__get_depot_addition_master_query("state"),
                "district": self.__get_depot_addition_master_query("district"),
                "taluka": self.__get_depot_addition_master_query("taluka"),
            },
        )


class DepotAdditionOutputViewSet(ModelViewSet):
    queryset = DepotAdditionOutputView.objects.all()
    serializer_class = DepotAdditionOutputSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "state",
        "district",
        "taluka",
        # "run",
    )
    pagination_class = CustomPagination

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        creation_date = self.request.query_params.get("creation_date")
        run_id = self.request.query_params.get("run__run_id")
        if run_id:
            queryset = queryset.filter(run__run_id=run_id)

        if creation_date:
            queryset = queryset.filter(creation_date__date=creation_date)

            average_ptpk = (
                super()
                .filter_queryset(
                    DepotAdditionMaster.objects.filter(
                        creation_date__date=creation_date
                    )
                )
                .aggregate(Avg("secondary_ptpk"))["secondary_ptpk__avg"]
            )
        else:
            average_ptpk = (
                super()
                .filter_queryset(DepotAdditionMaster.objects.all())
                .aggregate(Avg("secondary_ptpk"))["secondary_ptpk__avg"]
            )
        return queryset.annotate(
            expected_benefit=ExpressionWrapper(
                (F("existing_depo_lead") - F("recommended_depo_lead")) * average_ptpk,
                output_field=DecimalField(),
            )
        )


class DepotAdditionOutputDropdownViewSet(DepotAdditionMasterDropdownViewSet):
    queryset = DepotAdditionOutputView.objects.all()


class AverageDepotAdditionOutputView(GenericAPIView):
    queryset = DepotAdditionOutputView.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "state",
        "district",
        "taluka",
        # "run",
    )

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        run_id = request.query_params.get("run_id")

        if run_id:
            queryset = queryset.filter(run__run_id=run_id)
        average_ptpk = self.filter_queryset(
            DepotAdditionMaster.objects.all()
        ).aggregate(Avg("secondary_ptpk"))["secondary_ptpk__avg"]
        data = {
            "average_secondary_lead_current": queryset.aggregate(
                Avg("existing_depo_lead")
            )["existing_depo_lead__avg"],
            "average_secondary_lead_recommended": queryset.aggregate(
                Avg("recommended_depo_lead")
            )["recommended_depo_lead__avg"],
            "net_benefit": queryset.aggregate(
                expected_benefit=Sum(
                    (F("existing_depo_lead") - F("recommended_depo_lead"))
                    * average_ptpk,
                    output_field=DecimalField(),
                )
            )["expected_benefit"],
        }
        return Responses.success_response("average depot output data.", data=data)


class ConsensusTargetMonthlysalesplan(GenericAPIView):
    queryset = ConsensusTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get(self, request):
        month = request.query_params["month"]
        year = request.query_params["year"]

        data = self.filter_queryset(
            self.get_queryset().filter(
                ~Q(brand="Scl"), date__month=month, date__year=year
            )
        ).aggregate(
            Sum("premium_product_target"),
            Sum("other_product_target"),
            Sum("consensus_target"),
        )
        final_dict = {
            "peremium_product_data": self.format_val(
                data["premium_product_target__sum"]
            ),
            "other_product_data": self.format_val(data["other_product_target__sum"]),
            "consensus_target": self.format_val(data["consensus_target__sum"]),
        }
        return Responses.success_response("data fetched succesfully", data=final_dict)


# class PlanDataForMonthViewSet(ModelViewSet):
#     def get(self, request):
#         month = request.query_params["month"]
#         consensus_target_data = ConsensusTarget.objects.filter(month=month).aggregate(
#             peremium_product=Sum("premium_product_target"),other_product=Sum("other_product_target")
#         )
#         try:
#             peremium_product = consensus_target_data["peremium_product"]
#         except:
#             peremium_product = 0

#         try:
#             other_product = consensus_target_data["other_product"]
#         except:
#             other_product = 0
#         final_dict = {"monthly_data": peremium_product + other_product}
#         return Responses.success_response("data fetched ", data=final_dict)


class MarketPotentialAndShareMonthlyViewSet(ModelViewSet):
    def get(self, request, *args, **kwargs):
        state = request.query_params["state"]
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        brands = ["Rockstrong", "Shree", "Bangur"]
        market_potential = MarketMappingMarketPotential.objects.filter(
            month__month=month, month__year=year, state=state, brand__in=brands
        ).aggregate(Avg("market_potential"), Sum("sales"))

        average_market_potential = market_potential.get("market_potential__avg", 0)
        total_sales = market_potential.get("sales__sum", 0)
        if average_market_potential is not None and total_sales is not None:
            market_shares = total_sales / average_market_potential
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
                cust_categ="TR",
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


class ExistingDepotLocationsViewSet(DownloadUploadViewSet):
    queryset = ExistingDepotLocations.objects.all()
    serializer_class = ExistingDepotLocationsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ExistingDepotLocationsFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "existing_depot_locations"
