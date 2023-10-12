"""Filter module for handling agent"""
from datetime import date as datetime_date
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db.models import F, OuterRef, Q, Subquery
from django_filters import OrderingFilter
from django_filters.rest_framework import (
    BooleanFilter,
    DateFilter,
    DateFromToRangeFilter,
    FilterSet,
)

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import (
    EpodData,
    FreightChangeInitiation,
    SidingConstraints,
    TgtDepoDispatchData,
    TgtDepoInventoryStk,
    TgtMrnData,
    TgtPlantDepoMaster,
    TgtPlantDispatchData,
    TgtPlantLookup,
    TgtPlantSiloCapacity,
    TgtRakeLoading,
    TgtRakeLoadingDetails,
    TgtRakeUnloadingDetails,
    TgtSlhOrderPendency,
    TgtSlhServiceLevelDepo,
)
from analytical_data.models.handling_agent_models import (
    RailExpensesDetails,
    RailExpensesDetailsWarfage,
    TgtDayWiseLifting,
)


class TgtMrnDataFilter(FilterSet):
    receipt_date_null = BooleanFilter(
        field_name="receipt_date", method="filter_receipt_date_null"
    )
    actual_date_null = BooleanFilter(
        field_name="actual_departure_date", method="filter_actual_date_null"
    )
    receipt_date = CharInFilter(field_name="receipt_date__date", lookup_expr="in")
    customer = CharInFilter(field_name="customer", method="filter_depo")
    month = CharInFilter(field_name="receipt_date__month", lookup_expr="in")
    year = CharInFilter(field_name="receipt_date__year", lookup_expr="in")
    actual_date = CharInFilter(
        field_name="actual_departure_date__date", lookup_expr="in"
    )
    actual_month = CharInFilter(
        field_name="actual_departure_date__month", lookup_expr="in"
    )
    actual_year = CharInFilter(
        field_name="actual_departure_date__year", lookup_expr="in"
    )

    class Meta:
        model = TgtMrnData
        fields = ()

    def filter_depo(self, queryset, name, value):
        print(value[0])
        return queryset.filter(customer__startswith=value[0]).order_by(
            self.request.query_params["sorting_on"]
        )

    def filter_receipt_date_null(self, queryset, name, value):
        return queryset.filter(receipt_date__date__isnull=value).order_by(
            self.request.query_params["sorting_on"]
        )

    def filter_actual_date_null(self, queryset, name, value):
        return queryset.filter(actual_date__isnull=value).order_by(
            self.request.query_params["sorting_on"]
        )


class TgtPlantSiloCapacityFilter(FilterSet):
    """tgt plant silo capacity filter class."""

    product = CharInFilter(field_name="product", lookup_expr="in")
    code = CharInFilter(field_name="code", lookup_expr="in")

    class Meta:
        model = TgtPlantSiloCapacity
        fields = ()


class HandlingAgentDashboardFilter(FilterSet):
    depo = CharInFilter(field_name="excise_invoice_no", method="filter_depot")

    class Meta:
        model = TgtDepoDispatchData
        fields = ()

    def filter_depot(self, queryset, name, value):
        return queryset.filter(
            excise_invoice_no__excise_invoice_no__startswith=value[0]
        )


class GodownPerformanceFilter(HandlingAgentDashboardFilter):
    month_to_date = DateFilter(
        field_name="tax_invoice_date", method="filter_month_to_date"
    )
    tax_invoice_date = CharInFilter(
        field_name="tax_invoice_date", method="filter_tax_invoice_date"
    )
    is_di_date_null = BooleanFilter(
        field_name="di_date", method="filter_is_di_date_null"
    )
    is_excise_invoice_no_null = BooleanFilter(
        field_name="excise_invoice_no", method="filter_is_excise_invoice_no_null"
    )
    product = CharInFilter(field_name="product", lookup_expr="in")

    class Meta:
        fields = ("tax_invoice_date",)

    def filter_month_to_date(self, queryset, name, value):
        return queryset.filter(
            tax_invoice_date__range=[
                value.replace(day=1),
                value,
            ]
        )

    def filter_is_di_date_null(self, queryset, name, value):
        return queryset.filter(di_date__isnull=value)

    def filter_is_excise_invoice_no_null(self, queryset, name, value):
        return queryset.filter(excise_invoice_no__isnull=value)

    def filter_tax_invoice_date(self, queryset, name, value):
        return queryset.filter(tax_invoice_date__date=value[0])


