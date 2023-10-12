"""Analytical data monthly scheduling serializers module."""
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum, Value
from django.db.models.functions import Concat
from rest_framework import serializers

from analytical_data.models import (
    ClinkerDemandRun,
    ClinkerLinksMaster,
    Demand,
    DjpCounterScore,
    DjpRouteScore,
    DjpRun,
    FreightMaster,
    GdWharfageRunInput,
    GodownMaster,
    LinksMaster,
    LpMinCapacity,
    LpModelDfFnl,
    LpModelDfRank,
    LpModelRun,
    LpTargetSetting,
    PackagingMaster,
    PackerConstraintsMaster,
    PlantConstraintsMaster,
    PlantNameChoices,
    PlantProductsMaster,
    PriceMaster,
    RailHandling,
    ServiceLevelSla,
    TgtPlantLookup,
    TOebsHrAllOrganizationUnits,
    TOebsSclAddressLink,
    VehicleAvailability,
)
from analytical_data.serializers.custom_serializers import (
    BulkCreateListSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateListSerializer,
    BulkUpdateOrCreateListSerializer,
    OptionChoiceField,
)

User = get_user_model()


class DemandSerializer(serializers.ModelSerializer):
    """Demand list serializer."""

    city = serializers.CharField(source="destination.city")
    district = serializers.CharField(source="destination.district")
    state = serializers.CharField(source="destination.state")

    class Meta:
        model = Demand
        exclude = ("destination",)


class GodownMasterSerializer(serializers.ModelSerializer):
    """Godown master operations serializer."""

    class Meta:
        model = GodownMaster
        fields = "__all__"


class LinksMasterListSerializer(BulkUpdateListSerializer):
    def update(self, instances, validated_data):
        updated_instances = super().update(instances, validated_data)

        freight_master_objs = [
            instance.freight_master for instance in updated_instances
        ]

        try:
            FreightMaster.objects.bulk_update(
                freight_master_objs, fields=["notional_freight", "demurrage", "damages"]
            )
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return updated_instances


class LinksMasterSerializer(BulkOperationsModelSerializer):
    """Links master operations serializer."""

    primary_frt = serializers.DecimalField(
        source="freight_master.primary_frt", max_digits=20, decimal_places=2
    )
    secondary_frt = serializers.DecimalField(
        source="freight_master.secondary_frt", max_digits=20, decimal_places=2
    )
    rake_charges = serializers.DecimalField(
        source="freight_master.rake_charges", max_digits=20, decimal_places=2
    )
    notional_freight = serializers.DecimalField(
        source="freight_master.notional_freight",
        max_digits=20,
        decimal_places=2,
        allow_null=True,
    )
    demurrage = serializers.DecimalField(
        source="freight_master.demurrage",
        max_digits=20,
        decimal_places=2,
        allow_null=True,
    )
    damages = serializers.DecimalField(
        source="freight_master.damages",
        max_digits=20,
        decimal_places=2,
        allow_null=True,
    )

    class Meta:
        model = LinksMaster
        fields = "__all__"
        list_serializer_class = LinksMasterListSerializer
        editable_fields = {
            "is_active",
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in validated_data.get("freight_master", {}).items():
            setattr(instance.freight_master, attr, value)

        if isinstance(self._kwargs.get("data"), dict):
            instance.freight_master.save()

        return instance


class PlantDispatchPlanSerializer(serializers.ModelSerializer):
    """Plant dispatch plant serializer class."""

    capacity = serializers.DecimalField(max_digits=10, decimal_places=2)
    source = serializers.CharField(source="plant_id")
    utilization = serializers.DecimalField(max_digits=10, decimal_places=2)
    dispatch = serializers.DecimalField(
        source="qty__sum", max_digits=10, decimal_places=2
    )

    class Meta:
        model = PlantProductsMaster
        fields = ("capacity", "source", "utilization", "dispatch", "grade")


# class ClinkerALlocationSerializer(serializers.ModelSerializer):
#     """Clinker Allocation serializer class."""

#     quantity_lf = serializers.DecimalField(decimal_places=2, max_digits=10)
#     quantity = serializers.DecimalField(decimal_places=2, max_digits=10)

#     class Meta:
#         model = LpModelDfFnl
#         fields = ("plant_id", "clinker_plant", "quantity", "quantity_lf")


class DeactivateLinksMasterSerializer(serializers.ModelSerializer):
    """Activate/Deactivate LinkMaster model class objects."""

    notional_freight = serializers.DecimalField(
        source="freight_master.notional_freight",
        max_digits=20,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = LinksMaster
        fields = ("is_active", "notional_freight")

    def update(self, instance, validated_data):
        for key, value in validated_data.pop("freight_master", {}):
            setattr(instance.freight_master, key, value)
        instance.freight_master.save()
        return super().update(instance, validated_data)


class LinksMasterStateSerializer(serializers.ModelSerializer):
    """
    Links master destination district, city, state listing serializer.
    """

    class Meta:
        model = LinksMaster
        fields = ("destination_district", "destination_city", "destination_state")


class PackagingMasterSerializer(BulkOperationsModelSerializer):
    """Packaging master operations serializer."""

    class Meta:
        model = PackagingMaster
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "plant_id",
            "brand",
            "product",
            "packaging",
        )
        editable_fields = {
            "cost",
        }


class PackerConstraintsSerializer(serializers.ModelSerializer):
    """Packer constraints master operations serializer."""

    class Meta:
        model = PackerConstraintsMaster
        fields = "__all__"


class PlantConstraintsSerializer(serializers.ModelSerializer):
    """Plant constraints master serializer."""

    class Meta:
        model = PlantConstraintsMaster
        fields = "__all__"


class PlantProductsSerializer(BulkOperationsModelSerializer):
    """Plant product master operations serializer."""

    class Meta:
        model = PlantProductsMaster
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "plant_id",
            "grade",
        )
        editable_fields = {
            "quantity",
            "clinker_cf",
            "variable_production_cost",
            "min_inventory",
            "silo_capacity",
        }


