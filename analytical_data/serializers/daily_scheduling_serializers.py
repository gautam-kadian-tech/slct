"""Daily scheduling serializers module."""
import json
from datetime import date, datetime

import pytz
import requests
from django.db import IntegrityError
from rest_framework import serializers, status

from analytical_data.enum_classes import ApprovalStatusChoices
from analytical_data.models import (
    ApprovalThreshold,
    BackhaulingProcess,
    DepotAdditionOutputView,
    DepotAdditionRun,
    LpModelDfRank,
    LpSchedulingCrmChecks,
    LpSchedulingDiDetails,
    LpSchedulingExecutableDtl,
    LpSchedulingOrderMaster,
    LpSchedulingPackerConstraints,
    LpSchedulingPlantConstraints,
    LpSchedulingPpCallDtl,
    LpSchedulingVehicleConstraints,
    PackerShiftConstraint,
    PpOrderTagging,
    RouteRestrictions,
    SourceChangeApproval,
    SourceChangeFreightMaster,
    TOebsHrAllOrganizationUnits,
    TOebsSclRouteMaster,
)
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateListSerializer,
    BulkUpdateOrCreateListSerializer,
    OptionChoiceField,
)


class BackhaulingProcessSerializer(serializers.ModelSerializer):
    """Packer shift constraint operations serializer."""

    class Meta:
        model = BackhaulingProcess
        fields = "__all__"


class PackerShiftConstraintSerializer(serializers.ModelSerializer):
    """Packer shift constraint operations serializer."""

    class Meta:
        model = PackerShiftConstraint
        fields = "__all__"


class RouteRestrictionSerializer(serializers.ModelSerializer):
    """Route restriction operations serializer."""

    class Meta:
        model = RouteRestrictions
        fields = "__all__"


class LpSchedulingPackerConstraintSerializer(serializers.ModelSerializer):
    """
    Serializer class for CRUDs on LpSchedulingPackerConstraint model.
    """

    class Meta:
        model = LpSchedulingPackerConstraints
        fields = "__all__"

    def update(self, instance, validated_data):
        # This update doesn't handle any relations, if in future any
        # relations are introduced, then they are needed to be handles.
        packer_available = validated_data.pop("packer_available", None)
        loader_available = validated_data.pop("loader_available", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if packer_available is False:
            LpSchedulingPackerConstraints.objects.filter(
                plant=instance.plant, packer_no=instance.packer_no
            ).update(loader_available=False, packer_available=False)
            instance.loader_available = False
            instance.packer_available = False
        elif packer_available:
            LpSchedulingPackerConstraints.objects.filter(
                plant=instance.plant, packer_no=instance.packer_no
            ).update(packer_available=True)
            instance.loader_available = loader_available
            instance.packer_available = packer_available

        instance.save()
        return instance


class LpSchedulingPlantConstraintSerializer(BulkOperationsModelSerializer):
    """
    Serializer class for CRUDs on LpSchedulingPlantConstraint model.
    """

    class Meta:
        model = LpSchedulingPlantConstraints
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("id",)
        editable_fields = {"capacity", "current_capacity"}

    def update(self, instance, validated_data):
        validated_data.pop("date", None)
        validated_data.pop("plant_id", None)
        validated_data.pop("grade", None)
        return super().update(instance, validated_data)


class LpSchedulingPlantConstraintUploadDownloadSerializer(serializers.ModelSerializer):
    """
    Serializer class for CRUDs on LpSchedulingPlantConstraint model download.
    """

    class Meta:
        model = LpSchedulingPlantConstraints
        exclude = ("current_capacity",)
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"capacity"}


class LpSchedulingVehicleConstraintSerializer(BulkOperationsModelSerializer):
    """
    Serializer class for CRUDs on LpSchedulingVehicleConstraint model.
    """

    class Meta:
        model = LpSchedulingVehicleConstraints
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "no_of_vehicles",
            "vehicle_size",
            "date",
            "vehicle_type",
            "current_vehicles",
        }


class LpSchedulingExecutableDtlSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingExecutableDtl model."""

    class Meta:
        model = LpSchedulingExecutableDtl
        fields = "__all__"


class LpSchedulingPpCallDtlSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingPpCallDtl model."""

    class Meta:
        model = LpSchedulingPpCallDtl
        fields = "__all__"


class LpSchedulingDiDetailsSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingDiDetails model."""

    class Meta:
        model = LpSchedulingDiDetails
        fields = "__all__"


class LpSchedulingCrmChecksSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingCrmChecks model."""

    class Meta:
        model = LpSchedulingCrmChecks
        fields = "__all__"


class BulkLpSchedulingOrderMasterSerializer(serializers.ListSerializer):
    """
    List serializer for LpSchedulingOrderMaster model to implement bulk_update.
    """

    def update(self, instances, validated_data):
        result = list()
        for index, attrs in enumerate(validated_data):
            updated_instance = self.child.update(instances[index], attrs)
            # if not updated_instance._is_updated == 0:
            #     result.append(updated_instance)
            result.append(updated_instance)

        try:
            self.child.Meta.model.objects.bulk_update(
                result,
                fields=[
                    "auto_tagged_source",
                    "auto_tagged_mode",
                    "changed_source",
                    "current_source",
                    "changed_mode",
                    "reason",
                    "transferred_to_depot",
                    "source_change_time",
                ],
            )
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class LpSchedulingOrderMasterSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingOrderMaster model."""

    duration = serializers.SerializerMethodField()
    cost_impact = serializers.SerializerMethodField()
    sla = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    freight = serializers.SerializerMethodField()

    class Meta:
        model = LpSchedulingOrderMaster
        fields = "__all__"
        list_serializer_class = BulkLpSchedulingOrderMasterSerializer
        read_only_fields = (
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
        )

    def update(self, instance, validated_data):
        # allowed_source_and_mode = (
        #     LpSchedulingOrderExecutableDropdownHelper._get_dropdown_data(instance.id)
        # )

        # instance._is_updated = 2
        # if not validated_data.get("auto_tagged_source") in allowed_source_and_mode.get(
        #     "changed_source"
        # ):
        #     instance._is_updated -= 1
        #     validated_data.pop("auto_tagged_source")

        # if not validated_data.get("auto_tagged_mode") in allowed_source_and_mode.get(
        #     "changed_mode"
        # ):
        #     instance._is_updated -= 1
        #     validated_data.pop("auto_tagged_mode")

        instance.changed_source = instance.auto_tagged_source
        instance.changed_mode = instance.auto_tagged_mode
        instance.source_change_time = datetime.now(pytz.timezone("Asia/Kolkata"))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance

    def get_duration(self, obj):
        """Get duration."""
        try:
            return obj.delivery_due_date - date.today()
        except TypeError:
            return "0"

    def get_cost_impact(self, obj):
        """Get cost_impact."""
        return 0

    def get_sla(self, obj):
        distance = getattr(
            TOebsSclRouteMaster.objects.filter(route_id=obj.route).first(),
            "distance",
            0,
        )
        if "FG" in obj.auto_tagged_source:
            return (int(distance) / 25) + 10
        return (int(distance) / 25) + 4

    def get_distance(self, obj):
        return getattr(
            TOebsSclRouteMaster.objects.filter(route_id=obj.route).first(),
            "distance",
            0,
        )

    def get_freight(self, obj):
        return (
            LpModelDfRank.objects.filter(
                plant_id=obj.auto_tagged_source, primary_secondary_route="PRIMARY"
            )
            .order_by("-run_id")
            .values(
                "primary_frt",
                "secondary_frt",
                "variable_production_cost",
                "contribution",
            )
            .first()
        )


class LpSchedulingDiDetailsReadOnlySerializer(LpSchedulingDiDetailsSerializer):
    order_master = LpSchedulingOrderMasterSerializer(read_only=True)


class LpSchedulingOrderMasterUpdateSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingOrderMaster model."""

    class Meta:
        model = LpSchedulingOrderMaster
        fields = "__all__"


