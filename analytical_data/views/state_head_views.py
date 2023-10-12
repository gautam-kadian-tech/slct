"""State head views module."""
import calendar
import json
from calendar import monthrange
from datetime import date, datetime, timedelta
from io import BytesIO
from operator import itemgetter

import numpy as np
import pandas as pd
from django.db import transaction
from django.db.models import (
    Avg,
    Case,
    Count,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
    functions,
)
from django.db.models.functions import Substr
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import *
from analytical_data.custom_permissions import IsNationalStateHead, IsStateHead
from analytical_data.enum_classes import NSHApprovalChoices
from analytical_data.filters import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils import (
    CustomPagination,
    MultipartJsonParser,
    Responses,
    dump_to_excel,
)
from analytical_data.view_helpers.get_user_detail import (
    GetDistrictsDataByState,
    user_details,
)
from analytical_data.views.custom_viewsets import DownloadUploadViewSet


class SalesPlanApproval(ModelViewSet):
    """Sales Plan Approval ViewSet."""

    # permission_classes = (IsAuthenticated, IsNationalStateHead)
    permission_classes = (IsAuthenticated,)
    queryset = SlctAnnualSalesPlan.objects.all()
    serializer_class = SlctAnnualSalesPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctAnnualSalesPlanFilter

    def get(self, request):
        email_id = self.request.user.email
        # email_id = "testers@shreecement.com"
        state = (
            TgtStateHeadNsh.objects.filter(email=email_id)
            .values("state")
            .order_by("employee_code")
            .first()
        )
        data = (
            self.filter_queryset(self.get_queryset())
            .filter(state=state["state"])
            .values()
        )
        return Responses.success_response("data Show", data=data)


class StateHeadBaseClass(ModelViewSet):
    permission_classes = (IsStateHead, IsNationalStateHead)

    def get_queryset(self):
        queryset = super().get_queryset()
        nsh_status_query = Q(
            status__in=(
                NSHApprovalChoices.INITIATED.value,
                NSHApprovalChoices.APPROVED.value,
                NSHApprovalChoices.REJECTED.value,
            )
        )

        if self.request.user.role == "NSH":
            queryset = queryset.filter(nsh_status_query)
        if self.request.user.role == "SH":
            queryset = queryset.filter(~nsh_status_query)
        return queryset


class SlctCashDiscPropsByIDViewSet(ModelViewSet):
    """slct cash disc props by id"""

    queryset = SlctCashDiscProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset
        slct_cash_disc_serializer = SlctCashDiscPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_cash_disc_serializer.data
        )


class TNmOmxSchemesViewSet(ModelViewSet):
    """tnm omx schemes get api"""

    queryset = TNmOmxSchemes.objects.all()

    def get(self, request):
        tnm_omx_scheme = TNmOmxSchemesSerializer(self.queryset, many=True)
        return Responses.success_response("data fetch", data=tnm_omx_scheme.data)


class SlctPartyWiseSchemePropsViewSet(ModelViewSet):
    "Slct Party Wise Scheme API's"
    queryset = SlctPartyWiseSchemeProps.objects.all()
    serializer_class = SlctPartyWiseSchemePropsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctPartyWiseSchemePropsFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        saletype = json.loads(request.data["saletype"])
        saletype = ", ".join(saletype)
        product = json.loads(request.data["product"])
        product = ", ".join(product)
        request.data["saletype"] = saletype
        request.data["product"] = product
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "Slct Party Scheme Insertion Error", data=serializer.errors
            )
        slct_party_scheme_obj = serializer.save()
        for inc_data in json.loads(request.data["party_wise_target_incentive"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data["party_wise_scheme"] = slct_party_scheme_obj.id
            party_wise_incent_serializer = SlctPartyWiseSchemePropsIncentiveSerializer(
                data=inc_data
            )
            if not party_wise_incent_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Party Wise Incentive Insertion Error", data=serializer.errors
                )
            party_wise_incent_serializer.save()
        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class UpdateSlctPartyWiseSchemePropsViewSet(ModelViewSet):
    """slct party wise scheme props  api"""

    def post(self, request):
        id = request.query_params.get("id")
        party_wise_obj = SlctPartyWiseSchemeProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            saletype = json.loads(request.data["saletype"])
            saletype = ", ".join(saletype)
            product = json.loads(request.data["product"])
            product = ", ".join(product)
            request.data["saletype"] = saletype
            request.data["product"] = product
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            serializer = SlctPartyWiseSchemePropsSerializer(
                party_wise_obj, data=request.data
            )
            if not serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Slct Party Scheme Insertion Error", data=serializer.errors
                )
            slct_party_scheme_obj = serializer.save()
            party_wise_inc = SlctPartyWiseSchemePropsIncentive.objects.filter(
                party_wise_scheme__id=slct_party_scheme_obj.id
            )
            if party_wise_inc:
                party_wise_inc.delete()
            for inc_data in json.loads(request.data["party_wise_target_incentive"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["party_wise_scheme"] = slct_party_scheme_obj.id
                party_wise_incent_serializer = (
                    SlctPartyWiseSchemePropsIncentiveSerializer(data=inc_data)
                )
                if not party_wise_incent_serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "Party Wise Incentive Insertion Error",
                        data=serializer.errors,
                    )
                party_wise_incent_serializer.save()
        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class SlctPartyWiseSchemePropsByIdViewSet(ModelViewSet):
    queryset = SlctPartyWiseSchemeProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")

        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset

        slct_party_wise_scheme_obj = SlctPartyWiseSchemePropsSerializer(
            queryset, many=True
        )
        return Responses.success_response(
            "data fetched by id successfully", data=slct_party_wise_scheme_obj.data
        )


class SlctCashDiscPropsViewSet(ModelViewSet):
    """slct cash discount props api"""

    queryset = SlctCashDiscProps.objects.all()
    serializer_class = SlctCashDiscPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filterset_class = SlctCashDiscPropsFilter
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        saletype = json.loads(request.data["saletype"])
        saletype = ", ".join(saletype)
        product = json.loads(request.data["product"])
        product = ", ".join(product)
        request.data["saletype"] = saletype
        request.data["product"] = product
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        sl_ct_cash_del = SlctCashDiscPropsSerializer(data=request.data)
        if not sl_ct_cash_del.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=sl_ct_cash_del.errors
            )
        cash_disc_obj = sl_ct_cash_del.save()
        no_of_days_lower = json.loads(request.data["no_of_days_lower"])
        no_of_days_upper = json.loads(request.data["no_of_days_upper"])
        incentive = json.loads(request.data["incentive"])
        for val in range(len(no_of_days_lower)):
            sl_ct_cash_desc_dict = {
                "no_of_days_lower": no_of_days_lower[val],
                "no_of_days_upper": no_of_days_upper[val],
                "incentive": incentive[val],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "cash_disc": cash_disc_obj.id,
            }
            sl_ct_cash_dels = SlctCashDiscDaysIncentiveSerializer(
                data=sl_ct_cash_desc_dict
            )
            if not sl_ct_cash_dels.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occurred while inserting slct cash discount data ",
                    data=sl_ct_cash_dels.errors,
                )
            sl_ct_cash_dels.save()
        return Responses.success_response(
            "slct cash discount data inserted successfully", data=sl_ct_cash_del.data
        )


class UpdateSlctCashDiscPropseViewSet(ModelViewSet):
    """slct cash discount props api"""

    @transaction.atomic()
    def post(self, request):
        id = request.query_params.get("id")
        cash_disc_obj = SlctCashDiscProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            saletype = json.loads(request.data["saletype"])
            saletype = ", ".join(saletype)
            product = json.loads(request.data["product"])
            product = ", ".join(product)
            request.data["saletype"] = saletype
            request.data["product"] = product
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            sl_ct_cash_del = SlctCashDiscPropsSerializer(
                cash_disc_obj, data=request.data
            )
            if not sl_ct_cash_del.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=sl_ct_cash_del.errors
                )
            cash_disc_obj = sl_ct_cash_del.save()
            cash_dis_inc = SlctCashDiscDaysIncentive.objects.filter(
                cash_disc__id=cash_disc_obj.id
            )
            if cash_dis_inc:
                cash_dis_inc.delete()
            no_of_days_lower = json.loads(request.data["no_of_days_lower"])
            no_of_days_upper = json.loads(request.data["no_of_days_upper"])
            incentive = json.loads(request.data["incentive"])
            for val in range(len(no_of_days_lower)):
                sl_ct_cash_desc_dict = {
                    "no_of_days_lower": no_of_days_lower[val],
                    "no_of_days_upper": no_of_days_upper[val],
                    "incentive": incentive[val],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "cash_disc": cash_disc_obj.id,
                }
                sl_ct_cash_dels = SlctCashDiscDaysIncentiveSerializer(
                    data=sl_ct_cash_desc_dict
                )
                if not sl_ct_cash_dels.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "error occurred while inserting slct cash discount data ",
                        data=sl_ct_cash_dels.errors,
                    )
                sl_ct_cash_dels.save()
        return Responses.success_response(
            "slct cash discount data inserted successfully", data=sl_ct_cash_del.data
        )


class SlctQuantitySlabPropsByIdViewSet(ModelViewSet):
    queryset = SlctQuantitySlabProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset

        slct_obj = SlctQuantitySlabPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctQuantitySlabPropsViewSet(ModelViewSet):
    """slct quantity slab props api"""

    queryset = SlctQuantitySlabProps.objects.all()
    serializer_class = SlctQuantitySlabPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filterset_class = SlctQuantitySlabPropsFilter
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        saletype = json.loads(request.data["saletype"])
        saletype = ", ".join(saletype)
        product = json.loads(request.data["product"])
        product = ", ".join(product)
        request.data["saletype"] = saletype
        request.data["product"] = product
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_quant_slab_serializer = SlctQuantitySlabPropsSerializer(data=request.data)
        if not slct_quant_slab_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "SlctQuantitySlab Data Insertion Error",
                data=slct_quant_slab_serializer.errors,
            )
        qty_slab_obj = slct_quant_slab_serializer.save()
        quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
        quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
        incentive = json.loads(request.data["incentive"])
        incentive_kind = json.loads(request.data["incentive_kind"])
        for val in range(len(quantity_slab_lower)):
            slct_qty_slab_inc_dict = {
                "quantity_slab_lower": quantity_slab_lower[val],
                "quantity_slab_upper": quantity_slab_upper[val],
                "incentive": incentive[val],
                "incentive_kind": incentive_kind[val],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "quantity_slab": qty_slab_obj.id,
            }

            slct_qty_slab_inc_serializer = SlctQuantitySlabPropsIncentiveSerializer(
                data=slct_qty_slab_inc_dict
            )
            if not slct_qty_slab_inc_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occurred while inserting slct quantity slab data ",
                    data=slct_qty_slab_inc_serializer.errors,
                )
            slct_qty_slab_inc_serializer.save()
        return Responses.success_response(
            "slct quantity slab data inserted successfully",
            data=slct_quant_slab_serializer.data,
        )


class UpdateSlctQuantitySlabPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_qua_slab_obj = SlctQuantitySlabProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            saletype = json.loads(request.data["saletype"])
            saletype = ", ".join(saletype)
            product = json.loads(request.data["product"])
            product = ", ".join(product)
            request.data["saletype"] = saletype
            request.data["product"] = product
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_quant_slab_serializer = SlctQuantitySlabPropsSerializer(
                slct_qua_slab_obj, data=request.data
            )
            if not slct_quant_slab_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "SlctQuantitySlab Data Insertion Error",
                    data=slct_quant_slab_serializer.errors,
                )
            qty_slab_obj = slct_quant_slab_serializer.save()
            qua_slab_inc = SlctQuantitySlabPropsIncentive.objects.filter(
                quantity_slab__id=qty_slab_obj.id
            )
            if qua_slab_inc:
                qua_slab_inc.delete()
            quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
            quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
            incentive = json.loads(request.data["incentive"])
            incentive_kind = json.loads(request.data["incentive_kind"])
            for val in range(len(quantity_slab_lower)):
                slct_qty_slab_inc_dict = {
                    "quantity_slab_lower": quantity_slab_lower[val],
                    "quantity_slab_upper": quantity_slab_upper[val],
                    "incentive": incentive[val],
                    "incentive_kind": incentive_kind[val],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "quantity_slab": qty_slab_obj.id,
                }

                slct_qty_slab_inc_serializer = SlctQuantitySlabPropsIncentiveSerializer(
                    data=slct_qty_slab_inc_dict
                )
                if not slct_qty_slab_inc_serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "error occurred while inserting slct quantity slab data ",
                        data=slct_qty_slab_inc_serializer.errors,
                    )
                slct_qty_slab_inc_serializer.save()
        return Responses.success_response(
            "slct quantity slab data inserted successfully",
            data=slct_quant_slab_serializer.data,
        )


class SlctDirPltBilngDiscPropsViewSet(ModelViewSet):
    """select direct plt billing discount proposal get and post and patch api"""

    queryset = SlctDirPltBilngDiscProps.objects.all()
    serializer_class = SlctDirPltBilngDiscPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctDirPltBilngDiscPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_dir_plbtbiling_serializer = SlctDirPltBilngDiscPropsSerializer(
            data=request.data
        )
        if not slct_dir_plbtbiling_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "Error occured while inserting direct plant billing data ",
                data=slct_dir_plbtbiling_serializer.errors,
            )
        dir_plbtbiling_obj = slct_dir_plbtbiling_serializer.save()
        district = json.loads(request.data["inc_district"])
        plant = json.loads(request.data["plant"])
        incentive = json.loads(request.data["incentive"])
        for val in range(len(plant)):
            dir_plbtbiling_inc_dict = {
                "inc_district": district[val],
                "plant": plant[val],
                "incentive": incentive[val],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "dir_plt_bilng": dir_plbtbiling_obj.id,
            }

            slct_dir_plbtbiling_inc_serializer = (
                SlctDirPltBilngDiscPropsIncentivesSerializer(
                    data=dir_plbtbiling_inc_dict
                )
            )
            if not slct_dir_plbtbiling_inc_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occured while inserting slct direct plant billing incentive data ",
                    data=slct_dir_plbtbiling_inc_serializer.errors,
                )
            slct_dir_plbtbiling_inc_serializer.save()
        return Responses.success_response(
            "slct direct plant billing data inserted successfully",
            data=slct_dir_plbtbiling_serializer.data,
        )


class UpdateSlctDirPltBilngDiscPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        dir_plt_billing_disc_obj = SlctDirPltBilngDiscProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_dir_plt_billing_serializer = SlctDirPltBilngDiscPropsSerializer(
                dir_plt_billing_disc_obj, data=request.data
            )
            if not slct_dir_plt_billing_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Error occurred while inserting direct plant billing data ",
                    data=slct_dir_plt_billing_serializer.errors,
                )
            dir_plt_billing_obj = slct_dir_plt_billing_serializer.save()
            dir_plt_billing_disc_inc_obj = (
                SlctDirPltBilngDiscPropsIncentives.objects.filter(
                    dir_plt_bilng__id=dir_plt_billing_obj.id
                )
            )
            if dir_plt_billing_disc_inc_obj:
                dir_plt_billing_disc_inc_obj.delete()
            district = json.loads(request.data["inc_district"])
            plant = json.loads(request.data["plant"])
            incentive = json.loads(request.data["incentive"])
            for val in range(len(plant)):
                dir_plbtbiling_inc_dict = {
                    "inc_district": district[val],
                    "plant": plant[val],
                    "incentive": incentive[val],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "dir_plt_bilng": dir_plt_billing_obj.id,
                }

                slct_dir_plt_billing_inc_serializer = (
                    SlctDirPltBilngDiscPropsIncentivesSerializer(
                        data=dir_plbtbiling_inc_dict
                    )
                )
                if not slct_dir_plt_billing_inc_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "error occurred while inserting slct direct plant billing incentive data ",
                        data=slct_dir_plt_billing_inc_serializer.errors,
                    )
                slct_dir_plt_billing_inc_serializer.save()
        return Responses.success_response(
            "slct direct plant billing data inserted successfully",
            data=slct_dir_plt_billing_serializer.data,
        )


class SlctPrmPrdComboScmPropsViewSet(ModelViewSet):
    """select prm product combo scm proposal"""

    queryset = SlctPrmPrdComboScmProps.objects.all()
    serializer_class = SlctPrmPrdComboScmPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctPrmPrdComboScmPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_prm_prod_combo_serializer = SlctPrmPrdComboScmPropsSerializer(
            data=request.data
        )
        if not slct_prm_prod_combo_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "Error occurred while inserting slct premium product combo scheme data ",
                data=slct_prm_prod_combo_serializer.errors,
            )
        slct_prm_prod_combo_obj = slct_prm_prod_combo_serializer.save()
        quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
        quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
        incentive = json.loads(request.data["incentive"])
        inkind_incentive = json.loads(request.data["inkind_incentive"])
        for val in range(len(quantity_slab_lower)):
            slct_prm_prod_combo_inc_dict = {
                "quantity_slab_lower": quantity_slab_lower[val],
                "quantity_slab_upper": quantity_slab_upper[val],
                "incentive": incentive[val],
                "inkind_incentive": inkind_incentive[val],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "prm_prdt_combo": slct_prm_prod_combo_obj.id,
            }
            slct_prm_prod_combo_inc_serializer = (
                SlctPrmPrdComboScmPropsIncentivesSerializer(
                    data=slct_prm_prod_combo_inc_dict
                )
            )
            if not slct_prm_prod_combo_inc_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occurred while inserting slct premium product combo scheme incentive data ",
                    data=slct_prm_prod_combo_inc_serializer.errors,
                )
            slct_prm_prod_combo_inc_serializer.save()
        return Responses.success_response(
            "slct premium product combo scheme data inserted successfully",
            data=slct_prm_prod_combo_serializer.data,
        )


class UpdateSlctPrmPrdComboScmPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        prm_product_combo_obj = SlctPrmPrdComboScmProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_prm_prod_combo_serializer = SlctPrmPrdComboScmPropsSerializer(
                prm_product_combo_obj, data=request.data
            )
            if not slct_prm_prod_combo_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Error occurred while inserting slct premium product combo scheme data ",
                    data=slct_prm_prod_combo_serializer.errors,
                )
            slct_prm_prod_combo_obj = slct_prm_prod_combo_serializer.save()
            prm_product_combo_inc_obj = (
                SlctPrmPrdComboScmPropsIncentives.objects.filter(
                    prm_prdt_combo__id=slct_prm_prod_combo_obj.id
                )
            )
            if prm_product_combo_inc_obj:
                prm_product_combo_inc_obj.delete()
            quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
            quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
            incentive = json.loads(request.data["incentive"])
            inkind_incentive = json.loads(request.data["inkind_incentive"])
            for val in range(len(quantity_slab_lower)):
                slct_prm_prod_combo_inc_dict = {
                    "quantity_slab_lower": quantity_slab_lower[val],
                    "quantity_slab_upper": quantity_slab_upper[val],
                    "incentive": incentive[val],
                    "inkind_incentive": inkind_incentive[val],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "prm_prdt_combo": slct_prm_prod_combo_obj.id,
                }
                slct_prm_prod_combo_inc_serializer = (
                    SlctPrmPrdComboScmPropsIncentivesSerializer(
                        data=slct_prm_prod_combo_inc_dict
                    )
                )
                if not slct_prm_prod_combo_inc_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "error occurred while inserting slct premium product combo scheme incentive data ",
                        data=slct_prm_prod_combo_inc_serializer.errors,
                    )
                slct_prm_prod_combo_inc_serializer.save()
        return Responses.success_response(
            "slct premium product combo scheme data inserted successfully",
            data=slct_prm_prod_combo_serializer.data,
        )


