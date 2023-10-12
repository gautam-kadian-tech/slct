"""Filter module for Influencer Manager Module."""
import datetime

from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.influencer_manager_models import (
    AugmentationOutputTable,
    CrmInflGiftMaster,
    CrmInflMgrAnnualPlan,
    CrmInflMgrAnnualPlanMonthly,
    CrmInflMgrMeetPlan,
    CrmInflMgrMeetPlanMonthly,
    CrmInflMgrSchemeBudget,
    CrmInflScheme,
    InfluencerMeetBudgetOutput,
    InfluencerMeetingOutput,
)


class CrmInflMgrMeetPlanFilter(FilterSet):
    """crm infl meet plan filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    influencer_type = CharInFilter(field_name="influencer_type", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    plan_year = CharInFilter(field_name="plan_year", lookup_expr="in")

    class Meta:
        model = CrmInflMgrMeetPlan
        fields = ()


class CrmInflMgrAnnualPlanFilter(FilterSet):
    """crm infl manager annual plan filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    influencer_type = CharInFilter(field_name="influencer_type", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    plan_year = CharInFilter(field_name="plan_year", lookup_expr="in")

    class Meta:
        model = CrmInflMgrAnnualPlan
        fields = ()


class CrmInflMgrSchemeBudgetFilter(FilterSet):
    """crm influencer manager scheme budget filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    plan_year = CharInFilter(field_name="plan_year", lookup_expr="in")
    district = CharInFilter(field_name="disrict", lookup_expr="in")

    class Meta:
        model = CrmInflMgrSchemeBudget
        fields = ()


class InfluencerOutputFilter(FilterSet):
    """crm influencer manager scheme budget filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    technical_activity_type = CharInFilter(
        field_name="technical_activity_type", lookup_expr="in"
    )
    date = DateFilter(field_name="date")

    class Meta:
        model = InfluencerMeetingOutput
        fields = ()


class InfluencerMeetBudgetOutputFilter(FilterSet):
    """crm influencer manager scheme budget filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    technical_activity_type = CharInFilter(
        field_name="technical_activity_type", lookup_expr="in"
    )

    class Meta:
        model = InfluencerMeetBudgetOutput
        fields = ()


class AugmentationOutputFilter(FilterSet):
    date = CharInFilter(field_name="date__month")

    class Meta:
        model = AugmentationOutputTable
        fields = ()


class CrmInflSchemeFilter(FilterSet):
    class Meta:
        model = CrmInflScheme
        fields = ()


class CrmInflMgrMeetPlanMonthlyFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    influencer_type = CharInFilter(field_name="influencer_type", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")

    class Meta:
        model = CrmInflMgrMeetPlanMonthly
        fields = ()


class CrmInflMgrAnnualPlanMonthlyFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    influencer_type = CharInFilter(field_name="influencer_type", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")

    class Meta:
        model = CrmInflMgrAnnualPlanMonthly
        fields = ()
