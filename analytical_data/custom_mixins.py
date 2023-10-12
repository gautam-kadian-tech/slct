"""Custom mixins module."""
import json
from datetime import date, datetime

import pandas as pd
from django.http import HttpResponse
from rest_framework.response import Response

from analytical_data.enum_classes import ApprovalStatusChoices
from analytical_data.utils import dump_to_excel
from analytical_data.utils.responses import Responses
from analytical_data.view_helpers.get_user_detail import (
    GetDistrictsDataByState,
)

# from accounts.models import TgtRlsRoleData


class DownloadModelMixin:
    """
    Download dump of a model to an excel sheet.
    """

    def download(self, request, *args, **kwargs):
        """API to export data to excel sheet."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        df = pd.DataFrame(json.loads(json.dumps(serializer.data)))
        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response

    def download_by_state(self, request, *args, **kwargs):
        """API to export data to excel sheet."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = GetDistrictsDataByState(self.request.user.email, queryset)
        serializer = self.get_serializer(queryset, many=True)
        df = pd.DataFrame(json.loads(json.dumps(serializer.data)))
        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response


class RequestsCountMixin:
    def request_count(self, request, *args, **kwargs):
        current_date = date.today()
        queryset = self.filter_queryset(self.get_queryset())
        return Response(
            {
                "pending": queryset.filter(
                    persona=request.query_params.get("persona"),
                    status=ApprovalStatusChoices.PENDING.value,
                ).count(),
                "approved": queryset.filter(
                    persona=request.query_params.get("persona"),
                    creation_date__date=current_date,
                    status=ApprovalStatusChoices.APPROVED.value,
                ).count(),
                "rejected": queryset.filter(
                    persona=request.query_params.get("persona"),
                    creation_date__date=current_date,
                    status=ApprovalStatusChoices.REJECTED.value,
                ).count(),
            }
        )


class AlertsCountMixin:
    def alerts_count(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.filter_queryset(self.get_queryset()).filter(
            user_id=user_id, is_active="Y"
        )
        return Responses.success_response(
            message="fetched the count of alerts",
            data={
                "unread_count": queryset.filter(is_read="N").count(),
                "read_count": queryset.filter(is_read="Y").count(),
            },
        )