class SlctVehicleSchPropsViewSet(ModelViewSet):
    """select vechicle scheme proposal get and post and patch api"""

    queryset = SlctVehicleSchProps.objects.all()
    serializer_class = SlctVehicleSchPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctVehicleSchPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_vechile_schprops = SlctVehicleSchPropsSerializer(data=request.data)
        if not slct_vechile_schprops.is_valid(raise_exception=True):
            return Responses.error_response(
                "error occurred while inserting data in slct vehicle scheme props ",
                data=slct_vechile_schprops.errors,
            )
        vechicle_sch_props_obj = slct_vechile_schprops.save()
        district = json.loads(request.data["inc_district"])
        plant = json.loads(request.data["plant"])
        city = json.loads(request.data["city"])
        vehicle_type = json.loads(request.data["inc_vehicle_type"])
        incentive = json.loads(request.data["incentive"])

        for value in range(len(plant)):
            sl_ct_vehicle_sch_props_dict = {
                "inc_district": district[value],
                "plant": plant[value],
                "incentive": incentive[value],
                "city": city[value],
                "inc_vehicle_type": vehicle_type[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "vechicle_sch_props": vechicle_sch_props_obj.id,
            }
            sl_ct_vehicle_sch_props = SlctVehicleSchPropsIncentivesSerializer(
                data=sl_ct_vehicle_sch_props_dict
            )

            if not sl_ct_vehicle_sch_props.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in Slct Vehicle Scheme Proposal Incentives",
                    data=sl_ct_vehicle_sch_props.errors,
                )
            sl_ct_vehicle_sch_props.save()
        return Responses.success_response(
            "slct vehicle scheme props data inserted successfully",
            data=slct_vechile_schprops.data,
        )


class UpdateSlctVehicleSchPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        vechile_sch_obj = SlctVehicleSchProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_vechile_schprops = SlctVehicleSchPropsSerializer(
                vechile_sch_obj, data=request.data
            )
            if not slct_vechile_schprops.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occurred while inserting data in slct vehicle scheme props ",
                    data=slct_vechile_schprops.errors,
                )
            vechicle_sch_props_obj = slct_vechile_schprops.save()
            vechile_sch_inc_obj = SlctVehicleSchPropsIncentives.objects.filter(
                vechicle_sch_props__id=vechicle_sch_props_obj.id
            )
            if vechile_sch_inc_obj:
                vechile_sch_inc_obj.delete()
            district = json.loads(request.data["inc_district"])
            plant = json.loads(request.data["plant"])
            city = json.loads(request.data["city"])
            vehicle_type = json.loads(request.data["inc_vehicle_type"])
            incentive = json.loads(request.data["incentive"])

            for value in range(len(plant)):
                sl_ct_vehicle_sch_props_dict = {
                    "inc_district": district[value],
                    "plant": plant[value],
                    "incentive": incentive[value],
                    "city": city[value],
                    "inc_vehicle_type": vehicle_type[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "vechicle_sch_props": vechicle_sch_props_obj.id,
                }
                sl_ct_vehicle_sch_props = SlctVehicleSchPropsIncentivesSerializer(
                    data=sl_ct_vehicle_sch_props_dict
                )

                if not sl_ct_vehicle_sch_props.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "Insertion Error in Slct Vehicle Scheme Proposal Incentives",
                        data=sl_ct_vehicle_sch_props.errors,
                    )
                sl_ct_vehicle_sch_props.save()
        return Responses.success_response(
            "slct vehicle scheme props data inserted successfully",
            data=slct_vechile_schprops.data,
        )


class SlctBorderDiscPropsViewSet(ModelViewSet):
    """select border discount proposal get and post and patch api"""

    queryset = SlctBorderDiscProps.objects.all()
    serializer_class = SlctBorderDiscPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctBorderDiscPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_border_disc_proposal = SlctBorderDiscPropsSerializer(data=request.data)
        if not slct_border_disc_proposal.is_valid(raise_exception=True):
            return Responses.error_response(
                "error occurred while inserting data in slct border discount",
                data=slct_border_disc_proposal.errors,
            )
        slct_border_disc = slct_border_disc_proposal.save()
        district = json.loads(request.data["inc_district"])
        plant = json.loads(request.data["plant"])
        incentive = json.loads(request.data["incentive"])
        for value in range(len(plant)):
            slct_border_disc_props_incentive = {
                "inc_district": district[value],
                "plant": plant[value],
                "incentive": incentive[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "border_disc": slct_border_disc.id,
            }
            slct_border_discount_incentive = SlctBorderDiscPropsIncentivesSerializer(
                data=slct_border_disc_props_incentive
            )
            if not slct_border_discount_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct border discount propsoal incentives",
                    data=slct_border_discount_incentive.errors,
                )
            slct_border_discount_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct border discount incentive",
            data=slct_border_disc_proposal.data,
        )


class UpdateSlctBorderDiscPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        border_disc_obj = SlctBorderDiscProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_border_disc_proposal = SlctBorderDiscPropsSerializer(
                border_disc_obj, data=request.data
            )
            if not slct_border_disc_proposal.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error occurred while inserting data in slct border discount",
                    data=slct_border_disc_proposal.errors,
                )
            slct_border_disc = slct_border_disc_proposal.save()
            border_disc_inc_obj = SlctBorderDiscPropsIncentives.objects.filter(
                border_disc__id=slct_border_disc.id
            )
            if border_disc_inc_obj:
                border_disc_inc_obj.delete()
            district = json.loads(request.data["inc_district"])
            plant = json.loads(request.data["plant"])
            incentive = json.loads(request.data["incentive"])
            for value in range(len(plant)):
                slct_border_disc_props_incentive = {
                    "inc_district": district[value],
                    "plant": plant[value],
                    "incentive": incentive[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "border_disc": slct_border_disc.id,
                }
                slct_border_discount_incentive = (
                    SlctBorderDiscPropsIncentivesSerializer(
                        data=slct_border_disc_props_incentive
                    )
                )
                if not slct_border_discount_incentive.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct border discount propsoal incentives",
                        data=slct_border_discount_incentive.errors,
                    )
                slct_border_discount_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct border discount incentive",
            data=slct_border_disc_proposal.data,
        )


class SlctActivityPropsViewSet(ModelViewSet):
    """select activity proposal get and post and patch api"""

    queryset = SlctActivityProps.objects.all()
    serializer_class = SlctActivityPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctActivityPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_activity_props = SlctActivityPropsSerializer(data=request.data)
        if not slct_activity_props.is_valid(raise_exception=True):
            return Response.error_response(
                "some issue rise in slct activity props",
                data=slct_activity_props.errors,
            )
        slct_activity_props_obj = slct_activity_props.save()
        cost_head = request.data["cost_head"]
        no_of_pax = request.data["no_of_pax"]
        cost_per_head = request.data["cost_per_head"]
        total_expense = request.data["total_expense"]
        for value in range(len(cost_head)):
            slct_activity_props_incentive = {
                "cost_head": cost_head[value],
                "no_of_pax": no_of_pax[value],
                "cost_per_head": cost_per_head[value],
                "total_expense": total_expense[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "activity_props": slct_activity_props_obj.id,
            }
            slct_activity_incentive = SlctActivityPropsIncentiveSerializer(
                data=slct_activity_props_incentive
            )
            if not slct_activity_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion Error in slcl activity incentives",
                    data=slct_activity_incentive.errors,
                )
            slct_activity_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct activity incentive",
            data=slct_activity_props.data,
        )


class UpdateSlctActivityPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        activity_props_obj = SlctActivityProps.objects.get(id=id)
        if id:
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_activity_props = SlctActivityPropsSerializer(
                activity_props_obj, data=request.data
            )
            if not slct_activity_props.is_valid(raise_exception=True):
                return Response.error_response(
                    "some issue rise in slct activity props",
                    data=slct_activity_props.errors,
                )
            slct_activity_props_obj = slct_activity_props.save()
            activity_props_inc_obj = SlctActivityPropsIncentive.objects.filter(
                activity_props__id=slct_activity_props_obj.id
            )
            if activity_props_inc_obj:
                activity_props_inc_obj.delete()
            cost_head = request.data["cost_head"]
            no_of_pax = request.data["no_of_pax"]
            cost_per_head = request.data["cost_per_head"]
            total_expense = request.data["total_expense"]
            for value in range(len(cost_head)):
                slct_activity_props_incentive = {
                    "cost_head": cost_head[value],
                    "no_of_pax": no_of_pax[value],
                    "cost_per_head": cost_per_head[value],
                    "total_expense": total_expense[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "activity_props": slct_activity_props_obj.id,
                }
                slct_activity_incentive = SlctActivityPropsIncentiveSerializer(
                    data=slct_activity_props_incentive
                )
                if not slct_activity_incentive.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion Error in slcl activity incentives",
                        data=slct_activity_incentive.errors,
                    )
                slct_activity_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct activity incentive",
            data=slct_activity_props.data,
        )


class SlctMasonKindSchPropsViewSet(ModelViewSet):
    """select mason kind scheme proposal get and post and patch api"""

    queryset = SlctMasonKindSchProps.objects.all()
    serializer_class = SlctMasonKindSchPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctMasonKindSchPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        mason_kind_sch_serializer = SlctMasonKindSchPropsSerializer(data=request.data)
        if not mason_kind_sch_serializer.is_valid(raise_exception=True):
            return Response.error_response(
                "some issue rise in slct activity props",
                data=mason_kind_sch_serializer.errors,
            )
        mason_kind_sch_obj = mason_kind_sch_serializer.save()

        brand = json.loads(request.data["brand"])
        product = json.loads(request.data["product"])
        packaging = json.loads(request.data["packaging"])
        bags_point_conv_rto = json.loads(request.data["bags_point_conv_rto"])

        for value in range(len(brand)):
            MasonKindSchBagPointConv = {
                "brand": brand[value],
                "product": product[value],
                "packaging": packaging[value],
                "bags_point_conv_rto": bags_point_conv_rto[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "mason_kind_sch": mason_kind_sch_obj.id,
            }
            mason_kind_sch_bag_point_serializer = (
                SlctMasonKindSchBagPointConvSerializer(data=MasonKindSchBagPointConv)
            )
            if not mason_kind_sch_bag_point_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion Error in slcl activity incentives",
                    data=mason_kind_sch_bag_point_serializer.errors,
                )
            mason_kind_sch_bag_point_serializer.save()

        point_slab_lower = json.loads(request.data["point_slab_lower"])
        point_slab_upper = json.loads(request.data["point_slab_upper"])
        inkind_incentive = json.loads(request.data["inkind_incentive"])
        cash_incentive = json.loads(request.data["cash_incentive"])

        for value in range(len(point_slab_lower)):
            MasonKindSchProps = {
                "point_slab_lower": point_slab_lower[value],
                "point_slab_upper": point_slab_upper[value],
                "inkind_incentive": inkind_incentive[value],
                "cash_incentive": cash_incentive[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "mason_kind_sch": mason_kind_sch_obj.id,
            }

            mason_kind_incentive_serializer = SlctMasonKindSchPropsIncentiveSerializer(
                data=MasonKindSchProps
            )
            if not mason_kind_incentive_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion Error in slcl activity incentives",
                    data=mason_kind_incentive_serializer.errors,
                )
            mason_kind_incentive_serializer.save()

        return Responses.success_response(
            "data inserted successfully in slct activity incentive",
            data=mason_kind_sch_serializer.data,
        )


class UpdateSlctMasonKindSchPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_mason_kind_sch_props_obj = SlctMasonKindSchProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            mason_kind_sch_serializer = SlctMasonKindSchPropsSerializer(
                slct_mason_kind_sch_props_obj, data=request.data
            )
            if not mason_kind_sch_serializer.is_valid(raise_exception=True):
                return Response.error_response(
                    "some issue rise in slct activity props",
                    data=mason_kind_sch_serializer.errors,
                )
            mason_kind_sch_obj = mason_kind_sch_serializer.save()
            slct_mason_kind_sch_bag_point = SlctMasonKindSchBagPointConv.objects.filter(
                mason_kind_sch__id=mason_kind_sch_obj.id
            )
            if slct_mason_kind_sch_bag_point:
                slct_mason_kind_sch_bag_point.delete()

            brand = json.loads(request.data["brand"])
            product = json.loads(request.data["product"])
            packaging = json.loads(request.data["packaging"])
            bags_point_conv_rto = json.loads(request.data["bags_point_conv_rto"])

            for value in range(len(brand)):
                MasonKindSchBagPointConv = {
                    "brand": brand[value],
                    "product": product[value],
                    "packaging": packaging[value],
                    "bags_point_conv_rto": bags_point_conv_rto[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "mason_kind_sch": mason_kind_sch_obj.id,
                }
                mason_kind_sch_bag_point_serializer = (
                    SlctMasonKindSchBagPointConvSerializer(
                        data=MasonKindSchBagPointConv
                    )
                )
                if not mason_kind_sch_bag_point_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "insertion Error in slcl activity incentives",
                        data=mason_kind_sch_bag_point_serializer.errors,
                    )
                mason_kind_sch_bag_point_serializer.save()
            slct_mason_kind_sch_bag_point_inc = (
                SlctMasonKindSchPropsIncentive.objects.filter(
                    mason_kind_sch__id=mason_kind_sch_obj.id
                )
            )
            if slct_mason_kind_sch_bag_point_inc:
                slct_mason_kind_sch_bag_point_inc.delete()

            point_slab_lower = json.loads(request.data["point_slab_lower"])
            point_slab_upper = json.loads(request.data["point_slab_upper"])
            inkind_incentive = json.loads(request.data["inkind_incentive"])
            cash_incentive = json.loads(request.data["cash_incentive"])

            for value in range(len(point_slab_lower)):
                MasonKindSchProps = {
                    "point_slab_lower": point_slab_lower[value],
                    "point_slab_upper": point_slab_upper[value],
                    "inkind_incentive": inkind_incentive[value],
                    "cash_incentive": cash_incentive[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "mason_kind_sch": mason_kind_sch_obj.id,
                }

                mason_kind_incentive_serializer = (
                    SlctMasonKindSchPropsIncentiveSerializer(data=MasonKindSchProps)
                )
                if not mason_kind_incentive_serializer.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion Error in slcl activity incentives",
                        data=mason_kind_incentive_serializer.errors,
                    )
                mason_kind_incentive_serializer.save()

        return Responses.success_response(
            "data inserted successfully in slct activity incentive",
            data=mason_kind_sch_serializer.data,
        )


class SlctEngCashSchPtPropsViewSet(ModelViewSet):
    """slct engineer cash scheme proposal get and post and patch api"""

    queryset = SlctEngCashSchPtProps.objects.all()
    serializer_class = SlctEngCashSchPtPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctEngCashSchPtPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_eng_cash_scheme = SlctEngCashSchPtPropsSerializer(data=request.data)
        if not slct_eng_cash_scheme.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise in slct engineer cash scheme point based",
                data=slct_eng_cash_scheme.errors,
            )
        slct_eng_cash_scheme_pt_obj = slct_eng_cash_scheme.save()

        brand = json.loads(request.data["brand"])
        product = json.loads(request.data["product"])
        packaging = json.loads(request.data["packaging"])
        bags_point_conv_rto = json.loads(request.data["bags_point_conv_rto"])
        for value in range(len(brand)):
            slct_eng_cash_schpt_bagpoint_dict = {
                "brand": brand[value],
                "product": product[value],
                "packaging": packaging[value],
                "bags_point_conv_rto": bags_point_conv_rto[value],
                "eng_cash_sch_pt": slct_eng_cash_scheme_pt_obj.id,
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
            }
            slct_eng_cash_scheme_pt_conv = SlctEngCashSchPtBagPointConvSerializer(
                data=slct_eng_cash_schpt_bagpoint_dict
            )
            if not slct_eng_cash_scheme_pt_conv.is_valid(raise_exception=True):
                return Responses.error_response(
                    "error while inserting data in slct engineer cash scheme bag point conv",
                    data=slct_eng_cash_scheme_pt_conv.errors,
                )
            slct_eng_cash_scheme_pt_conv.save()

        point_slab_lower = json.loads(request.data["point_slab_lower"])
        point_slab_upper = json.loads(request.data["point_slab_upper"])
        in_kind_incentive = json.loads(request.data["in_kind_incentive"])
        cash_incentive = json.loads(request.data["cash_incentive"])
        for values in range(len(point_slab_lower)):
            slct_eng_cash_ptprops_incentive_dict = {
                "point_slab_lower": point_slab_lower[values],
                "point_slab_upper": point_slab_upper[values],
                "in_kind_incentive": in_kind_incentive[values],
                "cash_incentive": cash_incentive[values],
                "eng_cash_sch_pt": slct_eng_cash_scheme_pt_obj.id,
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
            }
            slct_eng_cash_ptprops_incentive = SlctEngCashSchPtPropsIncentiveSerializer(
                data=slct_eng_cash_ptprops_incentive_dict
            )
            if not slct_eng_cash_ptprops_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise in slct engineer cash point proposal incentive",
                    data=slct_eng_cash_ptprops_incentive.errors,
                )
            slct_eng_cash_ptprops_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct engineer cash point proposal incentive",
            data=slct_eng_cash_scheme.data,
        )


class UpdateSlctEngCashSchPtPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_eng_cash_sch_obj = SlctEngCashSchPtProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_eng_cash_scheme = SlctEngCashSchPtPropsSerializer(
                slct_eng_cash_sch_obj, data=request.data
            )
            if not slct_eng_cash_scheme.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise in slct engineer cash scheme point based",
                    data=slct_eng_cash_scheme.errors,
                )
            slct_eng_cash_scheme_pt_obj = slct_eng_cash_scheme.save()
            slct_eng_cash_sch_point_conv_obj = (
                SlctEngCashSchPtBagPointConv.objects.filter(
                    eng_cash_sch_pt__id=slct_eng_cash_scheme_pt_obj.id
                )
            )
            if slct_eng_cash_sch_point_conv_obj:
                slct_eng_cash_sch_point_conv_obj.delete()
            brand = json.loads(request.data["brand"])
            product = json.loads(request.data["product"])
            packaging = json.loads(request.data["packaging"])
            bags_point_conv_rto = json.loads(request.data["bags_point_conv_rto"])
            for value in range(len(brand)):
                slct_eng_cash_schpt_bagpoint_dict = {
                    "brand": brand[value],
                    "product": product[value],
                    "packaging": packaging[value],
                    "bags_point_conv_rto": bags_point_conv_rto[value],
                    "eng_cash_sch_pt": slct_eng_cash_scheme_pt_obj.id,
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                }
                slct_eng_cash_scheme_pt_conv = SlctEngCashSchPtBagPointConvSerializer(
                    data=slct_eng_cash_schpt_bagpoint_dict
                )
                if not slct_eng_cash_scheme_pt_conv.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "error while inserting data in slct engineer cash scheme bag point conv",
                        data=slct_eng_cash_scheme_pt_conv.errors,
                    )
                slct_eng_cash_scheme_pt_conv.save()
            slct_eng_cash_sch_inc_obj = SlctEngCashSchPtPropsIncentive.objects.filter(
                eng_cash_sch_pt__id=slct_eng_cash_scheme_pt_obj.id
            )
            if slct_eng_cash_sch_inc_obj:
                slct_eng_cash_sch_inc_obj.delete()
            point_slab_lower = json.loads(request.data["point_slab_lower"])
            point_slab_upper = json.loads(request.data["point_slab_upper"])
            in_kind_incentive = json.loads(request.data["in_kind_incentive"])
            cash_incentive = json.loads(request.data["cash_incentive"])
            for values in range(len(point_slab_lower)):
                slct_eng_cash_ptprops_incentive_dict = {
                    "point_slab_lower": point_slab_lower[values],
                    "point_slab_upper": point_slab_upper[values],
                    "in_kind_incentive": in_kind_incentive[values],
                    "cash_incentive": cash_incentive[values],
                    "eng_cash_sch_pt": slct_eng_cash_scheme_pt_obj.id,
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                }
                slct_eng_cash_ptprops_incentive = (
                    SlctEngCashSchPtPropsIncentiveSerializer(
                        data=slct_eng_cash_ptprops_incentive_dict
                    )
                )
                if not slct_eng_cash_ptprops_incentive.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "some issue rise in slct engineer cash point proposal incentive",
                        data=slct_eng_cash_ptprops_incentive.errors,
                    )
                slct_eng_cash_ptprops_incentive.save()
        return Responses.success_response(
            "data inserted successfully in slct engineer cash point proposal incentive",
            data=slct_eng_cash_scheme.data,
        )