class PriceMasterSerializer(BulkOperationsModelSerializer):
    """Price master operations serializer."""

    city = serializers.CharField(source="destination.city")
    district = serializers.CharField(source="destination.district")
    state = serializers.CharField(source="destination.state")

    class Meta:
        model = PriceMaster
        fields = (
            "cust_category",
            "brand",
            "grade",
            "packaging",
            "price",
            "created_at",
            "updated_at",
            "pack_type",
            "ha_commission",
            "discount",
            "taxes",
            "sp_commission",
            "isp_commission",
            "misc_charges",
            "city",
            "district",
            "state",
            "id",
        )
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "id",
            "cust_category",
            "brand",
            "grade",
            "packaging",
            "pack_type",
            "isp_commission",
        )
        editable_fields = {
            "price",
            "ha_commission",
            "discount",
            "taxes",
            "sp_commission",
            "misc_charges",
        }


class ServiceLevelSlaSerializer(BulkOperationsModelSerializer):
    """ServiceLevelSla model operations serializer."""

    city = serializers.CharField(source="destination.city")
    district = serializers.CharField(source="destination.district")
    state = serializers.CharField(source="destination.state")

    class Meta:
        model = ServiceLevelSla
        exclude = ("destination",)
        list_serializer_class = BulkUpdateListSerializer
        editable_fields = {"sla", "destination"}

    def validate(self, attrs):
        attrs = super().validate(attrs)

        destination = attrs.get("destination", {})
        if destination:
            city = destination.get("city", None)
            district = destination.get("district", None)
            state = destination.get("state", None)
            attrs["destination"] = TOebsSclAddressLink.objects.filter(
                city=city, district=district, state=state
            ).first()
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class VehicleAvailabilitySerializer(BulkOperationsModelSerializer):
    """Vehicle availability operations serializer."""

    class Meta:
        model = VehicleAvailability
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        # read_only_fields = ("plant_id",)
        editable_fields = {
            "plant_id",
            "state",
            "district",
            "city",
            "mode",
            "vehicle_type",
            "grade",
            "cust_category",
            "pack_type",
            "quantity",
        }


