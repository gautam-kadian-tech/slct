"custom_perm"
from rest_framework.permissions import IsAuthenticated

from accounts.user_role_choices import UserRoleChoice
from analytical_data.enum_classes import NSHApprovalChoices
from analytical_data.models.state_head_models import *


class IsLogisticsHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "Logistics" in request.user.roles.values_list("role_name", flat=True)


class IsAACBusinessHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "AACBusinessHead" in request.user.roles.values_list(
            "role_name", flat=True
        )


class IsNationalInfluencerManager(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "NIM" in request.user.roles.values_list("role_name", flat=True)


class IsStateInfluencerManager(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "SIM" in request.user.roles.values_list("role_name", flat=True)


class IsMBGeography(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "MBG" in request.user.roles.values_list("role_name", flat=True)


class IsMBNational(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "MBN" in request.user.roles.values_list("role_name", flat=True)


class IsNonTradeHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "NTH" in request.user.roles.values_list("role_name", flat=True)


class IsPlantLogisticsHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "PLH" in request.user.roles.values_list("role_name", flat=True)


class IsZonalLogisticsHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "ZLH" in request.user.roles.values_list("role_name", flat=True)


class IsNationalStateHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "NSH" in request.user.roles.values_list("role_name", flat=True)

    def has_object_permission(self, request, view, obj):
        if not getattr(obj, "status") == NSHApprovalChoices.INITIATED.value:
            return False
        return super().has_object_permission(request, view, obj)


class IsStateHead(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "SH" in request.user.roles.values_list("role_name", flat=True)

    def has_object_permission(self, request, view, obj):
        if not getattr(obj, "status") in (
            NSHApprovalChoices.PENDING.value,
            NSHApprovalChoices.REVIEWAL.value,
        ):
            return False
        return super().has_object_permission(request, view, obj)


class IsLBT(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "LBT" in request.user.roles.values_list("role_name", flat=True)


class IsCBT(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and "CBT" in request.user.roles.values_list("role_name", flat=True)


class IsHandlingAgent(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and UserRoleChoice.HA.value in request.user.roles.values_list(
            "role_name", flat=True
        )


class IsRRCCement(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and UserRoleChoice.RRCCEMENT.value in request.user.roles.values_list(
            "role_name", flat=True
        )


class IsSuperAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
            request, view
        ) and UserRoleChoice.SuperAdmin.value in request.user.roles.values_list(
            "role_name", flat=True
        )
