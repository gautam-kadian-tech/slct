from django_filters.rest_framework import DateFilter, FilterSet, filters

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    PremiumProductsMasterTmp,
    PricingProposalApproval,
)
from analytical_data.models.pricing_strategy_models import *


class CompetitionPriceNewMarketsFilter(FilterSet):
    """competition price new markets filter class"""

    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    month = CharInFilter(field_name="date__month")
    year = CharInFilter(field_name="date__year")

    class Meta:
        model = CompetitionPriceNewMarkets
        fields = ()


class PriceBenchmarksFilter(FilterSet):
    """price benchmark filter set"""

    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    benchmark_name = CharInFilter(field_name="benchmark_name", lookup_expr="in")
    month = CharInFilter(field_name="month__month")
    year = CharInFilter(field_name="month__year")

    class Meta:
        model = PriceBenchmarks
        fields = ()


class NewPriceComputationFilter(FilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    active = CharInFilter(field_name="active", lookup_expr="in")
    date = DateFilter(field_name="date")
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = NewPriceComputation
        fields = ()


class NmMarketSharePotentialFilter(FilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    month = CharInFilter(field_name="month__month")
    year = CharInFilter(field_name="month__year")

    class Meta:
        model = NmMarketSharePotential
        fields = ()


class NmMarket4X4OutputFilter(FilterSet):
    plan_month = DateFilter(field_name="plan_month")

    class Meta:
        model = NmMarket4X4Output
        fields = ()


class PriceChangeRequestApprovalFilterset(FilterSet):
    zone = CharInFilter(field_name="zone", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")
    region = CharInFilter(field_name="region", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    BRAND_CHOICES = [
        ("shree", "Shree"),
        ("Bangur", "Bangur"),
        ("Rockstrong", "Rockstrong"),
    ]
    brand = filters.ChoiceFilter(
        field_name="brand",
        choices=BRAND_CHOICES,
    )
    status = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = PriceChangeRequestApproval
        fields = ()


class PricingProposalApprovalFilter(FilterSet):
    class Meta:
        model = PricingProposalApproval
        fields = ()
