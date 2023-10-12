from django.contrib import admin
from django.db.models import Q

from import_export.admin import ImportExportModelAdmin
from Master_Data_Logistics.models import *
from Master_Data_Sales.models import *

from .models import *


@admin.register(ZoneMappingNew)
class ZoneMappingNewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=zone",
        "=state",
        "=region",
        "=district",
        "=taluka",
        "=city",
        "=city_id",
        "=pincode",
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(zone__contains=bit)
                    | Q(state__contains=bit)
                    | Q(district__contains=bit)
                    | Q(city_id__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("pincode", "status", "org_id", "so_code")
        return self.readonly_fields


@admin.register(SoTalukaMappingDelhiHyd)
class SoTalukaMappingDelhiHydAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=brand",
        "=org_id",
        "=state",
        "=emp_code",
        "=emp_name",
        "=taluka",
        "=district",
        "=mobile_number",
        "=email_id_shree",
        "=playstore_id",
        "=ios_or_android",
    ]
    list_display = [
        "brand",
        "org_id",
        "state",
        "emp_code",
        "emp_name",
        "taluka",
        "district",
        "mobile_number",
        "email_id_shree",
        "playstore_id",
        "ios_or_android",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(taluka__contains=bit)
                    | Q(state__contains=bit)
                    | Q(district__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(EtaUpdatedNoEntry)
class EtaUpdatedNoEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=destination_city",
        "=destination_district",
        "=source_city",
        "=start_time",
        "=end_time",
        "=start_time_no_entry_2",
        "=end_time_no_entry_2",
        "=start_time_no_entry_3",
        "=end_time_no_entry_3",
        "=pack_type",
    ]
    list_display = [
        "destination_city",
        "destination_district",
        "source_city",
        "route_id",
        "pack_type",
        "start_time",
        "end_time",
        "start_time_no_entry_2",
        "end_time_no_entry_2",
        "start_time_no_entry_3",
        "end_time_no_entry_3",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(destination_city__contains=bit)
                    | Q(destination_district__contains=bit)
                    | Q(source_city__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(PackerRatedCapacity)
class PackerRatedCapacityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=plant",
        "=packer",
        "=workers_req_for_packer",
        "=packer_rated_capacity_mt_hr",
        "=truck_loader",
        "=tl_rated_capacity_mt_hr",
        "=workers_req_for_tl",
        "=can_run_multiple_brands",
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
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(plant__contains=bit)
                    | Q(truck_loader__contains=bit)
                    | Q(packer__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(PlantwiseSwitchoverTime)
class PlantwiseSwitchoverTimeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=plant",
        "=worker_switch_time_diff_packer_min",
        "=switch_time_bw_trucks_min",
        "=grade_switch_time_min",
        "=brand_switch_time_min",
        "=tea_break_time_min",
    ]
    list_display = [
        "plant",
        "grade_switch_time_min",
        "worker_switch_time_diff_packer_min",
        "switch_time_bw_trucks_min",
        "brand_switch_time_min",
        "tea_break_time_min",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(plant__contains=bit)
                    | Q(worker_switch_time_diff_packer_min__contains=bit)
                    | Q(switch_time_bw_trucks_min__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(RouteWeightage)
class RouteWeightageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["=parameter", "=weightage", "=inverse_score"]
    list_display = [
        "parameter",
        "weightage",
        "inverse_score",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(parameter__contains=bit)
                    | Q(weightage__contains=bit)
                    | Q(inverse_score__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(ObjectiveWeightage)
class ObjectiveWeightageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["=objective", "=parameter", "=weightage", "=inverse_score"]
    list_display = [
        "objective",
        "parameter",
        "weightage",
        "inverse_score",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(parameter__contains=bit)
                    | Q(weightage__contains=bit)
                    | Q(inverse_score__contains=bit)
                    | Q(__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(FreightMaster)
class FreightMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=link_id",
        "=primary_frt",
        "=demurrage",
        "=secondary_frt",
        "=cust_category",
        "=rake_charges",
        "=handling_charges",
        "=pack_type",
        "=damages",
        "=notional_freight",
    ]
    list_display = [
        "link_id",
        "primary_frt",
        "secondary_frt",
        "demurrage",
        "cust_category",
        "rake_charges",
        "handling_charges",
        "pack_type",
        "damages",
        "notional_freight",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(link_id__contains=bit)
                    | Q(primary_frt__contains=bit)
                    | Q(demurrage__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(PricingInputTemplateAllIndia)
class PricingInputTemplateAllIndiaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=state",
        "=district",
        "=brand",
        "=price_type",
        "=price",
        "=date",
    ]
    list_display = [
        "state",
        "district",
        "brand",
        "price_type",
        "price",
        "date",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(state__contains=bit)
                    | Q(district__contains=bit)
                    | Q(brand__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(DoMasterAllIndiaData)
class DoMasterAllIndiaDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=brand",
        "=state",
        "=do_emp_code",
        "=mobile_number",
        "email",
        "name",
    ]
    list_display = [
        "state",
        "brand",
        "name",
        "do_emp_code",
        "email",
        "mobile_number",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(brand__contains=bit)
                    | Q(state__contains=bit)
                    | Q(do_emp_code__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(TgtRlsRoleData)
class TgtRlsRoleDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=emp_id",
        "=name",
        "=email",
        "=role",
        "=zone",
        "=state",
        "=district",
        "=regions",
        "=plant_name",
    ]

    list_display = [
        "emp_id",
        "name",
        "email",
        "role",
        "zone",
        "state",
        "district",
        "regions",
        "plant_name",
    ]

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(
    #         request, queryset, search_term
    #     )
    #     if search_term:
    #         filters = Q()
    #         for bit in search_term.split():
    #             # Perform case-sensitive search on specific fields
    #             filters |= (
    #                 Q(zone__contains=bit)
    #                 | Q(state__contains=bit)
    #                 | Q(district__contains=bit)
    #                 | Q(regions__contains=bit)
    #             )
    #         queryset = queryset.filter(filters)
    #     return queryset, use_distinct


@admin.register(TgtPlantLookup)
class TgtPlantLookupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["=plant_name", "=org", "=zone", "=commudity"]
    list_display = [
        "zone",
        "org",
        "plant_name",
        "commudity",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(zone__contains=bit)
                    | Q(plant_name__contains=bit)
                    | Q(org__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(LpSourceMappingTlc)
class LpSourceMappingTlcAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=order_type",
        "=cust_category",
        "=source_id",
        "=from_city_id",
        "=source_city",
        "=source_district",
        "=source_taluka",
        "=source_state",
        "=source_type",
        "=mode",
        "=to_city_id",
        "=destination_city",
        "=destination_district",
        "=destination_state",
        "=brand",
        "=grade",
        "=packaging",
        "=contribution_per_mt",
        "=tlc_per_mt",
        "=ncr_per_mt",
        "=route_id",
        "=distance",
        "=sla",
        "=primary_secondary_route",
        "=type",
        "=priority",
        "=destination_taluka",
        "=route_id_secondary",
        "=reasons",
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
        "ncr_per_mt",
        "route_id",
        "distance",
        "sla",
        "primary_secondary_route",
        "type",
        "priority",
        "destination_taluka",
        "route_id_secondary",
        "reasons",
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(source_city__contains=bit)
                    | Q(source_district__contains=bit)
                    | Q(source_taluka__contains=bit)
                    | Q(source_state__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(L1SourceMapping)
class L1SourceMappingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=order_type",
        "=cust_category",
        "=source_id",
        "=from_city_id",
        "=source_city",
        "=source_district",
        "=source_taluka",
        "=source_state",
        "=source_type",
        "=mode",
        "=to_city_id",
        "=destination_city",
        "=destination_district",
        "=destination_state",
        "=brand",
        "=grade",
        "=packaging",
        "=contribution_per_mt",
        "=tlc_per_mt",
        "=route_id",
        "=distance",
        "=sla",
        "=primary_secondary_route",
        "=type",
        "=priority",
        "=destination_taluka",
        "=route_id_secondary",
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(source_city__contains=bit)
                    | Q(source_district__contains=bit)
                    | Q(source_taluka__contains=bit)
                    | Q(source_state__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct


@admin.register(NcrThreshold)
class NcrThresholdAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "=zone",
        "=state",
        "=region",
        "=district",
        "=grade",
        "=brand",
        "=pack",
        "=red_ncr_threshold",
        "=green_ncr_threshold",
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
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            filters = Q()
            for bit in search_term.split():
                # Perform case-sensitive search on specific fields
                filters |= (
                    Q(zone__contains=bit)
                    | Q(state__contains=bit)
                    | Q(district__contains=bit)
                    | Q(region__contains=bit)
                )
            queryset = queryset.filter(filters)
        return queryset, use_distinct
