"""Filter class module for brand approval."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.marketing_branding_models import (
    CrmMabBrandingAppr,
    CrmMabBtlPlanning,
    CrmMabInitReq,
    CrmMabPastRequisitions,
    MarketMappingBrandingBudget,
    NewMarketPricingApproval,
    SponsorshipBudget,
    TNmOmxMaterialTransactionsV,
    VendorDetailMaster,
)
from analytical_data.models.state_head_models import BrandingActivity


class CrmMabBrandingApprFilter(FilterSet):
    """Crm Mab Branding approval filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    raised_by = CharInFilter(field_name="raised_by", lookup_expr="in")
    activity_type = CharInFilter(field_name="activity_type", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")

    class Meta:
        model = CrmMabBrandingAppr
        fields = ()


class CrmMabBtlPlanningFilter(FilterSet):
    """Crm Mab Bt Planning filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    branding_activity = CharInFilter(field_name="branding_activity", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = CrmMabBtlPlanning
        fields = ()


class CrmMabPastRequisitionsFilter(FilterSet):
    """Crm Mab Past Requisitions filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    po_number = CharInFilter(field_name="po_number", lookup_expr="in")
    req_number = CharInFilter(field_name="req_number", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = CrmMabPastRequisitions
        fields = ()


class VendorDetailMasterFilter(FilterSet):
    """vendor detail master filter class."""

    vendor_name = CharInFilter(field_name="vendor_name", lookup_expr="in")

    class Meta:
        model = VendorDetailMaster
        fields = ()


class VendorDetailMasterVendorCodeFilter(FilterSet):
    class Meta:
        model = VendorDetailMaster
        fields = ()


class TNmOmxMaterialTransactionsVFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    org_id = CharInFilter(field_name="org_id", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")

    class Meta:
        model = TNmOmxMaterialTransactionsV
        fields = ()


class MarketMappingBrandingBudgetFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")

    class Meta:
        model = MarketMappingBrandingBudget
        fields = ()


class BrandingActivityFilter(FilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    vendor_name = CharInFilter(field_name="vendor_name", lookup_expr="in")
    status_of_scheme = CharInFilter(field_name="status_of_scheme", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    activity_type = CharInFilter(field_name="activity_type", lookup_expr="in")
    activity_for = CharInFilter(field_name="activity_for", lookup_expr="in")
    activity_category = CharInFilter(field_name="activity_category", lookup_expr="in")
    activity_name = CharInFilter(field_name="activity_name", lookup_expr="in")
    site_type = CharInFilter(field_name="site_type", lookup_expr="in")
    objective_of_activity = CharInFilter(
        field_name="objective_of_activity", lookup_expr="in"
    )
    start_date = DateFilter(field_name="date_of_start", lookup_expr="gte")
    end_date = DateFilter(field_name="date_of_start", lookup_expr="lte")
    raised_by = CharInFilter(field_name="raised_by", lookup_expr="in")

    class Meta:
        model = BrandingActivity
        fields = ()


class SponsorshipBudgetFilter(FilterSet):
    """sponsorship budget filter class."""

    status = CharInFilter(field_name="status", lookup_expr="in")
    market_mapping_branding_budget = CharInFilter(
        field_name="market_mapping_branding_budget__id", lookup_expr="in"
    )
    raised_by = CharInFilter(field_name="raised_by", lookup_expr="in")

    class Meta:
        model = SponsorshipBudget
        fields = ()
