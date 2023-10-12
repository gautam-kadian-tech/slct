from django.contrib import admin

from accounts.user_role_choices import UserRoleChoice
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .custome_read_only import (
    READ_ONLY_FIELDS,
    READ_ONLY_FIELDS_2,
    ExportFormat,
)
from .models import *

# Register your models here.


@admin.register(EtaUpdatedNoEntry)
class EtaUpdatedNoEntryAdmin(ImportExportModelAdmin, ExportFormat):
    def start_time_no_entry_2_value(self, obj):
        return obj.start_time_no_entry_2.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "start_time_no_entry_2"

    def start_time_value(self, obj):
        return obj.start_time.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "start_time"

    def end_time_value(self, obj):
        return obj.end_time.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "end_time"

    def end_time_no_entry_2_value(self, obj):
        return obj.end_time_no_entry_2.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "end_time_no_entry_2"

    def start_time_no_entry_3_value(self, obj):
        return obj.start_time_no_entry_3.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "start_time_no_entry_3"

    def end_time_no_entry_3_value(self, obj):
        return obj.end_time_no_entry_3.strftime("%H:%M:%S")

    start_time_no_entry_2_value.short_description = "end_time_no_entry_3"

    search_fields = [
        "destination_city",
        "destination_district",
        "source_city",
        "start_time_value",
        "end_time_value",
        "start_time_no_entry_2_value",
        "end_time_no_entry_2_value",
        "start_time_no_entry_3_value",
        "end_time_no_entry_3_value",
        "pack_type",
    ]
    list_display = [
        "destination_city",
        "destination_district",
        "source_city",
        "route_id",
        "pack_type",
        "start_time_value",
        "end_time_value",
        "start_time_no_entry_2_value",
        "end_time_no_entry_2_value",
        "start_time_no_entry_3_value",
        "end_time_no_entry_3_value",
    ]

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(EtaUpdatedNoEntryAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    list_per_page = 20


@admin.register(PackerRatedCapacity)
class PackerRatedCapacityAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "plant",
        "packer",
        "workers_req_for_packer",
        "packer_rated_capacity_mt_hr",
        "truck_loader",
        "tl_rated_capacity_mt_hr",
        "workers_req_for_tl",
        "can_run_multiple_brands",
        "last_update_date",
    ]
    list_display = [
        "plant",
        "packer",
        "workers_req_for_packer",
        "packer_rated_capacity_mt_hr",
        "truck_loader",
        "tl_rated_capacity_mt_hr",
        "workers_req_for_tl",
        "can_run_multiple_brands",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(PackerRatedCapacityAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(PlantwiseSwitchoverTime)
class PlantwiseSwitchoverTimeAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "plant",
        "worker_switch_time_diff_packer_min",
        "switch_time_bw_trucks_min",
        "grade_switch_time_min",
        "brand_switch_time_min",
        "tea_break_time_min",
        "last_update_date",
    ]
    list_display = [
        "plant",
        "grade_switch_time_min",
        "worker_switch_time_diff_packer_min",
        "switch_time_bw_trucks_min",
        "brand_switch_time_min",
        "tea_break_time_min",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(PlantwiseSwitchoverTimeAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(TgtPlantLookup)
class TgtPlantLookupAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["plant_name", "org", "zone", "commudity"]
    list_display = ["zone", "org", "plant_name", "commudity", "last_update_date"]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(TgtPlantLookupAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(ReasonsForFreightChange)
class ReasonsForFreightChangeAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["reasons", "last_update_date"]
    list_display = [
        "reasons",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(ReasonsForFreightChangeAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(RakeTypes)
class RakeTypesAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["rake_types", "last_update_date"]
    list_display = [
        "rake_types",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(RakeTypesAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(SidingCodeMapping)
class SidingCodeMappingAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = [
        "rake_point",
        "rake_point_code",
        "rake_point_type",
        "last_update_date",
    ]
    list_display = [
        "rake_point",
        "rake_point_code",
        "rake_point_type",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(SidingCodeMappingAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(ReasonsForDispatchDelay)
class ReasonsForDispatchDelayAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["reasons", "no_trucks_available", "last_update_date"]
    list_display = [
        "reasons",
        "no_trucks_available",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(ReasonsForDispatchDelayAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(SourceChangeFreightMaster)
class SourceChangeFreightMasterAdmin(ImportExportModelAdmin, ExportFormat):
    list_filter = [
        "state",
    ]
    search_fields = [
        "state",
        "brand",
        "district",
        "org_type",
        "incoterm",
        "freight_term",
        "last_update_date",
    ]
    list_display = [
        "state",
        "brand",
        "district",
        "org_type",
        "incoterm",
        "freight_term",
        "last_update_date",
    ]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(SourceChangeFreightMasterAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(VpcHistorical)
class VpcHistoricalAdmin(ImportExportModelAdmin, ExportFormat):
    list_filter = [
        "month",
    ]
    search_fields = [
        "month",
        "plant_id",
        "grade",
        "vpc",
    ]
    list_display = ["id", "month", "plant_id", "grade", "vpc_without_clinker"]
    readonly_fields = READ_ONLY_FIELDS_2
    list_per_page = 20

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.LOGISTICSMDMADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(VpcHistoricalAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    def vpc_without_clinker(self, obj):
        return obj.vpc
