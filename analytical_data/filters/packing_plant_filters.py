"""Filter modules for Packing Plant Model"""
from django.db.models import Q
from django_filters.rest_framework import BooleanFilter, DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.packing_plant_models import (
    L1SourceMapping,
    LpSchedulingDpc,
    MvPendingReasonsForDelay,
    PackerShiftLevelStoppages,
    PlantDepoSlaNew,
    PpOrderTagging,
    ShiftwiseAdhocQty,
    TOebsSclRouteMaster,
)


class LpSchedulingDpcFilter(FilterSet):
    """Lp Scheduling Dpc filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    ship_state = CharInFilter(field_name="ship_state", lookup_expr="in")
    ship_district = CharInFilter(field_name="ship_district", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")

    class Meta:
        model = LpSchedulingDpc
        fields = ()


class PlantDepoSlaNewFilter(FilterSet):
    """Plant depo sla new filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        model = PlantDepoSlaNew
        fields = ()


class ShiftWiseAdhocQtyFilter(FilterSet):
    """SHIFTWISE ADHOC QTY filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    shift = CharInFilter(field_name="shift", lookup_expr="in")
    date = DateFilter(field_name="date")

    class Meta:
        model = ShiftwiseAdhocQty
        fields = ()


class MvPendingReasonsForDelayFilter(FilterSet):
    """MvPendingReasonsForDelay filter class."""

    plant = CharInFilter(field_name="plant", method="filter_plant")
    reasons_for_delay = CharInFilter(
        field_name="reasons_for_delay", method="filter_reason_for_delay"
    )
    source_line_id = CharInFilter(field_name="source_line_id", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    packing_type = CharInFilter(field_name="packing_type", lookup_expr="in")
    segment = CharInFilter(field_name="segment", lookup_expr="in")
    ship_to_state = CharInFilter(field_name="ship_to_state", lookup_expr="in")
    ship_to_district = CharInFilter(field_name="ship_to_district", lookup_expr="in")
    ship_to_city = CharInFilter(field_name="ship_to_city", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    delivery_id = CharInFilter(field_name="delivery_id", lookup_expr="in")
    date = DateFilter(field_name="order_line_creation_date__date")

    def filter_plant(self, queryset, name, value):
        return queryset.filter(plant__startswith=value[0])

    def filter_reason_for_delay(self, queryset, name, value):
        if value[0] == "Yes":
            return queryset.filter(reasons_for_delay__isnull=False)
        elif value[0] == "No":
            return queryset.filter(reasons_for_delay__isnull=True)

    class Meta:
        model = MvPendingReasonsForDelay
        fields = ()


class PpOrderTaggingFilter(FilterSet):
    """Packing plant output filterset class."""

    delivery_id = CharInFilter(
        field_name="order_master_id__delivery_id", lookup_expr="in"
    )
    token_id = CharInFilter(field_name="order_master_id__token_id", lookup_expr="in")
    order_line_id = CharInFilter(
        field_name="order_master_id__order_line_id", lookup_expr="in"
    )
    brand = CharInFilter(field_name="order_master_id__brand", lookup_expr="in")
    order_quantity = CharInFilter(
        field_name="order_master_id__order_quantity", lookup_expr="in"
    )
    pack_type = CharInFilter(field_name="order_master_id__pack_type", lookup_expr="in")
    auto_tagged_mode = CharInFilter(
        field_name="order_master_id__auto_tagged_mode", lookup_expr="in"
    )
    # priority = CharInFilter(method="filter_priority")

    class Meta:
        model = PpOrderTagging
        fields = (
            "tl_code",
            "packer_code",
        )

    # def filter_priority(self, queryset, field_name, value):
    #     pass


class PackerShiftLevelStoppagesFilter(FilterSet):
    """packer shift level stoppage filter class."""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    shift = CharInFilter(field_name="shift", lookup_expr="in")
    date = DateFilter(field_name="date")

    class Meta:
        model = PackerShiftLevelStoppages
        fields = ()


class TOebsSclRouteMasterFilter(FilterSet):
    """packer shift level stoppage filter class."""

    route_id = CharInFilter(field_name="route_id", lookup_expr="in")
    active_flag = CharInFilter(field_name="active_flag", lookup_expr="in")
    mode_of_transport = CharInFilter(field_name="mode_of_transport", lookup_expr="in")
    is_route_id_starts_with = BooleanFilter(
        field_name="route_id", method="filter_route_id"
    )

    class Meta:
        model = TOebsSclRouteMaster
        fields = ()

    def filter_route_id(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(whse__startswith="FC")
                | Q(whse__startswith="RM")
                | Q(whse__startswith="FG")
            )


class L1SourceMappingFilter(FilterSet):
    """packer shift level stoppage filter class."""

    route_id = CharInFilter(field_name="route_id", lookup_expr="in")
    grade = CharInFilter(field_name="grade", lookup_expr="in")
    brand = CharInFilter(field_name="brand", lookup_expr="in")

    class Meta:
        model = L1SourceMapping
        fields = ()
