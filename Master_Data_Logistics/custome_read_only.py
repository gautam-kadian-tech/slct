from django.contrib import admin

from import_export.admin import ExportMixin
from import_export.formats import base_formats

READ_ONLY_FIELDS = [
    "created_by",
    "last_updated_by",
    "creation_date",
    "last_update_login",
    "last_update_date",
    "effective_start_date",
    "effective_end_date",
]

READ_ONLY_FIELDS_2 = [
    "created_by",
    "last_updated_by",
    "creation_date",
    "last_update_login",
    "last_update_date",
]


class ExportFormat(ExportMixin, admin.ModelAdmin):
    # your normal stuff
    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