class LpModelRunSerializer(serializers.ModelSerializer):
    """LpModelRun operations serializer."""

    def validate(self, attrs):
        try:
            if not Demand.objects.filter(month=attrs["plan_date"]).exists():
                raise serializers.ValidationError(
                    "Demand is not available for selected month"
                )
        except KeyError:
            pass
        return attrs

    class Meta:
        model = LpModelRun
        fields = "__all__"


class GdWharfageRunInputserializer(serializers.ModelSerializer):
    class Meta:
        model = GdWharfageRunInput
        fields = "__all__"


class LpModelDfRankCreateSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = LpModelDfRank
        fields = "__all__"
        editable_fields = set()
        list_serializer_class = BulkCreateListSerializer


class BulkCreateLpModelDfFnlListSerializer(serializers.ListSerializer):
    """
    List serializer for LpModelDfFnl model to implement bulk_create.
    """

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class LpModelDfFnlSerializer(serializers.ModelSerializer):
    """LpModelDfFnl model operations serializer."""

    class Meta:
        model = LpModelDfFnl
        exclude = ("plant_products_master",)
        list_serializer_class = BulkCreateLpModelDfFnlListSerializer

    def create(self, validated_data):
        validated_data.update({"run_id": self.context.get("run_id")})

        instance = LpModelDfFnl(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class LpModelDfRankSerializer(serializers.ModelSerializer):
    """Lp model df rank model serializer."""

    tlc = serializers.SerializerMethodField()
    planned_source = serializers.SerializerMethodField()
    warehouse_id = serializers.SerializerMethodField()
    w_house = None

    def get_planned_source(self, data):
        obj_planned_source = LpModelDfRank.objects.filter(id=data.id).values(
            "warehouse", "plant_id"
        )

        for keys in obj_planned_source:
            if keys["warehouse"] == "":
                self.w_house = keys["plant_id"]
                return keys["plant_id"]
            else:
                self.w_house = keys["warehouse"]
                return keys["warehouse"]

    def get_tlc(self, data):
        obj_tlc = LpModelDfRank.objects.filter(id=data.id).values(
            "primary_frt",
            "secondary_frt",
            "ha_commission",
            "rake_charges",
            "demurrage",
            "damages",
            "direct_plant_discount",
            "fiscal_benefit_amt",
        )

        for keys in obj_tlc:
            if keys["primary_frt"] is not None:
                keys["primary_frt"] = int(keys["primary_frt"])
            else:
                keys["primary_frt"] = 0

            if keys["secondary_frt"] is not None:
                keys["secondary_frt"] = int(keys["secondary_frt"])
            else:
                keys["secondary_frt"] = 0

            if keys["fiscal_benefit_amt"] is not None:
                keys["fiscal_benefit_amt"] = int(keys["fiscal_benefit_amt"])
            else:
                keys["fiscal_benefit_amt"] = 0

            if keys["rake_charges"] is not None:
                keys["rake_charges"] = int(keys["rake_charges"])
            else:
                keys["rake_charges"] = 0

            if keys["demurrage"] is not None:
                keys["demurrage"] = int(keys["demurrage"])
            else:
                keys["demurrage"] = 0

            if keys["damages"] is not None:
                keys["damages"] = int(keys["damages"])
            else:
                keys["damages"] = 0

            if keys["direct_plant_discount"] is not None:
                keys["direct_plant_discount"] = int(keys["direct_plant_discount"])
            else:
                keys["direct_plant_discount"] = 0

            tlc_calc_obj = (
                keys["primary_frt"]
                + keys["secondary_frt"]
                + keys["ha_commission"]
                + keys["rake_charges"]
                + keys["demurrage"]
                + keys["damages"]
                + keys["direct_plant_discount"]
                + keys["fiscal_benefit_amt"]
            )
            return tlc_calc_obj

    def get_warehouse_id(self, data):
        if self.w_house != None:
            warehouse_obj = TOebsHrAllOrganizationUnits.objects.filter(
                name__startswith=self.w_house
            ).first()
            if warehouse_obj != None:
                warehouse_id_obj = warehouse_obj.organization_id
            else:
                warehouse_id_obj = None

        else:
            warehouse_id_obj = None

        return warehouse_id_obj

    class Meta:
        model = LpModelDfRank
        fields = (
            "contribution",
            "route_id_secondary",
            "planned_source",
            "mode",
            "rank",
            "tlc",
            "route_id",
            "from_city_id",
            "node_city_id",
            "freight_type",
            "warehouse_id",
        )


class RakeTransferSerializer(LpModelDfFnlSerializer):
    """Rake transfer details serializer."""

    total_qty = serializers.DecimalField(max_digits=20, decimal_places=2)


class ClinkerLinksMasterSerializer(BulkOperationsModelSerializer):
    """Clinker links master serializer class."""

    class Meta:
        model = ClinkerLinksMaster
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "fg_whse",
            "fc_whse",
            "mode_of_transport",
        )
        editable_fields = {
            "is_active",
            "clinker_bridging_loading",
            "clinker_bridging_unloading",
            "clinker_notional_freight",
        }


