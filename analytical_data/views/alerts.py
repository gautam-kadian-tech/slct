from django_filters.rest_framework import DjangoFilterBackend

from analytical_data.custom_mixins import AlertsCountMixin
from analytical_data.filters.alerts_filters import *
from analytical_data.models.alerts_models import *
from analytical_data.serializers.alerts_serializers import *
from analytical_data.utils import CustomPagination
from analytical_data.utils.responses import Responses
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class AlertTransactionViewSet(DownloadUploadViewSet, AlertsCountMixin):
    queryset = AlertTransaction.objects.all().order_by("-id")
    serializer_class = AlertTransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AlertTransactionFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "alert_transaction"

    def get(self, request):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        serializers = AlertTransactionSerializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializers.data))


class CrmApprovalStageGatesViewSet(DownloadUploadViewSet):
    queryset = CrmApprovalStageGates.objects.all()
    serializer_class = CrmApprovalStageGatesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmApprovalStageGatesFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "crm_approval_stage_gates"
