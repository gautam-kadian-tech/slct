"""Bulk update model view set module."""
import json
import os
from logging import getLogger
from operator import itemgetter

import pandas as pd
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from analytical_data.custom_mixins import DownloadModelMixin
from analytical_data.models import ApprovalThreshold, TOebsSclRouteMaster
from analytical_data.models.non_trade_head_models import NtNotesComms
from analytical_data.utils import MultipartJsonParser, Response, Responses

log = getLogger()


class FileUploadViewSet(ModelViewSet):
    """ViewSet class to upload and dump a file on server."""

    file_name = None
    file_path = ""
    parser_classes = (MultipartJsonParser,)

    def create(self, request, *args, **kwargs):
        self.file_name = request.FILES.get("file_name")

        dump_file = open(self.file_path + f"{self.file_name}", "bw")

        try:
            dump_file.write(self.file_name.read())
            dump_file.close()
        except AttributeError:
            pass
        return super().create(request, *args, **kwargs)

    def download(self, request, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, NtNotesComms):
            file = instance.attachment
        else:
            file = instance.nnc_id.attachment
        response = HttpResponse(open(file, "rb"), content_type="image/jpeg")
        response["Content-Length"] = os.path.getsize(file)
        response["Content-Disposition"] = f"attachment; filename={file}"
        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ["POST", "PUT"]:
            context.update(
                {
                    "user_id": self.request.user.id,
                    "attachment": self.file_path + f"{self.file_name}"
                    if self.file_name
                    else None,
                }
            )
        return context


class DownloadUploadViewSet(ModelViewSet, DownloadModelMixin):
    """View-set class to download and upload an excel sheet."""

    parser_classes = (MultiPartParser, JSONParser)
    values = list()
    file_name = None
    sorting_fields = ("id",)
    update_response_message = "Bulk update success!"
    upload_response_message = "File upload success!"
    auto_generated_fields = []

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            return super().create(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Implement bulk_update for randomly ordered incoming data.

        Args:
            request (HttpRequest): request object

        Returns:
            HttpResponse: response object
        """
        if isinstance(request.data, dict):
            return super().update(request, *args, **kwargs)

        # Sorts list of dicts based on a value of a key in dictionary.
        self.data = sorted(request.data, key=self.get_sorting_key())

        queryset = self.get_queryset().order_by(*self.sorting_fields)
        serializer = self.get_serializer(
            queryset, self.data, partial=kwargs.pop("partial", None), many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            self.update_response_message, data=serializer.data
        )

    def get_queryset(self):
        if self.request.method in ["PATCH", "PUT"] and not isinstance(
            getattr(self, "data", {}), dict
        ):
            return (
                super()
                .get_queryset()
                .filter(id__in=map(lambda x: x.get("id"), self.data))
            )
        return super().get_queryset()

    def read_file_get_json(self, file):
        try:
            df = pd.read_excel(file.read())
            df.columns = df.columns.str.lower()
            df = df.drop(self.auto_generated_fields, axis=1, errors="ignore")
            df = df.round(decimals=2)
            for column in df.columns:
                if df[column].dtype == "datetime64[ns]":
                    df[column] = df[column].astype(str)
        except Exception as e:
            log.error("FileError: %s", e)
            return Responses.error_response("FileError: Unable to read file.")
        return json.loads(df.to_json(orient="records"))

    def upload_update(self, request, *args, **kwargs):
        self.data = sorted(
            self.read_file_get_json(request.FILES.get("file_name")),
            key=self.get_sorting_key(),
        )
        queryset = self.get_queryset().order_by(*self.sorting_fields)
        serializer = self.get_serializer(queryset, data=self.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            self.upload_response_message, data=serializer.data
        )

    def get_sorting_key(self):
        if self.sorting_fields == ("id",):
            return lambda x: x.get("id") or 1000000000000000
        else:
            return itemgetter(*self.sorting_fields)

    def upload_create(self, request, *args, **kwargs):
        data = self.read_file_get_json(request.FILES.get("file_name"))
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            "File uploaded and data saved to db.", data=serializer.data
        )

    def freight_change_upload_create(self, request, *args, **kwargs):
        data = self.read_file_get_json(request.FILES.get("file_name"))
        new_data = []
        for record in data:
            route_code = record["route_code"]
            to_be_freight = record["to_be_freight"]

            try:
                route_code_record = TOebsSclRouteMaster.objects.filter(
                    route_id=route_code
                ).first()
                current_freight = route_code_record.freight_amount
            except TOebsSclRouteMaster.DoesNotExist:
                current_freight = None

            record["contribution"] = to_be_freight - float(current_freight)
            record["approval_type"] = "FREIGHT_CHANGE"
            record["status"] = "PENDING"
            persona = None
            try:
                queryset = ApprovalThreshold.objects.filter(
                    approval=record["approval_type"],
                    min__lte=record["contribution"],
                    max__gte=record["contribution"],
                )
                if queryset:
                    persona = queryset.first().persona
            except:
                persona = None

            record["persona"] = persona
            new_data.append(record)
        serializer = self.get_serializer(data=new_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responses.success_response(
            "File uploaded and data saved to db.", data=[]
        )