class SlctRailBasedSchPropsViewSet(ModelViewSet):
    queryset = SlctRailBasedSchProps.objects.all()
    serializer_class = SlctRailBasedSchPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctRailBasedSchPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        rail_based_sch = SlctRailBasedSchPropsSerializer(data=request.data)
        if not rail_based_sch.is_valid(raise_exception=True):
            return Response.error_response(
                "Insertion Error in SlctRailBasedSchProps",
                data=rail_based_sch.errors,
            )
        rail_based_sch_obj = rail_based_sch.save()

        point_slab_lower = json.loads(request.data["point_slab_lower"])
        point_slab_upper = json.loads(request.data["point_slab_upper"])
        incentive_total_sales = json.loads(request.data["incentive_total_sales"])
        in_kind_incentive = json.loads(request.data["in_kind_incentive"])

        for value in range(len(point_slab_lower)):
            rail_based_sch_incentive_data = {
                "point_slab_lower": point_slab_lower[value],
                "point_slab_upper": point_slab_upper[value],
                "incentive_total_sales": incentive_total_sales[value],
                "in_kind_incentive": in_kind_incentive[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "rail_based_sch": rail_based_sch_obj.id,
            }
            rail_based_sch_incentive_serializer = (
                SlctRailBasedSchPropsIncentiveSerializer(
                    data=rail_based_sch_incentive_data
                )
            )
            if not rail_based_sch_incentive_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in SlclActivityIncentives",
                    data=rail_based_sch_incentive_serializer.errors,
                )
            rail_based_sch_incentive_serializer.save()
        return Responses.success_response(
            "Data Inserted Successfully in SlctRailBasedSchProps & Incentive",
            data=rail_based_sch.data,
        )


class UpdateSlctRailBasedSchPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_rail_based_obj = SlctRailBasedSchProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            rail_based_sch = SlctRailBasedSchPropsSerializer(
                slct_rail_based_obj, data=request.data
            )
            if not rail_based_sch.is_valid(raise_exception=True):
                return Response.error_response(
                    "Insertion Error in SlctRailBasedSchProps",
                    data=rail_based_sch.errors,
                )
            rail_based_sch_obj = rail_based_sch.save()
            rail_based_sch_inc_obj = SlctRailBasedSchPropsIncentive.objects.filter(
                rail_based_sch__id=rail_based_sch_obj.id
            )
            if rail_based_sch_inc_obj:
                rail_based_sch_inc_obj.delete()
            point_slab_lower = json.loads(request.data["point_slab_lower"])
            point_slab_upper = json.loads(request.data["point_slab_upper"])
            incentive_total_sales = json.loads(request.data["incentive_total_sales"])
            in_kind_incentive = json.loads(request.data["in_kind_incentive"])

            for value in range(len(point_slab_lower)):
                rail_based_sch_incentive_data = {
                    "point_slab_lower": point_slab_lower[value],
                    "point_slab_upper": point_slab_upper[value],
                    "incentive_total_sales": incentive_total_sales[value],
                    "in_kind_incentive": in_kind_incentive[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "rail_based_sch": rail_based_sch_obj.id,
                }
                rail_based_sch_incentive_serializer = (
                    SlctRailBasedSchPropsIncentiveSerializer(
                        data=rail_based_sch_incentive_data
                    )
                )
                if not rail_based_sch_incentive_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in SlclActivityIncentives",
                        data=rail_based_sch_incentive_serializer.errors,
                    )
                rail_based_sch_incentive_serializer.save()
        return Responses.success_response(
            "Data Inserted Successfully in SlctRailBasedSchProps & Incentive",
            data=rail_based_sch.data,
        )


class SlctDealerOutsBasedPropsViewSet(ModelViewSet):
    queryset = SlctDealerOutsBasedProps.objects.all()
    serializer_class = SlctDealerOutsBasedPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctDealerOutsBasedPropsFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        dealer_outs_props_serializer = SlctDealerOutsBasedPropsSerializer(
            data=request.data
        )
        if not dealer_outs_props_serializer.is_valid(raise_exception=True):
            return Response.error_response(
                "Insertion Error in SlctDealerOutsBasedProp",
                data=dealer_outs_props_serializer.errors,
            )
        dealer_outs_props_obj = dealer_outs_props_serializer.save()

        outstanding_threshold = json.loads(request.data["outstanding_threshold"])
        target_incentive = json.loads(request.data["target_incentive"])
        in_kind_incentive = json.loads(request.data["in_kind_incentive"])

        for value in range(len(outstanding_threshold)):
            dealer_outs_sch_incentive_data = {
                "outstanding_threshold": outstanding_threshold[value],
                "target_incentive": target_incentive[value],
                "in_kind_incentive": in_kind_incentive[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "dealer_outs": dealer_outs_props_obj.id,
            }

            dealer_outs_sch_incentive_serializer = (
                SlctDealerOutsBasedPropsIncentiveSerializer(
                    data=dealer_outs_sch_incentive_data
                )
            )
            if not dealer_outs_sch_incentive_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in SlctDealerOutsBasedPropIncentive",
                    data=dealer_outs_sch_incentive_serializer.errors,
                )
            dealer_outs_sch_incentive_serializer.save()

        return Responses.success_response(
            "Data Inserted Successfully in SlctDealerOutsBasedProp & Incentive",
            data=dealer_outs_props_serializer.data,
        )


class UpdateSlctDealerOutsBasedPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_dealer_outsbased_obj = SlctDealerOutsBasedProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            dealer_outs_props_serializer = SlctDealerOutsBasedPropsSerializer(
                slct_dealer_outsbased_obj, data=request.data
            )
            if not dealer_outs_props_serializer.is_valid(raise_exception=True):
                return Response.error_response(
                    "Insertion Error in SlctDealerOutsBasedProp",
                    data=dealer_outs_props_serializer.errors,
                )
            dealer_outs_props_obj = dealer_outs_props_serializer.save()
            slct_dealer_outsbased_inc = (
                SlctDealerOutsBasedPropsIncentive.objects.filter(
                    dealer_outs__id=dealer_outs_props_obj.id
                )
            )
            if slct_dealer_outsbased_inc:
                slct_dealer_outsbased_inc.delete()
            outstanding_threshold = json.loads(request.data["outstanding_threshold"])
            target_incentive = json.loads(request.data["target_incentive"])
            in_kind_incentive = json.loads(request.data["in_kind_incentive"])

            for value in range(len(outstanding_threshold)):
                dealer_outs_sch_incentive_data = {
                    "outstanding_threshold": outstanding_threshold[value],
                    "target_incentive": target_incentive[value],
                    "in_kind_incentive": in_kind_incentive[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "dealer_outs": dealer_outs_props_obj.id,
                }

                dealer_outs_sch_incentive_serializer = (
                    SlctDealerOutsBasedPropsIncentiveSerializer(
                        data=dealer_outs_sch_incentive_data
                    )
                )
                if not dealer_outs_sch_incentive_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in SlctDealerOutsBasedPropIncentive",
                        data=dealer_outs_sch_incentive_serializer.errors,
                    )
                dealer_outs_sch_incentive_serializer.save()
        return Responses.success_response(
            "Data Inserted Successfully in SlctDealerOutsBasedProp & Incentive",
            data=dealer_outs_props_serializer.data,
        )


class SlctDealerLinkedSchPropsViewSet(ModelViewSet):
    """slct dealer linked scheme proposal get post and patch api""" ""

    queryset = SlctDealerLinkedSchProps.objects.all()
    serializer_class = SlctDealerLinkedSchPropsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctDealerLinkedSchPropsFilter

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_dealer_linked_scheme = SlctDealerLinkedSchPropsSerializer(
            data=request.data
        )
        if not slct_dealer_linked_scheme.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in slct dealer linked scheme proposal",
                data=slct_dealer_linked_scheme.errors,
            )
        slct_dealer_linked_scheme_obj = slct_dealer_linked_scheme.save()
        quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
        quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
        incentive_on_t_sale = json.loads(request.data["incentive_on_t_sale"])
        inkind_incentive = json.loads(request.data["inkind_incentive"])
        point = json.loads(request.data["points"])
        add_incentive_thres = json.loads(request.data["add_incentive_thres"])
        add_incentive = json.loads(request.data["add_incentive"])
        add_inkind_incentive = json.loads(request.data["add_inkind_incentive"])
        add_points = json.loads(request.data["add_points"])
        for value in range(len(quantity_slab_lower)):
            quantity_slab_lower_incentive_dict = {
                "quantity_slab_lower": quantity_slab_lower[value],
                "quantity_slab_upper": quantity_slab_upper[value],
                "incentive_on_t_sale": incentive_on_t_sale[value],
                "inkind_incentive": inkind_incentive[value],
                "points": point[value],
                "add_incentive_thres": add_incentive_thres[value],
                "add_incentive": add_incentive[value],
                "add_inkind_incentive": add_inkind_incentive[value],
                "add_points": add_points[value],
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
                "dealer_linked_sch": slct_dealer_linked_scheme_obj.id,
            }
            slct_dealer_linked_scheme_props_conversation = (
                SlctDealerLinkedSchPropsIncentiveSerializer(
                    data=quantity_slab_lower_incentive_dict
                )
            )
            if not slct_dealer_linked_scheme_props_conversation.is_valid(
                raise_exception=True
            ):
                return Responses.error_response(
                    "insertion error in  slct  dealer linked scheme proposal incentive",
                    slct_dealer_linked_scheme_props_conversation.errors,
                )
            slct_dealer_linked_scheme_props_conversation.save()
        return Responses.success_response(
            "data inserted successfully in  slct  dealer linked scheme proposal incentive",
            data=slct_dealer_linked_scheme.data,
        )


class UpdateSlctDealerLinkedSchPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_dealer_linked_sch_obj = SlctDealerLinkedSchProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_dealer_linked_scheme = SlctDealerLinkedSchPropsSerializer(
                slct_dealer_linked_sch_obj, data=request.data
            )
            if not slct_dealer_linked_scheme.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct dealer linked scheme proposal",
                    data=slct_dealer_linked_scheme.errors,
                )
            slct_dealer_linked_scheme_obj = slct_dealer_linked_scheme.save()
            slct_dealer_linked_sch_inc_obj = (
                SlctDealerLinkedSchPropsIncentive.objects.filter(
                    dealer_linked_sch__id=slct_dealer_linked_scheme_obj.id
                )
            )
            if slct_dealer_linked_sch_inc_obj:
                slct_dealer_linked_sch_inc_obj.delete()
            quantity_slab_lower = json.loads(request.data["quantity_slab_lower"])
            quantity_slab_upper = json.loads(request.data["quantity_slab_upper"])
            incentive_on_t_sale = json.loads(request.data["incentive_on_t_sale"])
            inkind_incentive = json.loads(request.data["inkind_incentive"])
            point = json.loads(request.data["points"])
            add_incentive_thres = json.loads(request.data["add_incentive_thres"])
            add_incentive = json.loads(request.data["add_incentive"])
            add_inkind_incentive = json.loads(request.data["add_inkind_incentive"])
            add_points = json.loads(request.data["add_points"])
            for value in range(len(quantity_slab_lower)):
                quantity_slab_lower_incentive_dict = {
                    "quantity_slab_lower": quantity_slab_lower[value],
                    "quantity_slab_upper": quantity_slab_upper[value],
                    "incentive_on_t_sale": incentive_on_t_sale[value],
                    "inkind_incentive": inkind_incentive[value],
                    "points": point[value],
                    "add_incentive_thres": add_incentive_thres[value],
                    "add_incentive": add_incentive[value],
                    "add_inkind_incentive": add_inkind_incentive[value],
                    "add_points": add_points[value],
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                    "dealer_linked_sch": slct_dealer_linked_scheme_obj.id,
                }
                slct_dealer_linked_scheme_props_conversation = (
                    SlctDealerLinkedSchPropsIncentiveSerializer(
                        data=quantity_slab_lower_incentive_dict
                    )
                )
                if not slct_dealer_linked_scheme_props_conversation.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "insertion error in  slct  dealer linked scheme proposal incentive",
                        slct_dealer_linked_scheme_props_conversation.errors,
                    )
                slct_dealer_linked_scheme_props_conversation.save()
        return Responses.success_response(
            "data inserted successfully in  slct  dealer linked scheme proposal incentive",
            data=slct_dealer_linked_scheme.data,
        )


class SlctCombSlabGrowthPropsViewSet(ModelViewSet):
    """Combination of slab growth based scheme proposal view class."""

    queryset = SlctCombSlabGrowthProps.objects.all()
    serializer_class = SlctCombSlabGrowthPropsSerializer
    pagination_class = CustomPagination
    lookup_field = "id"
    filterset_class = SlctCombSlabGrowthPropsFilter

    # parser_classes = (MultipartJsonParser,)
    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        saletype = json.loads(request.data["saletype"])
        saletype = ", ".join(saletype)
        product = json.loads(request.data["product"])
        product = ", ".join(product)
        request.data["saletype"] = saletype
        request.data["product"] = product
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_comb_slab_growth = SlctCombSlabGrowthPropsSerializer(data=request.data)
        if not slct_comb_slab_growth.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in this table ", slct_comb_slab_growth.errors
            )
        slct_comb_slab_growth_obj = slct_comb_slab_growth.save()
        for inc_obj in json.loads(request.data["incentives"]):
            inc_obj["comb_slab_props"] = slct_comb_slab_growth_obj.id
            inc_obj["created_by"] = request.user.id
            inc_obj["last_updated_by"] = request.user.id
            inc_obj["last_update_login"] = request.user.id
            slct_comb_slab_growth_incentive_obj = (
                SlctCombSlabGrowthPropsIncentiveSerializer(data=inc_obj)
            )
            if not slct_comb_slab_growth_incentive_obj.is_valid(raise_exception=True):
                return Responses.error_response(
                    "data wrong in slct comb slab growth table",
                    slct_comb_slab_growth_incentive_obj.errors,
                )
            slct_comb_slab_growth_incentive_obj.save()
        return Responses.success_response(
            "data successfully add in slct comb growth table",
            data=slct_comb_slab_growth.data,
        )


class UpdateSlctCombSlabGrowthPropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_comb_slab_growth_obj = SlctCombSlabGrowthProps.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            saletype = json.loads(request.data["saletype"])
            saletype = ", ".join(saletype)
            product = json.loads(request.data["product"])
            product = ", ".join(product)
            request.data["saletype"] = saletype
            request.data["product"] = product
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_comb_slab_growth_props = UpdateSlctCombSlabGrowthPropsSerializer(
                slct_comb_slab_growth_obj, data=request.data
            )
            if not slct_comb_slab_growth_props.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct combination slab growth proposal",
                    slct_comb_slab_growth_props.errors,
                )
            slct_comb_slab_growth_props_obj = slct_comb_slab_growth_props.save()
            slct_comb_slab_growth_props_incentive_obj = (
                SlctCombSlabGrowthPropsIncentive.objects.filter(
                    comb_slab_props__id=slct_comb_slab_growth_props_obj.id
                )
            )
            if slct_comb_slab_growth_props_incentive_obj:
                slct_comb_slab_growth_props_incentive_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["comb_slab_props"] = slct_comb_slab_growth_props_obj.id
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id

                slct_comb_slab_growth_props_incentive_serializer = (
                    UpdateSlctCombSlabGrowthPropsIncentiveSerializer(data=inc_data)
                )
                if not slct_comb_slab_growth_props_incentive_serializer.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "insertion error in slct inkind booster incentives",
                        slct_comb_slab_growth_props_incentive_serializer.errors,
                    )
                slct_comb_slab_growth_props_incentive_serializer.save()
        return Responses.success_response(
            "data insterted successfully in slct combination slab growth props data",
            data=slct_comb_slab_growth_props.data,
        )


class SlctAnnualDiscTargetBasedViewSet(ModelViewSet):
    """slct annual disc proposal target"""

    queryset = SlctAnnualDiscTargetBased.objects.all()
    serializer_class = SlctAnnualDiscTargetBasedSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"
    filterset_class = SlctAnnualDiscTargetBasedFilter

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_annual_disc_target = SlctAnnualDiscTargetBasedSerializer(data=request.data)
        if not slct_annual_disc_target.is_valid(raise_exception=True):
            return Response.error_response(
                "insertion error in slct annual disc target",
                data=slct_annual_disc_target.errors,
            )
        slct_annual_disc_target_obj = slct_annual_disc_target.save()
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data["annual_disc_props_slab"] = slct_annual_disc_target_obj.id
            slct_annual_disc_incentive = SlctAnnualDiscTargetBasedIncentivesSerializer(
                data=inc_data
            )
            if not slct_annual_disc_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct annual disc proposal target incentive",
                    data=slct_annual_disc_incentive.errors,
                )
            slct_annual_disc_incentive.save()
        return Responses.success_response(
            "data inserted  in slct annual disc target ",
            data=slct_annual_disc_target.data,
        )


class UpdateSlctAnnualDiscTargetBasedViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        slct_annual_disc_target_obj = SlctAnnualDiscTargetBased.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_annual_disc_target = SlctAnnualDiscTargetBasedSerializer(
                slct_annual_disc_target_obj, data=request.data
            )
            if not slct_annual_disc_target.is_valid(raise_exception=True):
                return Response.error_response(
                    "insertion error in slct annual disc target",
                    data=slct_annual_disc_target.errors,
                )
            slct_annual_disc_target_obj = slct_annual_disc_target.save()
            slct_annual_target_based_inc = (
                SlctAnnualDiscTargetBasedIncentives.objects.filter(
                    annual_disc_props_slab__id=slct_annual_disc_target_obj.id
                )
            )
            if slct_annual_target_based_inc:
                slct_annual_target_based_inc.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["annual_disc_props_slab"] = slct_annual_disc_target_obj.id
                slct_annual_disc_incentive = (
                    SlctAnnualDiscTargetBasedIncentivesSerializer(data=inc_data)
                )
                if not slct_annual_disc_incentive.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct annual disc proposal target incentive",
                        data=slct_annual_disc_incentive.errors,
                    )
                slct_annual_disc_incentive.save()
        return Responses.success_response(
            "data inserted  in slct annual disc target ",
            data=slct_annual_disc_target.data,
        )


class SlctAnnualDiscSlabBasedViewSet(ModelViewSet):
    """slct annual disc slab based veiwset"""

    queryset = SlctAnnualDiscSlabBased.objects.all()
    serializer_class = SlctAnnualDiscSlabBasedSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctAnnualDiscSlabBasedFilter
    pagination_class = CustomPagination

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_annual_disc_slab_based = SlctAnnualDiscSlabBasedSerializer(
            data=request.data
        )
        if not slct_annual_disc_slab_based.is_valid(raise_exception=True):
            return Responses(
                "insertion error in slct annual disc target",
                slct_annual_disc_slab_based.errors,
            )
        slct_annual_disc_slab_based_obj = slct_annual_disc_slab_based.save()
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data["disc_props_tgt"] = slct_annual_disc_slab_based_obj.id
            slct_annual_disc_slab_based_incentive = (
                SlctAnnualDiscSlabBasedIncentiveSerializer(data=inc_data)
            )
            if not slct_annual_disc_slab_based_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct annual disc target incentive",
                    slct_annual_disc_slab_based_incentive.errors,
                )
            slct_annual_disc_slab_based_incentive.save()
            return Responses.success_response(
                "data inserted  in slct annual disc target",
                data=slct_annual_disc_slab_based.data,
            )


