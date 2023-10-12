"""Analytical data non-trade head serializers module."""
from django.db import IntegrityError
from rest_framework import serializers

from analytical_data.models import (
    BottomUpNt,
    CrmNthBankGuartAppr,
    CrmNthCustCodeCre,
    CrmNthExtendValidity,
    CrmNthLeadForm,
    CrmNthOrderCancAppr,
    CrmNthQuotNcrExcpAppr,
    CrmNthRefuReq,
    CrmNthSoNcrExcpAppr,
    CrmNthSourceChgReq,
    DimAccountType,
    DimCustomersTest,
    DimPeriod,
    DimProjectDetails,
    DimResources,
    FactBrandApproval,
    FactNtSalesPlanAnnual,
    FactNtSalesPlanning,
    FactNtSalesPlanningMonth,
    FactNtSalesPlanningNcr,
    MonthlyTargetSetting,
    NonTradeSalesPlanningAccount,
    NonTradeSalesPlanningAccountMonthly,
    NonTradeSalesPlanningDesignation,
    NonTradeSalesPlanningDesignationMonthly,
    NonTradeSalesPlanningMonthlyNcrTarget,
    NonTradeSalesPlanningProduct,
    NonTradeSalesPlanningProductMonthly,
    NonTradeSalesPlanningState,
    NonTradeSalesPlanningStateMonthly,
    NonTradeTopDownMonthlyTarget,
    NshNonTradeSales,
    NtAccRelation,
    NtCommsNotified,
    NtCreditLimit,
    NtMarketTarget,
    NtNcrThreshold,
    NtNotesComms,
    NtResourceTarget,
    SclHierarchyMaster,
    TOebsHzCustAccounts,
    TOebsSclArNcrAdvanceCalcTab,
    TpcCustomerMapping,
)
from analytical_data.serializers.custom_serializers import (
    BulkCreateListSerializer,
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class TOebsHzCustAccountsSerializer(serializers.ModelSerializer):
    """T_OEBS_HZ_CUST_ACCOUNTS serializer class."""

    mh_code = serializers.CharField(source="attribute3.mh_code")
    mh_name = serializers.CharField(source="attribute3.mh_name")
    # party_name = serializers.CharField(source="rec_link_id.party_name")

    class Meta:
        modes = TOebsHzCustAccounts
        fields = (
            "party_id",
            # "party_name",
            "mh_code",
            "mh_name",
        )


class NtCreditLimitCreateSerializer(serializers.ModelSerializer):
    """CREDIT_LIMIT_NT serializer create class."""

    cust = serializers.SlugRelatedField(
        slug_field="id", queryset=DimCustomersTest.objects.all()
    )

    class Meta:
        model = NtCreditLimit
        exclude = (
            "status",
            "account_number",
            "created_by",
            "last_updated_by",
            "last_update_login",
        )

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {
                "created_by": user_id,
                "last_updated_by": user_id,
                "last_update_login": user_id,
            }
        )
        # return super().create(validated_data)

        instance, created = self.Meta.model.objects.update_or_create(
            cust=validated_data.get("cust"), defaults=validated_data
        )
        return instance


class DimProjectSerializer(serializers.ModelSerializer):
    """Dim project details serializer class."""

    class Meta:
        model = DimProjectDetails
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True},
            "last_updated_by": {"read_only": True},
            "last_update_login": {"read_only": True},
        }


class DimCustomersSerializer(serializers.ModelSerializer):
    """Dim customers serializer class."""

    class Meta:
        model = DimCustomersTest
        # fields = "__all__"
        fields = ("party_id", "party_name", "cust_account_id")


class CreditLimitNtSerializer(serializers.ModelSerializer):
    """CREDIT_LIMIT_NT serializer list and update class."""

    cust = DimCustomersSerializer()
    nt_acc_relation = serializers.SerializerMethodField()
    parent_customer_type = serializers.SerializerMethodField()

    class Meta:
        model = NtCreditLimit
        fields = "__all__"
        read_only_fields = (
            "credit_limit_id",
            "cust",
            "account_number",
            "nt_acc_relation",
            "reason_for_escalation",
        )

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {"last_updated_by": user_id, "last_update_login": user_id}
        )
        return super().update(instance, validated_data)

    def __get_nt_acc_relation_query(self, obj, designation):
        account_type_code = self.context.get("account_type_code")
        if account_type_code:
            return obj.cust.acc_relations.filter(
                resource__designation=designation,
                account_type__acct_type_code=account_type_code,
            )[:1]
        else:
            return obj.cust.acc_relations.filter(
                account_type__acct_type_code=account_type_code
            )[:1]

    def get_nt_acc_relation(self, obj):
        acc_relations_data = (
            self.__get_nt_acc_relation_query(obj, "TPC")
            | self.__get_nt_acc_relation_query(obj, "KAM")
            | self.__get_nt_acc_relation_query(obj, "NTSO")
        )
        return NtAccRelationSerializer(acc_relations_data, many=True).data

    def get_parent_customer_type(self, obj):
        try:
            return (
                obj.cust.acc_relations.order_by("-creation_date")
                .first()
                .account_type.acct_type_code
            )
        except:
            return None