class LpSchedulingOrderExecutableSerializer(LpSchedulingOrderMasterSerializer):
    """Daily scheduling order executable serializer."""

    lp_scheduling_crm_checks = LpSchedulingCrmChecksSerializer(
        read_only=True, many=True
    )
    lp_scheduling_executable_dtl = LpSchedulingExecutableDtlSerializer(
        read_only=True, many=True
    )
    lp_scheduling_pp_call_dtl = LpSchedulingPpCallDtlSerializer(
        read_only=True, many=True
    )


class LpSchedulingOrderNonExecutableSerializer(LpSchedulingOrderExecutableSerializer):
    """Daily scheduling order non-executable serializer."""

    color = serializers.SerializerMethodField()

    def get_color(self, obj):
        """Get color."""
        if obj.club_id:
            return self.context.get("colors")[obj.club_id]
        return "FFFFFF"


class PpOrderTaggingGetSerializer(serializers.ModelSerializer):
    """Serializer class for LpSchedulingPpCallDtl model."""

    class Meta:
        model = PpOrderTagging
        fields = ["tl_code"]


class LpSchedulingPpSequenceSerializer(LpSchedulingOrderMasterSerializer):
    """Daily scheduling pp sequence serializer."""

    lp_scheduling_di_details = LpSchedulingDiDetailsSerializer(
        read_only=True, many=True
    )
    lp_scheduling_pp_call_dtl = LpSchedulingPpCallDtlSerializer(
        read_only=True, many=True
    )
    pp_order_tagging = PpOrderTaggingGetSerializer(read_only=True, many=True)


class DepotAdditionRunSerializer(serializers.ModelSerializer):
    """Serializer class for DepotAdditionOutputSerializer model."""

    class Meta:
        model = DepotAdditionRun
        fields = "__all__"