class DjpCounterScoreSerializer(serializers.ModelSerializer):
    """Djp counter score serializer class."""

    class Meta:
        model = DjpCounterScore
        fields = "__all__"


class DjpRouteScoreSerializer(serializers.ModelSerializer):
    """Djp route score serializer class."""

    class Meta:
        model = DjpRouteScore
        fields = "__all__"


class DjpRunSerializer(serializers.ModelSerializer):
    """Djp run serializer class."""

    djp_route_score = DjpRouteScoreSerializer(read_only=True, many=True)
    djp_counter_score = DjpCounterScoreSerializer(read_only=True, many=True)

    class Meta:
        model = DjpRun
        fields = "__all__"


class LpTargetSettingSerializer(BulkOperationsModelSerializer):
    """LpTargetSetting Serializer class."""

    class Meta:
        model = LpTargetSetting
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("id",)
        editable_fields = {
            "state",
            "district",
            "freight_type",
            "target",
        }

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.state_district_target = dict(
            LpTargetSetting.objects.values("state", "district")
            .annotate(
                state_district=Concat("state", Value("_"), "district"),
                target=Sum("target"),
            )
            .values_list("state_district", "target")
        )

    def update(self, instance, validated_data):
        validated_target = validated_data.get("target", instance.target)
        total_state_district_target = self.state_district_target.get(
            f"{instance.state}_{instance.district}", instance.target
        )
        individual_state_district_target = total_state_district_target - instance.target

        if individual_state_district_target + validated_target > 100:
            raise serializers.ValidationError({"target": ["Target exceeds value 100."]})

        return super().update(instance, validated_data)


class ClinkerDemandRunListSerializer(serializers.ListSerializer):
    """Parent list serializer class for ClinkerDemandRunSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class ClinkerDemandRunSerializer(serializers.ModelSerializer):
    """ClinkerDemandRun Serializer class."""

    class Meta:
        model = ClinkerDemandRun
        fields = "__all__"
        list_serializer_class = ClinkerDemandRunListSerializer

    def create(self, validated_data):
        validated_data.update({"run_id": self.context.get("run_id")})

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class RailHandlingSerializer(BulkOperationsModelSerializer):
    """Rail handling serializer class."""

    class Meta:
        model = RailHandling
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "city",
            "state",
            "district",
            "taluka",
            "depot",
            "brand",
            "packing",
            "freight_type",
            "mode",
        )
        editable_fields = {
            "ha_commission",
        }


class LpMinCapacitySerializer(serializers.ModelSerializer):
    """lp min capacity serializer class."""

    class Meta:
        model = LpMinCapacity
        fields = "__all__"


class GetClinkerDemandRunDataSerializer(serializers.ModelSerializer):
    fc_whse = OptionChoiceField(choices=PlantNameChoices.choices)
    plant_id_1 = OptionChoiceField(choices=PlantNameChoices.choices)

    class Meta:
        model = ClinkerDemandRun
        fields = "__all__"


class TgtPlantLookupSerializer(serializers.ModelSerializer):
    org = OptionChoiceField(choices=PlantNameChoices.choices)

    class Meta:
        model = TgtPlantLookup
        fields = ("org",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data.get("org")