class NtCreditLimitChangeStatusSerializer(serializers.ModelSerializer):
    credit_limit_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = NtCreditLimit
        fields = ("status", "credit_limit_ids")


class DimResourcesSerializer(serializers.ModelSerializer):
    """Dim resources(NTSOs List) serializer class."""

    class Meta:
        model = DimResources
        fields = "__all__"


class BrandApprovalSerializer(serializers.ModelSerializer):
    """Brand approval serializer class."""

    customer_id = DimCustomersSerializer()
    project_key = DimProjectSerializer()
    assignee_key = serializers.SlugRelatedField(
        slug_field="id", queryset=DimResources.objects.all()
    )

    class Meta:
        model = FactBrandApproval
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True},
            "last_update_login": {"read_only": True},
            "last_updated_by": {"read_only": True},
        }

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        auto_generated_fields = {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }

        customer_details = validated_data.pop("customer_id")
        customer_obj = DimCustomersTest(**customer_details)
        customer_obj.save()

        project_details = validated_data.pop("project_key")
        project_obj = DimProjectDetails(**project_details, **auto_generated_fields)
        project_obj.save()

        validated_data.update(
            {
                **auto_generated_fields,
                **{
                    "customer_id": customer_obj,
                    "project_key": project_obj,
                    "document": self.context.get("attachment"),
                },
            }
        )

        if validated_data.get("document") and validated_data.get("assignee_key"):
            validated_data["status"] = "Document Uploaded"
        elif not validated_data.get("document") and validated_data.get("assignee_key"):
            validated_data["status"] = "NTSO Assigned"
        else:
            validated_data["status"] = "New Request"
        return super().create(validated_data)

    def update(self, instance, validated_data):
        project_data = validated_data.pop("project_key", {})
        customer_data = validated_data.pop("customer_id", {})

        if self.context.get("attachment"):
            validated_data.update({"document": self.context.get("attachment")})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for attr, value in customer_data.items():
            setattr(instance.customer_id, attr, value)

        for attr, value in project_data.items():
            setattr(instance.project_key, attr, value)

        if instance.document and instance.assignee_key:
            instance.status = "Document Uploaded"
        elif not instance.document and instance.assignee_key:
            instance.status = "NTSO Assigned"
        else:
            instance.status = "New Request"

        instance.customer_id.save()
        instance.project_key.save()
        instance.save()
        return instance


class NtNotesCommsSerializer(serializers.ModelSerializer):
    """NT_NOTES_COMMS serializer class."""

    notified_to = serializers.SerializerMethodField()

    class Meta:
        model = NtNotesComms
        exclude = ("created_by", "last_updated_by", "last_update_login")

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {
                "type": "Note",
                "created_by": user_id,
                "last_updated_by": user_id,
                "last_update_login": user_id,
                "attachment": self.context.get("attachment"),
            }
        )
        return super().create(validated_data)

    def get_notified_to(self, obj):
        return obj.communication_notifies.values_list(
            "notified_to__resource_name", "notified_to__id"
        )


class NtNcrThresholdSerializer(serializers.ModelSerializer):
    """NT_NCR_THRESHOLD serializer class."""

    class Meta:
        model = NtNcrThreshold
        fields = "__all__"

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        auto_incrementing_fields = {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
        validated_data.update(auto_incrementing_fields)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DimAccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimAccountType
        fields = ("id", "acct_type_code", "account_name")


class NtAccRelationListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        objects_list = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(objects_list)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return objects_list


class ParentAccountSerializer(serializers.ModelSerializer):
    """Parent account serializer class."""

    resource_name = serializers.SerializerMethodField()

    def get_resource_name(self, data):
        return (
            NtAccRelation.objects.filter(parent_id=data)
            .values_list("resource__resource_name", "id")
            .first()
        )

    class Meta:
        model = NtAccRelation
        fields = ("id", "resource_name")


class NtAccRelationSerializer(serializers.ModelSerializer):
    """Non-trade account relations serializer class."""

    resource = DimResourcesSerializer()
    account_type = DimAccountTypeSerializer()
    cust = DimCustomersSerializer(read_only=True)
    parent_id = ParentAccountSerializer()

    class Meta:
        model = NtAccRelation
        exclude = ("created_by", "last_updated_by", "last_update_login")

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {
                "created_by": user_id,
                "last_updated_by": user_id,
                "last_update_login": user_id,
            }
        )
        customer = DimCustomersTest(**validated_data.pop("cust"))
        customer.save()
        validated_data.update({"cust": customer})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {
                "last_updated_by": user_id,
                "last_update_login": user_id,
            }
        )
        return super().update(instance, validated_data)