class UpdateSlctAnnualDiscSlabBasedViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        annual_disc_slab_based = SlctAnnualDiscSlabBased.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_annual_disc_slab_based = SlctAnnualDiscSlabBasedSerializer(
                annual_disc_slab_based, data=request.data
            )
            if not slct_annual_disc_slab_based.is_valid(raise_exception=True):
                return Responses(
                    "insertion error in slct annual disc target",
                    slct_annual_disc_slab_based.errors,
                )
            slct_annual_disc_slab_based_obj = slct_annual_disc_slab_based.save()
            annual_disc_slab_based_inc = (
                SlctAnnualDiscSlabBasedIncentive.objects.filter(
                    disc_props_tgt__id=slct_annual_disc_slab_based_obj.id
                )
            )
            if annual_disc_slab_based_inc:
                annual_disc_slab_based_inc.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["disc_props_tgt"] = slct_annual_disc_slab_based_obj.id
                slct_annual_disc_slab_based_incentive = (
                    SlctAnnualDiscSlabBasedIncentiveSerializer(data=inc_data)
                )
                if not slct_annual_disc_slab_based_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "insertion error in slct annual disc target incentive",
                        slct_annual_disc_slab_based_incentive.errors,
                    )
                slct_annual_disc_slab_based_incentive.save()
            return Responses.success_response(
                "data inserted  in slct annual disc target",
                data=slct_annual_disc_slab_based.data,
            )


class SlctVolCutterTargetBasedViewSet(ModelViewSet):
    """slct vol cutter target based viewset get post and patch api"""

    queryset = SlctVolCutterTargetBased.objects.all()
    serializer_class = SlctVolCutterTargetBasedSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = SlctVolCutterTargetBasedFilter
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_vol_cutter_target_based = SlctVolCutterTargetBasedSerializer(
            data=request.data
        )
        if not slct_vol_cutter_target_based.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct vol cutter target based",
                data=slct_vol_cutter_target_based.errors,
            )
        slct_vol_cutter_target_based_obj = slct_vol_cutter_target_based.save()
        if slct_vol_cutter_target_based_obj:
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["vol_cutter_slab_basd"] = slct_vol_cutter_target_based_obj.id
                slct_vol_cutter_slab_based_incentive = (
                    SlctVolCutterTargetBasedIncentiveSerializer(data=inc_data)
                )
                if not slct_vol_cutter_slab_based_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct vol cutter target based incentive",
                        slct_vol_cutter_slab_based_incentive.errors,
                    )
                slct_vol_cutter_slab_based_incentive.save()
        return Responses.success_response(
            "data inserted  in slct vol cutter target based",
            data=slct_vol_cutter_target_based.data,
        )


class UpdateSlctVolCutterTargetBasedViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        vol_cutter_target_obj = SlctVolCutterTargetBased.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_vol_cutter_target_based = SlctVolCutterTargetBasedSerializer(
                vol_cutter_target_obj, data=request.data
            )
            if not slct_vol_cutter_target_based.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct vol cutter target based",
                    data=slct_vol_cutter_target_based.errors,
                )
            slct_vol_cutter_target_based_obj = slct_vol_cutter_target_based.save()
            vol_cutter_target_inc_obj = (
                SlctVolCutterTargetBasedIncentive.objects.filter(
                    vol_cutter_slab_basd__id=slct_vol_cutter_target_based_obj.id
                )
            )
            if vol_cutter_target_inc_obj:
                vol_cutter_target_inc_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["vol_cutter_slab_basd"] = slct_vol_cutter_target_based_obj.id
                slct_vol_cutter_slab_based_incentive = (
                    SlctVolCutterTargetBasedIncentiveSerializer(data=inc_data)
                )
                if not slct_vol_cutter_slab_based_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct vol cutter target based incentive",
                        slct_vol_cutter_slab_based_incentive.errors,
                    )
                slct_vol_cutter_slab_based_incentive.save()
        return Responses.success_response(
            "data inserted  in slct vol cutter target based",
            data=slct_vol_cutter_target_based.data,
        )


class SlctVolCutterSlabBasedProposalViewSet(ModelViewSet):
    """slct vol cutter slab based proposal get post and patch api"""

    queryset = SlctVolCutterSlabBasedProposal.objects.all()
    serializer_class = SlctVolCutterSlabBasedProposalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctVolCutterSlabBasedProposalFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_vol_cutter_slab_based = SlctVolCutterSlabBasedProposalSerializer(
            data=request.data
        )
        if not slct_vol_cutter_slab_based.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct vol cutter slab based",
                slct_vol_cutter_slab_based.errors,
            )
        slct_vol_cutter_slab_based_obj = slct_vol_cutter_slab_based.save()
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data["vol_cutter_slab_bsd"] = slct_vol_cutter_slab_based_obj.id
            slct_vol_cutter_slab_based_incentive = (
                SlctVolCutterSlabBasedProposalIncentivesSerializer(data=inc_data)
            )
            if not slct_vol_cutter_slab_based_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct vol cutter slab based incentive",
                    slct_vol_cutter_slab_based_incentive.errors,
                )
            slct_vol_cutter_slab_based_incentive.save()
        return Responses.success_response(
            "data inserted  in slct vol cutter slab based incentive",
            data=slct_vol_cutter_slab_based.data,
        )


class UpdateSlctVolCutterSlabBasedProposalViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        vol_cutter_slab_based_obj = SlctVolCutterSlabBasedProposal.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_vol_cutter_slab_based = SlctVolCutterSlabBasedProposalSerializer(
                vol_cutter_slab_based_obj, data=request.data
            )
            if not slct_vol_cutter_slab_based.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct vol cutter slab based",
                    slct_vol_cutter_slab_based.errors,
                )
            slct_vol_cutter_slab_based_obj = slct_vol_cutter_slab_based.save()
            vol_cutter_slab_based_inc_obj = (
                SlctVolCutterSlabBasedProposalIncentives.objects.filter(
                    vol_cutter_slab_bsd__id=slct_vol_cutter_slab_based_obj.id
                )
            )
            if vol_cutter_slab_based_inc_obj:
                vol_cutter_slab_based_inc_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["vol_cutter_slab_bsd"] = slct_vol_cutter_slab_based_obj.id
                slct_vol_cutter_slab_based_incentive = (
                    SlctVolCutterSlabBasedProposalIncentivesSerializer(data=inc_data)
                )
                if not slct_vol_cutter_slab_based_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct vol cutter slab based incentive",
                        slct_vol_cutter_slab_based_incentive.errors,
                    )
                slct_vol_cutter_slab_based_incentive.save()
        return Responses.success_response(
            "data inserted  in slct vol cutter slab based incentive",
            data=slct_vol_cutter_slab_based.data,
        )


class SlctBoosterPerDayTargetSchemeViewSet(ModelViewSet):
    """slct booser per day target scheme get post and patch api"""

    queryset = SlctBoosterPerDayTargetScheme.objects.all()
    serializer_class = SlctBoosterPerDayTargetSchemeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctBoosterPerDayTargetSchemeFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_booster_per_day_target_scheme = SlctBoosterPerDayTargetSchemeSerializer(
            data=request.data
        )
        if not slct_booster_per_day_target_scheme.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct booster per day target scheme",
                slct_booster_per_day_target_scheme.errors,
            )
        slct_booster_per_day_target_scheme_obj = (
            slct_booster_per_day_target_scheme.save()
        )
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data[
                "booster_per_day_target"
            ] = slct_booster_per_day_target_scheme_obj.id
            slct_booster_per_day_target_scheme_incentive = (
                SlctBoosterPerDayTargetSchemeIncentiveSerializer(data=inc_data)
            )
            if not slct_booster_per_day_target_scheme_incentive.is_valid(
                raise_exception=True
            ):
                return Responses.error_response(
                    "Insertion Error in slct booster per day target scheme incentive",
                    slct_booster_per_day_target_scheme_incentive.errors,
                )
            slct_booster_per_day_target_scheme_incentive.save()
        return Responses.success_response(
            "data inserted  in slct  booster per day target scheme incentive",
            data=slct_booster_per_day_target_scheme.data,
        )


class UpdateSlctBoosterPerDayTargetSchemeViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        booster_per_day_target_obj = SlctBoosterPerDayTargetScheme.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_booster_per_day_target_scheme = (
                SlctBoosterPerDayTargetSchemeSerializer(
                    booster_per_day_target_obj, data=request.data
                )
            )
            if not slct_booster_per_day_target_scheme.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct booster per day target scheme",
                    slct_booster_per_day_target_scheme.errors,
                )
            slct_booster_per_day_target_scheme_obj = (
                slct_booster_per_day_target_scheme.save()
            )
            booster_per_day_target_inc_obj = (
                SlctBoosterPerDayTargetSchemeIncentive.objects.filter(
                    booster_per_day_target__id=slct_booster_per_day_target_scheme_obj.id
                )
            )
            if booster_per_day_target_inc_obj:
                booster_per_day_target_inc_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data[
                    "booster_per_day_target"
                ] = slct_booster_per_day_target_scheme_obj.id
                slct_booster_per_day_target_scheme_incentive = (
                    SlctBoosterPerDayTargetSchemeIncentiveSerializer(data=inc_data)
                )
                if not slct_booster_per_day_target_scheme_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct booster per day target scheme incentive",
                        slct_booster_per_day_target_scheme_incentive.errors,
                    )
                slct_booster_per_day_target_scheme_incentive.save()
        return Responses.success_response(
            "data inserted  in slct  booster per day target scheme incentive",
            data=slct_booster_per_day_target_scheme.data,
        )


class SlctBoosterPerDayGrowthSchemeViewSet(ModelViewSet):
    """slct booster per day growth scheme get post and patch api"""

    queryset = SlctBoosterPerDayGrowthScheme.objects.all()
    serializer_class = SlctBoosterPerDayGrowthSchemeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctBoosterPerDayGrowthSchemeFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_booster_per_day_growth_scheme = SlctBoosterPerDayGrowthSchemeSerializer(
            data=request.data
        )
        if not slct_booster_per_day_growth_scheme.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct booster per day growth scheme",
                slct_booster_per_day_growth_scheme.errors,
            )
        slct_booster_per_day_growth_scheme_obj = (
            slct_booster_per_day_growth_scheme.save()
        )
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data[
                "booster_per_growth_target"
            ] = slct_booster_per_day_growth_scheme_obj.id

            slct_booster_per_day_growth_scheme_incentive = (
                SlctBoosterPerDayGrowthSchemeIncentiveSerializer(data=inc_data)
            )
        if not slct_booster_per_day_growth_scheme_incentive.is_valid(
            raise_exception=True
        ):
            return Responses.error_response(
                "Insertion Error in slct booster per day growth scheme incentive",
                slct_booster_per_day_growth_scheme_incentive.errors,
            )
        slct_booster_per_day_growth_scheme_incentive.save()
        return Responses.success_response(
            "data inserted  in slct  booster per day growth scheme incentive",
            data=slct_booster_per_day_growth_scheme.data,
        )


class UpdateSlctBoosterPerDayGrowthSchemeViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        per_day_growth_scheme = SlctBoosterPerDayGrowthScheme.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_booster_per_day_growth_scheme = (
                SlctBoosterPerDayGrowthSchemeSerializer(
                    per_day_growth_scheme, data=request.data
                )
            )
            if not slct_booster_per_day_growth_scheme.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct booster per day growth scheme",
                    slct_booster_per_day_growth_scheme.errors,
                )
            slct_booster_per_day_growth_scheme_obj = (
                slct_booster_per_day_growth_scheme.save()
            )
            per_day_growth_scheme_inc = SlctBoosterPerDayGrowthSchemeIncentive.objects.filter(
                booster_per_growth_target__id=slct_booster_per_day_growth_scheme_obj.id
            )
            if per_day_growth_scheme_inc:
                per_day_growth_scheme_inc.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data[
                    "booster_per_growth_target"
                ] = slct_booster_per_day_growth_scheme_obj.id

                slct_booster_per_day_growth_scheme_incentive = (
                    SlctBoosterPerDayGrowthSchemeIncentiveSerializer(data=inc_data)
                )
                if not slct_booster_per_day_growth_scheme_incentive.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct booster per day growth scheme incentive",
                        slct_booster_per_day_growth_scheme_incentive.errors,
                    )
                slct_booster_per_day_growth_scheme_incentive.save()
        return Responses.success_response(
            "data inserted  in slct  booster per day growth scheme incentive",
            data=slct_booster_per_day_growth_scheme.data,
        )


class SlctBenchmarkChangeRequestViewSet(ModelViewSet):
    """slct benchmark change request get post and patch api"""

    queryset = SlctBenchmarkChangeRequest.objects.all()
    serializer_class = SlctBenchmarkChangeRequestSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctBenchmarkChangeRequestFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_benchmark_change_request = SlctBenchmarkChangeRequestSerializer(
            data=request.data
        )
        if not slct_benchmark_change_request.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct benchmark change request",
                slct_benchmark_change_request.errors,
            )
        slct_benchmark_change_request_obj = slct_benchmark_change_request.save()
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_update_login"] = request.user.id
            inc_data["bench_mark_chq_req"] = slct_benchmark_change_request_obj.id
            slct_bench_mark_chq_req_billing_gap = (
                SlctBenchmarkChangeRequestBillingGapSerializer(data=inc_data)
            )
            if not slct_bench_mark_chq_req_billing_gap.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct benchmark change request billing gap",
                    slct_bench_mark_chq_req_billing_gap.errors,
                )
            slct_bench_mark_chq_req_billing_gap.save()
        return Responses.success_response(
            "data inserted  in slct benchmark change request billing gap",
            data=slct_benchmark_change_request.data,
        )


class UpdateSlctBenchmarkChangeRequestViewSet(ModelViewSet):
    """update slct benchmark change request get post and patch api"""

    def post(self, request):
        id = request.query_params.get("id")
        slct_bench_mark_chg_obj = SlctBenchmarkChangeRequest.objects.get(id=id)

        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_benchmark_change_request = SlctBenchmarkChangeRequestSerializer(
                slct_bench_mark_chg_obj, data=request.data
            )
            if not slct_benchmark_change_request.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct benchmark change request",
                    slct_benchmark_change_request.errors,
                )
            slct_benchmark_change_request_obj = slct_benchmark_change_request.save()
            slct_bench_mark_chg_inc_obj = (
                SlctBenchmarkChangeRequestBillingGap.objects.filter(
                    bench_mark_chq_req__id=slct_benchmark_change_request_obj.id
                )
            )
            if slct_bench_mark_chg_inc_obj:
                slct_bench_mark_chg_inc_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["bench_mark_chq_req"] = slct_benchmark_change_request_obj.id
                slct_bench_mark_chq_req_billing_gap = (
                    SlctBenchmarkChangeRequestBillingGapSerializer(data=inc_data)
                )
                if not slct_bench_mark_chq_req_billing_gap.is_valid(
                    raise_exception=True
                ):
                    return Responses.error_response(
                        "Insertion Error in slct benchmark change request billing gap",
                        slct_bench_mark_chq_req_billing_gap.errors,
                    )
                slct_bench_mark_chq_req_billing_gap.save()
        return Responses.success_response(
            "data inserted  in slct benchmark change request billing gap",
            data=slct_benchmark_change_request.data,
        )


class SlctPriceChangeRequestExistingMarktViewSet(ModelViewSet):
    """slct price change request existing market"""

    queryset = SlctPriceChangeRequestExistingMarkt.objects.all()
    serializer_class = SlctPriceChangeRequestExistingMarktSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctPriceChangeRequestExistingMarktFilter
    pagination_class = CustomPagination

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id

        slct_price_change_req = SlctPriceChangeRequestExistingMarktSerializer(
            data=request.data
        )
        if not slct_price_change_req.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct price change request existing",
                slct_price_change_req.errors,
            )
        slct_price_change_req_obj = slct_price_change_req.save()
        for inc_data in json.loads(request.data["incentives"]):
            inc_data["created_by"] = request.user.id
            inc_data["last_updated_by"] = request.user.id
            inc_data["last_updated_login"] = request.user.id
            inc_data[
                "slct_price_change_request_existing_markt"
            ] = slct_price_change_req_obj.id

            slct_price_change_request_brand = (
                SlctPriceChangeRequestBrandVsCompetitorsSerializer(data=inc_data)
            )

            if not slct_price_change_request_brand.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct price change request brand vs competitiors",
                    slct_price_change_request_brand.errors,
                )
            slct_price_change_request_brand.save()

        slct_benchmark_price_working_obj = {
            "created_by": request.user.id,
            "last_updated_by": request.user.id,
            "last_updated_login": request.user.id,
            "benchmark_brand": request.data["benchmark_brand"],
            "benchmark_wsp": request.data["benchmark_wsp"],
            "parameter": request.data["parameter"],
            "brand_wsp_based_on_benchmark": request.data[
                "brand_wsp_based_on_benchmark"
            ],
            "brand_wsp_wrt_desired_wso": request.data["brand_wsp_wrt_desired_wso"],
            "slct_benchmark_price": slct_price_change_req_obj.id,
        }

        slct_benchmark_price_working = SlctBenchmarkPriceWorkingSerializer(
            data=slct_benchmark_price_working_obj
        )

        if not slct_benchmark_price_working.is_valid(raise_exception=True):
            return Responses.error_response(
                "Insertion Error in slct bench work price working",
                slct_benchmark_price_working.errors,
            )
        slct_benchmark_price_working.save()
        return Responses.success_response(
            "data inserted  in slct benchmark price working",
            data=slct_price_change_req.data,
        )


