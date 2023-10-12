"""Technical head serializer."""
from rest_framework import serializers

from analytical_data.models import (
    CrmAnnualSiteConvPlan,
    CrmAnnualSiteConvPlanMonthly,
    CrmMabRateList,
    CrmMaterialtestCertificate,
    CrmNthActivityPlan,
    CrmNthProductApproval,
    NthBudgetPlan,
    NthBudgetPlanMonthly,
)
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class CrmMaterialtestCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmMaterialtestCertificate
        fields = "__all__"


class CrmAnnualSiteConvPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmAnnualSiteConvPlan
        fields = "__all__"


class CrmNthProductApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthProductApproval
        fields = "__all__"


class CrmNthActivityPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthActivityPlan
        fields = "__all__"


class NthBudgetPlanSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = NthBudgetPlan

        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"activity_plan", "budget"}
        read_only_fields = ("id",)


class CrmMabRateListSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    """Rate list serializer class."""

    class Meta:
        model = CrmMabRateList
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = set()


class CrmAnnualSiteConvPlanMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmAnnualSiteConvPlanMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "site_conversion",
            "volume_generated",
        }
        read_only_fields = ("id",)


class NthBudgetPlanMonthlySerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = NthBudgetPlanMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "activity_plan",
            "budget",
        }
        read_only_fields = ("id",)
