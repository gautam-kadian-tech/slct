from django_filters import DateFilter
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.scheme_models import CrmComplaints
from analytical_data.models.technical_head_models import (
    CrmAnnualSiteConvPlan,
    CrmAnnualSiteConvPlanMonthly,
    CrmMaterialtestCertificate,
    CrmNthProductApproval,
    NthBudgetPlan,
    NthBudgetPlanMonthly,
)


class CrmNthProductApprovalfilter(FilterSet):
    """Crm Nthproduct Approval filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr=("in"))
    approval_date = DateFilter(field_name="approval_date")

    class Meta:
        model = CrmNthProductApproval
        fields = ()


class CrmNthActivityPlanfilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")


class CrmMaterialtestCertificatefilter(FilterSet):
    """Crm mkttst certificate filter class."""

    from_date = DateFilter(field_name="from_date")
    end_date = DateFilter(field_name="end_date")

    class Meta:
        model = CrmMaterialtestCertificate
        fields = ()


class CrmComplaintsFilter(FilterSet):
    """Crm Complaints certificate filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    creation_date = DateFilter(field_name="creation_date")
    comp_cat = CharInFilter(field_name="comp_cat", lookup_expr="in")
    comp_sub_cat = CharInFilter(field_name="comp_sub_cat", lookup_expr="in")
    so_name = CharInFilter(field_name="so_name", lookup_expr="in")
    assign_tso = CharInFilter(field_name="assign_tso", lookup_expr="in")
    start_date = DateFilter(field_name="creation_date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date", lookup_expr="lte")

    class Meta:
        model = CrmComplaints
        fields = ()


class CrmAnnualSiteConvPlanFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    plan_year = CharInFilter(field_name="plan_year", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")

    class Meta:
        model = CrmAnnualSiteConvPlan
        fields = ()


class NthBudgetPlanfilter(FilterSet):
    """Crm Nthproduct Approval filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    service = CharInFilter(field_name="service", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    sub_service = CharInFilter(field_name="sub_service", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    activity_plan = CharInFilter(field_name="activity_plan", lookup_expr="in")
    budget = CharInFilter(field_name="budget", lookup_expr="in")

    class Meta:
        model = NthBudgetPlan
        fields = ()


class CrmAnnualSiteConvPlanMonthlyFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")

    class Meta:
        model = CrmAnnualSiteConvPlanMonthly
        fields = ()


class NthBudgetPlanMonthlyFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    service = CharInFilter(field_name="service", lookup_expr="in")
    sub_service = CharInFilter(field_name="sub_service", lookup_expr="in")

    class Meta:
        model = NthBudgetPlanMonthly
        fields = ()
