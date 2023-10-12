"""NtNcrThreshold views helper."""
from django.db.models import Avg, Count, Q, Sum

from analytical_data.models import (
    SclHierarchyMaster,
    TOebsSclArNcrAdvanceCalcTab,
)


class NtNcrThresholdHelper:
    """NtNcrThreshold view helper class."""

    @classmethod
    def _get_monthly_ncr_sales(cls, queryset):
        """Get month wise sales data.

        Returns:
            queryset: data contains monthly average ncr_threshold.
        """
        return queryset.values(
            "creation_date__month",
        ).annotate(
            Count("creation_date__month"),
            average_ncr=Avg("ncr"),
            monthly_sales=Sum("quantity_invoiced"),
        )

    @classmethod
    def __get_scl_hierarchy_master_query(cls, query, query_string):
        return (
            SclHierarchyMaster.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    @classmethod
    def __get_advance_calc_tab(cls, query_string, query=Q()):
        return (
            TOebsSclArNcrAdvanceCalcTab.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    @classmethod
    def _get_credit_limit_setting_dropdown(cls):
        return {
            "products": TOebsSclArNcrAdvanceCalcTab.objects.exclude(
                Q(product__exact=" ") | Q(product__startswith="AAC")
            )
            .values_list("product", flat=True)
            .annotate(Count("product")),
            "valid_for": [3, 7],
            "state": cls.__get_scl_hierarchy_master_query(
                Q(state_erp__isnull=False), "state_erp"
            ),
            "key": cls.__get_advance_calc_tab("key", Q(key__isnull=False)),
            "month": cls.__get_advance_calc_tab("creation_date__month"),
        }

    @classmethod
    def _get_credit_limit_setting_district_dropdown(cls, query_params):
        return cls.__get_scl_hierarchy_master_query(
            Q(district_erp__isnull=False, state_erp=query_params.get("state_erp")),
            "district_erp",
        )

    @classmethod
    def _get_credit_limit_setting_city_dropdown(cls, query_params):
        return cls.__get_scl_hierarchy_master_query(
            Q(
                city_erp__isnull=False,
                state_erp=query_params.get("state_erp"),
                district_erp=query_params.get("district_erp"),
            ),
            "city_erp",
        )
