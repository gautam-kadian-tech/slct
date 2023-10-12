from datetime import timezone

from django import forms
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from accounts.models import TgtRlsRoleData, User, UserRole
from accounts.user_role_choices import UserRoleChoice
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from Master_Data_Logistics.custome_read_only import ExportFormat

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.site_header = "SLCT Admin Console"


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "name",
            "email",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_staff",
            "date_joined",
        )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["email"]
    exclude = ("password", "last_login", "groups", "user_permissions")
    resource_class = CustomUserResource

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.USERADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(UserAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        obj.email = obj.email.lower()
        super(UserAdmin, self).save_model(request, obj, form, change)

    def get_export_fields(self):
        fields = [
            "id",
            "is_active",
            "name",
            "email",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_staff",
            "date_joined",
        ]

        return fields


@admin.register(UserRole)
class UserRoleAdmin(ImportExportModelAdmin, ExportFormat):
    search_fields = ["role_name", "user__email"]
    autocomplete_fields = ["user"]
    list_display = [
        "role_name",
        "user",
    ]

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.USERADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(UserRoleAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]


@admin.register(TgtRlsRoleData)
class TgtRlsRoleDataAdmin(ImportExportModelAdmin, ExportFormat):
    list_filter = ["role", "zone", "state", "plant_name"]
    search_fields = [
        "=emp_id",
        "name",
        "email",
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
    exclude = (
        "created_by",
        "last_updated_by",
        "last_update_login",
        "transporter_company_name",
    )

    def get_model_perms(self, request):
        user_roles = request.user.roles.values_list("role_name", flat=True).distinct()
        if UserRoleChoice.USERADMIN and UserRoleChoice.SLCTADMIN in user_roles:
            return super(TgtRlsRoleDataAdmin, self).get_model_perms(request)
        return {}

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX)
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.id
        obj.last_updated_by = request.user.id
        obj.last_update_login = request.user.id
        super().save_model(request, obj, form, change)