class DepotAdditionOutputViewListSerializer(serializers.ListSerializer):
    """Parent list serializer class for DepotAdditionOutputViewListSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class DepotAdditionOutputViewOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepotAdditionOutputView
        exclude = ("created_by", "last_updated_by", "last_update_login", "run")
        list_serializer_class = DepotAdditionOutputViewListSerializer

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


class DepotAdditionOutputViewSerializer(serializers.ModelSerializer):
    """Serializer class for DepotAdditionOutputView model."""

    class Meta:
        model = DepotAdditionOutputView
        fields = "__all__"


class SourceChangeFreightMasterSerializer(serializers.ModelSerializer):
    """Serializer class for source change freight master model."""

    class Meta:
        model = SourceChangeFreightMaster
        fields = ["incoterm", "freight_term"]


class LpModelDfRankReadOnlySerializer(serializers.ModelSerializer):
    sla = serializers.SerializerMethodField()

    class Meta:
        model = LpModelDfRank
        fields = (
            "sla",
            "primary_frt",
            "secondary_frt",
            "distance",
            "variable_production_cost",
            "contribution",
            "route_id",
        )

    def get_sla(self, obj):
        if "FG" in obj.plant_id:
            return (obj.distance / 25) + 10
        return (obj.distance / 25) + 4


class SourceChangeApprovalListSerializer(BulkUpdateOrCreateListSerializer):
    def update(self, instances, validated_data):
        objects_updated = list()
        order_objects_updated = list()
        try:
            for index, attrs in enumerate(validated_data):
                updated_instance = self.child.update(instances[index], attrs)
                objects_updated.append(updated_instance)

                if updated_instance.status == ApprovalStatusChoices.APPROVED.value:
                    order = updated_instance.order
                    order.changed_source = updated_instance.changed_source
                    order.changed_mode = updated_instance.changed_mode
                    order.source_change_time = datetime.now(
                        pytz.timezone("Asia/Kolkata")
                    )
                    order.current_source = updated_instance.changed_source
                    order.order_executable = False
                    order.changed_inco_terms = updated_instance.changed_inco_terms
                    order.changed_freight_terms = updated_instance.changed_freight_terms
                    order.changed_route_id = updated_instance.changed_route_id
                    order.changed_fob = updated_instance.changed_fob
                    order.changed_run_id_for_changed_source = instances[
                        index
                    ].changed_run_id_for_changed_source
                    order.total_impact = updated_instance.total_impact
                    order_objects_updated.append(order)

                    url = "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/OrderUpdate/OrderUpdate/"
                    if updated_instance.rank.primary_secondary_route == "PRIMARY":
                        source = updated_instance.rank.plant_id
                    else:
                        source = updated_instance.rank.warehouse
                    warehouse = (
                        TOebsHrAllOrganizationUnits.objects.filter(
                            name__startswith=source
                        )
                        .first()
                        .organization_id
                    )
                    erp_payload = {
                        "data": {
                            "PLINE_ID": order.order_line_id,
                            "SHIPINGLOCATION": order.shipinglocation,
                            "WAREHOUSE": warehouse,
                            "FOB": order.fob,
                            "FREIGHTTERMS": order.freightterms,
                            "ROUTE": updated_instance.rank.route_id,
                            "P_USER_CODE": "02039",
                        }
                    }
                    response = requests.post(url, json=erp_payload)
                    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                        raise serializers.ValidationError(
                            "Error in response of ERP API"
                        )
                    if response.status_code == status.HTTP_404_NOT_FOUND:
                        raise serializers.ValidationError(
                            "Error in response of ERP API"
                        )

                    response_body = json.loads(response.content)
                    if response_body.get("STATUS") == "E":
                        raise serializers.ValidationError(
                            f"Error in response of ERP API: {response_body.get('STATUS', '')}"
                        )

            LpSchedulingOrderMaster.objects.bulk_update(
                order_objects_updated,
                fields=[
                    "changed_source",
                    "current_source",
                    "changed_mode",
                    "source_change_time",
                    "changed_inco_terms",
                    "changed_freight_terms",
                    "changed_route_id",
                    "changed_fob",
                    "changed_run_id_for_changed_source",
                    "total_impact",
                    "order_executable",
                ],
            )
            self.child.Meta.model.objects.bulk_update(
                objects_updated,
                fields=[*getattr(self.child.Meta, "editable_fields", None)],
            )
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": f"Data not saved, original exception was: {e}"}
            )
        except IndexError as e:
            raise serializers.ValidationError(
                {
                    "message": f"Some of the IDs provided are not available in the database, original exception was: {e}."
                }
            )

        return objects_updated


class SourceChangeApprovalSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    order = serializers.SlugRelatedField(
        slug_field="id",
        queryset=LpSchedulingOrderMaster.objects.all(),
        write_only=True,
        required=False,
    )
    rank = serializers.SlugRelatedField(
        slug_field="id",
        queryset=LpModelDfRank.objects.all(),
        write_only=True,
        required=False,
    )
    order_data = LpSchedulingOrderMasterSerializer(source="order", read_only=True)
    rank_data = LpModelDfRankReadOnlySerializer(source="rank", read_only=True)
    status = OptionChoiceField(choices=ApprovalStatusChoices.choices)

    class Meta:
        model = SourceChangeApproval
        fields = "__all__"
        list_serializer_class = SourceChangeApprovalListSerializer
        read_only_fields = (
            "last_updated_by",
            "last_update_login",
        )
        editable_fields = {"status", "approver_action_reason"}

    def create(self, validated_data):
        obj = (
            ApprovalThreshold.objects.filter(
                approval=validated_data["approval_type"],
                min__lte=validated_data["contribution"],
                max__gte=validated_data["contribution"],
            )
            .values("persona")
            .first()
        )
        persona = obj["persona"]
        if int(validated_data["contribution"]) > 0:
            print(validated_data["contribution"])
            validated_data["status"] = "APPROVED"
        validated_data["persona"] = persona
        validated_data.pop("approved_at", "")
        validated_data.pop("approver_action_reason", "")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("status") == ApprovalStatusChoices.APPROVED.value:
            validated_data.update(
                {
                    "approved_by": self.context.get("request").user.id,
                    "approved_at": datetime.now(),
                }
            )
        return super().update(instance, validated_data)

    def get_auto_generated_fields(self):
        fields = super().get_auto_generated_fields()
        fields["created_by"] = self.context.get("request").user
        return fields


class LpSchedulingOrderMasterPPCallSerializer(serializers.ModelSerializer):
    """Serializer class for DepotAdditionOutputView model."""

    class Meta:
        model = LpSchedulingOrderMaster
        fields = "__all__"