class UpdateSlctPriceChangeRequestExistingMarktViewSet(ModelViewSet):
    """update slct price change request existing market"""

    def post(self, request):
        id = request.query_params.get("id")
        slct_price_chg_req_obj = SlctPriceChangeRequestExistingMarkt.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id

            slct_price_change_req = SlctPriceChangeRequestExistingMarktSerializer(
                slct_price_chg_req_obj, data=request.data
            )
            if not slct_price_change_req.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct price change request existing",
                    slct_price_change_req.errors,
                )
            slct_price_change_req_obj = slct_price_change_req.save()
            slct_price_chg_req_brand_comp_obj = SlctPriceChangeRequestBrandVsCompetitors.objects.filter(
                slct_price_change_request_existing_markt__id=slct_price_change_req_obj.id
            )
            if slct_price_chg_req_brand_comp_obj:
                slct_price_chg_req_brand_comp_obj.delete()
            for inc_data in json.loads(request.data["incentives"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_updated_login"] = request.user.id
                inc_data[
                    "slct_price_change_request_existing_markt"
                ] = slct_price_change_req_obj.id

                slct_price_change_request_brand = (
                    SlctPriceChangeRequestBrandVsCompetitorsSerializer(data=inc_data)
                )

                if not slct_price_change_request_brand.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "Insertion Error in slct price change request brand vs competitiors",
                        slct_price_change_request_brand.errors,
                    )
                slct_price_change_request_brand.save()
            slct_bench_mark_obj = SlctBenchmarkPriceWorking.objects.filter(
                slct_benchmark_price__id=slct_price_change_req_obj.id
            )
            if slct_bench_mark_obj:
                slct_bench_mark_obj.delete()

            slct_benchmark_price_working_obj = {
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_updated_login": request.user.id,
                "benchmark_brand": request.data["benchmark_brand"],
                "benchmark_wsp": request.data["benchmark_wsp"],
                "parameter": request.data["parameter"],
                "brand_wsp_based_on_benchmark": request.data[
                    "brand_wsp_based_on_benchmark"
                ],
                "brand_wsp_wrt_desired_wso": request.data["brand_wsp_wrt_desired_wso"],
                "slct_benchmark_price": slct_price_change_req_obj.id,
            }
            slct_benchmark_price_working = SlctBenchmarkPriceWorkingSerializer(
                data=slct_benchmark_price_working_obj
            )
            if not slct_benchmark_price_working.is_valid(raise_exception=True):
                return Responses.error_response(
                    "Insertion Error in slct bench work price working",
                    slct_benchmark_price_working.errors,
                )
            slct_benchmark_price_working.save()
            return Responses.success_response(
                "data inserted  in slct benchmark price working",
                data=slct_price_change_req.data,
            )


class SlctInKindTourProposalViewSet(ModelViewSet):
    """SlctInKindTourProposal view-set class."""

    queryset = SlctInKindTourProposal.objects.all()
    serializer_class = SlctInKindTourProposalSerializer
    pagination_class = CustomPagination
    filterset_class = SlctInKindTourProposalFilter
    parser_classes = (MultipartJsonParser,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        request.data["related_doc"] = request.FILES.get("related_doc")
        return super().create(request, *args, **kwargs)


class UpdateSlctInKindTourPropsalViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        inkind_tour_scheme_obj = SlctInKindTourProposal.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_inkind_tour_props = UpdateSlctInKindTourProposalSerializer(
                inkind_tour_scheme_obj, data=request.data
            )
            if not slct_inkind_tour_props.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct inkind booster",
                    slct_inkind_tour_props.errors,
                )
            slct_inkind_booster_props_obj = slct_inkind_tour_props.save()

            inkind_booster_scheme_inc_obj = (
                SlctInKindQuantitySlabTourDestination.objects.filter(
                    in_kind_tour_prop__id=slct_inkind_booster_props_obj.id
                )
            )
            if inkind_booster_scheme_inc_obj:
                inkind_booster_scheme_inc_obj.delete()
            for inc_data in json.loads(request.data["inkind_tour_destinations"]):
                inc_data["created_by"] = request.user.id
                inc_data["last_updated_by"] = request.user.id
                inc_data["last_update_login"] = request.user.id
                inc_data["in_kind_tour_prop"] = slct_inkind_booster_props_obj.id
                slct_in_kind_qua_slab_des = (
                    UpdateSlctInKindQuantitySlabTourDestinationSerializer(data=inc_data)
                )

                if not slct_in_kind_qua_slab_des.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "Insertion Error in slct in kind tour",
                        slct_in_kind_qua_slab_des.errors,
                    )
                slct_in_kind_qua_slab_des.save()
            return Responses.success_response(
                "data inserted in in kind tour", data=slct_inkind_tour_props.data
            )


class SlctSchemeDiscountProposalViewSet(ModelViewSet):
    """SlctSchemeDiscountProposal view-set class."""

    queryset = SlctSchemeDiscountProposal.objects.all()
    serializer_class = SlctSchemeDiscountProposalSerializer
    pagination_class = CustomPagination
    filterset_class = SlctSchemeDiscountProposalFilter


class UpdateSlctSchemeDiscountProposalViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        scheme_discount_props_obj = SlctSchemeDiscountProposal.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            scheme_discount_props = UpdateSlctSchemeDiscountProposalSerializer(
                scheme_discount_props_obj, data=request.data
            )
            if not scheme_discount_props.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in scheme discount obj",
                    scheme_discount_props.errors,
                )
            scheme_discount_props_obj_id = scheme_discount_props.save()
            slct_scheme_props_gap_obj = SlctSchemeProposalGap.objects.filter(
                scheme_discount_proposal__id=scheme_discount_props_obj_id.id
            )
            if slct_scheme_props_gap_obj:
                slct_scheme_props_gap_obj.delete()
            for other_data in json.loads(request.data["scheme_proposal_gap"]):
                other_data["created_by"] = request.user.id
                other_data["last_updated_by"] = request.user.id
                other_data["last_update_login"] = request.user.id
                other_data["scheme_discount_proposal"] = scheme_discount_props_obj_id.id
                slct_scheme_props_gap = UpdateSlctSchemeProposalGapSerializer(
                    data=other_data
                )
                if not slct_scheme_props_gap.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct scheme props gap",
                        slct_scheme_props_gap.errors,
                    )
                slct_scheme_props_gap.save()
            slct_market_info = SlctMarketInformation.objects.filter(
                scheme_discount_proposal__id=scheme_discount_props_obj_id.id
            )
            if slct_market_info:
                slct_market_info.delete()
            for other_data in json.loads(request.data["market_information"]):
                other_data["created_by"] = request.user.id
                other_data["last_updated_by"] = request.user.id
                other_data["last_update_login"] = request.user.id
                other_data["scheme_discount_proposal"] = scheme_discount_props_obj_id.id
                slct_market_info_obj = UpdateSlctMarketInformationSerializer(
                    data=other_data
                )
                if not slct_market_info_obj.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct market information",
                        slct_market_info_obj.errors,
                    )
                slct_market_info_obj.save()
            return Responses.success_response(
                "data successfully inserted in slct discount proposal",
                data=scheme_discount_props.data,
            )


class SlctNewMarketPricingRequestViewSet(ModelViewSet):
    """slct new market pricing request get post api"""

    queryset = SlctNewMarketPricingRequest.objects.all()
    serializer_class = SlctNewMarketPricingRequestSerializer
    pagination_class = CustomPagination
    filterset_class = SlctNewMarketPricingRequestFilter

    def post(self, request):
        request.data._mutable = True
        request.data["related_doc"] = request.FILES.get("related_doc")
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_new_market_pricing = SlctNewMarketPricingRequestSerializer(
            data=request.data
        )
        if not slct_new_market_pricing.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in slct new market pricing",
                slct_new_market_pricing.errors,
            )
        slct_new_market_pricing_obj = slct_new_market_pricing.save()
        for other_data in json.loads(request.data["gap_with_other_product"]):
            other_data["created_by"] = request.user.id
            other_data["last_updated_by"] = request.user.id
            other_data["last_update_login"] = request.user.id
            other_data["new_market_pricing_request"] = slct_new_market_pricing_obj.id
            slct_gap_with_other_product = SlctGapWithOtherProductSerializer(
                data=other_data
            )
            if not slct_gap_with_other_product.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct gap with other product",
                    slct_gap_with_other_product.errors,
                )
            slct_gap_with_other_product.save()
        for price_data in json.loads(request.data["price_packing_information"]):
            price_data["created_by"] = request.user.id
            price_data["last_updated_by"] = request.user.id
            price_data["last_update_login"] = request.user.id
            price_data["pricing_packing_request"] = slct_new_market_pricing_obj.id
            slct_price_packing_information = SlctPricePackingInformationSerializer(
                data=price_data
            )
            if not slct_price_packing_information.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct price packing information",
                    slct_price_packing_information.errors,
                )
            slct_price_packing_information.save()
        for market_inf in json.loads(request.data["marketing_information"]):
            market_inf["created_by"] = request.user.id
            market_inf["last_updated_by"] = request.user.id
            market_inf["last_update_login"] = request.user.id
            market_inf["marketing_information"] = slct_new_market_pricing_obj.id
            slct_marketing_information = SlctMarketingInformationSerializer(
                data=market_inf
            )
            if not slct_marketing_information.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct price packing information",
                    slct_marketing_information.errors,
                )
            slct_marketing_information.save()
        return Responses.success_response(
            "data insterted successfully in slct new market pricing",
            data=slct_new_market_pricing.data,
        )


class UpdateSlctNewMarketPricingRequestViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        new_market_pricing_obj = SlctNewMarketPricingRequest.objects.get(id=id)
        if id:
            request.data._mutable = True
            request.data["related_doc"] = request.FILES.get("related_doc")
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_new_market_pricing = SlctNewMarketPricingRequestSerializer(
                new_market_pricing_obj, data=request.data
            )
            if not slct_new_market_pricing.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct new market pricing",
                    slct_new_market_pricing.errors,
                )
            slct_new_market_pricing_obj = slct_new_market_pricing.save()
            slct_gap_with_other_product_obj = SlctGapWithOtherProduct.objects.filter(
                new_market_pricing_request__id=slct_new_market_pricing_obj.id
            )
            if slct_gap_with_other_product_obj:
                slct_gap_with_other_product_obj.delete()
            for other_data in json.loads(request.data["gap_with_other_product"]):
                other_data["created_by"] = request.user.id
                other_data["last_updated_by"] = request.user.id
                other_data["last_update_login"] = request.user.id
                other_data[
                    "new_market_pricing_request"
                ] = slct_new_market_pricing_obj.id
                slct_gap_with_other_product = SlctGapWithOtherProductSerializer(
                    data=other_data
                )
                if not slct_gap_with_other_product.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct gap with other product",
                        slct_gap_with_other_product.errors,
                    )
                slct_gap_with_other_product.save()
        slct_packing_information_obj = SlctPricePackingInformation.objects.filter(
            pricing_packing_request__id=slct_new_market_pricing_obj.id
        )
        if slct_packing_information_obj:
            slct_packing_information_obj.delete()
        for price_data in json.loads(request.data["price_packing_information"]):
            price_data["created_by"] = request.user.id
            price_data["last_updated_by"] = request.user.id
            price_data["last_update_login"] = request.user.id
            price_data["pricing_packing_request"] = slct_new_market_pricing_obj.id
            slct_price_packing_information = SlctPricePackingInformationSerializer(
                data=price_data
            )
            if not slct_price_packing_information.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct price packing information",
                    slct_price_packing_information.errors,
                )
            slct_price_packing_information.save()
        slct_markting_information_obj = SlctMarktingInformation.objects.filter(
            marketing_information__id=slct_new_market_pricing_obj.id
        )
        if slct_markting_information_obj:
            slct_markting_information_obj.delete()
        for market_inf in json.loads(request.data["marketing_information"]):
            market_inf["created_by"] = request.user.id
            market_inf["last_updated_by"] = request.user.id
            market_inf["last_update_login"] = request.user.id
            market_inf["marketing_information"] = slct_new_market_pricing_obj.id
            slct_marketing_information = SlctMarketingInformationSerializer(
                data=market_inf
            )
            if not slct_marketing_information.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct price packing information",
                    slct_marketing_information.errors,
                )
            slct_marketing_information.save()
        return Responses.success_response(
            "data insterted successfully in slct new market pricing",
            data=slct_new_market_pricing.data,
        )


class SlctBrandingRequestsViewSet(ModelViewSet):
    """slct branding request get and post api"""

    queryset = SlctBrandingRequests.objects.all()
    serializer_class = SlctBrandingRequestsSerializer
    filterset_class = SlctBrandingRequestsFilter
    pagination_class = CustomPagination

    def post(self, request):
        request.data._mutable = True
        document = request.FILES.get("related_doc")
        branding_activity = json.loads(request.data["branding_activity"])
        branding_address = json.loads(request.data["branding_address"])
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        request.data["photo_before_branding_activity"] = document
        slct_branding_request = self.serializer_class(data=request.data)
        if not slct_branding_request.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in slct branding request", slct_branding_request.errors
            )
        slct_branding_request_obj = slct_branding_request.save()
        for activity_data in branding_activity:
            activity_data["created_by"] = request.user.id
            activity_data["last_updated_by"] = request.user.id
            activity_data["last_update_login"] = request.user.id
            activity_data["branding_request_activity"] = slct_branding_request_obj.id
            slct_branding_activity = SlctBrandingActivitySerializer(data=activity_data)
            if not slct_branding_activity.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct branding activity",
                    slct_branding_activity.errors,
                )
            slct_branding_activity.save()
        for address_data in branding_address:
            address_data["created_by"] = request.user.id
            address_data["last_updated_by"] = request.user.id
            address_data["last_update_login"] = request.user.id
            address_data["branding_request"] = slct_branding_request_obj.id
            slct_branding_address = SlctBrandingAddressSerializer(data=address_data)
            if not slct_branding_address.is_valid(raise_exception=True):
                return (
                    "insertion error in slct branding address",
                    slct_branding_address.errors,
                )
            slct_branding_address.save()
        return Responses.success_response(
            "data insterted successfully in slct branding request",
            data=slct_branding_request.data,
        )


class SlctInKindBoosterSchemePropsViewSet(ModelViewSet):
    """slct inkind booster scheme props get and post api"""

    queryset = SlctInKindBoosterSchemeProps.objects.all()
    serializer_class = SlctInKindBoosterSchemePropsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctInKindBoosterSchemePropsFilter
    pagination_class = CustomPagination

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_inkind_booster_props = SlctInKindBoosterSchemePropsSerializer(
            data=request.data
        )
        if not slct_inkind_booster_props.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in slct inkind booster",
                slct_inkind_booster_props.errors,
            )
        slct_inkind_booster_props_obj = slct_inkind_booster_props.save()
        quantity_slab_lower = request.data["quantity_slab_lower"]
        quantity_slab_upper = request.data["quantity_slab_upper"]
        inkind_gift_detail = request.data["inkind_gift_detail"]
        for inc_data in range(len(quantity_slab_lower)):
            slct_inkind_booster_props_dict = {
                "quantity_slab_lower": quantity_slab_lower[inc_data],
                "quantity_slab_upper": quantity_slab_upper[inc_data],
                "inkind_gift_detail": inkind_gift_detail[inc_data],
                "in_kind_booster_scheme": slct_inkind_booster_props_obj.id,
                "created_by": request.user.id,
                "last_updated_by": request.user.id,
                "last_update_login": request.user.id,
            }

            slct_inkind_booster_incentive = (
                SlctInKindBoosterSchemePropsIncentiveSerializer(
                    data=slct_inkind_booster_props_dict
                )
            )
            if not slct_inkind_booster_incentive.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct inkind booster incentives",
                    slct_inkind_booster_incentive.errors,
                )
            slct_inkind_booster_incentive.save()
        return Responses.success_response(
            "data insterted successfully in slct inkind booster incentive",
            data=slct_inkind_booster_props.data,
        )


class UpdateSlctInKindBoosterSchemePropsViewSet(ModelViewSet):
    def post(self, request):
        id = request.query_params.get("id")
        inkind_booster_scheme_obj = SlctInKindBoosterSchemeProps.objects.get(id=id)
        if id:
            request.data["created_by"] = request.user.id
            request.data["last_updated_by"] = request.user.id
            request.data["last_update_login"] = request.user.id
            slct_inkind_booster_props = SlctInKindBoosterSchemePropsSerializer(
                inkind_booster_scheme_obj, data=request.data
            )
            if not slct_inkind_booster_props.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct inkind booster",
                    slct_inkind_booster_props.errors,
                )
            slct_inkind_booster_props_obj = slct_inkind_booster_props.save()
            inkind_booster_scheme_inc_obj = (
                SlctInKindBoosterSchemePropsIncentive.objects.filter(
                    in_kind_booster_scheme__id=slct_inkind_booster_props_obj.id
                )
            )
            if inkind_booster_scheme_inc_obj:
                inkind_booster_scheme_inc_obj.delete()
            quantity_slab_lower = request.data["quantity_slab_lower"]
            quantity_slab_upper = request.data["quantity_slab_upper"]
            inkind_gift_detail = request.data["inkind_gift_detail"]
            for inc_data in range(len(quantity_slab_lower)):
                slct_inkind_booster_props_dict = {
                    "quantity_slab_lower": quantity_slab_lower[inc_data],
                    "quantity_slab_upper": quantity_slab_upper[inc_data],
                    "inkind_gift_detail": inkind_gift_detail[inc_data],
                    "in_kind_booster_scheme": slct_inkind_booster_props_obj.id,
                    "created_by": request.user.id,
                    "last_updated_by": request.user.id,
                    "last_update_login": request.user.id,
                }

                slct_inkind_booster_incentive = (
                    SlctInKindBoosterSchemePropsIncentiveSerializer(
                        data=slct_inkind_booster_props_dict
                    )
                )
                if not slct_inkind_booster_incentive.is_valid(raise_exception=True):
                    return Responses.error_response(
                        "insertion error in slct inkind booster incentives",
                        slct_inkind_booster_incentive.errors,
                    )
                slct_inkind_booster_incentive.save()
        return Responses.success_response(
            "data insterted successfully in slct inkind booster incentive",
            data=slct_inkind_booster_props.data,
        )


class SlctAnnualSalesPlanViewSet(ModelViewSet):
    """slct annual sales plan get and post api"""

    queryset = SlctAnnualSalesPlan.objects.all()
    serializer_class = SlctAnnualSalesPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctAnnualSalesPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        for data in request.data:
            data["created_by"] = request.user.id
            data["last_updated_by"] = request.user.id
            data["last_update_login"] = request.user.id
            slct_annual_Sales = SlctAnnualSalesPlanSerializer(data=data)
            if not slct_annual_Sales.is_valid(raise_exception=True):
                return Responses.error_response(
                    "insertion error in slct annual sales plan",
                    slct_annual_Sales.errors,
                )
            slct_annual_Sales.save()
        return Responses.success_response(
            "data insterted successfully in slct annual sales plan",
            data=slct_annual_Sales.data,
        )


class SlctAnnualSalesPlanDownloadViewSet(DownloadUploadViewSet):
    """slct annual sales plan download api"""

    queryset = SlctAnnualSalesPlan.objects.all()
    serializer_class = SlctAnnualSalesPlandownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctAnnualSalesPlanFilter
    pagination_class = CustomPagination
    file_name = "slct_annual_sales_plan"
    sorting_fields = ("id",)

    # def create(self, request, *args, **kwargs):
    #     request.data["created_by"] = request.user.id
    #     request.data["last_updated_by"] = request.user.id
    #     request.data["last_update_login"] = request.user.id
    #     return super().create(request, *args, **kwargs)


class SlctMonthlySalesPlanViewSet(ModelViewSet):
    """ "slct monthly sales plan get post api"""

    queryset = SlctMonthlySalesPlan.objects.all()
    serializer_class = SlctMonthlySalesPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctMonthlySalesPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    def post(self, request):
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        slct_monthly_sales_plan = SlctMonthlySalesPlanSerializer(data=request.data)
        if not slct_monthly_sales_plan.is_valid(raise_exception=True):
            return Responses.error_response(
                "insertion error in slct monthly sales plan",
                slct_monthly_sales_plan.errors,
            )
        slct_monthly_sales_plan.save()
        return Responses.success_response(
            "data insterted successfully in slct monthly sales plan",
            data=slct_monthly_sales_plan.data,
        )


class SlctMonthlySalesPlanDownloadViewSet(DownloadUploadViewSet):
    """slct monthly sales plan download api"""

    queryset = SlctMonthlySalesPlan.objects.all()
    serializer_class = SlctMonthlySalesPlandownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SlctMonthlySalesPlanFilter
    pagination_class = CustomPagination
    file_name = "slct_monthly_sales_plan"
    sorting_fields = ("id",)

    # def create(self, request, *args, **kwargs):
    #     request.data["created_by"] = request.user.id
    #     request.data["last_updated_by"] = request.user.id
    #     request.data["last_update_login"] = request.user.id
    #     return super().create(request, *args, **kwargs)