class TransferAccountsSerializer(serializers.ModelSerializer):
    """Non-trade account relations serializer class."""

    resource = serializers.SlugRelatedField(
        slug_field="id", queryset=DimResources.objects.all()
    )
    cust = serializers.SlugRelatedField(
        slug_field="id", queryset=DimCustomersTest.objects.all()
    )
    account_type = serializers.SlugRelatedField(
        slug_field="id", queryset=DimAccountType.objects.all()
    )

    class Meta:
        model = NtAccRelation

        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = NtAccRelationListSerializer

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        validated_data.update(
            {
                "created_by": user_id,
                "last_updated_by": user_id,
                "last_update_login": user_id,
            }
        )
        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()
        return instance


class TransferOfficersAllAccountsSerializer(serializers.ModelSerializer):
    """Transfer officer's all accounts serializer."""

    transfer_from = serializers.SlugRelatedField(
        slug_field="id", queryset=DimResources.objects.all()
    )

    class Meta:
        model = NtAccRelation
        fields = ("transfer_from", "resource", "comments")


class SclHierarchyMasterSerializer(serializers.ModelSerializer):
    """SCL_HIERARCHY_MASTER serializer class."""

    class Meta:
        model = SclHierarchyMaster
        fields = ("city_erp", "state_erp", "district_erp")


class AnnualSalesPlanListSerializer(BulkUpdateOrCreateListSerializer):
    def update(self, instances, validated_data):
        # return super().update(instances, validated_data)
        objects_updated = super().update(instances, validated_data[: len(instances)])

        objects_created = [
            self.child.create(attrs) for attrs in validated_data[len(instances) :]
        ]

        try:
            self.child.Meta.model.objects.bulk_create(objects_created)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return objects_updated + objects_created


class AnnualSalesTargetSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    """Annual sales target bulk update or create serializer class."""

    year = serializers.DecimalField(
        source="period_key.year", max_digits=20, decimal_places=2
    )
    month = serializers.DecimalField(
        source="period_key.month", max_digits=20, decimal_places=2
    )

    class Meta:
        model = FactNtSalesPlanning
        fields = (
            "id",
            "year",
            "month",
            "brand",
            "state",
            "yearly_sales_plan",
            "account_key",
            "quarterly_sales_plan",
            "product",
            "grade",
            "packaging",
            "so_key",
            "kam_key",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "yearly_sales_plan",
        }
        extra_kwargs = {
            "product": {"read_only": True},
            "grade": {"read_only": True},
            "packaging": {"read_only": True},
            "so_key": {"read_only": True},
            "kam_key": {"read_only": True},
        }

    def create(self, validated_data):
        dim_period = DimPeriod.objects.get(
            year=validated_data.get("period_key").get("year"),
            month=validated_data.get("period_key").get("month"),
        )
        validated_data.update(
            {
                "period_key": dim_period,
            }
        )
        return super().create(validated_data)


class FactNtSalesPlanningSerializer(serializers.ModelSerializer):
    """fact nt dales planning serializer."""

    month = serializers.CharField(source="period_key.month")
    year = serializers.CharField(source="period_key.year")

    class Meta:
        model = FactNtSalesPlanning
        fields = "__all__"


class NshNonTradeHeadSerializer(serializers.ModelSerializer):
    """Nsh non trade head serializer class."""

    month = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, data):
        return data["month"].month

    def get_year(self, data):
        return data["month"].year

    def get_sum(self, data):
        return data["sum"]

    class Meta:
        model = NshNonTradeSales
        fields = ("sum", "month", "year")


class DimCustomersSerializer(serializers.ModelSerializer):
    """Dim customers test serializer class."""

    class Meta:
        model = DimCustomersTest
        fields = "__all__"


