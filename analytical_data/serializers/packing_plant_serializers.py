from datetime import date, datetime, timedelta

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from analytical_data.models import (
    BackUnloadingEnrouteMarketsMaster,
    ClinkerDispatchPlan,
    L1SourceMapping,
    LogisticsForecastRun,
    LogisticsForecastRunDtl,
    LpSchedulingDpc,
    LpSchedulingPpCallDtl,
    MvPendingReasonsForDelay,
    PackerBagBurstingDesc,
    PackerRatedCapacity,
    PackerShiftLevelStoppages,
    PackingPlantAacTatReasons,
    PackingPlantBagsStock,
    PackingPlantCementTatReasons,
    PlantDepoSla,
    PlantDepoSlaNew,
    PlantNameChoices,
    PlantStorage,
    PpDowntime,
    PpMaster,
    PpOrderTagging,
    PpRailOrderTagging,
    PpShiftDetails,
    ShiftWiseAdhocPercentage,
    ShiftwiseAdhocQty,
    SourceChangeMode,
    TgtBridgingCost,
    TgtTruckCycleTat,
    TOebsSclRouteMaster,
)
from analytical_data.serializers.custom_serializers import (
    BulkCreateListSerializer,
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkUpdateOrCreateListSerializer,
    OptionChoiceField,
)


class TgtTruckCycleTatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtTruckCycleTat
        fields = "__all__"


class PackingPlantAacTatReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingPlantAacTatReasons
        fields = "__all__"


class PackingPlantCementTatReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingPlantCementTatReasons
        fields = "__all__"


class PlantStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantStorage
        fields = "__all__"
        read_only_fields = [
            "id",
            "product",
            "organization_id",
            "inventory_item_id",
            "org_id",
            "effective_start_date",
            "effective_end_date",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        ]


class PlantDepoSlaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantDepoSla
        fields = "__all__"


class ClinkerDispatchPlanSerializer(serializers.ModelSerializer):
    shipped_from_plant = OptionChoiceField(choices=PlantNameChoices.choices)
    shipped_to_plant = OptionChoiceField(choices=PlantNameChoices.choices)

    class Meta:
        model = ClinkerDispatchPlan
        fields = "__all__"


class PackingPlantBagsStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingPlantBagsStock
        fields = "__all__"


class PackerBagBurstingDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackerBagBurstingDesc
        fields = "__all__"


class PackerShiftLevelStoppagesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackerShiftLevelStoppages
        fields = "__all__"


class PackerShiftLevelStoppagesSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = PackerShiftLevelStoppages
        fields = "__all__"
        list_serializer_class = BulkCreateListSerializer
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        editable_fields = set()

    def create(self, validated_data):
        stoppage_hrs = (
            validated_data["mech_hrs"]
            + validated_data["elec_hrs"]
            + validated_data["inst_hrs"]
            + validated_data["sch_maintainence"]
            + validated_data["mat_extraction"]
            + validated_data["compressor_down"]
            + validated_data["mg_changeover"]
            + validated_data["no_trucks"]
            + validated_data["other_misc"]
            + validated_data["shift_change_or_tea_break_or_truck_placement"]
            + validated_data["other"]
            + validated_data["labour_unavailability"]
        )
        validated_data["stoppage_hrs"] = stoppage_hrs
        return super().create(validated_data)


class ShiftWiseAdhocPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftWiseAdhocPercentage
        read_only_fields = (
            "id",
            "plant",
            "grade",
            "planned_qty",
            "shift",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        fields = "__all__"


class PpMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpMaster
        fields = "__all__"


class PpShiftDetailsListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PpShiftDetails."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class PpShiftDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpShiftDetails
        exclude = ("created_by", "last_updated_by", "last_update_login", "run")
        list_serializer_class = PpShiftDetailsListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )
        # validated_data.update({"created_by":self.context.get("request_user")})

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class PackerRatedCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackerRatedCapacity
        fields = "__all__"


# class PpDowntimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PpDowntime
#         fields = "__all__"


class PpOrderTaggingListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PpShiftDetails."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class PpOrderTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpOrderTagging
        exclude = ("created_by", "last_updated_by", "last_update_login", "run")
        list_serializer_class = PpOrderTaggingListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class PpOrderTaggingViewSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order_master_id.order_id")
    order_line_id = serializers.CharField(source="order_master_id.order_line_id")
    order_date = serializers.CharField(source="order_master_id.order_date")
    brand = serializers.CharField(source="order_master_id.brand")
    grade = serializers.CharField(source="order_master_id.grade")
    packaging = serializers.CharField(source="order_master_id.packaging")
    pack_type = serializers.CharField(source="order_master_id.pack_type")
    order_type = serializers.CharField(source="order_master_id.order_type")
    order_quantity = serializers.CharField(source="order_master_id.order_quantity")
    customer_type = serializers.CharField(source="order_master_id.customer_type")
    cust_sub_cat = serializers.CharField(source="order_master_id.cust_sub_cat")
    cust_name = serializers.CharField(source="order_master_id.cust_name")
    auto_tagged_mode = serializers.CharField(source="order_master_id.auto_tagged_mode")
    dispatch_due_date = serializers.CharField(
        source="order_master_id.dispatch_due_date"
    )
    delivery_id = serializers.CharField(source="order_master_id.delivery_id")
    token_id = serializers.CharField(source="order_master_id.token_id")
    route = serializers.CharField(source="order_master_id.route")
    priority = serializers.SerializerMethodField()

    def get_priority(self, data):
        if LpSchedulingPpCallDtl.objects.filter(
            order_master=data.order_master_id
        ).first():
            return (
                LpSchedulingPpCallDtl.objects.filter(order_master=data.order_master_id)
                .first()
                .pp_calling_sequence
            )
        else:
            return None

    class Meta:
        model = PpOrderTagging
        fields = "__all__"


class LpSchedulingDpcSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = LpSchedulingDpc
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("created_by", "last_updated_by", "last_update_login")
        editable_fields = {"inv_qty"}


class PlantDepoSlaNewSerializer(serializers.ModelSerializer):
    hrs_to_min_threshold = serializers.SerializerMethodField()

    class Meta:
        model = PlantDepoSlaNew
        fields = "__all__"

    def hours_to_minutes(self, tm):
        if tm:
            time = datetime.strptime(tm, "%H:%M")
            minutes = time.hour * 60 + time.minute
            return minutes
        return None

    def get_hrs_to_min_threshold(self, data):
        yard_to_di_link = (
            PlantDepoSlaNew.objects.filter(id=data.id)
            .values(
                "yard_to_di_link",
                "sla_to_di_link",
                "sla_to_dispatch",
                "di_link_to_pp_call",
                "pp_call_to_sec_in",
                "sec_in_to_tare",
                "tare_to_pp_in",
                "pp_in_to_pp_out",
                "pp_out_to_invoice",
                "invoice_to_gross",
                "gross_to_sec_out",
                "sec_out_to_plant_out",
            )
            .first()
        )

        yard_to_di_link_min = self.hours_to_minutes(yard_to_di_link["yard_to_di_link"])
        sla_to_di_link_min = self.hours_to_minutes(yard_to_di_link["sla_to_di_link"])
        sla_to_dispatch_min = self.hours_to_minutes(yard_to_di_link["sla_to_dispatch"])
        di_link_to_pp_call_min = self.hours_to_minutes(
            yard_to_di_link["di_link_to_pp_call"]
        )
        pp_call_to_sec_in_min = self.hours_to_minutes(
            yard_to_di_link["pp_call_to_sec_in"]
        )
        sec_in_to_tare_min = self.hours_to_minutes(yard_to_di_link["sec_in_to_tare"])
        tare_to_pp_in_min = self.hours_to_minutes(yard_to_di_link["tare_to_pp_in"])
        pp_in_to_pp_out_min = self.hours_to_minutes(yard_to_di_link["pp_in_to_pp_out"])
        pp_out_to_invoice_min = self.hours_to_minutes(
            yard_to_di_link["pp_out_to_invoice"]
        )
        invoice_to_gross_min = self.hours_to_minutes(
            yard_to_di_link["invoice_to_gross"]
        )
        gross_to_sec_out_min = self.hours_to_minutes(
            yard_to_di_link["gross_to_sec_out"]
        )
        sec_out_to_plant_out_min = self.hours_to_minutes(
            yard_to_di_link["sec_out_to_plant_out"]
        )

        data = {
            "yard_to_di_link_min": yard_to_di_link_min,
            "sla_to_di_link_min": sla_to_di_link_min,
            "sla_to_dispatch_min": sla_to_dispatch_min,
            "di_link_to_pp_call_min": di_link_to_pp_call_min,
            "pp_call_to_sec_in_min": pp_call_to_sec_in_min,
            "sec_in_to_tare_min": sec_in_to_tare_min,
            "tare_to_pp_in_min": tare_to_pp_in_min,
            "pp_in_to_pp_out_min": pp_in_to_pp_out_min,
            "pp_out_to_invoice_min": pp_out_to_invoice_min,
            "invoice_to_gross_min": invoice_to_gross_min,
            "gross_to_sec_out_min": gross_to_sec_out_min,
            "sec_out_to_plant_out_min": sec_out_to_plant_out_min,
        }
        return data


class ShiftWiseAdhocQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftwiseAdhocQty
        fields = "__all__"


class PpRailOrderTaggingListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PpShiftDetails."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class PpRailOrderTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpRailOrderTagging
        exclude = ("created_by", "last_updated_by", "last_update_login", "run")
        list_serializer_class = PpRailOrderTaggingListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )
        # validated_data.update({"created_by":self.context.get("request_user")})

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


# class PpDowntimeBulkCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PpDowntime
#         list_serializer_class = BulkCreateListSerializer
#         exclude = ("created_by", "last_updated_by", "last_update_login")
#         editable_fields = set()

#     def create(self, validated_data):
#         validated_data.update(
#             {
#                 "created_by": self.context.get("created_by"),
#                 "last_updated_by": self.context.get("created_by"),
#                 "last_update_login": self.context.get("created_by"),
#             }
#         )