class SlctCombSlabGrowthPropsByIdViewSet(ModelViewSet):
    queryset = SlctCombSlabGrowthProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctCombSlabGrowthPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctPartyWiseSchemePropsByIdViewSet(ModelViewSet):
    queryset = SlctPartyWiseSchemeProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctPartyWiseSchemePropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctAnnualDiscSlabBasedByIdViewSet(ModelViewSet):
    queryset = SlctAnnualDiscSlabBased.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctAnnualDiscSlabBasedSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctAnnualDiscTargetBasedByIdViewSet(ModelViewSet):
    queryset = SlctAnnualDiscTargetBased.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctAnnualDiscTargetBasedSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctBoosterPerDayTargetSchemeByIdViewSet(ModelViewSet):
    queryset = SlctBoosterPerDayTargetScheme.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctBoosterPerDayTargetSchemeSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctBoosterPerDayGrowthSchemeByIdViewSet(ModelViewSet):
    queryset = SlctBoosterPerDayGrowthScheme.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctBoosterPerDayGrowthSchemeSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctInKindBoosterSchemePropsByIdViewSet(ModelViewSet):
    queryset = SlctInKindBoosterSchemeProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctInKindBoosterSchemePropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctPrmPrdComboScmPropsByIdViewSet(ModelViewSet):
    queryset = SlctPrmPrdComboScmProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctPrmPrdComboScmPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctDirPltBilngDiscPropsByIdViewSet(ModelViewSet):
    queryset = SlctDirPltBilngDiscProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctDirPltBilngDiscPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctBorderDiscPropsByIdViewSet(ModelViewSet):
    queryset = SlctBorderDiscProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctBorderDiscPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctActivityPropsByIdViewSet(ModelViewSet):
    queryset = SlctActivityProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctActivityPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctVolCutterSlabBasedProposalByIdViewSet(ModelViewSet):
    queryset = SlctVolCutterSlabBasedProposal.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctVolCutterSlabBasedProposalSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctVolCutterTargetBasedByIdViewSet(ModelViewSet):
    queryset = SlctVolCutterTargetBased.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctVolCutterTargetBasedSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctVolCutterTargetBasedByIdViewSet(ModelViewSet):
    queryset = SlctVolCutterTargetBased.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctVolCutterTargetBasedSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctInKindTourProposalByIdViewSet(ModelViewSet):
    queryset = SlctInKindTourProposal.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctInKindTourProposalSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctEngCashSchPtPropsByIdViewSet(ModelViewSet):
    queryset = SlctEngCashSchPtProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctEngCashSchPtPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctMasonKindSchPropsByIdViewSet(ModelViewSet):
    queryset = SlctMasonKindSchProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctMasonKindSchPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctDealerLinkedSchPropsByIdViewSet(ModelViewSet):
    queryset = SlctDealerLinkedSchProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctDealerLinkedSchPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctVehicleSchPropsByIdViewSet(ModelViewSet):
    queryset = SlctVehicleSchProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctVehicleSchPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctDealerOutsBasedPropsByIdViewSet(ModelViewSet):
    queryset = SlctDealerOutsBasedProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctDealerOutsBasedPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctRailBasedSchPropsByIdViewSet(ModelViewSet):
    queryset = SlctRailBasedSchProps.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctRailBasedSchPropsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctPriceChangeRequestExistingMarktByIdViewSet(ModelViewSet):
    queryset = SlctPriceChangeRequestExistingMarkt.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctPriceChangeRequestExistingMarktSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctGapWithOtherProductByIdViewSet(ModelViewSet):
    queryset = SlctGapWithOtherProduct.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctGapWithOtherProductSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctBenchmarkChangeRequestByIdViewSet(ModelViewSet):
    queryset = SlctBenchmarkChangeRequest.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctBenchmarkChangeRequestSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctNewMarketPricingRequestByIdViewSet(ModelViewSet):
    queryset = SlctNewMarketPricingRequest.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctNewMarketPricingRequestSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctBrandingRequestsByIdViewSet(ModelViewSet):
    queryset = SlctBrandingRequests.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctBrandingRequestsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctAnnualSalesPlanByIdViewSet(ModelViewSet):
    queryset = SlctAnnualSalesPlan.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctAnnualSalesPlanSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class SlctMonthlySalesPlanByIdViewSet(ModelViewSet):
    queryset = SlctMonthlySalesPlan.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            queryset = self.queryset

        slct_obj = SlctMonthlySalesPlanSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetched by id successfully", data=slct_obj.data
        )


class ZoneMappingNewDropdown(GenericAPIView):
    queryset = ZoneMappingNew.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = (
        "zone",
        "state",
        "district",
        "city",
        "region",
        "city_id",
        "taluka",
    )

    def __get_zone_mapping_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_zone_mapping_dropdown_query("zone"),
            "state": self.__get_zone_mapping_dropdown_query("state"),
            "city": self.__get_zone_mapping_dropdown_query("city"),
            "district": self.__get_zone_mapping_dropdown_query("district"),
            "region": self.__get_zone_mapping_dropdown_query("region"),
            "city_id": self.__get_zone_mapping_dropdown_query("city_id"),
            "taluka": self.__get_zone_mapping_dropdown_query("taluka"),
        }
        return Responses.success_response("zone mapping new dropdown data.", data=data)


class TOebsXxsclVehicleMasterViewSet(GenericAPIView):
    queryset = TOebsXxsclVehicleMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("vehicle_type",)

    def __get_vehicle_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "vehicle_type": self.__get_vehicle_dropdown_query("vehicle_type"),
        }
        return Responses.success_response("vehicle type dropdown data.", data=data)


class PlantDepoMasterDropdownView(GenericAPIView):
    """Brand approval dropdown api."""

    queryset = TgtPlantDepoMaster.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TgtPlantDepoMasterFilter

    def __get_plant_master_query(self, query_string, query=Q()):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(
                (
                    Q(party_name__startswith="FC")
                    | Q(party_name__startswith="RM")
                    | Q(party_name__startswith="FG")
                )
            )
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "plant": (
                self.filter_queryset(self.get_queryset())
                .filter(
                    (
                        Q(party_name__startswith="FC")
                        | Q(party_name__startswith="RM")
                        | Q(party_name__startswith="FG")
                    )
                )
                .values_list("party_name")
                .annotate(
                    Count("party_name"), depo=Substr("party_name", pos=1, length=3)
                )
                .values_list("depo", flat=True)
            ),
            "district": self.__get_plant_master_query("district"),
            "city": self.__get_plant_master_query("city"),
        }
        return Responses.success_response("Brand approval dropdown data.", data=data)


class SlctDownloadExcel(GenericAPIView):
    def post(self, request, *args, **kwargs):
        """API to export data to excel sheet."""
        df = pd.DataFrame.from_dict(request.data[0], orient="index")
        df = df.transpose()
        bio = BytesIO()
        writer = pd.ExcelWriter(
            bio, engine="xlsxwriter", datetime_format="dd-mm-yyyy hh:mm:ss.000"
        )
        for column in df.columns:
            if isinstance(df[column][0], list):
                sub_df = pd.DataFrame(df[column][0])
                sub_df.reset_index(drop=True, inplace=False)
                sub_df.index += 1
                sub_df.to_excel(writer, sheet_name=column, index=False)
                df = df.drop([column], axis=1)

        df.reset_index(drop=True, inplace=False)
        df.index += 1
        df.to_excel(writer, sheet_name="slct_data", index=False)
        writer.save()

        bio.seek(0)
        bio.getvalue()
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(bio, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename=slct_data.xlsx"
        return response


class TgtPlantDepoMasterDropdown(GenericAPIView):
    category_code = ["CEMENTO DEPOT", "BANGUR DEPOT", "SHREE DEPOT", "CEMENT"]
    queryset = TgtPlantDepoMaster.objects.filter(category_code__in=category_code)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("party_name",)
    search_fields = ("party_name",)

    def __get_plant_depo_dropdown_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "party_name": self.__get_plant_depo_dropdown_query("party_name"),
        }
        return Responses.success_response(
            "tgt plant depo master dropdown data.", data=data
        )


class CrmMarketMappingPricingViewSet(DownloadUploadViewSet):
    """crm market mapping pricing view"""

    queryset = CrmMarketMappingPricing.objects.all().order_by(
        "-counter_visit_start_time"
    )
    serializer_class = CrmMarketMappingPricingDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmMarketMappingPricingFilter
    pagination_class = CustomPagination
    file_name = "crm_market_mapping_pricing"


class CrmPricingViewSet(DownloadUploadViewSet):
    """crm pricing view"""

    queryset = CrmPricing.objects.all().order_by("-date")
    serializer_class = CrmPricingDownloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmPricingFilter
    pagination_class = CustomPagination
    file_name = "crm_pricing"
    sorting_fields = (
        "district",
        "date",
        "brand",
        "product",
    )

    def get_queryset(self):
        if self.request.method in ["PATCH", "PUT"]:
            return (
                super(DownloadUploadViewSet, self)
                .get_queryset()
                .filter(
                    district__in=map(itemgetter("district"), self.data),
                    date__in=map(itemgetter("date"), self.data),
                    brand__in=map(itemgetter("brand"), self.data),
                    product__in=map(itemgetter("product"), self.data),
                )
            )
        return super().get_queryset()


class PricingInputCrmPricingListViewSet(ModelViewSet):
    queryset = CrmMarketMappingPricing.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmMarketMappingPricingFilter
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .values(
                "district",
                "taluka",
                "brand",
                "product",
                "counter_visit_start_time__date",
            )
            .annotate(
                Count("district"),
                Count("taluka"),
                Count("brand"),
                Count("product"),
                Count("counter_visit_start_time__date"),
                date=F("counter_visit_start_time__date"),
                wsp_price=Avg("whole_sale_price"),
                rsp_price=Avg("retail_sale_price"),
            )
            .values(
                "district",
                "taluka",
                "brand",
                "product",
                "counter_visit_start_time__date",
                "date",
                "wsp_price",
                "rsp_price",
            )
        )

        return Responses.success_response("pricing input crm pricing list", data=data)


class CrmMarketMappingPricingDropdown(GenericAPIView):
    queryset = CrmMarketMappingPricing.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("district", "taluka", "brand", "product")

    def __get_crm_market_mapping_dropdown_query(self, query_string, queryset):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {}
        queryset = self.filter_queryset(self.get_queryset())
        queryset = GetDistrictsDataByState(request.user.email, queryset)
        data = {
            "district": self.__get_crm_market_mapping_dropdown_query(
                "district", queryset
            ),
            "taluka": self.__get_crm_market_mapping_dropdown_query("taluka", queryset),
            "brand": self.__get_crm_market_mapping_dropdown_query("brand", queryset),
            "product": self.__get_crm_market_mapping_dropdown_query(
                "product", queryset
            ),
        }
        return Responses.success_response(
            "crm market mapping dropdown data.", data=data
        )


# class BrandingActivitySumApiView(GenericAPIView):
#     queryset = BrandingActivity.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ("state", "district", "status_of_scheme", "brand")
#     pagination_class = CustomPagination

#     def get(self, request, *args, **kwargs):
#         prv_yr_start, prv_yr_end = self.get_previour_fiscal_year_range()
#         cr_yr_start, cr_yr_end = self.get_current_fiscal_year_range()

#         branding_activity_df = pd.DataFrame(
#             self.filter_queryset(self.get_queryset())
#             .filter(date_of_start__range=[prv_yr_start, prv_yr_end])
#             .values(
#                 "state",
#                 "district",
#                 "brand",
#             )
#             .annotate(
#                 Count("state"),
#                 Count("district"),
#                 Count("brand"),
#                 budget_planned=Sum("budget_planned"),
#                 actual_spend=Sum("actual_spend"),
#             )
#         )

#         branding_output_df = pd.DataFrame(
#             self.get_branding_output_data(cr_yr_start, cr_yr_end)
#         )

#         branding_budget_df = pd.DataFrame(self.get_branding_budget_data())

#         if branding_output_df.empty:
#             branding_output_df = pd.DataFrame(
#                 columns=[
#                     "state",
#                     "district",
#                     "brand",
#                     "state__count",
#                     "district__count",
#                     "brand__count",
#                     "pos_budget",
#                     "outdoor_budget",
#                     "event_budget",
#                     "corporate_budget",
#                     "total_budget",
#                 ]
#             )

#         if branding_budget_df.empty:
#             branding_budget_df = pd.DataFrame(
#                 columns=[
#                     "id",
#                     "state",
#                     "district",
#                     "brand",
#                     "change_tot_cost_rs_lac",
#                     "status",
#                     "sponsor_budget__id",
#                     "sponsor_budget__budget",
#                     "sponsor_budget__comment_approved_by",
#                     "sponsor_budget__comment_raised_by",
#                     "sponsor_budget__status",
#                     "sponsor_budget__raised_by",
#                     "tot_cost_rs_lac",
#                 ]
#             )

#         if branding_activity_df.empty:
#             return self.get_paginated_response(self.paginate_queryset([]))

#         branding_activity_df = branding_activity_df.merge(
#             branding_output_df, on=["state", "district", "brand"], how="left"
#         ).merge(branding_budget_df, on=["state", "district", "brand"], how="left")
#         status = request.query_params.get("status")
#         if status:
#             branding_activity_df = branding_activity_df[
#                 branding_activity_df["status"] == status
#             ]

#         branding_activity_df = branding_activity_df.drop(
#             columns=[
#                 "state__count_x",
#                 "district__count_x",
#                 "brand__count_x",
#                 "state__count_y",
#                 "district__count_y",
#                 "brand__count_y",
#             ]
#         ).to_json(orient="records")

#         data = json.loads(branding_activity_df)
#         return self.get_paginated_response(self.paginate_queryset(data))

#     def get_branding_budget_data(self):
#         return MarketMappingBrandingBudget.objects.values(
#             "id",
#             "state",
#             "district",
#             "brand",
#             "change_tot_cost_rs_lac",
#             "status",
#             "sponsor_budget__id",
#             "sponsor_budget__budget",
#             "sponsor_budget__comment_approved_by",
#             "sponsor_budget__comment_raised_by",
#             "sponsor_budget__status",
#             "sponsor_budget__raised_by",
#         ).annotate(tot_cost_rs_lac=Sum("tot_cost_rs_lac"))

#     def get_branding_output_data(self, start, end):
#         return (
#             MarketMappingBrandingOuput.objects.filter(run__run_date__range=[start, end])
#             .values(
#                 "state",
#                 "district",
#                 "brand",
#             )
#             .annotate(
#                 Count("state"),
#                 Count("district"),
#                 Count("brand"),
#                 pos_budget=Sum("pos_budget"),
#                 outdoor_budget=Sum("outdoor_budget"),
#                 event_budget=Sum("event_budget"),
#                 corporate_budget=Sum("corporate_budget"),
#                 total_budget=Sum("total_budget"),
#             )
#         )

#     def get_previour_fiscal_year_range(self):
#         now = date.today()
#         if now.month >= 4:
#             start = now.replace(day=1, month=4, year=now.year - 1)
#             end = now.replace(day=31, month=3, year=now.year)
#         else:
#             start = now.replace(day=1, month=4, year=now.year - 2)
#             end = now.replace(day=31, month=3, year=now.year - 1)
#         return start, end

#     def get_current_fiscal_year_range(self):
#         now = date.today()
#         if now.month >= 4:
#             start = now.replace(day=1, month=4, year=now.year)
#             end = now
#         else:
#             start = now.replace(day=1, month=4, year=now.year - 1)
#             end = now
#         return start, end


class ActivityBudgetExpenseAPI(GenericAPIView):
    queryset = MarketMappingBrandingBudget.objects.all().order_by("id")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "brand", "id", "status")
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        prv_yr_start, prv_yr_end = self.get_previour_fiscal_year_range()
        cr_yr_start, cr_yr_end = self.get_current_fiscal_year_range()

        activity_df = pd.DataFrame(
            BrandingActivity.objects.filter(
                date_of_start__range=[prv_yr_start, prv_yr_end]
            )
            .values(
                "state",
                "district",
                "brand",
            )
            .annotate(
                Count("state"),
                Count("district"),
                Count("brand"),
                budget_planned=Sum("budget_planned"),
                actual_spend=Sum("actual_spend"),
            )
        )
        budget_df = pd.DataFrame(
            self.filter_queryset(self.get_queryset())
            .values(
                "id",
                "state",
                "district",
                "brand",
                "change_tot_cost_rs_lac",
                "status",
                "sponsor_budget__id",
                "sponsor_budget__budget",
                "sponsor_budget__comment_approved_by",
                "sponsor_budget__comment_raised_by",
                "sponsor_budget__status",
                "sponsor_budget__raised_by",
            )
            .annotate(tot_cost_rs_lac=Sum("tot_cost_rs_lac"))
        )

        branding_output_df = pd.DataFrame(
            self.get_branding_output_data(cr_yr_start, cr_yr_end)
        )

        if branding_output_df.empty:
            branding_output_df = pd.DataFrame(
                columns=[
                    "state",
                    "district",
                    "brand",
                    "state__count",
                    "district__count",
                    "brand__count",
                    "pos_budget",
                    "outdoor_budget",
                    "event_budget",
                    "corporate_budget",
                    "total_budget",
                ]
            )

        if activity_df.empty:
            activity_df = pd.DataFrame(
                columns=[
                    "state",
                    "district",
                    "brand",
                    "budget_planned",
                    "actual_spend",
                ]
            )

        if budget_df.empty:
            return self.get_paginated_response(self.paginate_queryset([]))

        budget_df = budget_df.merge(
            branding_output_df, on=["state", "district", "brand"], how="left"
        ).merge(activity_df, on=["state", "district", "brand"], how="left")
        # status = request.query_params.get("status")
        # if status:
        #     budget_df = budget_df[
        #         budget_df["status"] == status
        #     ]

        budget_df = budget_df.drop(
            columns=[
                "state__count_x",
                "district__count_x",
                "brand__count_x",
                "state__count_y",
                "district__count_y",
                "brand__count_y",
            ]
        ).to_json(orient="records")

        data = json.loads(budget_df)
        return self.get_paginated_response(self.paginate_queryset(data))

    def get_branding_output_data(self, start, end):
        return (
            MarketMappingBrandingOuput.objects.filter(run__run_date__range=[start, end])
            .values(
                "state",
                "district",
                "brand",
            )
            .annotate(
                Count("state"),
                Count("district"),
                Count("brand"),
                pos_budget=Sum("pos_budget"),
                outdoor_budget=Sum("outdoor_budget"),
                event_budget=Sum("event_budget"),
                corporate_budget=Sum("corporate_budget"),
                total_budget=Sum("total_budget"),
            )
        )

    def get_previour_fiscal_year_range(self):
        now = date.today()
        if now.month >= 4:
            start = now.replace(day=1, month=4, year=now.year - 1)
            end = now.replace(day=31, month=3, year=now.year)
        else:
            start = now.replace(day=1, month=4, year=now.year - 2)
            end = now.replace(day=31, month=3, year=now.year - 1)
        return start, end

    def get_current_fiscal_year_range(self):
        now = date.today()
        if now.month >= 4:
            start = now.replace(day=1, month=4, year=now.year)
            end = now
        else:
            start = now.replace(day=1, month=4, year=now.year - 1)
            end = now
        return start, end