class NshNonTradeSalesForThreeMonthOldSerializer(serializers.ModelSerializer):
    """Non-trade account relations serializer class."""

    class Meta:
        model = NshNonTradeSales
        fields = "__all__"


class CrmNthQuotNcrExcpApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthQuotNcrExcpAppr
        fields = "__all__"


class CrmNthSoNcrExcpApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthSoNcrExcpAppr
        fields = "__all__"


class CrmNthSourceChgReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthSourceChgReq
        fields = "__all__"


class CrmNthExtendValiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthExtendValidity
        fields = "__all__"


class CrmNthOrderCancApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthOrderCancAppr
        fields = "__all__"


class CrmNthBankGuartApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthBankGuartAppr
        fields = "__all__"


class CrmNthLeadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthLeadForm
        fields = "__all__"


class CrmNthRefuReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthRefuReq
        fields = "__all__"


class CrmNthCustCodeCreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmNthCustCodeCre
        fields = "__all__"


class FactNtSalesPlanAnnualSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        fields_obj = {
            "created_by": self.context.get("request").user.id,
            "last_updated_by": self.context.get("request").user.id,
            "last_update_login": self.context.get("request").user.id,
        }
        validated_data.update(fields_obj)
        return super().create(validated_data)

    class Meta:
        model = FactNtSalesPlanAnnual
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )


class FactNtSalesPlanningMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactNtSalesPlanningMonth
        fields = "__all__"


class FactNtSalesPlanningNcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactNtSalesPlanningNcr
        fields = "__all__"


class DimCustomersTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCustomersTest
        fields = "__all__"


class TOebsSclArNcrAdvanceCalcTabSerializer(serializers.ModelSerializer):
    incentive = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )
    third_party = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )
    other_expenses = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )
    sgst_igst = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )
    variable_cost = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )
    clinker_avg_freight = serializers.DecimalField(
        max_digits=20, decimal_places=2, write_only=True
    )

    class Meta:
        model = TOebsSclArNcrAdvanceCalcTab
        fields = (
            "id",
            "product",
            "quantity_invoiced",
            "packing_type",
            "unloading_by",
            "state",
            "city",
            "misc_charges",
            "district",
            "mode_of_transport",
            "unit_selling_price",
            "unloading_charges",
            "demurrages_and_warfages",
            "shortage",
            "primary_freight",
            "secondary_freight",
            "rebate_and_discount",
            "ncr_subsidy",
            "uom_code",
            "subsidy_lot",
            "packing_charges",
            "rake_charges",
            "incentive",
            "third_party",
            "other_expenses",
            "sgst_igst",
            "variable_cost",
            "clinker_avg_freight",
        )


class NtResourceTargetSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    # TODO: add validation to check if sum of target for a month isn't
    # greater than sum for target for that month in consensus target.
    class Meta:
        model = NtResourceTarget
        list_serializer_class = BulkUpdateOrCreateListSerializer
        read_only_fields = ("created_by", "last_updated_by", "last_update_login")
        editable_fields = {
            "zone",
            "state",
            "district",
            "resource_name",
            "resource_type",
            "resource_id",
            "business_segment",
            "brand",
            "product",
            "pack",
            "pack_type",
            "year",
            "quarter",
            "month",
            "date",
            "non_trade_target",
        }


class NtMarketTargettBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NtMarketTarget
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


class MonthlyTargetSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTargetSetting
        fields = "__all__"
        read_only_fields = ("last_update_login", "last_updated_by", "created_by")

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request").user.id,
                "last_updated_by": self.context.get("request").user.id,
                "last_update_login": self.context.get("request").user.id,
            }
        )
        return super().create(validated_data)


class NonTradeSalesPlanningStateSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningState
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningProductSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningProduct
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningAccountSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningAccount
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningDesignationSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningDesignation
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningProductMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningProductMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningAccountMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningAccountMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningDesignationMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningDesignationMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeTopDownMonthlyTargetSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeTopDownMonthlyTarget
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NonTradeSalesPlanningMonthlyNcrTargetSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningMonthlyNcrTarget
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class NtAccRelationUpdateOrCreateSerializer(serializers.ModelSerializer):
    """Dim resources(NTSOs List) serializer class."""

    class Meta:
        model = NtAccRelation
        fields = "__all__"


class NonTradeSalesPlanningStateMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = NonTradeSalesPlanningStateMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"target"}
        read_only_fields = ("id",)


class TpcCustomerMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TpcCustomerMapping
        fields = "__all__"
