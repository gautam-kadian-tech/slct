from django.db import IntegrityError
from rest_framework import serializers

from analytical_data.models import (
    BackhaulingInboundTruck,
    BackhaulingOpportunities,
    LpSchedulingOrderMaster,
)
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class BackhaulingOpportunitiesSerializer(serializers.ModelSerializer):
    lp_scheduling_data = serializers.SerializerMethodField()
    in_bound_truck_data = serializers.SerializerMethodField()

    class Meta:
        model = BackhaulingOpportunities
        fields = "__all__"

    def get_lp_scheduling_data(self, data):
        lp_scheduling_obj = (
            LpSchedulingOrderMaster.objects.filter(id=data.order_master.id)
            .values("order_quantity")
            .first()
        )
        return lp_scheduling_obj

    def get_in_bound_truck_data(self, data):
        in_bound_truck_obj = (
            BackhaulingInboundTruck.objects.filter(id=data.inbound.id)
            .values(
                "plant_id",
                "truck_number",
                "departure_date",
                "vehicle_type",
                "vehicle_size",
                "destination_state",
                "destination_district",
                "destination_city",
            )
            .first()
        )
        return in_bound_truck_obj


# class BackhaulingInboundTruckSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
#     class Meta:
#         model = BackhaulingInboundTruck
#         fields = "__all__"
#         list_serializer_class = BulkUpdateOrCreateListSerializer
#         read_only_fields = ("created_by", "last_updated_by", "last_update_login")
#         editable_fields = {"inv_qty"}


class BackhaulingInboundTruckSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = BackhaulingInboundTruck
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        editable_fields = {
            "plant_id",
            "truck_number",
            "arrival_date",
            "departure_date",
            "vehicle_type",
            "vehicle_size",
            "destination_state",
            "destination_district",
        }


class BackhaulingOpportunitiesListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PpShiftDetails."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class BackhaulingOpportunitiesModelRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackhaulingOpportunities
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = BackhaulingOpportunitiesListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
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