class SponsorshipBudgetGetView(GenericAPIView):
    queryset = BrandingActivity.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "status_of_scheme", "brand")
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        prv_yr_start, prv_yr_end = self.get_previour_fiscal_year_range()
        cr_yr_start, cr_yr_end = self.get_current_fiscal_year_range()

        branding_activity_df = pd.DataFrame(
            self.filter_queryset(self.get_queryset())
            .filter(date_of_start__range=[prv_yr_start, prv_yr_end])
            .values(
                "state",
                "district",
                "brand",
            )
            .annotate(
                Count("state"),
                Count("district"),
                Count("brand"),
                budget_planned=Sum("budget_planned"),
                actual_spend=Sum("actual_spend"),
            )
        )

        branding_output_df = pd.DataFrame(
            self.get_branding_output_data(cr_yr_start, cr_yr_end)
        )

        branding_budget_df = pd.DataFrame(self.get_branding_budget_data())

        if branding_output_df.empty:
            branding_output_df = pd.DataFrame(
                columns=[
                    "state",
                    "district",
                    "brand",
                    "state__count",
                    "district__count",
                    "brand__count",
                    "pos_budget",
                    "outdoor_budget",
                    "event_budget",
                    "corporate_budget",
                    "total_budget",
                ]
            )

        if branding_budget_df.empty:
            branding_budget_df = pd.DataFrame(
                columns=[
                    "id",
                    "state",
                    "district",
                    "brand",
                    "change_tot_cost_rs_lac",
                    "status",
                    "sponsor_budget__id",
                    "sponsor_budget__budget",
                    "sponsor_budget__comment_approved_by",
                    "sponsor_budget__comment_raised_by",
                    "sponsor_budget__status",
                    "sponsor_budget__raised_by",
                    "tot_cost_rs_lac",
                ]
            )

        if branding_activity_df.empty:
            return self.get_paginated_response(self.paginate_queryset([]))

        branding_activity_df = branding_activity_df.merge(
            branding_output_df, on=["state", "district", "brand"], how="left"
        ).merge(branding_budget_df, on=["state", "district", "brand"], how="left")
        status = request.query_params.get("status")
        if status:
            branding_activity_df = branding_activity_df[
                branding_activity_df["sponsor_budget__status"] == status
            ]

        branding_activity_df = branding_activity_df.drop(
            columns=[
                "state__count_x",
                "district__count_x",
                "brand__count_x",
                "state__count_y",
                "district__count_y",
                "brand__count_y",
            ]
        ).to_json(orient="records")

        data = json.loads(branding_activity_df)
        return self.get_paginated_response(self.paginate_queryset(data))

    def get_branding_budget_data(self):
        return MarketMappingBrandingBudget.objects.values(
            "id",
            "state",
            "district",
            "brand",
            "change_tot_cost_rs_lac",
            "status",
            "sponsor_budget__id",
            "sponsor_budget__budget",
            "sponsor_budget__comment_approved_by",
            "sponsor_budget__comment_raised_by",
            "sponsor_budget__status",
            "sponsor_budget__raised_by",
        ).annotate(tot_cost_rs_lac=Sum("tot_cost_rs_lac"))

    def get_branding_output_data(self, start, end):
        return (
            MarketMappingBrandingOuput.objects.filter(run__run_date__range=[start, end])
            .values(
                "state",
                "district",
                "brand",
            )
            .annotate(
                Count("state"),
                Count("district"),
                Count("brand"),
                pos_budget=Sum("pos_budget"),
                outdoor_budget=Sum("outdoor_budget"),
                event_budget=Sum("event_budget"),
                corporate_budget=Sum("corporate_budget"),
                total_budget=Sum("total_budget"),
            )
        )

    def get_previour_fiscal_year_range(self):
        now = date.today()
        if now.month >= 4:
            start = now.replace(day=1, month=4, year=now.year - 1)
            end = now.replace(day=31, month=3, year=now.year)
        else:
            start = now.replace(day=1, month=4, year=now.year - 2)
            end = now.replace(day=31, month=3, year=now.year - 1)
        return start, end

    def get_current_fiscal_year_range(self):
        now = date.today()
        if now.month >= 4:
            start = now.replace(day=1, month=4, year=now.year)
            end = now
        else:
            start = now.replace(day=1, month=4, year=now.year - 1)
            end = now
        return start, end


class AutomatedModelsRunStatusView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AutomatedModelsRunStatusSerializer(data=request.data)
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Responses.success_response(
                "data save successfully", data=serializer.data
            )
        return Responses.error_response("something went wrong", data=serializer.errors)