class TgtSlhOrderPendencyFilter(FilterSet):
    tax_invoice_date_isnull = BooleanFilter(
        field_name="tax_invoice_date", method="filter_tax_invoice_date_isnull"
    )
    month = CharInFilter(field_name="order_date__month", lookup_expr="in")
    year = CharInFilter(field_name="order_date__year", lookup_expr="in")
    order_date = CharInFilter(field_name="order_date__date", lookup_expr="in")

    class Meta:
        model = TgtSlhOrderPendency
        fields = (
            "auto_tagged_source",
            "tax_invoice_date",
            "delivery_due_date",
            "order_status",
        )

    def filter_tax_invoice_date_isnull(self, queryset, name, value):
        return queryset.filter(tax_invoice_date__isnull=value)


class TgtDepoInventoryStkFilter(FilterSet):
    """tgt depot inventory stk f filter class."""

    item = CharInFilter(field_name="item", lookup_expr="in")
    whse_code = CharInFilter(field_name="whse_code", lookup_expr="in")
    location = CharInFilter(field_name="location", lookup_expr="in")
    start_date = DateFilter(field_name="trans_date", lookup_expr="gte")
    end_date = DateFilter(field_name="trans_date", lookup_expr="lte")

    class Meta:
        model = TgtDepoInventoryStk
        fields = ()


class TgtPlantDepoMasterFilter(FilterSet):
    """tgt plant depot master filter"""

    district = CharInFilter(field_name="district", lookup_expr="in")
    city = CharInFilter(field_name="city", lookup_expr="in")
    party_name = CharInFilter(field_name="party_name", lookup_expr="in")
    plant = CharInFilter(field_name="party_name", method="filter_plant")

    class Meta:
        model = TgtPlantDepoMaster
        fields = ()

    def filter_plant(self, queryset, name, value):
        return queryset.filter(party_name__startswith=value[0])


