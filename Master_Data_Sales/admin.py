from datetime import timezone

from django.contrib import admin
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.user_role_choices import UserRoleChoice
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from Master_Data_Logistics.custome_read_only import ExportFormat

from .custom_read_only import READ_ONLY_FIELDS
from .models import *


class ZoneMappingNewAdminResource(resources.ModelResource):
    class Meta:
        model = ZoneMappingNew
        fields = (
            "zone",
            "state",
            "region",
            "district",
            "taluka",
            "city",
            "city_id",
            "pincode",
            "active",
            "status",
            "id",
        )


@admin.register(ZoneMappingNew)
class ZoneMappingNewAdmin(ImportExportModelAdmin, ExportFormat):
    resource_class = ZoneMappingNewAdminResource
    search_fields = [
        "zone",
        "state",
        "region",
        "district",
        "taluka",
        "city",
        "city_id",
        "pincode",
    ]
    list_display = [
        "zone",
        "state",
        "region",
        "district",
        "taluka",
        "city",
        "city_id",
        "pincode",
    ]

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(ZoneMappingNewAdmin, self).get_model_perms(request)
        return {}

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("pincode", "status", "org_id", "so_code")
        return self.readonly_fields

    list_per_page = 20

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


class SoTalukaMappingDelhiHydAdminResource(resources.ModelResource):
    class Meta:
        model = SoTalukaMappingDelhiHyd
        fields = (
            "id",
            "brand",
            "state",
            "emp_code",
            "emp_name",
            "email_id",
            "taluka",
            "district",
            "active",
        )


@admin.register(SoTalukaMappingDelhiHyd)
class SoTalukaMappingDelhiHydAdmin(ImportExportModelAdmin, ExportFormat):
    list_filter = [
        "state",
    ]
    resource_class = SoTalukaMappingDelhiHydAdminResource
    search_fields = [
        "brand",
        "org_id",
        "state",
        "emp_code",
        "emp_name",
        "email_id",
        "taluka",
        "district",
        "last_update_date",
    ]
    list_display = [
        "brand",
        # "org_id",
        "state",
        "district",
        "taluka",
        "emp_code",
        # "emp_name",
        "email_id",
        "active",
        "crm_updated",
        "last_update_date",
    ]
    readonly_fields = [
        "org_id",
        "mobile_number",
        # "email_id_shree",
        "playstore_id",
        "ios_or_android",
        "created_by",
        "last_updated_by",
        "creation_date",
        "last_update_login",
        "last_update_date",
        "crm_updated",
    ]
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        return False

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(SoTalukaMappingDelhiHydAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        obj.crm_updated = "N"
        print(f"Saving object with change={change}, crm_updated={obj.crm_updated}")
        super(SoTalukaMappingDelhiHydAdmin, self).save_model(request, obj, form, change)

    # def save_model(self, request, obj, form, change):
    #     if (
    #         form.data.get("modified_by") == "SLCT"
    #         or "modified_by" in form.cleaned_data
    #         and form.cleaned_data["modified_by"] == "SLCT"
    #     ):
    #         obj.crm_updated = "N"
    #     super(SoTalukaMappingDelhiHydAdmin, self).save_model(request, obj, form, change)


@admin.register(ObjectiveWeightage)
class ObjectiveWeightageAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["objective", "parameter", "weightage", "updated_at"]
    list_display = ["objective", "parameter", "weightage", "updated_at"]
    readonly_fields = ["inverse_score", "updated_at", "created_at"]
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(ObjectiveWeightageAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(PricingInputTemplateAllIndia)
class PricingInputTemplateAllIndiaAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "state",
        "district",
        "brand",
        "price_type",
        "price",
        "date",
        "last_update_date",
    ]
    list_display = [
        "state",
        "district",
        "brand",
        "price_type",
        "price",
        "date",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(PricingInputTemplateAllIndiaAdmin, self).get_model_perms(
                request
            )
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


class DoMasterAllIndiaDataAdminResource(resources.ModelResource):
    class Meta:
        model = DoMasterAllIndiaData
        fields = (
            "id",
            "email",
            "brand",
            "state",
            "do_emp_code",
            "name",
            # "mobile_number",
            "active",
        )
        # exclude = ('email')


@admin.register(DoMasterAllIndiaData)
class DoMasterAllIndiaDataAdmin(ImportExportModelAdmin, ExportFormat):
    list_filter = [
        "state",
    ]
    resource_class = DoMasterAllIndiaDataAdminResource
    search_fields = [
        "brand",
        "state",
        "do_emp_code",
        "mobile_number",
        "email",
        "name",
        "last_update_date",
    ]
    list_display = [
        "state",
        "brand",
        "name",
        "do_emp_code",
        "email",
        "mobile_number",
        "active",
        "crm_updated",
        "last_update_date",
    ]

    readonly_fields = [
        "created_by",
        "last_updated_by",
        "creation_date",
        "last_update_login",
        "last_update_date",
        "crm_updated",
    ]
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        return False

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(DoMasterAllIndiaDataAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        if form.data.get("modified_by") == "SLCT":
            obj.crm_updated = "N"
        super(DoMasterAllIndiaDataAdmin, self).save_model(request, obj, form, change)


@admin.register(NcrThreshold)
class NcrThresholdAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "zone",
        "state",
        "region",
        "district",
        "grade",
        "brand",
        "pack",
        "red_ncr_threshold",
        "green_ncr_threshold",
        "last_update_date",
    ]
    list_display = [
        "zone",
        "state",
        "region",
        "district",
        "grade",
        "brand",
        "pack",
        "red_ncr_threshold",
        "green_ncr_threshold",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(NcrThresholdAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(L1SourceMapping)
class L1SourceMappingAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "order_type",
        "cust_category",
        "source_id",
        "from_city_id",
        "source_city",
        "source_district",
        "source_taluka",
        "source_state",
        "source_type",
        "mode",
        "to_city_id",
        "destination_city",
        "destination_district",
        "destination_state",
        "brand",
        "grade",
        "packaging",
        "contribution_per_mt",
        "tlc_per_mt",
        "route_id",
        "distance",
        "sla",
        "primary_secondary_route",
        "type",
        "priority",
        "destination_taluka",
        "route_id_secondary",
    ]
    list_display = [
        "order_type",
        "cust_category",
        "source_id",
        "from_city_id",
        "source_city",
        "source_district",
        "source_taluka",
        "source_state",
        "source_type",
        "mode",
        "to_city_id",
        "destination_city",
        "destination_district",
        "destination_state",
        "brand",
        "grade",
        "packaging",
        "contribution_per_mt",
        "tlc_per_mt",
        "route_id",
        "distance",
        "sla",
        "primary_secondary_route",
        "type",
        "priority",
        "destination_taluka",
        "route_id_secondary",
    ]
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(L1SourceMappingAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(RouteWeightage)
class RouteWeightageAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["parameter", "weightage", "inverse_score"]
    list_display = [
        "parameter",
        "weightage",
        "inverse_score",
    ]
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(RouteWeightageAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(PremiumProductsMasterTmp)
class PremiumProductsMasterTmpAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "org_id",
        "code",
        "state",
        "cust_cat",
        "inventory_id",
        "grade",
        "packaging_condition",
        "bag_type",
        "revised_name",
        "premium",
    ]
    list_display = [
        "org_id",
        "code",
        "state",
        "cust_cat",
        "inventory_id",
        "grade",
        "packaging_condition",
        "bag_type",
        "revised_name",
        "premium",
    ]
    readonly_fields = READ_ONLY_FIELDS
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.SALESMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(PremiumProductsMasterTmpAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]