class StateHeadMonthlySalesData(DownloadUploadViewSet):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.filter(
        ~Q(sales_type="DM"),
        ~Q(org_id=101),
        cust_categ="TR",
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("org_id", "cust_categ", "sales_type", "district", "city")
    serializer_class = TOebsSclArNcrAdvanceCalcTabDownloadSerializer
    pagination_class = CustomPagination
    file_name = "state_head_monthly_sales_data"

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def bucket_data(self, days, districts_list):
        queryset = (
            self.filter_queryset(
                self.get_queryset().filter(
                    invoice_date__range=days, district__in=districts_list
                )
            )
            .values("state", "district", "org_id", "packing_bag", "product")
            .annotate(
                bucket=Sum("quantity_invoiced"),
            )
        )
        bucket_df = pd.DataFrame(queryset)
        return bucket_df

    def list(self, request, *args, **kwargs):
        try:
            month = int(request.query_params.get("month", datetime.now().month))
            year = int(request.query_params.get("year", datetime.now().year))
            state = request.query_params.get("state")
            districts_list = self.get_districts(state)

            current_month_total_sales = self.bucket_data(
                [
                    date(day=1, month=month, year=year),
                    date(day=monthrange(year, month)[1], month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_total_sales"})
            current_month_bucket1 = self.bucket_data(
                [
                    date(day=1, month=month, year=year),
                    date(day=10, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket1"})
            if current_month_bucket1.empty:
                current_month_bucket1 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket1",
                    ]
                )
            current_month_bucket2 = self.bucket_data(
                [
                    date(day=11, month=month, year=year),
                    date(day=20, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket2"})
            if current_month_bucket2.empty:
                current_month_bucket2 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket2",
                    ]
                )
            current_month_bucket3 = self.bucket_data(
                [
                    date(day=21, month=month, year=year),
                    date(day=monthrange(year, month)[1], month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket3"})
            if current_month_bucket3.empty:
                current_month_bucket3 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket3",
                    ]
                )

            merge_df = pd.merge(
                pd.merge(
                    pd.merge(
                        current_month_bucket1,
                        current_month_bucket2,
                        on=["state", "district", "org_id", "packing_bag", "product"],
                        how="outer",
                    ),
                    current_month_bucket3,
                    on=["state", "district", "org_id", "packing_bag", "product"],
                    how="outer",
                ),
                current_month_total_sales,
                on=["state", "district", "org_id", "packing_bag", "product"],
                how="outer",
            ).fillna(0)

            premium_products_master_data = pd.DataFrame(
                PremiumProductsMasterTmp.objects.filter(
                    org_id__in=merge_df["org_id"].unique(),
                    state__in=merge_df["state"].unique(),
                    grade__in=merge_df["product"].unique(),
                    packaging_condition__in=merge_df["packing_bag"].unique(),
                ).values("org_id", "state", "premium", "grade", "packaging_condition")
            ).rename(columns={"grade": "product", "packaging_condition": "packing_bag"})

            premium_products_merge_df = pd.merge(
                merge_df,
                premium_products_master_data,
                on=["state", "org_id", "packing_bag", "product"],
            )
            premium_products_merge_df = premium_products_merge_df.drop(
                ["product", "org_id", "packing_bag"], axis=1
            )

            premium_products_merge_df = (
                premium_products_merge_df.groupby(["state", "district", "premium"])
                .aggregate(
                    {
                        "current_month_bucket1": "sum",
                        "current_month_bucket2": "sum",
                        "current_month_bucket3": "sum",
                        "current_month_total_sales": "sum",
                    }
                )
                .reset_index()
            )
            premium_products_merge_df["next_month_total_target"] = None
            premium_products_merge_df["next_month_bucket1"] = None
            premium_products_merge_df["next_month_bucket2"] = None
            premium_products_merge_df["next_month_bucket3"] = None

            data = premium_products_merge_df.to_dict(orient="records")
            return Responses.success_response(
                "state head monthly sales data.", data=data
            )
        except:
            return Responses.success_response("No data found", data=[])

    def download(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        data = response.data
        data = data["data"]
        df = pd.DataFrame(data)

        workbook = dump_to_excel(df, self.file_name)
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = HttpResponse(workbook, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={self.file_name}.xlsx"
        return response


class StateHeadMonthlySalesStateDropdown(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.filter(
        ~Q(sales_type="DM"),
        ~Q(org_id=101),
        cust_categ="TR",
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def __get_cal_tab_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {"state": self.__get_cal_tab_query("state")}
        return Responses.success_response(
            "monthly sales plan state dropdown", data=data
        )


class CrmSalesPlanningBottomUpTargetViewset(DownloadUploadViewSet):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.filter(
        ~Q(sales_type="DM"),
        ~Q(org_id=101),
        cust_categ="TR",
    ).order_by("district", "org_id", "packing_type", "product", "packing_bag")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("org_id", "cust_categ", "sales_type", "district", "city")
    serializer_class = TOebsSclArNcrAdvanceCalcTabDownloadSerializer
    file_name = "state_head_monthly_sales_data"

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def bucket_data(self, days, districts_list):
        queryset = (
            self.filter_queryset(
                self.get_queryset().filter(
                    invoice_date__range=days, district__in=districts_list
                )
            )
            .values("state", "district", "org_id", "packing_bag", "product")
            .annotate(
                bucket=Sum("quantity_invoiced"),
            )
        )
        bucket_df = pd.DataFrame(queryset)
        return bucket_df

    def target_bucket_data(self, districts_list, month, year):
        queryset = (
            CrmSalesPlanningBottomUpTarget.objects.filter(
                district__in=districts_list, month=month, year=year
            )
            .values("district", "brand", "packaging", "product", "bucket")
            .annotate(
                Count("bucket"),
                Sum("bottom_up_targets"),
                Sum("planned"),
                # deviation=((Sum("planned") - Sum("bottom_up_targets")) / Sum("planned"))* 100,
            )
        )
        target_bucket_df = pd.DataFrame(queryset)
        return target_bucket_df

    def list(self, request, *args, **kwargs):
        try:
            month = int(request.query_params.get("month", datetime.now().month))
            year = int(request.query_params.get("year", datetime.now().year))
            state = request.query_params.get("state")
            districts_list = self.get_districts(state)

            # Add one month to the current month
            next_month = (
                datetime(year=year, month=month, day=1) + timedelta(days=31)
            ).month

            # Numeric month to string month mapping
            MONTH_MAPPING = {
                1: "January",
                2: "Febraury",
                3: "March",
                4: "April",
                5: "May",
                6: "June",
                7: "July",
                8: "August",
                9: "September",
                10: "October",
                11: "November",
                12: "December",
            }
            # Convert numeric month to string month using the mapping dictionary
            string_month = MONTH_MAPPING.get(next_month)

            target_sale = self.target_bucket_data(districts_list, string_month, year)

            if not target_sale.empty:
                grouped_df = (
                    target_sale.groupby(
                        ["district", "brand", "packaging", "product", "bucket"]
                    )
                    .agg(
                        {
                            "bottom_up_targets__sum": "sum",
                            # "deviation": "sum",
                            "planned__sum": "sum",
                        }
                    )
                    .unstack(fill_value=0)
                )

                grouped_df.reset_index(inplace=True)
                grouped_df.columns.name = None
                grouped_df.columns = [
                    "district",
                    "brand",
                    "packaging",
                    "product",
                    "target_bucket1",
                    "target_bucket2",
                    "target_bucket3",
                    # "deviation_bucket1",
                    # "deviation_bucket2",
                    # "deviation_bucket3",
                    "planned_bucket1",
                    "planned_bucket2",
                    "planned_bucket3",
                ]

                # Calculate the 'bottom_up_targets__sum' for each row
                grouped_df["bottom_up_targets__sum"] = grouped_df[
                    ["target_bucket1", "target_bucket2", "target_bucket3"]
                ].sum(axis=1)

                # Calculate the 'deviation' for each row
                # grouped_df["deviation"] = round(
                #     grouped_df[
                #         ["deviation_bucket1", "deviation_bucket2", "deviation_bucket3"]
                #     ].sum(axis=1),
                #     2,
                # )
                # Calculate the 'planned' for each row
                grouped_df["planned__sum"] = round(
                    grouped_df[
                        [
                            "planned_bucket1",
                            "planned_bucket2",
                            "planned_bucket3",
                        ]
                    ].sum(axis=1),
                    2,
                )

                # Reorder the columns to match the desired output
                target_output_df = grouped_df[
                    [
                        "district",
                        "brand",
                        "packaging",
                        "product",
                        "target_bucket1",
                        "target_bucket2",
                        "target_bucket3",
                        "bottom_up_targets__sum",
                        # "deviation",
                        "planned__sum",
                    ]
                ]
                target_output_df["deviation"] = (
                    (
                        target_output_df["planned__sum"]
                        - target_output_df["bottom_up_targets__sum"]
                    )
                    / target_output_df["planned__sum"]
                ) * 100
                target_output_df["deviation"] = target_output_df["deviation"].replace(
                    -np.inf, 0
                )

                # Mapping of brand IDs to names
                brand_mapping = {"102": "SHREE", "103": "BANGUR", "104": "ROCKSTRONG"}

                # Replace brand IDs with names using the mapping
                target_output_df["brand"] = target_output_df["brand"].replace(
                    brand_mapping
                )

            else:
                target_output_df = pd.DataFrame(
                    columns=[
                        "district",
                        "brand",
                        "packaging",
                        "product",
                        "target_bucket1",
                        "target_bucket2",
                        "target_bucket3",
                        "bottom_up_targets__sum",
                        "deviation",
                        "planned__sum",
                    ]
                )

            current_month_total_sales = self.bucket_data(
                [
                    date(day=1, month=month, year=year),
                    date(day=monthrange(year, month)[1], month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_total_sales"})
            if current_month_total_sales.empty:
                current_month_total_sales = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_total_sales",
                    ]
                )
            current_month_bucket1 = self.bucket_data(
                [
                    date(day=1, month=month, year=year),
                    date(day=10, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket1"})
            if current_month_bucket1.empty:
                current_month_bucket1 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket1",
                    ]
                )
            current_month_bucket2 = self.bucket_data(
                [
                    date(day=11, month=month, year=year),
                    date(day=20, month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket2"})
            if current_month_bucket2.empty:
                current_month_bucket2 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket2",
                    ]
                )
            current_month_bucket3 = self.bucket_data(
                [
                    date(day=21, month=month, year=year),
                    date(day=monthrange(year, month)[1], month=month, year=year),
                ],
                districts_list,
            ).rename(columns={"bucket": "current_month_bucket3"})
            if current_month_bucket3.empty:
                current_month_bucket3 = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "org_id",
                        "packing_bag",
                        "product",
                        "current_month_bucket3",
                    ]
                )
            merge_df = pd.merge(
                pd.merge(
                    pd.merge(
                        current_month_bucket1,
                        current_month_bucket2,
                        on=["state", "district", "org_id", "packing_bag", "product"],
                        how="outer",
                    ),
                    current_month_bucket3,
                    on=["state", "district", "org_id", "packing_bag", "product"],
                    how="outer",
                ),
                current_month_total_sales,
                on=["state", "district", "org_id", "packing_bag", "product"],
                how="outer",
            ).fillna(0)
            merge_df["org_id"] = merge_df["org_id"].replace(
                {102: "SHREE", 103: "BANGUR", 104: "ROCKSTRONG"}
            )

            merge_df.rename(
                columns={"org_id": "brand", "packing_bag": "packaging"}, inplace=True
            )
            # print(merge_df)

            final_merge_df = pd.merge(
                merge_df,
                target_output_df,
                on=["district", "brand", "packaging", "product"],
                how="outer",
            ).fillna(0)
            final_merge_df["state"] = state

            approve_data = pd.DataFrame(
                TargetSalesPlanningMonthly.objects.filter(
                    month=next_month, year=year, state=state
                ).values(
                    "state",
                    "district",
                    "brand",
                    "packaging",
                    "product",
                    "target_bucket1",
                    "target_bucket2",
                    "target_bucket3",
                    "bottom_up_targets_sum",
                    "status",
                )
            ).rename(
                columns={
                    "target_bucket1": "approved_target_bucket1",
                    "target_bucket2": "approved_target_bucket2",
                    "target_bucket3": "approved_target_bucket3",
                    "bottom_up_targets_sum": "approved_bottom_up_targets_sum",
                }
            )
            if approve_data.empty:
                approve_data = pd.DataFrame(
                    columns=[
                        "state",
                        "district",
                        "brand",
                        "packaging",
                        "product",
                        "approved_target_bucket1",
                        "approved_target_bucket2",
                        "approved_target_bucket3",
                        "approved_bottom_up_targets_sum",
                        "status",
                    ]
                )

            if final_merge_df.empty:
                data = final_merge_df.to_dict(orient="records")
                return Responses.success_response(
                    "state head monthly sales data.", data=data
                )
            else:
                approved_merge_df = pd.merge(
                    final_merge_df,
                    approve_data,
                    on=["state", "district", "brand", "packaging", "product"],
                    how="outer",
                ).fillna(0)

                data = approved_merge_df.to_dict(orient="records")
                return Responses.success_response(
                    "state head monthly sales data.", data=data
                )

        except:
            return Responses.success_response("No data found", data=[])


class CrmSalesPlanningBottomUpTargetSum(GenericAPIView):
    queryset = CrmSalesPlanningBottomUpTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get_month_name(self, month_number):
        if not isinstance(month_number, int) or month_number < 1 or month_number > 12:
            return None

        return calendar.month_name[month_number]

    def get(self, request, *args, **kwargs):
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        state = request.query_params.get("state")
        next_month = month % 12 + 1

        # formatted_year = str(year)
        districts_list = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        month = self.get_month_name(month)
        next_month_name = self.get_month_name(next_month)

        queryset = (
            self.get_queryset()
            .filter(month=next_month_name, year=year, district__in=districts_list)
            .values("bottom_up_targets")
            .aggregate(target=Sum("bottom_up_targets"))
        )

        final_dict = {
            "bottoms_ups_target": self.format_val(queryset["target"]),
        }
        return Responses.success_response("data fetced", data=final_dict)


class TargetSalesPlanningMonthlyViewSet(DownloadUploadViewSet):
    queryset = TargetSalesPlanningMonthly.objects.all()
    serializer_class = TargetSalesPlanningMonthlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TargetSalesPlanningMonthlyFilter
    pagination_class = CustomPagination
    sorting_fields = (
        "state",
        "district",
        "brand",
        "packaging",
        "product",
    )

    def get_queryset(self):
        if self.request.method in ["PATCH", "PUT"] and not isinstance(
            getattr(self, "data", {}), dict
        ):
            lookups = {
                field + "__in": list(map(lambda x: x.get(field), self.data))
                for field in self.sorting_fields
            }
            return super(DownloadUploadViewSet, self).get_queryset().filter(**lookups)
        return super().get_queryset()

    def get_sorting_key(self):
        return lambda x: (
            x[field] if x.get(field) else "" for field in self.sorting_fields
        )


class CrmSalesPlanAndAdherenceViewset(GenericAPIView):
    def get_month_name(self, month_number):
        if not isinstance(month_number, int) or month_number < 1 or month_number > 12:
            return None
        return calendar.month_name[month_number]

    def get(self, request):
        month = int(request.query_params["month"])
        year = request.query_params["year"]
        state = request.query_params.get("state")
        formatted_year = str(year)

        districts_list = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )

        plan = (
            CrmSalesPlanningBottomUpTarget.objects.filter(
                month=self.get_month_name(month),
                year=formatted_year,
                district__in=districts_list,
            )
            .values("bottom_up_targets")
            .aggregate(Sum("bottom_up_targets"))
        )

        sale = (
            TOebsSclArNcrAdvanceCalcTab.objects.filter(
                state=state,
                invoice_date__month=month,
                invoice_date__year=int(year) - 1,
                cust_categ="TR",
            )
            .exclude(Q(org_id=101) | Q(sales_type="DM"))
            .aggregate(Sum("quantity_invoiced"))
        )

        quantity_invoiced_sum = sale.get("quantity_invoiced__sum")

        bottom_up_targets_sum = plan.get("bottom_up_targets__sum")

        if (
            quantity_invoiced_sum is not None
            and bottom_up_targets_sum is not None
            and bottom_up_targets_sum != 0
        ):
            adherence = quantity_invoiced_sum / bottom_up_targets_sum
        else:
            adherence = 0

        final_dict = {
            "plan": plan["bottom_up_targets__sum"],
            "adherence": adherence,
        }
        return Responses.success_response("data fetced", data=final_dict)


class TargetsalesPlanningSumCard(GenericAPIView):
    queryset = TargetSalesPlanningMonthly.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "state",
        "status",
    )

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get(self, request, *args, **kwargs):
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        state = request.query_params.get("state")

        queryset = (
            self.filter_queryset(self.get_queryset())
            .filter(month=month, year=year, state=state)
            .values("bottom_up_targets_sum")
            .aggregate(target=Sum("bottom_up_targets_sum"))
        )

        final_dict = {
            "bottoms_ups_target_sum": self.format_val(queryset["target"]),
        }
        return Responses.success_response("data fetced", data=final_dict)


class DistrictWisePricingProposalViewSet(DownloadUploadViewSet):
    current_date = datetime.now()
    previous_date = current_date - timedelta(days=1)
    queryset = CrmPricing.objects.filter(date__lte=previous_date).order_by("-date")
    serializer_class = DistrictWisePricingProposalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DistrictWisePricingProposalFilter
    pagination_class = CustomPagination
    file_name = "crm_pricing"

    def post(self, request):
        pricing_proposal_approval_data_serializer = PricingProposalApprovalSerializer(
            data=request.data,
            context={
                "request_user": request.user.id,
            },
            many=True,
        )
        pricing_proposal_approval_data_serializer.is_valid(raise_exception=True)
        pricing_proposal_approval_data_serializer.save()
        return Responses.success_response(
            "pricing proposal approval data run successfully",
            data=pricing_proposal_approval_data_serializer.data,
        )


class NetworkAdditionPlanViewSet(DownloadUploadViewSet):
    queryset = NetworkAdditionPlan.objects.all()
    serializer_class = NetworkAdditionPlanSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkAdditionPlanFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "Network_Addition_Plan"


class NetworkAdditionPlanStateViewSet(DownloadUploadViewSet):
    queryset = NetworkAdditionPlanState.objects.all()
    serializer_class = NetworkAdditionPlanStateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkAdditionPlanStateFilter
    pagination_class = CustomPagination
    file_name = "Network_Addition_Plan_State"

    def put(self, request):
        querset_data = request.data[0]
        querset_data["created_by"] = request.user.id
        querset_data["last_updated_by"] = request.user.id
        querset_data["last_update_login"] = request.user.id
        type_pk_string = querset_data["type_pk_string"]
        state = querset_data["state"]
        year = querset_data["year"]
        NetworkAdditionPlanStateObj = NetworkAdditionPlanState.objects.filter(
            type_pk_string=type_pk_string, state=state, year=year
        )
        if NetworkAdditionPlanStateObj:
            NetworkAdditionPlanStateObj = NetworkAdditionPlanStateObj.latest("id")
            serializer = NetworkAdditionPlanStateUpdateCreateSerializer(
                NetworkAdditionPlanStateObj, data=request.data[0], partial=True
            )
            if serializer.is_valid():
                serializer.save(
                    last_updated_by=request.user.id, last_update_login=request.user.id
                )
                return Responses.success_response(
                    "status updated successfully ",
                    data=serializer.data,
                )
            else:
                return Responses.error_response("update failed", data=serializer.errors)
        else:
            seralizer_obj = NetworkAdditionPlanStateUpdateCreateSerializer(
                data=request.data[0]
            )
            if not seralizer_obj.is_valid(raise_exception=True):
                return Responses.error_response(seralizer_obj.errors, "something wrong")
            seralizer_obj.save()
            return Responses.success_response(
                "Created Succesfully", data=seralizer_obj.data
            )


class TradeOrderPlacementApprovalViewset(DownloadUploadViewSet):
    queryset = TradeOrderPlacementApproval.objects.order_by(
        "-code_crm_order_no", "-last_update_date"
    ).distinct("code_crm_order_no")
    serializer_class = TradeOrderPlacementApprovalserializer
    filterset_class = TradeOrderPlacementApprovalFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"


class AnnualStateLevelTargetDropdown(GenericAPIView):
    queryset = AnnualStateLevelTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)

    filterset_class = AnnualStateLevelTargetFilter

    def __get_annual_state_level_target_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "zone": self.__get_annual_state_level_target_dropdown("zone"),
            "state": self.__get_annual_state_level_target_dropdown("state"),
            "status": self.__get_annual_state_level_target_dropdown("status"),
            "grade": self.__get_annual_state_level_target_dropdown("grade"),
            "packaging_condition": self.__get_annual_state_level_target_dropdown(
                "packaging_condition"
            ),
            "year": self.__get_annual_state_level_target_dropdown("year"),
        }
        return Responses.success_response(
            "annual state level target dropdown data.", data=data
        )


class AnnualDistrictLevelTargetDropdown(GenericAPIView):
    queryset = AnnualDistrictLevelTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ("state", "year", "region", "district", "brand", "grade")
    filterset_class = AnnualDistrictLevelTargetFilter

    def __get_annual_district_level_target_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_annual_district_level_target_dropdown("state"),
            "year": self.__get_annual_district_level_target_dropdown("year"),
            "district": self.__get_annual_district_level_target_dropdown("district"),
            "brand": self.__get_annual_district_level_target_dropdown("brand"),
            "grade": self.__get_annual_district_level_target_dropdown("grade"),
            "packaging_condition": self.__get_annual_district_level_target_dropdown(
                "packaging_condition"
            ),
        }
        return Responses.success_response(
            "annual district level target dropdown data.", data=data
        )


class AnnualDistrictLevelTargetViewSet(DownloadUploadViewSet):
    queryset = AnnualDistrictLevelTarget.objects.all()
    serializer_class = AnnualDistrictLevelTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnnualDistrictLevelTargetFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "annual_district_level_target"


class AnnualStateLevelTargetViewSet(DownloadUploadViewSet):
    queryset = AnnualStateLevelTarget.objects.all()
    serializer_class = AnnualStateLevelTargetSerializer
    filterset_class = AnnualStateLevelTargetFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "annual_state_level_target"


class RevisedBucketsApprovalViewset(DownloadUploadViewSet):
    queryset = RevisedBucketsApproval.objects.all()
    serializer_class = RevisedBucketsApprovalSerializer
    filterset_class = RevisedBucketsApprovalFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"


class CrmExceptionApprovalForReplacementOfProductViewset(DownloadUploadViewSet):
    queryset = CrmExceptionApprovalForReplacementOfProduct.objects.all()
    serializer_class = CrmExceptionApprovalForReplacementOfProductSerializer
    filterset_class = CrmExceptionApprovalForReplacementOfProductFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"


class StateHeadStateWiseTarget(GenericAPIView):
    queryset = AnnualDistrictLevelTarget.objects.all()
    serializer_class = AnnualDistrictLevelTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"
    filterset_class = AnnualDistrictLevelTargetFilter

    def get(self, request, *args, **kwargs):
        state_data = (
            self.filter_queryset(self.get_queryset())
            .values("state")
            .annotate(
                Count("state"),
                total=Sum("total"),
                april=Sum("april"),
                may=Sum("may"),
                june=Sum("june"),
                july=Sum("july"),
                august=Sum("august"),
                september=Sum("september"),
                october=Sum("october"),
                november=Sum("november"),
                december=Sum("december"),
                january=Sum("january"),
                february=Sum("february"),
                march=Sum("march"),
            )
        )

        return Responses.success_response(
            "state head state wise target fetched succesfully", data=state_data
        )


class RevisedBucketsApprovalDropdown(GenericAPIView):
    queryset = RevisedBucketsApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RevisedBucketsApprovalFilter

    def __get_revised_bucket_approval(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_revised_bucket_approval("state"),
            "district": self.__get_revised_bucket_approval("district"),
            "taluka": self.__get_revised_bucket_approval("taluka"),
            "brand": self.__get_revised_bucket_approval("brand"),
            "grade": self.__get_revised_bucket_approval("grade"),
            "month": self.__get_revised_bucket_approval("month"),
            "year": self.__get_revised_bucket_approval("year"),
            "packaging_condition": self.__get_revised_bucket_approval(
                "packaging_condition"
            ),
            "status": self.__get_revised_bucket_approval("status"),
        }
        return Responses.success_response(
            "revised bucket approval dropdown data.", data=data
        )


class NetworkAdditionCardsData(GenericAPIView):
    queryset = NetworkAdditionPlan.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkAdditionPlanFilter

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .values("state")
            .annotate(
                Count("state"),
                shree_counter_total=Sum("shree_counter"),
                total_counter_total=Sum("total_counter"),
                revised_plan_total=Sum("revised_plan"),
            )
        ).values(
            "state", "shree_counter_total", "total_counter_total", "revised_plan_total"
        )
        if data:
            data = data[0]

            total_counter_sum = data["total_counter_total"]
            target_numeric_reach_total = 0
            revised_plan_total = 0
            shree_counter_total = 0
            if data["revised_plan_total"]:
                revised_plan_total = data["revised_plan_total"]
            if data["shree_counter_total"]:
                shree_counter_total = data["shree_counter_total"]
            if total_counter_sum:
                target_numeric_reach_total = (
                    ((revised_plan_total) + (shree_counter_total)) / total_counter_sum
                ) * 100
                data["target_numeric_reach_total"] = round(
                    target_numeric_reach_total, 2
                )

            zone_obj = ZoneMappingNew.objects.filter(state=data["state"]).first()
            zone = None
            if zone_obj:
                zone = zone_obj.zone

            data["zone"] = zone
        else:
            data = {}

        return Responses.success_response("network addition cards data", data=data)


class CrmExceptionApprovalForReplacementOfProductDropdown(GenericAPIView):
    queryset = CrmExceptionApprovalForReplacementOfProduct.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmExceptionApprovalForReplacementOfProductFilter

    def __get_crm_exception_approval_approval(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "customer_name": self.__get_crm_exception_approval_approval(
                "customer_name"
            ),
            "account_type": self.__get_crm_exception_approval_approval("account_type"),
            "tso_name": self.__get_crm_exception_approval_approval("tso_name"),
            "product_name": self.__get_crm_exception_approval_approval("product_name"),
        }
        return Responses.success_response(
            "crm execption approval dropdown data.", data=data
        )


class AnnualStateLevelTargetCommentAndStatus(GenericAPIView):
    queryset = AnnualStateLevelTarget.objects.all()
    serializer_class = AnnualStateLevelTargetSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    lookup_field = "id"
    filterset_class = AnnualStateLevelTargetFilter

    def get(self, request, *args, **kwargs):
        data_dict = None
        state_obj = self.filter_queryset(self.get_queryset())
        if state_obj:
            state_obj = state_obj.latest("creation_date")
            data_dict = {
                "state": state_obj.state,
                "status": state_obj.status,
                "comments_by_zh": state_obj.comments_by_zh,
                "revised_target_by_zh": state_obj.revised_target_by_zh,
            }

        return Responses.success_response(
            "state data fetched succesfully", data=data_dict
        )


class CrmVerificationAndApprovalOfDealerSpFormViewSet(DownloadUploadViewSet):
    queryset = CrmVerificationAndApprovalOfDealerSpForm.objects.all()
    serializer_class = CrmVerificationAndApprovalOfDealerSpFormSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmVerificationAndApprovalOfDealerSpFormFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "Crm_Verification_And_Approval"


class SHAnnualStateLevelTargetApprovalCards(GenericAPIView):
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.all()

    def get_districts(self, state):
        queryset = (
            ZoneMappingNew.objects.filter(state=state)
            .values_list("district", flat=True)
            .distinct()
        )
        return queryset

    def get(self, request, *args, **kwargs):
        state = request.query_params.get("state")
        year = int(request.query_params.get("year"))
        start_year = year - 1
        end_year = start_year + 1
        adherence = None
        if state:
            districts_list = self.get_districts(state)
            last_year_actual_sales = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    cust_categ="TR",
                    district__in=districts_list,
                    invoice_date__date__range=[
                        f"{start_year}-04-01",
                        f"{end_year}-03-31",
                    ],
                    active=1,
                )
                .aggregate(
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                last_year_actual_sales = round(
                    last_year_actual_sales["quantity_sum"], 2
                )
            except:
                last_year_actual_sales = None

            last_year_plan = AnnualStateLevelTarget.objects.filter(
                year=start_year, state=state, status="Approved"
            ).aggregate(Sum("total"))

            if last_year_actual_sales and last_year_plan["total__sum"]:
                adherence = round(
                    ((last_year_actual_sales / last_year_plan["total__sum"]) * 100), 2
                )
            current_year_plan = AnnualStateLevelTarget.objects.filter(
                year=year, state=state, status="Approved"
            ).aggregate(Sum("total"))
        else:
            last_year_actual_sales = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    cust_categ="TR",
                    invoice_date__date__range=[
                        f"{start_year}-04-01",
                        f"{end_year}-03-31",
                    ],
                    active=1,
                )
                .aggregate(
                    quantity_sum=Sum("quantity_invoiced"),
                )
            )
            try:
                last_year_actual_sales = round(
                    last_year_actual_sales["quantity_sum"], 2
                )
            except:
                last_year_actual_sales = None

            last_year_plan = AnnualStateLevelTarget.objects.filter(
                year=start_year, status="Approved"
            ).aggregate(Sum("total"))

            if last_year_actual_sales and last_year_plan["total__sum"]:
                adherence = round(
                    ((last_year_actual_sales / last_year_plan["total__sum"]) * 100), 2
                )

            current_year_plan = AnnualStateLevelTarget.objects.filter(
                year=year, status="Approved"
            ).aggregate(Sum("total"))

        data_dict = {
            "current_year_plan": current_year_plan["total__sum"],
            "last_year_plan": last_year_plan["total__sum"],
            "last_year_actual_sales": last_year_actual_sales,
            "adherence": adherence,
        }

        return Responses.success_response("Fetched Succesfully", data=data_dict)


class AnnualStateLevelTargetDropdown(GenericAPIView):
    queryset = AnnualStateLevelTarget.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnnualStateLevelTargetFilter

    def __get_annual_state_level_target_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_annual_state_level_target_dropdown("state"),
        }
        return Responses.success_response(
            "annual state level target dropdown data.", data=data
        )


class ExceptionDisbursementApprovalViewSet(DownloadUploadViewSet):
    queryset = ExceptionDisbursementApproval.objects.all()
    serializer_class = ExceptionDisbursementApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ExceptionDisbursementApprovalFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "exception-disbursement"


class GiftRedeemRequestApprovalViewSet(DownloadUploadViewSet):
    queryset = GiftRedeemRequestApproval.objects.all().order_by("-id")
    serializer_class = GiftRedeemRequestApprovalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GiftRedeemRequestApprovalFilter
    pagination_class = CustomPagination
    lookup_field = "id"
    file_name = "Gift_Redeem_Request"


class ExceptionDisbursementApprovalDropdown(GenericAPIView):
    queryset = ExceptionDisbursementApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ExceptionDisbursementApprovalFilter

    def __get_exception_disbursement_approval_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_exception_disbursement_approval_dropdown("state"),
            "district": self.__get_exception_disbursement_approval_dropdown("district"),
            "taluka": self.__get_exception_disbursement_approval_dropdown("taluka"),
            "type": self.__get_exception_disbursement_approval_dropdown("type"),
        }
        return Responses.success_response(
            "exception disbursement approval dropdown data.", data=data
        )


class GiftRedeemRequestApprovalDropdown(GenericAPIView):
    queryset = GiftRedeemRequestApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GiftRedeemRequestApprovalFilter

    def __get_gift_redeem_request_approval_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "district": self.__get_gift_redeem_request_approval_dropdown("district"),
            "taluka": self.__get_gift_redeem_request_approval_dropdown("taluka"),
        }
        return Responses.success_response(
            "gift redeem request approval dropdown data.", data=data
        )


class NetworkAdditionStateCardsData(GenericAPIView):
    queryset = NetworkAdditionPlanState.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkAdditionPlanStateFilter

    def get(self, request, *args, **kwargs):
        data = (
            self.filter_queryset(self.get_queryset())
            .values("shree_counter", "total_counter", "revised_plan")
            .aggregate(
                shree_counter_total=Sum("shree_counter"),
                total_counter_total=Sum("total_counter"),
                revised_plan_total=Sum("revised_plan"),
            )
        )

        total_counter_sum = data["total_counter_total"]
        target_numeric_reach_total = 0
        revised_plan_total = 0
        shree_counter_total = 0
        if data["revised_plan_total"]:
            revised_plan_total = data["revised_plan_total"]
        if data["shree_counter_total"]:
            shree_counter_total = data["shree_counter_total"]
        if total_counter_sum:
            target_numeric_reach_total = (
                ((revised_plan_total) + (shree_counter_total)) / total_counter_sum
            ) * 100

        data["target_numeric_reach_total"] = round(target_numeric_reach_total, 2)

        return Responses.success_response(
            "network addition plan state cards data", data=data
        )


class TradeOrderPlacementApprovalDropdown(GenericAPIView):
    queryset = TradeOrderPlacementApproval.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_class = TradeOrderPlacementApprovalFilter

    def __get_Trade_order_placement_approval_dropdown(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .exclude(**{f"{query_string}__isnull": True})
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_Trade_order_placement_approval_dropdown("state"),
            "district": self.__get_Trade_order_placement_approval_dropdown("district"),
            "taluka": self.__get_Trade_order_placement_approval_dropdown("taluka"),
        }
        return Responses.success_response(
            "trade order placement dropdown data.", data=data
        )


class NetworkAdditionPlanStateSendToNshButtonViewSet(GenericAPIView):
    queryset = NetworkAdditionPlanState.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkAdditionPlanStateFilter

    def get(self, request, *args, **kwargs):
        user_email = request.user.email
        user_state = TgtRlsRoleData.objects.filter(email=user_email, role="SH").values(
            "state"
        )
        if user_state:
            year = datetime.now().year
            status = ["APPROVED", "PENDING"]
            queryset_count = (
                self.filter_queryset(self.get_queryset())
                .filter(state__in=user_state, year=year, status__in=status)
                .count()
            )
            # queryset_count = NetworkAdditionPlanState.objects.filter(
            #     state__in=user_state, year=year, status__in=status
            # ).count()
            if queryset_count == 0:
                return Responses.success_response("show button", data=True)
            else:
                return Responses.success_response("button not show", data=False)

        else:
            return Responses.error_response("state not found", data="")


class TargetSalesPlanningMonthlyTargetSum(GenericAPIView):
    queryset = TargetSalesPlanningMonthly.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get(self, request, *args, **kwargs):
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        state = request.query_params.get("state")
        next_month = month % 12 + 1

        queryset = (
            self.get_queryset()
            .filter(month=next_month, year=year, state=state)
            .values("bottom_up_targets_sum")
            .aggregate(target=Sum("bottom_up_targets_sum"))
        )

        final_dict = {
            "bottoms_ups_target": self.format_val(queryset["target"]),
        }
        return Responses.success_response("data fetced", data=final_dict)


class TargetSalesPlanningMonthlyAdherenceViewswet(GenericAPIView):
    queryset = TargetSalesPlanningMonthly.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("state",)

    def format_val(self, val):
        if val == None:
            return str(0) + " " + "MT"
        return str(round(val, 2)) + " " + "MT"

    def get(self, request, *args, **kwargs):
        month = int(request.query_params["month"])
        year = int(request.query_params["year"])
        state = request.query_params.get("state")
        next_month = month % 12 + 1

        try:
            queryset = (
                self.filter_queryset(self.get_queryset())
                .filter(month=next_month, year=year, state=state)
                .values("current_month_total_sales")
                .aggregate(
                    current_sale=Sum("current_month_total_sales"),
                    # current_target=Sum("bottom_up_targets_sum"),
                )
            )

            queryset1 = (
                self.filter_queryset(self.get_queryset())
                .filter(
                    month=next_month, year=year, state=state, status_by_nsh="APPROVED"
                )
                .values("bottom_up_targets_sum")
                .aggregate(
                    current_target=Sum("bottom_up_targets_sum"),
                )
            )

            if (
                queryset["current_sale"] is not None
                and queryset1["current_target"] is not None
                and queryset1["current_target"] != 0
            ):
                adherence = (
                    queryset["current_sale"] / queryset1["current_target"]
                ) * 100
            else:
                adherence = 0

            final_dict = {
                "plan_for_selected_month": queryset1["current_target"],
                "adherence": adherence,
            }
        except:
            final_dict = {
                "plan_for_selected_month": 0,
                "adherence": 0,
            }

        return Responses.success_response("data fetced", data=final_dict)
