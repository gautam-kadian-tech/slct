"""Helper module for LP Model output screen."""
from io import BytesIO

import pandas as pd
from django.db.models import Avg, Count, DecimalField, F, Func, Q, Sum
from django.db.models.functions.comparison import NullIf

from analytical_data.models import Demand, LpModelRun


class LpModelOutputScreenViewHelper:
    """Helper class for FreightBasedQuantity view."""

    @classmethod
    def get_road_vs_rake_data(cls, filtered_data, total_qty):
        """
        Returns Road Vs Rake comparison data in percentage and total quantity.

        Args:
            filtered_data (QuerySet): Filtered data of LP Model.
            total_qty (int): Sum total of quantity in LpModelDfFnl.

        Returns:
            dict: Dictionary containing key value pairs of road and
                  rake data.
        """
        road_data = cls.get_total_and_percentage_quantity(
            Q(mode="ROAD"), filtered_data, total_qty
        )
        rake_data = cls.get_total_and_percentage_quantity(
            Q(mode="RAIL"), filtered_data, total_qty
        )
        data = {"road_data": road_data, "rake_data": rake_data}
        return data

    @classmethod
    def get_freight_based_quantity(cls, filtered_data, total_qty):
        """Returns freight based quantity share in database.

        Args:
            filtered_data (QuerySet): Filtered data of LP Model.
            total_qty (int): Sum total of quantity in LpModelDfFnl.

        Returns:
            dict: Dictionary containing key value pairs of freight
                  based quantity data share.
        """
        godown_transfer = cls.get_total_and_percentage_quantity(
            Q(freight_type="GD"), filtered_data, total_qty
        )
        rake_transfer = cls.get_total_and_percentage_quantity(
            Q(freight_type="RK"), filtered_data, total_qty
        )
        road_diversion = cls.get_total_and_percentage_quantity(
            Q(freight_type="RD"), filtered_data, total_qty
        )
        trans_shipment = cls.get_total_and_percentage_quantity(
            Q(freight_type="TP"), filtered_data, total_qty
        )

        data = {
            "godown_transfer": godown_transfer,
            "rake_transfer": rake_transfer,
            "road_diversion": road_diversion,
            "trans_shipment": trans_shipment,
        }
        return data

    @classmethod
    def get_dispatches_data(cls, filtered_data, total_qty):
        """Returns quantity data based on primary_secondary_route share
           in database.

        Args:
            filtered_data (QuerySet): Filtered data of LP Model.
            total_qty (int): Sum total of quantity in LpModelDfFnl.

        Returns:
            dict: Dictionary containing key value pairs of quantity
                  share based on dispatches.
        """
        direct_dispatch = cls.get_total_and_percentage_quantity(
            Q(primary_secondary_route="PRIMARY"), filtered_data, total_qty
        )
        indirect_dispatch = cls.get_total_and_percentage_quantity(
            Q(primary_secondary_route="SECONDARY"), filtered_data, total_qty
        )
        data = {
            "direct_dispatch": direct_dispatch,
            "indirect_dispatch": indirect_dispatch,
        }
        return data

    @classmethod
    def get_tlc_breakup_data(cls, view):
        """
        Calculates TLC Breakup data share of filtered data in percentage
        and total amount.

        Args:
            view (TLCBreakupView): Function calling view class.

        Returns:
            dict: Data containing key, value pairs representing data of
                  each field.
        """
        queryset = view.get_queryset()
        filtered_data = view.filter_queryset(queryset)
        total_data = queryset.aggregate(
            Sum("primary_frt"),
            Sum("rake_charges"),
            Sum("secondary_frt"),
            Sum("demurrage"),
            Sum("ha_commission"),
            Sum("misc_charges"),
        )

        total_quantity = filtered_data.aggregate(Sum("qty"))

        plan_month = LpModelRun.objects.filter(run_id=view.kwargs.get("run_id")).values(
            "plan_date"
        )
        demand_qty = Demand.objects.filter(month__in=plan_month).aggregate(
            Sum("demand_qty")
        )

        return {
            "primary_freight": cls.get_primary_freight_data(
                filtered_data, total_quantity
            ),
            "rake_charges": cls.get_rake_charges_data(filtered_data),
            "secondary_freight": cls.get_secondary_freight_data(
                filtered_data, total_quantity
            ),
            "demurrage": cls.get_demurrage_data(filtered_data),
            "handling_charges": cls.get_handling_charges_data(
                filtered_data, total_data, total_quantity
            ),
            "other_charges": cls.get_other_charges_data(filtered_data, total_quantity),
            "total_logistics_cost": cls.get_total_logistics_cost_data(
                filtered_data, total_quantity
            ),
            "total_contributions": cls.get_total_contribution(
                filtered_data, total_quantity
            ),
            "scenario": queryset.values("scenario").first().get("scenario"),
            "total_quantity": total_quantity.get("qty__sum"),
            "dispatch_plan_quantity": total_quantity.get("qty__sum"),
            "demand_sum": demand_qty.get("demand_qty__sum"),
        }

    @classmethod
    def get_total_contribution(cls, filtered_data, total_quantity):
        total_contribution = filtered_data.aggregate(
            quantity=Sum(F("contribution") * F("qty"))
        )
        try:
            total_contribution.update(
                {
                    "per_ton": total_contribution.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except:
            total_contribution.update({"per_ton": 0})
        return total_contribution

    @classmethod
    def get_total_logistics_cost_data(cls, filtered_data, total_quantity):
        total_logistics_cost = filtered_data.aggregate(quantity=Sum("tlc"))
        try:
            total_logistics_cost.update(
                {
                    "per_ton": total_logistics_cost.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except Exception:
            total_logistics_cost.update({"per_ton": 0})

        return total_logistics_cost

    @classmethod
    def get_other_charges_data(cls, filtered_data, total_quantity):
        other_charges_data = filtered_data.aggregate(
            quantity=Sum(F("misc_charges") * F("qty")),
        )
        try:
            other_charges_data.update(
                {
                    "per_ton": other_charges_data.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except Exception:
            other_charges_data.update({"per_ton": 0})

        return other_charges_data

    @classmethod
    def get_handling_charges_data(cls, filtered_data, total_data, total_quantity):
        handling_charges_data = filtered_data.aggregate(
            percentage=cls.get_percentage(
                "ha_commission", total_data.get("ha_commission__sum")
            ),
            quantity=Sum(F("ha_commission") * F("qty")),
        )
        try:
            handling_charges_data.update(
                {
                    "per_ton": handling_charges_data.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except Exception:
            handling_charges_data.update({"per_ton": 0})

        return handling_charges_data

    @classmethod
    def get_demurrage_data(cls, filtered_data):
        demurrage_data = filtered_data.aggregate(
            quantity=Sum(F("demurrage") * F("qty")),
        )
        demurrage_filtered_total_qty = (
            filtered_data.filter(demurrage__gt=0).aggregate(Sum("qty")).get("qty__sum")
        )
        try:
            demurrage_data.update(
                {"per_ton": demurrage_data["quantity"] / demurrage_filtered_total_qty}
            )
        except Exception:
            demurrage_data.update({"per_ton": 0})

        return demurrage_data

    @classmethod
    def get_secondary_freight_data(cls, filtered_data, total_quantity):
        secondary_freight_data = filtered_data.aggregate(
            quantity=Sum(F("secondary_frt") * F("qty")),
        )
        try:
            secondary_freight_data.update(
                {
                    "per_ton": secondary_freight_data.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except Exception:
            secondary_freight_data.update({"per_ton": 0})

        return secondary_freight_data

    @classmethod
    def get_rake_charges_data(cls, filtered_data):
        rake_charges_data = filtered_data.aggregate(
            quantity=Sum(F("rake_charges") * F("qty"))
        )
        rake_filtered_total_qty = filtered_data.aggregate(Sum("qty")).get("qty__sum")
        try:
            rake_charges_data.update(
                {"per_ton": rake_charges_data.get("quantity") / rake_filtered_total_qty}
            )
        except Exception:
            rake_charges_data.update({"per_ton": 0})

        return rake_charges_data

    @classmethod
    def get_primary_freight_data(cls, filtered_data, total_quantity):
        primary_freight_data = filtered_data.aggregate(
            quantity=Sum(F("primary_frt") * F("qty"))
        )
        try:
            primary_freight_data.update(
                {
                    "per_ton": primary_freight_data.get("quantity")
                    / total_quantity.get("qty__sum")
                }
            )
        except Exception as e:
            primary_freight_data.update({"per_ton": 0})

        return primary_freight_data

    @classmethod
    def get_total_and_percentage_quantity(cls, query, filtered_data, total_qty):
        """Calculates percentage and total amount of filtered data share
           in database.

        Args:
            query (Q): Django Q object against which data will be
                       filtered.
            filtered_data (QuerySet): Filtered data of LP Model.
            total_qty (int): Sum total of quantity.

        Returns:
            dict: key, value pairs representing percentage and total
                  amount.
        """
        return filtered_data.filter(query).aggregate(
            percentage=cls.get_percentage("qty", total_qty),
            quantity=Sum("qty", default=0),
        )

    @classmethod
    def get_percentage(cls, percent_param, total):
        """Calculated percentage and round it off to 2 decimal digits.

        Args:
            percent_param (str): Field of which percentage will be calculated.
            total (int): Total amount of the percent_param field.

        Returns:
            int: Percentage
        """
        if total == 0:
            return Avg(0, output_field=DecimalField())
        return Func(
            Sum(percent_param) / total,
            2,
            function="ROUND",
            arity=2,
            output_field=DecimalField(),
        )

    @classmethod
    def get_plant_dispatch_data(cls, dispatch_data):
        """Get plant dispatch plan data.

        Args:
            dispatch_data (QuerySet): filtered data

        Returns:
            Queryset: List of dicts containing plant dispatch plan data.
        """
        return dispatch_data.values(
            "plant_id", "grade", "plant_products_master__quantity"
        ).annotate(
            Count("plant_id"),
            Count("grade"),
            Sum("qty"),
            capacity=F("plant_products_master__quantity"),
            utilization=Sum("qty") / (F("plant_products_master__quantity") * 100000),
        )

    # @classmethod
    # def get_clinker_allocation_data(self, queryset):
    #     """Get clinker allocation data for output screen.

    #     Args:
    #         queryset (QuerySet): queryset to perform operations.

    #     Returns:
    #         QuerySet: clinker allocation data.
    #     """
    #     return (
    #         queryset.annotate(
    #             quantity_lf=Func(
    #                 F("qty") / NullIf(F("clinker_cf"), 0),
    #                 2,
    #                 function="ROUND",
    #                 arity=2,
    #                 output_field=DecimalField(),
    #             )
    #         )
    #         .values("plant_id", "clinker_plant")
    #         .annotate(
    #             Count("plant_id"),
    #             Count("clinker_plant"),
    #             quantity_lf=Sum("quantity_lf"),
    #             quantity=Sum("qty"),
    #         )
    #     )
