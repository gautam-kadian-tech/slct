from rest_framework import serializers

from analytical_data.models.marketing_branding_models import (
    CrmMabBrandingAppr,
    CrmMabBtlPlanning,
    CrmMabInitReq,
    CrmMabPastRequisitions,
    MarketMappingBrandingBudget,
    NewMarketPricingApproval,
    SponsorshipBudget,
    VendorDetailMaster,
)
from analytical_data.models.state_head_models import BrandingActivity

from .custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateListSerializer,
    BulkUpdateOrCreateListSerializer,
)


class CrmMabBrandingApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmMabBrandingAppr
        fields = "__all__"


class CrmMabBtlPlanningSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = CrmMabBtlPlanning
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
            "branding_activity",
            "branding_budget_last_year",
            "branding_expense_last_year",
            "branding_budget_curr_year",
            "recommend_matrix",
            "activities_count",
            "status",
        }
        read_only_fields = ("id",)


class CrmMabBtlPlanningGetByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmMabBtlPlanning
        fields = "__all__"


class CrmMabPastRequisitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmMabPastRequisitions
        fields = "__all__"


class CrmMabInitReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmMabInitReq
        fields = "__all__"


class VendorDetailMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetailMaster
        fields = "__all__"


class BrandingActivitySerializer(serializers.ModelSerializer):
    additional = serializers.SerializerMethodField()

    class Meta:
        model = BrandingActivity
        fields = "__all__"

    def get_additional(self, data):
        init_req_obj = CrmMabInitReq.objects.filter(branding_activity=data.id).values(
            "upload_doc",
            "photo_before_brand",
            "additional_comment",
            "photo_after_brand",
            "objective_actual",
            "comment_by_nsh",
            "comment_by_cbt",
            "comment_by_lbt",
        )
        return init_req_obj


class MarketMappingBrandingBudgetSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = MarketMappingBrandingBudget
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"tot_cost_rs_lac", "change_tot_cost_rs_lac", "status"}


class SponsorshipBudgetSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = SponsorshipBudget
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "budget",
            "comment_approved_by",
            "raised_by",
            "comment_raised_by",
            "status",
        }
        read_only_fields = ("id",)


class SponsorshipBudgetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorshipBudget
        fields = "__all__"


class NewMarketPricingApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMarketPricingApproval
        fields = "__all__"
