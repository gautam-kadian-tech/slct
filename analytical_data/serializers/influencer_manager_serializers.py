from django.db import IntegrityError
from rest_framework import serializers

from accounts.models import User
from analytical_data.models import (
    AugmentationOutputTable,
    CrmInflAssistReq,
    CrmInflChgReq,
    CrmInflGiftMaster,
    CrmInflGiftScheme,
    CrmInflGiftSchemeItemList,
    CrmInflMgrAnnualPlan,
    CrmInflMgrAnnualPlanMonthly,
    CrmInflMgrMeetPlan,
    CrmInflMgrMeetPlanMonthly,
    CrmInflMgrSchemeBudget,
    CrmInflMgrSchmBdgtActlExp,
    CrmInflScheme,
    CrmInflSchemeProductPoint,
    InfluencerMeetBudgetOutput,
    InfluencerMeetConstrainedRun,
    InfluencerMeetingOutput,
    InfluencerOutput,
    InfluencerTechActivityMaster,
    IntendedAudienceStates,
    InternalCaseResources,
    SclCaseObjects,
    SclCaseStudy,
)
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class SclCaseStudySerializer(serializers.ModelSerializer):
    int_case_res_relation = serializers.SerializerMethodField()
    int_aud_state_relation = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SclCaseStudy
        fields = "__all__"

    def get_int_case_res_relation(self, data):
        int_case_res_relation_obj = InternalCaseResources.objects.filter(
            case=data.id
        ).values("resource_id")
        return int_case_res_relation_obj

    def get_int_aud_state_relation(self, data):
        int_aud_state_obj = IntendedAudienceStates.objects.filter(case=data.id).values(
            "state_code"
        )
        return int_aud_state_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class InternalCaseResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalCaseResources
        fields = "__all__"


class IntendedAudienceStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntendedAudienceStates
        fields = "__all__"


class SclCaseObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SclCaseObjects
        fields = "__all__"


class CrmInflAssistReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflAssistReq
        fields = "__all__"


class CrmInflChgReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflChgReq
        fields = "__all__"


class CrmInflMgrAnnualPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflMgrAnnualPlan
        fields = "__all__"


class CrmInflMgrMeetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflMgrMeetPlan
        fields = "__all__"


class CrmInflMgrSchemeBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflMgrSchemeBudget
        fields = "__all__"


class CrmInflMgrSchmBdgtActlExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflMgrSchmBdgtActlExp
        fields = "__all__"


class InfluencerMeetConstrainedRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerMeetConstrainedRun
        fields = "__all__"


class InfluencerMeetingOutputListSerializer(serializers.ListSerializer):
    """Parent list serializer class for InfluencerMeetingOut."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class InfluencerMeetingOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerMeetingOutput
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = InfluencerMeetingOutputListSerializer

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


class InfluencerMeetBudgetOutputListSerializer(serializers.ListSerializer):
    """Parent list serializer class for InfluencerMeetBudgetOutputListSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class InfluencerMeetBudgetOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerMeetBudgetOutput
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = InfluencerMeetBudgetOutputListSerializer

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


class InfluencerOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerMeetingOutput
        # fields = "__all__"
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            "creation_date",
            "last_update_date",
            "id",
        )


class InfluencerMeetBudgetOutputGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerMeetBudgetOutput
        fields = ("id", "no_meetings", "total_budget")


class AugmentationOutputTableListSerializer(serializers.ListSerializer):
    """Parent list serializer class for AugmentationOutputTableListSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class AugmentationOutputTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AugmentationOutputTable
        exclude = ()
        list_serializer_class = AugmentationOutputTableListSerializer

    def create(self, validated_data):
        # validated_data.update(
        #     {
        #         "created_by": self.context.get("request_user"),
        #         "last_updated_by": self.context.get("request_user"),
        #         "last_update_login": self.context.get("request_user"),
        #     }
        # )
        # validated_data.update({"created_by":self.context.get("request_user")})

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class AugmentationOutputTableDownloadSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = AugmentationOutputTable
        fields = "__all__"
        editable_fields = set()
        list_serializer_class = BulkUpdateOrCreateListSerializer


class InfluencerTechActivityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerTechActivityMaster
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


class CrmInflSchemeSerializer(serializers.ModelSerializer):
    product_points = serializers.SerializerMethodField()

    class Meta:
        model = CrmInflScheme
        fields = "__all__"

    def get_product_points(self, data):
        product_point_obj = CrmInflSchemeProductPoint.objects.filter(
            scheme__id=data.id
        ).values("product", "points_per_bag")
        return product_point_obj


class CrmInflGiftMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmInflGiftMaster
        fields = "__all__"


class CrmInflGiftSchemeSerializer(serializers.ModelSerializer):
    item_list = serializers.SerializerMethodField()

    class Meta:
        model = CrmInflGiftMaster
        fields = "__all__"

    def get_item_list(self, data):
        gift_scheme_obj = CrmInflGiftSchemeItemList.objects.filter(
            gift_scheme__id=data.id
        ).values("item_id", "item_name", "points_per_item", "status")
        return gift_scheme_obj


class CrmInflMgrMeetPlanMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmInflMgrMeetPlanMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "meet_budget",
            "no_of_meets",
        }
        read_only_fields = ("id",)


class CrmInflMgrAnnualPlanMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmInflMgrAnnualPlanMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "registration_plan",
            "contribution_plan",
        }
        read_only_fields = ("id",)


class CrmInflMgrMeetPlanDownloadUploadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmInflMgrMeetPlan
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            "creation_date",
            "last_update_date",
        )
        editable_fields = {
            "state",
            "district",
            "plan",
            "influencer_type",
        }
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("id",)


class CrmInflMgrAnnualPlanDownloadUploadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmInflMgrAnnualPlan
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            "creation_date",
            "last_update_date",
        )
        editable_fields = {
            "state",
            "district",
            "plan",
            "influencer_type",
        }
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("id",)
