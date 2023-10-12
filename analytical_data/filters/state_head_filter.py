"""Route restrictions filter module."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    CrmMarketMappingPricing,
    CrmPricing,
    NetworkAdditionPlan,
    NetworkAdditionPlanState,
    SlctActivityProps,
    SlctAnnualDiscSlabBased,
    SlctAnnualDiscTargetBased,
    SlctAnnualSalesPlan,
    SlctBenchmarkChangeRequest,
    SlctBoosterPerDayGrowthScheme,
    SlctBoosterPerDayTargetScheme,
    SlctBorderDiscProps,
    SlctBrandingRequests,
    SlctCashDiscProps,
    SlctCombSlabGrowthProps,
    SlctDealerLinkedSchProps,
    SlctDealerOutsBasedProps,
    SlctDirPltBilngDiscProps,
    SlctEngCashSchPtProps,
    SlctInKindBoosterSchemeProps,
    SlctInKindQuantitySlabTourDestination,
    SlctInKindTourProposal,
    SlctMarketInformation,
    SlctMasonKindSchBagPointConv,
    SlctMasonKindSchProps,
    SlctMonthlySalesPlan,
    SlctNewMarketPricingRequest,
    SlctPartyWiseSchemeProps,
    SlctPriceChangeRequestExistingMarkt,
    SlctPrmPrdComboScmProps,
    SlctQuantitySlabProps,
    SlctRailBasedSchProps,
    SlctSchemeDiscountProposal,
    SlctSchemeProposalGap,
    SlctVehicleSchProps,
    SlctVolCutterSlabBasedProposal,
    SlctVolCutterTargetBased,
    TargetSalesPlanningMonthly,
    TOebsSclArNcrAdvanceCalcTab,
    TOebsXxsclVehicleMaster,
    TradeOrderPlacementApproval,
    ZoneMappingNew,
)
from analytical_data.models.state_head_models import (
    AnnualDistrictLevelTarget,
    AnnualStateLevelTarget,
    CrmExceptionApprovalForReplacementOfProduct,
    CrmVerificationAndApprovalOfDealerSpForm,
    ExceptionDisbursementApproval,
    GiftRedeemRequestApproval,
    RevisedBucketsApproval,
)


class BaseFilterSet(FilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    # city = CharInFilter(field_name="city", lookup_expr="in")
    # dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    # period_from_date = DateFilter(field_name="period_from_date")
    # period_to_date = DateFilter(field_name="period_to_date")
    # on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    scheme_status = CharInFilter(field_name="scheme_status", lookup_expr="in")


class SlctCashDiscPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealerscheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="periodstartdate")
    period_to_date = DateFilter(field_name="periodenddate")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctCashDiscProps
        fields = ()


class SlctCombSlabGrowthPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctCombSlabGrowthProps
        fields = ()


class SlctPartyWiseSchemePropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctPartyWiseSchemeProps
        fields = ()


# class ZoneMappingNewFilter(BaseFilterSet):

#     city = CharInFilter(field_name="city", lookup_expr="in")
#     class Meta:
#         model = ZoneMappingNew
#         fields = ()


class SlctQuantitySlabPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctQuantitySlabProps
        fields = ()


class SlctDirPltBilngDiscPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")

    class Meta:
        model = SlctDirPltBilngDiscProps
        fields = ()


class SlctPrmPrdComboScmPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctPrmPrdComboScmProps
        fields = ()


class SlctVehicleSchPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")

    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctVehicleSchProps
        fields = ()


class SlctMarketInformationFilter(BaseFilterSet):
    class Meta:
        model = SlctMarketInformation
        fields = ()


class SlctMasonKindSchPropsFilter(BaseFilterSet):
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctMasonKindSchProps
        fields = ()


class SlctMasonKindSchBagPointConvFilter(BaseFilterSet):
    class Meta:
        model = SlctMasonKindSchBagPointConv
        fields = ()


class SlctBorderDiscPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctBorderDiscProps
        fields = ()


class SlctSchemeProposalGapFilter(BaseFilterSet):
    class Meta:
        model = SlctSchemeProposalGap
        fields = ()


class SlctSchemeDiscountProposalFilter(BaseFilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = SlctSchemeDiscountProposal
        fields = ()


class SlctInKindQuantitySlabTourDestinationFilter(BaseFilterSet):
    class Meta:
        model = SlctInKindQuantitySlabTourDestination
        fields = ()


class SlctInKindTourProposalFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctInKindTourProposal
        fields = ()


class SlctActivityPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctActivityProps
        fields = ()


class SlctRailBasedSchPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctRailBasedSchProps
        fields = ()


class SlctDealerOutsBasedPropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctDealerOutsBasedProps
        fields = ()


class SlctEngCashSchPtPropsFilter(BaseFilterSet):
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctEngCashSchPtProps
        fields = ()


class SlctDealerLinkedSchPropsFilter(BaseFilterSet):
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctDealerLinkedSchProps
        fields = ()


class SlctVolCutterTargetBasedFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_scheme", lookup_expr="in")

    class Meta:
        model = SlctVolCutterTargetBased
        fields = ()


class SlctVolCutterSlabBasedProposalFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_invoice", lookup_expr="in")

    class Meta:
        model = SlctVolCutterSlabBasedProposal
        fields = ()


class SlctBoosterPerDayTargetSchemeFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctBoosterPerDayTargetScheme
        fields = ()


class SlctBoosterPerDayGrowthSchemeFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")

    class Meta:
        model = SlctBoosterPerDayGrowthScheme
        fields = ()


class SlctBenchmarkChangeRequestFilter(BaseFilterSet):
    class Meta:
        model = SlctBenchmarkChangeRequest
        fields = ()


class SlctPriceChangeRequestExistingMarktFilter(BaseFilterSet):
    class Meta:
        model = SlctPriceChangeRequestExistingMarkt
        fields = ()


class SlctNewMarketPricingRequestFilter(BaseFilterSet):
    class Meta:
        model = SlctNewMarketPricingRequest
        fields = ()


class SlctBrandingRequestsFilter(BaseFilterSet):
    class Meta:
        model = SlctBrandingRequests
        fields = ()


class SlctAnnualDiscSlabBasedFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")

    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctAnnualDiscSlabBased
        fields = ()


class SlctAnnualDiscTargetBasedFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")
    period_from_date = DateFilter(field_name="period_from_date")
    period_to_date = DateFilter(field_name="period_to_date")
    on_off_invoice = CharInFilter(field_name="on_off_invoice", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    slab_scheme = CharInFilter(field_name="slab_based_scheme", lookup_expr="in")

    class Meta:
        model = SlctAnnualDiscTargetBased
        fields = ()


class SlctInKindBoosterSchemePropsFilter(BaseFilterSet):
    dealer_scheme = CharInFilter(field_name="dealer_scheme", lookup_expr="in")

    class Meta:
        model = SlctInKindBoosterSchemeProps
        fields = ()


class SlctAnnualSalesPlanFilter(BaseFilterSet):
    class Meta:
        model = SlctAnnualSalesPlan
        fields = ()


class SlctMonthlySalesPlanFilter(BaseFilterSet):
    state = CharInFilter(field_name="state")
    month = CharInFilter(field_name="date__month")
    year = CharInFilter(field_name="date__year")

    class Meta:
        model = SlctMonthlySalesPlan
        fields = ()


class CrmMarketMappingPricingFilter(BaseFilterSet):
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    date = DateFilter(field_name="counter_visit_start_time__date")
    start_date = DateFilter(
        field_name="counter_visit_start_time__date", lookup_expr="gte"
    )
    end_date = DateFilter(
        field_name="counter_visit_start_time__date", lookup_expr="lte"
    )
    month = CharInFilter(field_name="counter_visit_start_time__date__month")
    year = CharInFilter(field_name="counter_visit_start_time__date__year")

    class Meta:
        model = CrmMarketMappingPricing
        fields = ()


class CrmPricingFilter(BaseFilterSet):
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    date = DateFilter(field_name="date")
    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")
    month = CharInFilter(field_name="date__month")
    year = CharInFilter(field_name="date__year")

    class Meta:
        model = CrmPricing
        fields = ()


class TOebsSclArNcrAdvanceCalcTabFilter(FilterSet):
    org_id = CharInFilter(field_name="org_id", lookup_expr="in")
    cust_categ = CharInFilter(field_name="cust_categ", lookup_expr="in")
    sales_type = CharInFilter(field_name="sales_type", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    start_date = DateFilter(field_name="invoice_date", lookup_expr="gte")
    end_date = DateFilter(field_name="invoice_date", lookup_expr="lte")

    class Meta:
        model = TOebsSclArNcrAdvanceCalcTab
        fields = ()


class TargetSalesPlanningMonthlyFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    packaging = CharInFilter(field_name="packaging", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = TargetSalesPlanningMonthly
        fields = ()


class DistrictWisePricingProposalFilter(FilterSet):
    product = CharInFilter(field_name="product", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    date = DateFilter(field_name="date")
    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")
    month = CharInFilter(field_name="date__month")
    year = CharInFilter(field_name="date__year")

    class Meta:
        model = CrmPricing
        fields = ()


class NetworkAdditionPlanFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    type_pk_string = CharInFilter(field_name="type_pk_string", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")

    class Meta:
        model = NetworkAdditionPlan
        fields = ()


class NetworkAdditionPlanStateFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    type_pk_string = CharInFilter(field_name="type_pk_string", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")

    class Meta:
        model = NetworkAdditionPlanState
        fields = ()


class AnnualStateLevelTargetFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    year = CharInFilter(field_name="year", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = AnnualStateLevelTarget
        fields = ()


class AnnualDistrictLevelTargetFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    packaging_condition = CharInFilter(
        field_name="packaging_condition", lookup_expr="in"
    )
    year = CharInFilter(field_name="year", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")

    class Meta:
        model = AnnualDistrictLevelTarget
        fields = ()


class RevisedBucketsApprovalFilter(FilterSet):
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    packaging_condition = CharInFilter(
        field_name="packaging_condition", lookup_expr="in"
    )
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = RevisedBucketsApproval
        fields = ()


class CrmExceptionApprovalForReplacementOfProductFilter(FilterSet):
    year = CharInFilter(field_name="year", lookup_expr="in")
    month = CharInFilter(field_name="month", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    status_by_sh = CharInFilter(field_name="status_by_sh", lookup_expr="in")
    status_by_nsh = CharInFilter(field_name="status_by_nsh", lookup_expr="in")
    customer_name = CharInFilter(field_name="customer_name", lookup_expr="in")
    product_name = CharInFilter(field_name="product_name", lookup_expr="in")
    tso_name = CharInFilter(field_name="tso_name", lookup_expr="in")
    account_type = CharInFilter(field_name="account_type", lookup_expr="in")
    approved_by = CharInFilter(field_name="approved_by", lookup_expr="in")

    class Meta:
        model = CrmExceptionApprovalForReplacementOfProduct
        fields = ()


class CrmVerificationAndApprovalOfDealerSpFormFilter(FilterSet):
    district = CharInFilter(field_name="district", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    dealer_name = CharInFilter(field_name="dealer_name", lookup_expr="in")
    dealer_crm_code = CharInFilter(field_name="dealer_crm_code", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    account_number = CharInFilter(field_name="account_number", lookup_expr="in")
    ifsc_code = CharInFilter(field_name="ifsc_code", lookup_expr="in")
    account_name = CharInFilter(field_name="account_name", lookup_expr="in")
    gst_number = CharInFilter(field_name="gst_number", lookup_expr="in")
    contact_number = CharInFilter(field_name="contact_number", lookup_expr="in")
    aadhaar_number = CharInFilter(field_name="aadhaar_number", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")
    status_by_sh = CharInFilter(field_name="status_by_sh", lookup_expr="in")
    status_by_nsh = CharInFilter(field_name="status_by_nsh", lookup_expr="in")
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")

    class Meta:
        model = CrmVerificationAndApprovalOfDealerSpForm
        fields = ()


class ExceptionDisbursementApprovalFilter(FilterSet):
    district = CharInFilter(field_name="district", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")
    status_by_sh = CharInFilter(field_name="status_by_sh", lookup_expr="in")
    status_by_nsh = CharInFilter(field_name="status_by_nsh", lookup_expr="in")
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")
    approved_by = CharInFilter(field_name="approved_by", lookup_expr="in")

    class Meta:
        model = ExceptionDisbursementApproval
        fields = ()


class GiftRedeemRequestApprovalFilter(FilterSet):
    district = CharInFilter(field_name="district", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    entity_type = CharInFilter(field_name="entity_type", lookup_expr="in")
    redeeem_type = CharInFilter(field_name="redeeem_type", lookup_expr="in")
    redeem_request_raised_by_type = CharInFilter(
        field_name="redeem_request_raised_by_type", lookup_expr="in"
    )
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")
    approved_by = CharInFilter(field_name="approved_by", lookup_expr="in")
    nsh_approved = CharInFilter(field_name="nsh_approved", lookup_expr="in")
    status_by_sh = CharInFilter(field_name="status_by_sh", lookup_expr="in")
    status_by_nsh = CharInFilter(field_name="status_by_nsh", lookup_expr="in")
    comment_by_sh = CharInFilter(field_name="comment_by_sh", lookup_expr="in")
    comment_by_nsh = CharInFilter(field_name="comment_by_nsh", lookup_expr="in")
    comment_by_do = CharInFilter(field_name="comment_by_do", lookup_expr="in")

    class Meta:
        model = GiftRedeemRequestApproval
        fields = ()


class TradeOrderPlacementApprovalFilter(FilterSet):
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    status_code = CharInFilter(field_name="status_code", lookup_expr="in")
    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")
    date_range_after = DateFilter(field_name="date", method="filter_date_range_after")
    date_range_before = DateFilter(field_name="date", method="filter_date_range_before")

    class Meta:
        model = TradeOrderPlacementApproval
        fields = ()

    def filter_date_range_after(self, queryset, name, value):
        return queryset.filter(date__date__lte=value)

    def filter_date_range_before(self, queryset, name, value):
        return queryset.filter(date__date__gte=value)
