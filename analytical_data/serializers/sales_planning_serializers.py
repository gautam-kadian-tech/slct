"""Analytical data sales planning serializers module."""
from django.db import IntegrityError

from analytical_data.models import (
    BottomUpNt,
    ConsensusTarget,
    DemandForecastRunDtl,
    DemandForMarketMapping,
    DepotAdditionMaster,
    DepotAdditionOutputView,
    DfAnnualUrbanizationRate,
    DfAverageFlatSize,
    DfBottomUpTargetsMonthly2,
    DfCementConsumptionPerSqFt,
    DfDesiredMarketShare,
    DfGeographicalPresence,
    DfHighRiseLowRiseSplit,
    DfKachaPakkaConversionRate,
    DfMacroOutputFinal,
    DfProjectDatabase,
    DfSeasonality,
    DfTopDownTargets,
    DfUrbanRuralHouseholdSize,
    ExistingDepotLocations,
    MarketMappingBrandingOuput,
    MarketMappingChannelStrategy,
    MarketMappingCounterStrategy,
    MarketMappingDistrictClassification,
    MarketMappingGrowthPotential,
    MarketMappingMarketPotential,
    MarketMappingPricingOuput,
    MarketMappingRun,
    MarketMappingSalesTarget,
    MarketMappingStateClassification,
    SalesTargetMonthly,
    TdtMultiplier,
    UrlMapping,
)
from analytical_data.serializers.custom_serializers import (
    BulkCreateListSerializer,
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateListSerializer,
    BulkUpdateOrCreateListSerializer,
    serializers,
)


class KachaPakkaConversionRateSerializer(BulkOperationsModelSerializer):
    """Kacha pakka conversion rate serializer class."""

    class Meta:
        model = DfKachaPakkaConversionRate
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "kacha_pakka_conversion_rate",
        }


class AnnualUrbanizationRateSerializer(BulkOperationsModelSerializer):
    """Annual urbanization rate serializer class."""

    class Meta:
        model = DfAnnualUrbanizationRate
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "annual_urbanization_rate",
        }


class AverageFlatSizeSerializer(BulkOperationsModelSerializer):
    """average flat size serializer class."""

    class Meta:
        model = DfAverageFlatSize
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"household_size_rural", "household_size_urban"}


class UrbanRuralHouseholdSizeSerializer(BulkOperationsModelSerializer):
    """urban rural household serializer class."""

    class Meta:
        model = DfUrbanRuralHouseholdSize
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"urban_household_size", "rural_household_size"}


class CementConsumptionSerializer(BulkOperationsModelSerializer):
    """cement consumption serializer class."""

    class Meta:
        model = DfCementConsumptionPerSqFt
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "low_rise_cement_consumption",
            "high_rise_cement_consumption",
        }


class ProjectDbSerializer(BulkOperationsModelSerializer):
    """project db serializer class."""

    class Meta:
        model = DfProjectDatabase
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "project_name",
            "cost",
            "duration",
            "type",
            "cement_value_as_percentage_of_cost",
        }


class DesiredMarketShareSerializer(BulkOperationsModelSerializer):
    """desired market share serializer class."""

    class Meta:
        model = DfDesiredMarketShare
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "desired_market_share",
        }


class GeographicalPresenceSerializer(BulkOperationsModelSerializer):
    """geographical presence serializer class."""

    class Meta:
        model = DfGeographicalPresence
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "geographical_presence",
        }


class SeasonalitySerializer(BulkOperationsModelSerializer):
    """seasonality serializer class."""

    class Meta:
        model = DfSeasonality
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "invoice_date_month",
            "quantity_invoiced",
            "sum_all",
            "total_sum",
            "percentage",
        }


class HighRiseLowRiseSplitSerializer(BulkOperationsModelSerializer):
    """high rise low rise serializer class."""

    class Meta:
        model = DfHighRiseLowRiseSplit
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "number_1_floor",
            "number_2_floor",
            "number_3_to_5_floor",
            "number_5_to_10_floor",
            "number_10_floor",
        }


class DemandForecastRunDtlSerializer(serializers.ModelSerializer):
    """Demand forecast run dtl serializer class."""

    statistical_forecast = serializers.DecimalField(
        max_digits=20, decimal_places=2, default=0.0
    )

    class Meta:
        model = DemandForecastRunDtl
        fields = "__all__"


class DfMacroOutputFinalSerializer(serializers.ModelSerializer):
    """Macro output final serializer class."""

    macro_analysis_output = serializers.DecimalField(
        max_digits=20, decimal_places=2, default=0.0
    )

    class Meta:
        model = DfMacroOutputFinal
        fields = "__all__"


class DfTopDownTargetsSerializer(serializers.ModelSerializer):
    """Top down targets serializer class."""

    top_down_target = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = DfTopDownTargets
        fields = "__all__"


class StateCitiesSerializer(serializers.ModelSerializer):
    """State, cities serializer for kacha-pakka conversion rate."""

    class Meta:
        model = DfKachaPakkaConversionRate
        fields = (
            "state",
            "district",
        )


