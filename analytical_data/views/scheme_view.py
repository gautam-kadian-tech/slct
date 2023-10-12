import json
from datetime import datetime as t_date

from django.db import transaction
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import CrmComplaintsFilter, SchemeDateRangeFilter
from analytical_data.models.scheme_models import (
    CrmComplaints,
    GiftMaster,
    Schemes,
)
from analytical_data.serializers import (
    CrmComplaintsSerializer,
    SchemeForSerializer,
    SchemeLocationSerializer,
    SchemeProductsSerializer,
    SchemeRewardsSerializer,
    SchemesSerializer,
)
from analytical_data.utils import CustomPagination, Responses


class SchemeViewSet(ModelViewSet):
    serializer_class = SchemesSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request):
        request.data._mutable = True
        request.data["created_by"] = request.user.id
        request.data["last_updated_by"] = request.user.id
        document = request.FILES.get("document")
        request.data["document"] = document
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        scheme_object = serializer.save()
        states = json.loads(request.data["state"])
        districts = json.loads(request.data["district"])
        states = ", ".join(states)
        districts = ", ".join(districts)
        scheme_location = {
            "scheme": scheme_object.id,
            "state": states,
            "district": districts,
            "created_by": request.user.id,
        }

        scheme_location_serializer = SchemeLocationSerializer(data=scheme_location)
        if not scheme_location_serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        scheme_location_serializer.save()

        eligibility_data = json.loads(request.data["scheme_for_code"])
        eligibility_data = ", ".join(eligibility_data)
        scheme_for_object = {
            "scheme": scheme_object.id,
            "scheme_for_code": eligibility_data,
            "created_by": request.user.id,
        }

        scheme_for_serializer = SchemeForSerializer(data=scheme_for_object)
        if not scheme_for_serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        scheme_for_serializer.save()
        no_of_bags = json.loads(request.data["no_of_bags"])
        org_id = json.loads(request.data["org_id"])
        grade = json.loads(request.data["grade"])
        packaging = json.loads(request.data["packaging"])
        bag_type = json.loads(request.data["bag_type"])
        for p_keys in range(len(org_id)):
            scheme_product_object = {
                "scheme": scheme_object.id,
                "no_of_bags": no_of_bags[p_keys],
                "org_id": org_id[p_keys],
                "grade": grade[p_keys],
                "packaging": packaging[p_keys],
                "bag_type": bag_type[p_keys],
                "created_by": request.user.id,
            }
            scheme_product_serializer = SchemeProductsSerializer(
                data=scheme_product_object
            )
            if not scheme_product_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=serializer.errors
                )
            scheme_product_serializer.save()
        rewards_points_data = json.loads(request.data["rewards_points"])
        rewards_data = json.loads(request.data["gift_or_cash"])
        remuneration_cash = json.loads(request.data["remuneration_cash"])
        remuneration_gift = json.loads(request.data["remuneration_gift"])

        for val in range(len(rewards_points_data)):
            scheme_reward_object = {
                "scheme": scheme_object.id,
                "rewards_points": rewards_points_data[val],
                "rewards": rewards_data[val],
                "gift": remuneration_gift[val],
                "cash": remuneration_cash[val],
                "created_by": request.user.id,
            }

            scheme_reward_serializer = SchemeRewardsSerializer(
                data=scheme_reward_object
            )
            if not scheme_reward_serializer.is_valid(raise_exception=True):
                return Responses.error_response(
                    "some issue rise", data=serializer.errors
                )
            scheme_reward_serializer.save()

        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class GetStateSchemeViewSet(ModelViewSet):
    queryset = Schemes.objects.all()
    serializer_class = SchemesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SchemeDateRangeFilter
    pagination_class = CustomPagination
    # lookup_field = "id"


class GetStateSchemeByIdViewSet(ModelViewSet):
    queryset = Schemes.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        scl_case_study_serializer = SchemesSerializer(queryset, many=True)
        return Responses.success_response(
            "data updated successfully", data=scl_case_study_serializer.data
        )


# National Technical Head Work
class CrmComplaintsViewSet(ModelViewSet):
    queryset = CrmComplaints.objects.all()
    serializer_class = CrmComplaintsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmComplaintsFilter
    pagination_class = CustomPagination
    lookup_field = "id"


class GetCrmComplaintsByIdViewSet(ModelViewSet):
    queryset = CrmComplaints.objects.all()

    def get(self, request, id=None):
        id = request.query_params.get("id")
        if id:
            queryset = self.queryset.filter(id=id)
        else:
            self.queryset
        crm_comp_obj = CrmComplaintsSerializer(queryset, many=True)
        return Responses.success_response(
            "data fetch by id successfully ", data=crm_comp_obj.data
        )


class CreateCrmComplaintsViewSet(ModelViewSet):
    queryset = CrmComplaints.objects.all()
    serializer_class = CrmComplaintsSerializer

    def post(self, request):
        request.data["created_by"] = request.user.id
        document = request.FILES["related_doc"]
        request.data["related_doc"] = document
        request.data["last_updated_by"] = request.user.id
        request.data["last_update_login"] = request.user.id
        request.data["last_update_date"] = t_date.today()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Responses.error_response("some issue rise", data=serializer.errors)
        serializer.save()
        return Responses.success_response(
            "data inserted successfully", data=serializer.data
        )


class GiftMasterDropdown(ModelViewSet):
    def get(self, request):
        data = GiftMaster.objects.values("item_code", "item_name")
        return Responses.success_response("gift master dropdown", data=data)


class CrmComplaintsDropdown(GenericAPIView):
    queryset = CrmComplaints.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CrmComplaintsFilter

    def __crm_complaint_dropdown_query(self, query_string, filter_query=Q):
        return (
            self.filter_queryset(self.get_queryset())
            .filter(filter_query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__crm_complaint_dropdown_query(
                "state", Q(state__isnull=False)
            ),
            "district": self.__crm_complaint_dropdown_query(
                "district", Q(district__isnull=False)
            ),
            "so_name": self.__crm_complaint_dropdown_query(
                "so_name", Q(so_name__isnull=False)
            ),
            "assign_tso": self.__crm_complaint_dropdown_query(
                "assign_tso", Q(assign_tso__isnull=False)
            ),
        }
        return Responses.success_response("crm complaint dropdown data.", data=data)
