from rest_framework import serializers

from analytical_data.models.alerts_models import *
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class AlertTransactionSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    alert_name_field = serializers.SerializerMethodField()

    class Meta:
        model = AlertTransaction
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"is_read", "is_active"}
        read_only_fields = ("id",)

    def get_alert_name_field(self, obj):
        alert_id = obj.alert_id
        alert = AlertMaster.objects.filter(id=alert_id).first()
        if alert:
            return alert.alert_name
        return None


class CrmApprovalStageGatesSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = CrmApprovalStageGates
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "approval_type",
            "record_id",
            "is_approved",
            "status",
            "date_time",
        }
        read_only_fields = ("id",)