class NewFreightInitiationFilter(FilterSet):
    """new freight initiations filter"""

    plant = CharInFilter(field_name="plant", lookup_expr="in")
    ship_state = CharInFilter(field_name="ship_state", lookup_expr="in")
    ship_district = CharInFilter(field_name="ship_district", lookup_expr="in")
    segment = CharInFilter(field_name="segment", lookup_expr="in")
    mode = CharInFilter(field_name="mode", lookup_expr="in")
    pack_type = CharInFilter(field_name="pack_type", lookup_expr="in")
    ship_city = CharInFilter(field_name="ship_city", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")


class TgtSlhServiceLevelDepoFilter(FilterSet):
    tax_invoice_date = CharInFilter(
        field_name="tax_invoice_date", method="filter_tax_invoice_date"
    )
    epod1_isnull = BooleanFilter(field_name="epod1_time", method="filter_epod1_isnull")
    epod2_isnull = BooleanFilter(field_name="epod2_time", method="filter_epod2_isnull")
    epod1_time = CharInFilter(field_name="epod1_time__date", lookup_expr="in")
    epod2_time = CharInFilter(field_name="epod2_time__date", lookup_expr="in")
    month = CharInFilter(field_name="epod2_time__month", lookup_expr="in")
    year = CharInFilter(field_name="epod2_time__year", lookup_expr="in")

    class Meta:
        model = TgtSlhServiceLevelDepo
        fields = ("depo", "sale_type")

    def filter_tax_invoice_date(self, queryset, name, value):
        return queryset.filter(tax_invoice_date__date=value[0])

    def filter_epod1_isnull(self, queryset, name, value):
        return queryset.filter(epod1_time__isnull=value)

    def filter_epod2_isnull(self, queryset, name, value):
        return queryset.filter(epod2_time__isnull=value)


class TgtPlantDispatchDataFilter(FilterSet):
    is_rake_loading_dtl_created = BooleanFilter(
        field_name="excise_invoice_no", method="filter_is_rake_loading_dtl_created"
    )
    plant = CharInFilter(field_name="excise_invoice_no", method="filter_plant")
    tax_invoice_date = DateFilter(
        field_name="tax_invoice_date__date", method="filter_tax_invoice_date"
    )
    truck_reach_time = BooleanFilter(
        field_name="truck_reach_time", method="truck_reach_time_null"
    )

    class Meta:
        model = TgtPlantDispatchData
        fields = (
            "mode_of_transport",
            "plant_depo",
            "tax_invoice_date",
            "di_so",
            "excise_invoice_no",
            "truck_reach_time",
        )

    def filter_tax_invoice_date(self, queryset, name, value):
        if value:
            date_filter = Q(tax_invoice_date__date=value) | Q(
                tax_invoice_date__date=value - timedelta(days=1)
            )
            return queryset.filter(date_filter)
        return queryset

    def filter_is_rake_loading_dtl_created(self, queryset, name, value):
        rld_excise_invoice_nos = TgtRakeLoadingDetails.objects.values_list(
            "excise_invoice_no", flat=True
        ).distinct()
        if value:
            return queryset.filter(excise_invoice_no__in=rld_excise_invoice_nos)
        return queryset.exclude(excise_invoice_no__in=rld_excise_invoice_nos)

    def filter_plant(self, queryset, name, value):
        return queryset.filter(excise_invoice_no__startswith=value[0])

    def truck_reach_time_null(self, queryset, name, value):
        if queryset:
            delivery_ids = queryset.values_list("delivery_id", flat=True).distinct()
            if delivery_ids:
                if value:
                    delivery_ids = (
                        EpodData.objects.filter(
                            delivery_id__in=delivery_ids, truck_reach_time__isnull=True
                        )
                        .values_list("delivery_id", flat=True)
                        .distinct()
                    )
                    return queryset.filter(delivery_id__in=delivery_ids)
                else:
                    delivery_ids = (
                        EpodData.objects.filter(
                            delivery_id__in=delivery_ids, truck_reach_time__isnull=False
                        )
                        .values_list("delivery_id", flat=True)
                        .distinct()
                    )
                    return queryset.filter(delivery_id__in=delivery_ids)
        return queryset


class TgtRakeLoadingFilter(FilterSet):
    placement_date_range_after = DateFilter(
        field_name="placement_date", method="filter_placement_date_range_after"
    )
    placement_date_range_before = DateFilter(
        field_name="placement_date", method="filter_placement_date_range_before"
    )
    siding_name = CharInFilter(field_name="siding_name", lookup_expr="in")
    siding_code = CharInFilter(field_name="siding_code", lookup_expr="in")
    dispatch_from_plant = CharInFilter(
        field_name="dispatch_from_plant", lookup_expr="in"
    )
    rake_id = CharInFilter(field_name="rake_id", lookup_expr="in")

    class Meta:
        model = TgtRakeLoading
        fields = ()

    def filter_placement_date_range_after(self, queryset, name, value):
        return queryset.filter(placement_date__date__gte=value)

    def filter_placement_date_range_before(self, queryset, name, value):
        return queryset.filter(placement_date__date__lte=value)


class TgtRakeLoadingDetailsFilter(FilterSet):
    placement_date_range_after = DateFilter(
        field_name="placement_date", method="filter_placement_date_range_after"
    )
    placement_date_range_before = DateFilter(
        field_name="placement_date", method="filter_placement_date_range_before"
    )
    rr_no = CharInFilter(field_name="rr_no", lookup_expr="in")
    siding_code = CharInFilter(field_name="siding_code", lookup_expr="in")
    siding_name = CharInFilter(field_name="siding_name", lookup_expr="in")
    rake_id = CharInFilter(field_name="rake__rake_id", lookup_expr="in")
    rake_point = CharInFilter(field_name="rake_point", lookup_expr="in")
    excise_invoice_no = CharInFilter(field_name="excise_invoice_no", lookup_expr="in")

    class Meta:
        model = TgtRakeLoadingDetails
        fields = (
            "siding_name",
            "siding_code",
            "rr_no",
            "excise_invoice_no",
            "rake__rake_id",
        )

    def filter_placement_date_range_after(self, queryset, name, value):
        return queryset.filter(rake__placement_date__date__gte=value)

    def filter_placement_date_range_before(self, queryset, name, value):
        return queryset.filter(rake__placement_date__date__lte=value)


class TgtRakeUnloadingDetailsFilter(FilterSet):
    excise_invoice_no = CharInFilter(
        field_name="rld__excise_invoice_no", lookup_expr="in"
    )
    rr_no = CharInFilter(field_name="rld__rr_no", lookup_expr="in")
    rake = CharInFilter(field_name="rld__rake__rake_id", lookup_expr="in")

    class Meta:
        model = TgtRakeUnloadingDetails
        fields = ("depo_org_id",)


class EpodDataFilter(FilterSet):
    truck_reach_time = BooleanFilter(
        field_name="truck_reach_time", method="truck_reach_time_null"
    )
    delivery_id = CharInFilter(field_name="delivery_id", lookup_expr="in")
    excise_invoice_no = CharInFilter(field_name="excise_invoice_no", lookup_expr="in")
    vehicle_no = CharInFilter(field_name="delivery_id", method="filter_vehicle_no")
    customer_name = CharInFilter(
        field_name="delivery_id", method="filter_customer_name"
    )
    consignee = CharInFilter(field_name="delivery_id", method="filter_consignee")
    ship_city = CharInFilter(field_name="delivery_id", method="filter_ship_city")
    ship_taluka = CharInFilter(field_name="delivery_id", method="filter_ship_taluka")
    ship_district = CharInFilter(
        field_name="delivery_id", method="filter_ship_district"
    )
    ship_state = CharInFilter(field_name="delivery_id", method="filter_ship_state")
    di_date = CharInFilter(field_name="di_date", lookup_expr="exact")
    order_by = OrderingFilter(fields=(("asc", "desc")))
    crm_order_number = CharInFilter(field_name="crm_order_number", lookup_expr="in")
    erp_order_number = CharInFilter(field_name="erp_order_number", lookup_expr="in")

    class Meta:
        model = EpodData
        fields = ()

    def filter_common(self, queryset, name, value, filter_field):
        end_date = datetime_date.today()
        start_date = end_date - timedelta(days=3)
        filter_kwargs = {
            filter_field: value[0],
            "tax_invoice_date__date__range": [start_date, end_date],
        }
        delivery_ids = TgtPlantDispatchData.objects.filter(**filter_kwargs).values_list(
            "delivery_id", flat=True
        )
        return queryset.filter(delivery_id__in=delivery_ids)

    def filter_vehicle_no(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "vehicle_no")

    def filter_ship_state(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "ship_state")

    def filter_ship_district(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "ship_district")

    def filter_ship_taluka(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "ship_taluka")

    def filter_ship_city(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "ship_city")

    def filter_consignee(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "consignee")

    def filter_customer_name(self, queryset, name, value):
        return self.filter_common(queryset, name, value, "customer_name")

    def truck_reach_time_null(self, queryset, name, value):
        if value:
            return queryset.filter(truck_reach_time__isnull=True)
        else:
            return queryset.filter(truck_reach_time__isnull=False)

    def order_di_date(self, queryset, value):
        if not value:
            raise ValidationError("The 'order_by' parameter is required")

        if value.lower() == "asc":
            subquery = TgtPlantDispatchData.objects.filter(
                delivery_id=OuterRef("delivery_id")
            ).values("di_date")[:1]

            queryset = queryset.annotate(tgt_di_date=Subquery(subquery)).order_by(
                "tgt_di_date"
            )
        elif value.lower() == "desc":
            subquery = TgtPlantDispatchData.objects.filter(
                delivery_id=OuterRef("delivery_id")
            ).values("di_date")[:1]

            queryset = queryset.annotate(tgt_di_date=Subquery(subquery)).order_by(
                "-tgt_di_date"
            )
        else:
            raise ValidationError("Use 'asc' or 'desc'.")

        return queryset


class FreightChangeInitiationFilter(FilterSet):
    start_date = DateFilter(field_name="creation_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="creation_date__date", lookup_expr="lte")

    class Meta:
        model = FreightChangeInitiation
        fields = (
            "plant",
            "ship_city",
            "ship_state",
            "ship_district",
            "mode",
            "segment",
            "pack_type",
            "status",
            "persona",
            "approved_by",
        )


class TgtPlantLookupFilter(FilterSet):
    exclude_org_startswith = CharInFilter(
        field_name="org", method="filter_excluded_org"
    )
    org_startswith = CharInFilter(field_name="org", method="filter_org_startswith")

    class Meta:
        model = TgtPlantLookup
        fields = ("org",)

    def filter_excluded_org(self, queryset, name, value):
        query = Q()
        for val in value:
            query = query | Q(org__startswith=val)
        return queryset.exclude(query)

    def filter_org_startswith(self, queryset, name, value):
        query = Q()
        for val in value:
            query = query | Q(org__startswith=val)
        return queryset.filter(query)


class TgtDayWiseLiftingFilter(FilterSet):
    rk_unload = CharInFilter(field_name="rk_unload", lookup_expr="in")

    class Meta:
        model = TgtDayWiseLifting
        fields = "__all__"


class RailExpensesDetailsWfFilterset(FilterSet):
    rake_id = CharInFilter(field_name="rake_id", lookup_expr="in")

    class Meta:
        model = RailExpensesDetailsWarfage
        fields = "__all__"


class TgtPlantDispatchDataFilternew(FilterSet):
    is_rake_loading_dtl_created = BooleanFilter(
        field_name="excise_invoice_no", method="filter_is_rake_loading_dtl_created"
    )
    plant = CharInFilter(field_name="excise_invoice_no", method="filter_plant")
    # tax_invoice_date = CharInFilter(
    #     field_name="tax_invoice_date", method="filter_tax_invoice_date"
    # )
    tax_invoice_date = DateFilter(field_name="tax_invoice_date__date")
    truck_reach_time = BooleanFilter(
        field_name="truck_reach_time", method="truck_reach_time_null"
    )

    class Meta:
        model = TgtPlantDispatchData
        fields = (
            "mode_of_transport",
            "plant_depo",
            "tax_invoice_date",
            "di_so",
            "excise_invoice_no",
            "truck_reach_time",
        )

    def filter_is_rake_loading_dtl_created(self, queryset, name, value):
        rld_excise_invoice_nos = TgtRakeLoadingDetails.objects.values_list(
            "excise_invoice_no", flat=True
        ).distinct()
        if value:
            return queryset.filter(excise_invoice_no__in=rld_excise_invoice_nos)
        return queryset.exclude(excise_invoice_no__in=rld_excise_invoice_nos)

    def filter_plant(self, queryset, name, value):
        return queryset.filter(excise_invoice_no__startswith=value[0])

    # def filter_tax_invoice_date(self, queryset, name, value):
    #     end_date = datetime.strptime(value[0], "%Y-%m-%d").date()
    #     start_date = end_date - timedelta(days=3)
    #     return queryset.filter(tax_invoice_date__date__range=[start_date, end_date])

    def truck_reach_time_null(self, queryset, name, value):
        if queryset:
            delivery_ids = queryset.values_list("delivery_id", flat=True).distinct()
            if delivery_ids:
                if value:
                    delivery_ids = (
                        EpodData.objects.filter(
                            delivery_id__in=delivery_ids, truck_reach_time__isnull=True
                        )
                        .values_list("delivery_id", flat=True)
                        .distinct()
                    )
                    return queryset.filter(delivery_id__in=delivery_ids)
                else:
                    delivery_ids = (
                        EpodData.objects.filter(
                            delivery_id__in=delivery_ids, truck_reach_time__isnull=False
                        )
                        .values_list("delivery_id", flat=True)
                        .distinct()
                    )
                    return queryset.filter(delivery_id__in=delivery_ids)
        return queryset


class RailExpensesDetailsFilterset(FilterSet):
    rake_id = CharInFilter(field_name="rake_id", lookup_expr="in")

    class Meta:
        model = RailExpensesDetails
        fields = "__all__"


class SidingConstraintsFilterset(FilterSet):
    rake_id = CharInFilter(field_name="rake_id", lookup_expr="in")

    class Meta:
        model = SidingConstraints
        fields = "__all__"