class ConsensusTargetSerializer(serializers.ModelSerializer):
    """Sales consensus target serializer class."""

    consensus_target__sum = serializers.DecimalField(max_digits=10, decimal_places=2)
    premium_product_target__sum = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )
    other_product_target__sum = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )

    class Meta:
        model = ConsensusTarget
        fields = (
            "consensus_target__sum",
            "zone",
            "state",
            "premium_product_target__sum",
            "other_product_target__sum",
            "nt_poduct_target",
        )


class ConsensusTargetUpdateDownloadSerializer(BulkOperationsModelSerializer):
    """Consensus target update/upload/download serializer class."""

    class Meta:
        model = ConsensusTarget
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "consensus_target",
            "premium_product_target",
            "other_product_target",
            "nt_poduct_target",
        }


class BottomUpTargetsMonthly2Serializer(serializers.ModelSerializer):
    bottom_up_target = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = DfBottomUpTargetsMonthly2
        fields = ("bottom_up_target", "zone", "state")


class SalesTargetMonthlySerializer(serializers.ModelSerializer):
    sales_target = serializers.DecimalField(max_digits=20, decimal_places=2)
    top_down_target = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = SalesTargetMonthly
        fields = ("sales_target", "state", "zone", "top_down_target")


class TdtMultiplierSerializer(BulkOperationsModelSerializer):
    """tdt multiplier data class."""

    class Meta:
        model = TdtMultiplier
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "multiplier",
        }


class MarketMappingMarketPotentialSerializer(BulkOperationsModelSerializer):
    """Market mapping market potential serializer class."""

    class Meta:
        model = MarketMappingMarketPotential
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"month", "sales", "market_potential"}


class MarketMappingGrowthPotentialSerializer(BulkOperationsModelSerializer):
    """Market mapping growth potential serializer class."""

    class Meta:
        model = MarketMappingGrowthPotential
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "state",
            "month",
            "target_type",
            "previous",
            "current",
            "next",
        }

    def get_auto_generated_fields(self):
        return {}


class ConsensusTargetForNtUseSerializer(serializers.ModelSerializer):
    """Sales consensus target serializer class."""

    class Meta:
        model = ConsensusTarget
        fields = "__all__"


class MarketMappingRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingRun
        fields = "__all__"


class MarketMappingStateClassificationListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingStateClassification."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingStateClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingStateClassification
        exclude = ("run",)
        list_serializer_class = MarketMappingStateClassificationListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingDistrictClassificationListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingDistrictClassification."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingDistrictClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingDistrictClassification
        exclude = ("run",)
        list_serializer_class = MarketMappingDistrictClassificationListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingSalesTargetListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingSalesTarget."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingSalesTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingSalesTarget
        exclude = ("run",)
        list_serializer_class = MarketMappingSalesTargetListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingChannelStrategyListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingChannelStrategy."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingChannelStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingChannelStrategy
        exclude = ("run",)
        list_serializer_class = MarketMappingChannelStrategyListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingCounterStrategyListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingCounterStrategy."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingCounterStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingCounterStrategy
        exclude = ("run",)
        list_serializer_class = MarketMappingCounterStrategyListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingBrandingOuputListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingBrandingOuput."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class MarketMappingBrandingOuputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMappingBrandingOuput
        exclude = ("run",)
        list_serializer_class = MarketMappingBrandingOuputListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class MarketMappingPricingOuputSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = MarketMappingPricingOuput
        exclude = ("run",)
        list_serializer_class = BulkCreateListSerializer
        editable_fields = set()

    def create(self, validated_data):
        validated_data["run_id"] = self.context.get("run_id")
        return super().create(validated_data)


class DemandForMarketMappingCreateSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = DemandForMarketMapping
        list_serializer_class = BulkCreateListSerializer
        fields = "__all__"
        editable_fields = set()


class BottomUpTargetsMonthly2CreateSerializer(BulkOperationsModelSerializer):
    """Bottom up target monthly 2 serializer class to create objects."""

    class Meta:
        model = DfBottomUpTargetsMonthly2
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "zone",
            "state",
            "district",
            "taluka",
            "so_name",
            "counter_name",
            "counter_type",
            "brand",
            "product",
            "year",
            "quarter",
            "month",
            "bucket",
            "date",
            "bottom_up_retailer_targets",
        }
        extra_kwargs = {"id": {"read_only": True}}


class BottomUpNtSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    """Bottom up nt serializer class."""

    class Meta:
        model = BottomUpNt
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "state",
            "customer_name",
            "customer_type",
            "year",
            "quarter",
            "month",
            "date",
            "brand",
            "product",
            "pack_type",
            "packaging",
            "cust_category",
            "demand_qty",
        }
        read_only_fields = ("id",)


class UrlMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlMapping
        fields = "__all__"


class DepotAdditionMasterSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = DepotAdditionMaster
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "state",
            "district",
            "taluka",
            "secondary_ptpk",
            "promised_market_sla",
        }


class DepotAdditionOutputSerializer(serializers.ModelSerializer):
    expected_benefit = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = DepotAdditionOutputView
        fields = "__all__"


class ExistingDepotLocationsSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = ExistingDepotLocations
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "state",
            "district",
            "taluka",
            "type",
            "existing_depo_lead",
            "run_id",
            "lat",
            "long",
            "potential",
            "depot_lat",
            "depot_long",
            "depot_name",
        }

        read_only_fields = ("id",)