#         instance = self.Meta.model(**validated_data)
#         if isinstance(self._kwargs.get("data"), dict):
#             instance.save()

#         return instance


class ShiftWiseAdhocQtyBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftwiseAdhocQty
        list_serializer_class = BulkCreateListSerializer
        exclude = ("created_by", "last_updated_by", "last_update_login")
        editable_fields = set()

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("created_by"),
                "last_updated_by": self.context.get("created_by"),
                "last_update_login": self.context.get("created_by"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


# class ShiftwiseAdhocQtyBulkUpdateSerializer(BulkOperationsModelSerializer):
#     """Shift wise adhoc qty bulk update serializer class."""

#     class Meta:
#         model = ShiftwiseAdhocQty
#         fields = "__all__"
#         list_serializer_class = BulkUpdateListSerializer
#         read_only_fields = (
#             "plant",
#             "brand",
#             "grade",
#             "shift",
#             "planned_qty",
#         )
#         editable_fields = {
#             "adhoc_qty",
#             "rail_planned_qty",
#         }


# class PpDowntimeBulkUpdateSerializer(BulkOperationsModelSerializer):
#     """Pp downtime bulk uupdate serializer class."""

#     class Meta:
#         model = PpDowntime
#         fields = "__all__"
#         list_serializer_class = BulkUpdateListSerializer
#         read_only_fields = (
#             "plant",
#             "shift",
#             "date",
#             "packer",
#             "packer_rated_output",
#             "tl_name",
#             "tl_rated_output",
#         )
#         editable_fields = {
#             "packer_downtime_hrs",
#             "tl_downtime_hrs",
#         }


class MvPendingReasonsForDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MvPendingReasonsForDelay
        fields = "__all__"


class TgtBridgingCostSerializer(serializers.ModelSerializer):
    """Tgt bridging cost model serializer class."""

    class Meta:
        model = TgtBridgingCost
        fields = "__all__"
        read_only_fields = (
            "rake_point",
            "effective_end_date",
            "active_flag",
        )

    def validate(self, attrs):
        past_active_bridging_cost = self.Meta.model.objects.filter(
            route_id=attrs.get("route_id", getattr(self.instance, "route_id", 0)),
            to_org=attrs.get("to_org", getattr(self.instance, "to_org", "")),
            active_flag=1,
        ).first()
        if (
            past_active_bridging_cost
            and attrs.get("effective_start_date")
            <= past_active_bridging_cost.effective_start_date
        ):
            raise serializers.ValidationError(
                {
                    "effective_start_date": "Value can't be less than or equal to last effective start date"
                }
            )
        return attrs

    def create(self, validated_data):
        route_id = get_object_or_404(
            TOebsSclRouteMaster,
            route_id=validated_data.get("route_id"),
            active_flag="Y",
        )
        validated_data.update(
            {
                "route_id": route_id.route_id,
                "rake_point": route_id.to_city,
            }
        )
        return self.update_existing_bridging_cost(validated_data)

    def update(self, instance, validated_data):
        validated_data.update(
            {
                "route_id": instance.route_id,
                "plant": instance.plant,
                "rake_point": instance.rake_point,
                "to_org": instance.to_org,
                "year": instance.year,
            }
        )
        return self.update_existing_bridging_cost(validated_data)

    def update_existing_bridging_cost(self, validated_data):
        queryset = self.Meta.model.objects.filter(
            effective_end_date__isnull=True,
            active_flag=1,
            route_id=validated_data.get("route_id"),
            to_org=validated_data.get("to_org"),
        )

        if validated_data.get("effective_start_date") <= date.today():
            queryset.update(
                effective_end_date=validated_data.get("effective_start_date")
                - timedelta(days=1),
                active_flag=0,
            )
            validated_data["active_flag"] = 1
            return super().create(validated_data)

        queryset.update(
            effective_end_date=validated_data.get("effective_start_date")
            - timedelta(days=1)
        )
        return super().create(validated_data)


class BackUnloadingEnrouteMarketsMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackUnloadingEnrouteMarketsMaster
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request").user.id,
                "last_updated_by": self.context.get("request").user.id,
                "last_update_login": self.context.get("request").user.id,
            }
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.update(
            {
                "last_updated_by": self.context.get("request").user.id,
                "last_update_login": self.context.get("request").user.id,
            }
        )
        return super().update(instance, validated_data)


class TOebsSclRouteMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOebsSclRouteMaster
        fields = "__all__"


class L1SourceMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = L1SourceMapping
        fields = "__all__"


class SourceChangeModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceChangeMode
        fields = "__all__"


class LogisticsForecastRunDtlSerializer(serializers.ModelSerializer):
    run_type = serializers.SerializerMethodField()

    def get_run_type(self, data):
        data = LogisticsForecastRun.objects.filter(run_id=data["run_id"]).values(
            "run_id", "run_type"
        )
        return data

    class Meta:
        model = LogisticsForecastRunDtl
        fields = "__all__"
