import json

import numpy_financial as npf
import requests
from django.conf import settings
from django.db import IntegrityError
from django.db.models import (
    Avg,
    DecimalField,
    ExpressionWrapper,
    F,
    IntegerField,
    Sum,
    Value,
    functions,
)
from django.db.models.functions import Coalesce
from rest_framework import serializers, status

from analytical_data.enum_classes import (
    ApprovalStatusChoices,
    BrandChoices,
    BrandChoices1,
    InventoryItemIdChoices,
    LpModelDfFnlBrandChoices,
)
from analytical_data.models import (
    ApprovalThreshold,
    CrwcChargesMaster,
    DemurrageSlabs,
    DepoWiseFreightMaster,
    EpodData,
    FdAnnualCharges,
    FdCapexComputations,
    FdCostProfile,
    FdDirectCostComputations,
    FdFinancialFeasibilityCheck,
    FdFixedCostComputations,
    FdFuelCharges,
    FdLocationOverview,
    FdMonthlyCharges,
    FdOtherVariableCharges,
    FdPrimaryAssumptions,
    FdProfitabilitySettings,
    FdPurchaseInputs,
    FdSemiVariableCostComputations,
    FdTyreCharges,
    FreightChangeInitiation,
    FreightDiscoveryProfiles,
    GdWharfageOutput,
    GdWharfageRunInput,
    HandlingMasters,
    HourlyLiftingEfficiency,
    HourlyLiftingEfficiencyMaster,
    LiftingPattern,
    NewFreightInitiation,
    RailExpensesDetails,
    RailExpensesDetailsWarfage,
    RailHeadToGodownShiftingCartageCosts,
    ReasonsForDemurrageWharfage,
    RoadHandlingMaster,
    SidingConstraints,
    SidingWiseLiasioningAgent,
    TgtDayWiseLifting,
    TgtDepoInventoryStk,
    TgtMrnData,
    TgtPlantDispatchData,
    TgtPlantSiloCapacity,
    TgtRakeCharges,
    TgtRakeDisposals,
    TgtRakeLoading,
    TgtRakeLoadingDetails,
    TgtRakeUnloadingDetails,
    TgtSlhOrderPendency,
    TgtSlhServiceLevelDepo,
    TOebsSclRouteMaster,
    TOebsWshNewDeliveries,
    WaiverCommissionMaster,
    WharfageSlabs,
)
from analytical_data.serializers import (
    BulkCreateListSerializer,
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkUpdateListSerializer,
    OptionChoiceField,
)
from analytical_data.serializers.custom_serializers import (
    BulkUpdateOrCreateListSerializer,
)
from Master_Data_Logistics.models import SidingCodeMapping

# from datetime import timedelta, timezone, datetime
# from decimal import Decimal


class TgtPlantSiloCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtPlantSiloCapacity
        fields = "__all__"


class TgtMrnDataSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = TgtMrnData
        fields = "__all__"

    def get_status(self, obj):
        if obj.receipt_number:
            return "MRN Received"
        # elif obj.excise_invoice_date is None and obj.delivery_id :
        elif obj.receipt_date is None and obj.actual_departure_date:
            return "Ready to Ship"
        elif obj.receipt_number == None and obj.excise_invoice_date:
            return "MRN Pending"


class TgtPlantDispatchDataSerializer(serializers.ModelSerializer):
    rr_no = serializers.SerializerMethodField()
    rake_point_code = serializers.SerializerMethodField()

    class Meta:
        model = TgtPlantDispatchData
        fields = "__all__"

    def get_rr_no(self, obj):
        return getattr(obj.delivery_id, "attribute2", "")

    def get_rake_point_code(self, obj):
        siding_obj = SidingCodeMapping.objects.filter(rake_point=obj.rake_point)
        if siding_obj:
            siding_obj = siding_obj.first()
            rake_point_code = siding_obj.rake_point_code
            return rake_point_code
        return None


class AutoGenerateFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = (
            "id",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )

    def create(self, validated_data):
        self.auto_generate_fields(validated_data)
        validated_data["created_by"] = validated_data["last_updated_by"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.auto_generate_fields(validated_data)
        return super().update(instance, validated_data)

    def auto_generate_fields(self, validated_data):
        user = self.context.get("request").user
        validated_data.update(
            {"last_updated_by": user.id, "last_update_login": user.id}
        )


class PrimaryAssumptionsSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdPrimaryAssumptions
        read_only_fields = (
            "loaded_km_run_per_trip",
            "loaded_km_run_per_month",
        )


class PurchaseInputsSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdPurchaseInputs


class ProfitabilitySettingSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdProfitabilitySettings
        read_only_fields = (
            "monthly_operating_cost",
            "profit_margin_percentage",
        )


class TyreChangesSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdTyreCharges


class FuelChargesSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdFuelCharges


class OtherVariableChargesSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdOtherVariableCharges


class AnnualChargesSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdAnnualCharges


class MonthlyChargesSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdMonthlyCharges


class SemiVariableCostComputationSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdSemiVariableCostComputations
        read_only_fields = (
            "loading_unloading_per_trip",
            "loading_unloading_per_month",
            "handling_cost_per_trip",
            "handling_cost_per_month",
            "route_expenses",
            "toll",
            "other_variable_cost_per_km",
            "other_variable_cost_per_month",
            "semi_variable_cost_per_month",
        )


class CostProfileSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdCostProfile
        read_only_fields = (
            "direct_ptpk",
            "semi_variable_ptpk",
            "fixed_ptpk",
            "profit_ptpk",
            "total_ptpk",
            "freight_per_tonne",
        )


class CapexComputations(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdCapexComputations
        read_only_fields = (
            "capacity",
            "cost_of_truck",
            "residual_value_of_truck",
            "loan_amount",
            "amount_paid_by_self",
            "current_value_of_truck",
            "depreciation_per_month",
            "interest_cost_per_month",
        )


class FinancialFeasibilityCheck(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdFinancialFeasibilityCheck
        read_only_fields = (
            "emi",
            "cash_inflow",
            "cash_flow_per_month",
            "irr",
        )


class DirectCostComputations(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdDirectCostComputations
        read_only_fields = (
            "tyre_cost_per_km",
            "net_mileage",
            "diesel_cost_per_km",
            "fuel_tyre_cost",
            "running_cost_per_month",
        )


class FixedCostComputation(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdFixedCostComputations
        read_only_fields = (
            "road_permit_per_month",
            "road_tax_per_month",
            "depreciation_per_month",
            "interest_cost_per_month",
            "insurance_per_month",
            "working_capital_interest_cost_per_month",
            "other_fixed_costs",
            "total_fixed_cost_per_month",
        )


class LocationOverviewSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FdLocationOverview


class RoadRakeCoordinatorSerializer(AutoGenerateFieldsSerializer):
    origin = LocationOverviewSerializer()
    destination = LocationOverviewSerializer()
    cost_profile = CostProfileSerializer(read_only=True)
    primary_assumptions = PrimaryAssumptionsSerializer()
    purchase_inputs = PurchaseInputsSerializer()
    capex_computations = CapexComputations(read_only=True)
    profitability_settings = ProfitabilitySettingSerializer()
    financial_feasibility_check = FinancialFeasibilityCheck(read_only=True)
    tyre_charges = TyreChangesSerializer()
    fuel_charges = FuelChargesSerializer()
    direct_cost_computations = DirectCostComputations(read_only=True)
    other_variable_charges = OtherVariableChargesSerializer()
    semi_variable_cost_computations = SemiVariableCostComputationSerializer()
    annual_charges = AnnualChargesSerializer()
    monthly_charges = MonthlyChargesSerializer()
    fixed_cost_computations = FixedCostComputation(read_only=True)

    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = FreightDiscoveryProfiles

    def validate(self, attrs):
        primary_assumptions = attrs.get("primary_assumptions")
        fuel_charges = attrs.get("fuel_charges")
        tyre_charges = attrs.get("tyre_charges")
        other_variable_charges = attrs.get("other_variable_charges")
        semi_variable_cost_computations = attrs.get("semi_variable_cost_computations")
        annual_charges = attrs.get("annual_charges")
        purchase_inputs = attrs.get("purchase_inputs")
        profitability_settings = attrs.get("profitability_settings")
        monthly_charges = attrs.get("monthly_charges")

        loaded_km_run_per_trip = (primary_assumptions["round_trip_distance"] / 2) * (
            1 + primary_assumptions["backhauling_percentage"] / 100
        )
        loaded_km_run_per_month = (
            loaded_km_run_per_trip * primary_assumptions["no_of_trips_per_month"]
        )

        tyre_cost_per_km = (
            primary_assumptions["no_of_tyres"]
            * (tyre_charges["tyre_cost"] + tyre_charges["tyre_cost_retredded"])
            / (tyre_charges["tyre_life"] + tyre_charges["tyre_life_retredded"])
        )
        net_mileage = (
            fuel_charges["mileage_with_load"]
            + (
                fuel_charges["mileage_with_load"]
                * (primary_assumptions["backhauling_percentage"] / 100)
            )
            + (
                (1 - primary_assumptions["backhauling_percentage"] / 100)
                * fuel_charges["mileage_without_load"]
            )
        ) / 2
        diesel_cost_per_km = fuel_charges["diesel_cost"] / net_mileage
        fuel_tyre_cost = (
            (tyre_cost_per_km + diesel_cost_per_km)
            * (
                primary_assumptions["round_trip_distance"]
                * primary_assumptions["no_of_trips_per_month"]
            )
            / loaded_km_run_per_month
        )
        running_cost_per_month = fuel_tyre_cost * loaded_km_run_per_month

        direct_cost_computation_data = {
            "tyre_cost_per_km": tyre_cost_per_km,
            "net_mileage": net_mileage,
            "diesel_cost_per_km": diesel_cost_per_km,
            "fuel_tyre_cost": fuel_tyre_cost,
            "running_cost_per_month": running_cost_per_month,
        }

        loading_unloading_per_trip = (
            other_variable_charges["loading_charges_per_mt"]
            + other_variable_charges["unloading_charges_per_mt"]
        )
        loading_unloading_per_month = (
            loading_unloading_per_trip
            * primary_assumptions["capacity"]
            * (1 + primary_assumptions["backhauling_percentage"] / 100)
        )
        handling_cost_per_trip = (
            loading_unloading_per_month
            + semi_variable_cost_computations["tarpaulin_charges_per_trip"]
        )
        handling_cost_per_month = (
            handling_cost_per_trip * primary_assumptions["no_of_trips_per_month"]
        )
        route_expenses = (
            other_variable_charges["route_expenses"] / loaded_km_run_per_trip
        )
        toll = other_variable_charges["toll"] / loaded_km_run_per_trip
        other_variable_cost_per_km = route_expenses + toll
        other_variable_cost_per_month = (
            other_variable_cost_per_km * loaded_km_run_per_month
        )
        semi_variable_cost_per_month = (
            other_variable_cost_per_month + handling_cost_per_month
        )

        semi_variable_cost_computations.update(
            {
                "loading_unloading_per_trip": loading_unloading_per_trip,
                "loading_unloading_per_month": loading_unloading_per_month,
                "handling_cost_per_trip": handling_cost_per_trip,
                "handling_cost_per_month": handling_cost_per_month,
                "route_expenses": route_expenses,
                "toll": toll,
                "other_variable_cost_per_km": other_variable_cost_per_km,
                "other_variable_cost_per_month": other_variable_cost_per_month,
                "semi_variable_cost_per_month": semi_variable_cost_per_month,
            }
        )

        cost_of_truck = purchase_inputs["cost_of_truck"]
        residual_value_of_truck = (
            purchase_inputs["residual_value_of_truck_at_end_of_emi"] / 100
        ) * cost_of_truck
        loan_amount = (purchase_inputs["loan_amoount_percentage"] / 100) * cost_of_truck
        amount_paid_by_self = cost_of_truck - loan_amount
        current_value_of_truck = cost_of_truck - (
            (
                (cost_of_truck - residual_value_of_truck)
                / purchase_inputs["no_of_years_emi"]
            )
            * primary_assumptions["age_of_truck"]
        )
        depreciation_per_month = (
            (cost_of_truck - residual_value_of_truck)
            / purchase_inputs["no_of_years_emi"]
        ) / 12
        interest_cost_per_month = (
            (purchase_inputs["flat_rate_of_interest_percentage"] / 100) * loan_amount
        ) / 12
        emi = npf.pmt(
            (purchase_inputs["emi_rate_of_interest_percentage"] / 100) / 12,
            purchase_inputs["no_of_years_emi"] * 12,
            loan_amount,
            0,
            0,
        )
        profit_margin = profitability_settings["profit_margin"]
        cash_inflow = depreciation_per_month + interest_cost_per_month + profit_margin
        cash_flow_per_month = cash_inflow + emi

        fixed_cost_computation_data = {
            "road_permit_per_month": annual_charges["road_permit_pa"] / 12,
            "road_tax_per_month": annual_charges["road_tax_pa"] / 12,
            "depreciation_per_month": depreciation_per_month,
            "interest_cost_per_month": interest_cost_per_month,
            "insurance_per_month": (
                current_value_of_truck
                * (purchase_inputs["insurance_as_percentage_of_vehicle_cost"] / 100)
            )
            / 12,
            "working_capital_interest_cost_per_month": max(
                0,
                -(
                    cash_flow_per_month
                    * purchase_inputs["interest_rate_on_working_capital"]
                )
                / 12,
            ),
            "other_fixed_costs": sum(monthly_charges.values()),
        }
        total_fixed_cost_per_month = sum(
            [value for value in fixed_cost_computation_data.values()]
        )
        fixed_cost_computation_data.update(
            {
                "total_fixed_cost_per_month": total_fixed_cost_per_month,
            }
        )

        capex_computations_data = {
            "capacity": primary_assumptions["capacity"],
            "cost_of_truck": cost_of_truck,
            "residual_value_of_truck": residual_value_of_truck,
            "loan_amount": loan_amount,
            "amount_paid_by_self": amount_paid_by_self,
            "current_value_of_truck": current_value_of_truck,
            "depreciation_per_month": depreciation_per_month,
            "interest_cost_per_month": interest_cost_per_month,
        }

        monthly_operating_cost = (
            total_fixed_cost_per_month
            + semi_variable_cost_per_month
            + running_cost_per_month
        )
        profitability_settings.update(
            {
                "monthly_operating_cost": round(monthly_operating_cost, 2),
                "profit_margin_percentage": round(
                    profit_margin / (monthly_operating_cost + profit_margin), 2
                ),
            }
        )

        financial_feasibility_check_data = {
            "emi": emi,
            "cash_inflow": cash_inflow,
            "cash_flow_per_month": cash_flow_per_month,
            "irr": npf.rate(
                purchase_inputs["no_of_years_emi"] * 12,
                cash_flow_per_month,
                -amount_paid_by_self,
                residual_value_of_truck,
            )
            * 1200,
        }

        loaded_km_run_per_trip = (primary_assumptions["round_trip_distance"] / 2) * (
            1 + primary_assumptions["backhauling_percentage"] / 100
        )
        primary_assumptions.update(
            {
                "loaded_km_run_per_trip": loaded_km_run_per_trip,
                "loaded_km_run_per_month": loaded_km_run_per_month,
            }
        )

        cost_profile_data = {
            "direct_ptpk": running_cost_per_month
            / (loaded_km_run_per_month * primary_assumptions["capacity"]),
            "semi_variable_ptpk": semi_variable_cost_per_month
            / (primary_assumptions["capacity"] * loaded_km_run_per_month),
            "fixed_ptpk": total_fixed_cost_per_month
            / (loaded_km_run_per_month * primary_assumptions["capacity"]),
            "profit_ptpk": profit_margin
            / (loaded_km_run_per_month * primary_assumptions["capacity"]),
        }
        total_ptpk = sum(cost_profile_data.values())
        cost_profile_data.update(
            {
                "total_ptpk": total_ptpk,
                "freight_per_tonne": round(total_ptpk * loaded_km_run_per_trip),
            }
        )

        attrs["cost_profile"] = {
            key: round(value, 2) for key, value in cost_profile_data.items()
        }
        attrs["capex_computations"] = {
            key: round(value, 2) for key, value in capex_computations_data.items()
        }
        attrs["financial_feasibility_check"] = {
            key: round(value, 2)
            for key, value in financial_feasibility_check_data.items()
        }
        attrs["direct_cost_computations"] = {
            key: round(value, 2) for key, value in direct_cost_computation_data.items()
        }
        attrs["fixed_cost_computations"] = {
            key: round(value, 2) for key, value in fixed_cost_computation_data.items()
        }
        semi_variable_cost_computations = {
            key: round(value, 2)
            for key, value in semi_variable_cost_computations.items()
        }
        semi_variable_cost_computations["toll"] = round(
            float(semi_variable_cost_computations["toll"]), 2
        )
        semi_variable_cost_computations["route_expenses"] = round(
            float(semi_variable_cost_computations["route_expenses"]), 2
        )

        attrs["semi_variable_cost_computations"] = semi_variable_cost_computations
        return attrs

    def update(self, instance, validated_data):
        FdDirectCostComputations.objects.filter(
            id=instance.direct_cost_computations.id
        ).update(**validated_data.pop("direct_cost_computations"))
        FdFinancialFeasibilityCheck.objects.filter(
            id=instance.financial_feasibility_check.id
        ).update(**validated_data.pop("financial_feasibility_check"))
        FdCapexComputations.objects.filter(id=instance.capex_computations.id).update(
            **validated_data.pop("capex_computations")
        )
        FdLocationOverview.objects.filter(id=instance.origin.id).update(
            **validated_data.pop("origin")
        )
        FdLocationOverview.objects.filter(id=instance.destination.id).update(
            **validated_data.pop("destination")
        )
        FdCostProfile.objects.filter(id=instance.cost_profile.id).update(
            **validated_data.pop("cost_profile")
        )
        FdFixedCostComputations.objects.filter(
            id=instance.fixed_cost_computations.id
        ).update(**validated_data.pop("fixed_cost_computations"))
        FdPrimaryAssumptions.objects.filter(id=instance.primary_assumptions.id).update(
            **validated_data.pop("primary_assumptions")
        )
        FdPurchaseInputs.objects.filter(id=instance.purchase_inputs.id).update(
            **validated_data.pop("purchase_inputs")
        )
        FdMonthlyCharges.objects.filter(id=instance.monthly_charges.id).update(
            **validated_data.pop("monthly_charges")
        )
        FdAnnualCharges.objects.filter(id=instance.annual_charges.id).update(
            **validated_data.pop("annual_charges")
        )
        FdSemiVariableCostComputations.objects.filter(
            id=instance.semi_variable_cost_computations.id
        ).update(**validated_data.pop("semi_variable_cost_computations"))
        FdOtherVariableCharges.objects.filter(
            id=instance.other_variable_charges.id
        ).update(**validated_data.pop("other_variable_charges"))
        FdFuelCharges.objects.filter(id=instance.fuel_charges.id).update(
            **validated_data.pop("fuel_charges")
        )
        FdTyreCharges.objects.filter(id=instance.tyre_charges.id).update(
            **validated_data.pop("tyre_charges")
        )
        FdProfitabilitySettings.objects.filter(
            id=instance.profitability_settings.id
        ).update(**validated_data.pop("profitability_settings"))

        return super().update(instance, validated_data)


class TgtSlhOrderPendencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtSlhOrderPendency
        fields = "__all__"


class TgtSlhServiceLevelDepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtSlhServiceLevelDepo
        fields = "__all__"


class TgtDepoInventoryStkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtDepoInventoryStk
        fields = "__all__"


class TgtRakeChargesSerializer(AutoGenerateFieldsSerializer):
    rld = serializers.SlugRelatedField(
        slug_field="rld_id", queryset=TgtRakeLoadingDetails.objects.all()
    )
    rake_id = serializers.IntegerField(source="rld.rake.rake_id", read_only=True)
    placement_date = serializers.DateTimeField(
        source="rld.rake.placement_date", read_only=True
    )
    actual_release_date = serializers.DateTimeField(
        source="rld.rake.actual_release_date", read_only=True
    )
    free_time_for_material_clearance = serializers.DateTimeField(
        source="rld.unloading_details.free_time_for_material_clearance", read_only=True
    )
    actual_time_for_rake_release = serializers.DateTimeField(
        source="rld.unloading_details.actual_time_for_rake_release", read_only=True
    )

    class Meta:
        model = TgtRakeCharges
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            # "total_demurrage_amount",
            # "dm_cgst_amt",
            # "dm_sgst_amt",
            # "dm_igst_amt",
            # "dm_total_gst",
            # "total_wharfage_amount",
            # "wf_cgst_amt",
            # "wf_sgst_amt",
            # "wf_igst_amt",
            # "wf_total_gst",
        )

    # def auto_generate_fields(self, validated_data):
    #     super().auto_generate_fields(validated_data)
    #     dm_hours = Decimal(
    #         validated_data["dm_hours"].hour
    #         + (validated_data["dm_hours"].minute / 60)
    #         + (validated_data["dm_hours"].second / 3600)
    #     )
    #     wf_hours = Decimal(
    #         validated_data["wf_hours"].hour
    #         + (validated_data["wf_hours"].minute / 60)
    #         + (validated_data["wf_hours"].second / 3600)
    #     )
    #     validated_data["created_by"] = self.context.get("request").user.id
    #     demurrage_amount = (
    #         validated_data["dm_total_wgn_placed"]
    #         * dm_hours
    #         * validated_data["dm_rate_per_wagon"]
    #     )
    #     wharfage_amount = (
    #         validated_data["wf_total_wgn_placed"]
    #         * wf_hours
    #         * validated_data["wf_rate_per_wagon"]
    #     )
    #     validated_data.update(
    #         {
    #             "dm_cgst_amt": demurrage_amount
    #             * validated_data["dm_cgst_percent"]
    #             / 100,
    #             "dm_sgst_amt": demurrage_amount
    #             * validated_data["dm_sgst_percent"]
    #             / 100,
    #             "dm_igst_amt": demurrage_amount
    #             * validated_data["dm_igst_percent"]
    #             / 100,
    #         }
    #     )
    #     free_time = (
    #         timedelta(hours=round(validated_data["free_hours"]))
    #         + validated_data["placement_time_at_depot_siding"]
    #     )
    #     validated_data.update(
    #         {
    #             "dm_total_gst": validated_data["dm_cgst_amt"]
    #             + validated_data["dm_sgst_amt"]
    #             + validated_data["dm_igst_amt"],
    #             "total_demurrage_amount": demurrage_amount
    #             + validated_data["dm_cgst_amt"]
    #             + validated_data["dm_sgst_amt"]
    #             + validated_data["dm_igst_amt"],
    #             "wf_cgst_amt": demurrage_amount
    #             * validated_data["wf_cgst_percent"]
    #             / 100,
    #             "wf_sgst_amt": demurrage_amount
    #             * validated_data["wf_sgst_percent"]
    #             / 100,
    #             "wf_igst_amt": demurrage_amount
    #             * validated_data["wf_igst_percent"]
    #             / 100,
    #             "free_time": free_time,
    #         }
    #     )
    #     validated_data.update(
    #         {
    #             "wf_total_gst": validated_data["wf_cgst_amt"]
    #             + validated_data["wf_sgst_amt"]
    #             + validated_data["wf_igst_amt"],
    #             "total_wharfage_amount": wharfage_amount
    #             + validated_data["wf_cgst_amt"]
    #             + validated_data["wf_sgst_amt"]
    #             + validated_data["wf_igst_amt"],
    #         }
    #     )


class TgtRakeUnloadingDetailsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtRakeUnloadingDetails
        fields = (
            "free_time",
            "placement_date",
            "material_clearing_from_siding",
            "actual_time_for_rake_release",
            "free_time_for_rake_release",
            "free_time_for_material_clearance",
            "dm_case_no",
            "dm_deposited_status",
            "dm_deposited_amount",
            "dm_waiver_percentage",
            "dm_waiver_amount",
            "dm_final_amount",
            "wf_case_no",
            "wf_deposited_status",
            "wf_deposited_amount",
            "wf_waiver_percentage",
            "wf_waiver_amount",
            "wf_final_amount",
            "dm_waiver_status",
            "wf_waiver_status",
        )


class TgtRakeLoadingReadOnlySerializer(serializers.ModelSerializer):
    rake_unloading_details = serializers.SerializerMethodField()
    rake_charges = serializers.SerializerMethodField()
    qty_dispatch_frm_plant = serializers.SerializerMethodField()
    no_of_wagons_per_depot = serializers.SerializerMethodField()
    liasioning_agent = serializers.SerializerMethodField()
    rake_point = serializers.SerializerMethodField()
    rake_point_code = serializers.SerializerMethodField()

    class Meta:
        model = TgtRakeLoading
        fields = "__all__"

    def get_no_of_wagons_per_depot(self, obj):
        amount_fields = "no_of_wagons"
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        queryset = TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        if queryset:
            rake_ids = queryset.values_list("rld__rake__rake_id", flat=True)
            depots = queryset.values_list("rld__ship_to_depot", flat=True)
            if rake_ids:
                loading_details_queryset = TgtRakeLoadingDetails.objects.filter(
                    rake_id__in=rake_ids, ship_to_depot__in=depots
                ).aggregate(Sum("no_of_wagons"))
                if loading_details_queryset:
                    return loading_details_queryset["no_of_wagons__sum"]
                return None

        return None

    def get_rake_point(self, obj):
        amount_fields = "no_of_wagons"
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        queryset = TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        if queryset:
            rake_ids = queryset.values_list("rld__rake__rake_id", flat=True)
            depots = queryset.values_list("rld__ship_to_depot", flat=True)
            if rake_ids:
                loading_details_queryset = TgtRakeLoadingDetails.objects.filter(
                    rake_id__in=rake_ids, ship_to_depot__in=depots
                ).first()
                # print(loading_details_queryset)
                if loading_details_queryset:
                    return loading_details_queryset.rake_point
                return None

        return None

    def get_rake_point_code(self, obj):
        amount_fields = "no_of_wagons"
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        queryset = TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        if queryset:
            rake_ids = queryset.values_list("rld__rake__rake_id", flat=True)
            depots = queryset.values_list("rld__ship_to_depot", flat=True)
            if rake_ids:
                loading_details_queryset = TgtRakeLoadingDetails.objects.filter(
                    rake_id__in=rake_ids, ship_to_depot__in=depots
                ).first()
                # print(loading_details_queryset)
                if loading_details_queryset:
                    return loading_details_queryset.rake_point_code
                return None

        return None

    def get_qty_dispatch_frm_plant(self, obj):
        amount_fields = "qty_dispatch_frm_plant"
        sum_dict = {field: Sum(field) for field in amount_fields}
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        queryset = TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        if queryset:
            rake_ids = queryset.values_list("rld__rake__rake_id", flat=True)
            depots = queryset.values_list("rld__ship_to_depot", flat=True)
            if rake_ids:
                loading_details_queryset = TgtRakeLoadingDetails.objects.filter(
                    rake_id__in=rake_ids, ship_to_depot__in=depots
                ).aggregate(Sum("qty_dispatch_frm_plant"))
                if loading_details_queryset:
                    return loading_details_queryset["qty_dispatch_frm_plant__sum"]
                return None

        return None

    def get_rake_unloading_details(self, obj):
        amount_fields = (
            "dm_waiver_amount",
            "dm_final_amount",
            "wf_deposited_amount",
            "wf_waiver_amount",
            "wf_final_amount",
            "dm_deposited_amount",
        )
        sum_dict = {field: Sum(field) for field in amount_fields}
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )

        queryset1 = TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        if queryset1.exists():
            return (
                TgtRakeUnloadingDetails.objects.filter(
                    rld__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
                )
                .values(
                    "free_time",
                    "placement_date",
                    "material_clearing_from_siding",
                    "actual_time_for_rake_release",
                    "free_time_for_rake_release",
                    "free_time_for_material_clearance",
                    "dm_case_no",
                    "dm_deposited_status",
                    "dm_waiver_percentage",
                    "wf_case_no",
                    "wf_deposited_status",
                    "wf_waiver_percentage",
                    "dm_waiver_status",
                    "wf_waiver_status",
                )
                .annotate(**sum_dict)[0]
            )
        return None

    def get_rake_charges(self, obj):
        amount_fields = (
            "dm_cgst_amt",
            "dm_sgst_amt",
            "dm_igst_amt",
            "wf_cgst_amt",
            "wf_sgst_amt",
            "wf_igst_amt",
            "dm_total_gst",
            "wf_total_gst",
            "total_demurrage_amount",
            "total_wharfage_amount",
        )
        # sum_dict = {field: Sum(field) for field in amount_fields}
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        queryset2 = TgtRakeCharges.objects.filter(
            rld_id__rake__rake_id=obj.rake_id, rld__ship_to_depot__in=total_depots
        )
        sum_result = queryset2.aggregate(
            dm_cgst_amt_sum=Sum("dm_cgst_amt"),
            dm_sgst_amt_sum=Sum("dm_sgst_amt"),
            dm_igst_amt_sum=Sum("dm_igst_amt"),
            wf_cgst_amt_sum=Sum("wf_cgst_amt"),
            wf_sgst_amt_sum=Sum("wf_sgst_amt"),
            wf_igst_amt_sum=Sum("wf_igst_amt"),
            dm_total_gst_sum=Sum("dm_total_gst"),
            wf_total_gst_sum=Sum("wf_total_gst"),
            total_demurrage_amount_sum=Sum("total_demurrage_amount"),
            total_wharfage_amount_sum=Sum("total_wharfage_amount"),
        )
        sum_dict = {
            "dm_cgst_amt_sum": sum_result["dm_cgst_amt_sum"],
            "dm_sgst_amt_sum": sum_result["dm_sgst_amt_sum"],
            "dm_igst_amt_sum": sum_result["dm_igst_amt_sum"],
            "wf_cgst_amt_sum": sum_result["wf_cgst_amt_sum"],
            "wf_sgst_amt_sum": sum_result["wf_sgst_amt_sum"],
            "wf_igst_amt_sum": sum_result["wf_igst_amt_sum"],
            "dm_total_gst_sum": sum_result["dm_total_gst_sum"],
            "wf_total_gst_sum": sum_result["wf_total_gst_sum"],
            "total_demurrage_amount_sum": sum_result["total_demurrage_amount_sum"],
            "total_wharfage_amount_sum": sum_result["total_wharfage_amount_sum"],
        }

        if queryset2.exists():
            return (
                TgtRakeCharges.objects.filter(
                    rld_id__rake__rake_id=obj.rake_id,
                    rld__ship_to_depot__in=total_depots,
                )
                .values(
                    "dm_hours",
                    "dm_total_wgn_placed",
                    "dm_rate_per_wagon",
                    "dm_cgst_percent",
                    "dm_sgst_percent",
                    "dm_igst_percent",
                    "dm_reason",
                    "wf_hours",
                    "wf_total_wgn_placed",
                    "wf_rate_per_wagon",
                    "wf_cgst_percent",
                    "wf_sgst_percent",
                    "wf_igst_percent",
                    "wf_reason",
                )
                .annotate(
                    dm_cgst_amt_sum=Value(
                        sum_dict["dm_cgst_amt_sum"], output_field=DecimalField()
                    ),
                    dm_sgst_amt_sum=Value(
                        sum_dict["dm_sgst_amt_sum"], output_field=DecimalField()
                    ),
                    dm_igst_amt_sum=Value(
                        sum_dict["dm_igst_amt_sum"], output_field=DecimalField()
                    ),
                    wf_cgst_amt_sum=Value(
                        sum_dict["wf_cgst_amt_sum"], output_field=DecimalField()
                    ),
                    wf_sgst_amt_sum=Value(
                        sum_dict["wf_sgst_amt_sum"], output_field=DecimalField()
                    ),
                    wf_igst_amt_sum=Value(
                        sum_dict["wf_igst_amt_sum"], output_field=DecimalField()
                    ),
                    dm_total_gst_sum=Value(
                        sum_dict["dm_total_gst_sum"], output_field=DecimalField()
                    ),
                    wf_total_gst_sum=Value(
                        sum_dict["wf_total_gst_sum"], output_field=DecimalField()
                    ),
                    total_demurrage_amount_sum=Value(
                        sum_dict["total_demurrage_amount_sum"],
                        output_field=DecimalField(),
                    ),
                    total_wharfage_amount_sum=Value(
                        sum_dict["total_wharfage_amount_sum"],
                        output_field=DecimalField(),
                    ),
                )[0]
            )

        return None

    def get_liasioning_agent(self, instance):
        # Access the siding_name and siding_code from the instance
        siding_name = instance.siding_name
        siding_code = instance.siding_code

        # Query the SidingWiseLiasioningAgent model based on the siding_name and siding_code
        agent_obj = SidingWiseLiasioningAgent.objects.filter(
            siding_name=siding_name, siding_code=siding_code
        ).first()
        if agent_obj:
            return agent_obj.liasioning_agent
        return None


class TgtRakeLoadingSerializer(AutoGenerateFieldsSerializer):
    rake_unloading_details = TgtRakeUnloadingDetailsEditSerializer(
        write_only=True, required=False
    )
    rake_charges = TgtRakeChargesSerializer(write_only=True, required=False)

    class Meta:
        model = TgtRakeLoading
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            # "waiver_amount",
            # "sgst_amt",
            # "cgst_amt",
            # "igst_amt",
            # "total_gst_amt",
            # "total_amount",
            # "total_time",
            # "free_time",
            # "total_demm_hours",
            # "total_demm_amount",
        )

    def update(self, instance, validated_data):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        total_depots_len = instance.loading_details.filter(
            ship_to_depot__in=total_depots
        ).count()

        if not total_depots_len:
            validated_data.pop("rake_charges", {})
            validated_data.pop("rake_unloading_details", {})
            return super().update(instance, validated_data)

        self.update_rake_unloading_details(
            instance, validated_data, total_depots, total_depots_len
        )
        self.update_rake_charges(
            instance, validated_data, total_depots, total_depots_len
        )
        return super().update(instance, validated_data)

    def update_rake_charges(
        self, instance, validated_data, total_depots, total_depots_len
    ):
        amount_fields = (
            "dm_cgst_amt",
            "dm_sgst_amt",
            "dm_igst_amt",
            "wf_cgst_amt",
            "wf_sgst_amt",
            "wf_igst_amt",
            "dm_total_gst",
            "wf_total_gst",
            "total_demurrage_amount",
            "total_wharfage_amount",
        )
        sum_dict = {field: Sum("rake_charges__" + field) for field in amount_fields}
        previous_charges = instance.loading_details.aggregate(**sum_dict)
        rake_charges = validated_data.pop("rake_charges", {})
        for field in amount_fields:
            rake_charges[field] = (
                rake_charges.get(field, previous_charges.get(field)) / total_depots_len
            )
        TgtRakeCharges.objects.filter(
            rld__rake__rake_id=instance.rake_id, rld__ship_to_depot__in=total_depots
        ).update(**rake_charges)

    def update_rake_unloading_details(
        self, instance, validated_data, total_depots, total_depots_len
    ):
        waiver_fields = {
            "dm_deposited_amount",
            "dm_waiver_amount",
            "dm_final_amount",
            "wf_deposited_amount",
            "wf_waiver_amount",
        }
        previous_waivers = instance.loading_details.aggregate(
            **{field: Sum("unloading_details__" + field) for field in waiver_fields}
        )
        rake_unloading_details = validated_data.pop("rake_unloading_details", {})
        for field in waiver_fields:
            value_from_rake = rake_unloading_details.get(field, 0)
            value_from_previous = previous_waivers.get(field, 0)

            if value_from_rake is not None and value_from_previous is not None:
                rake_unloading_details[field] = value_from_rake / total_depots_len
            else:
                rake_unloading_details[field] = 0
        TgtRakeUnloadingDetails.objects.filter(
            rld__rake__rake_id=instance.rake_id, rld__ship_to_depot__in=total_depots
        ).update(**rake_unloading_details)

    # def auto_generate_fields(self, validated_data):
    #     super().auto_generate_fields(validated_data)
    #     if self.instance:
    #         instance = self.instance
    #     else:
    #         instance = self.Meta.model(
    #             actual_release_date=datetime.now().replace(
    #                 year=datetime.now().year + 10, tzinfo=timezone.utc
    #             ),
    #             free_time=datetime.now().replace(
    #                 year=datetime.now().year + 10, tzinfo=timezone.utc
    #             )
    #         )
    #     total_demm_amount = validated_data.get(
    #         "demm_rate_per_wagon", instance.demm_rate_per_wagon
    #     ) * validated_data.get("no_of_wagons")
    #     waiver_amount = (
    #         total_demm_amount
    #         * validated_data.get("waiver_percent", instance.waiver_percent)
    #         / 100
    #     )
    #     sgst_amt = total_demm_amount * validated_data.get("sgst", instance.sgst) / 100
    #     cgst_amt = total_demm_amount * validated_data.get("cgst", instance.cgst) / 100
    #     igst_amt = total_demm_amount * validated_data.get("igst", instance.igst) / 100
    #     total_time = validated_data.get(
    #         "actual_release_date", instance.actual_release_date
    #     ) - validated_data.get("placement_date")

    #     total_demm_hours = validated_data.get("actual_release_date", instance.actual_release_date) - validated_data.get("free_time", instance.free_time)

    #     # free_time calculation being done at FE
    #     # free_time = timedelta(
    #     #     hours=round(validated_data.get("free_hours", instance.free_hours))
    #     # ) + validated_data.get("placement_date")

    #     validated_data.update(
    #         {
    #             "waiver_amount": waiver_amount,
    #             "total_demm_amount": total_demm_amount,
    #             "total_demm_hours": total_demm_hours.days * 24
    #             + total_demm_hours.seconds / 3600,
    #             "total_time": total_time.days * 24 + total_time.seconds / 3600,
    #             "sgst_amt": sgst_amt,
    #             "cgst_amt": cgst_amt,
    #             "igst_amt": igst_amt,
    #             "total_gst_amt": sgst_amt + cgst_amt + igst_amt,
    #             "total_amount": total_demm_amount
    #             - waiver_amount
    #             + cgst_amt
    #             + sgst_amt
    #             + igst_amt,
    #         }
    #     )


class TgtRakeLoadingDetailsSerializer(AutoGenerateFieldsSerializer):
    rake = serializers.SlugRelatedField(
        slug_field="rake_id", queryset=TgtRakeLoading.objects.all()
    )
    org_id = OptionChoiceField(choices=BrandChoices1.choices)
    inventory_item_id = OptionChoiceField(choices=InventoryItemIdChoices.choices)
    dispatch_from_plant = serializers.CharField(
        source="rake.dispatch_from_plant", read_only=True
    )
    actual_release_date = serializers.CharField(
        source="rake.actual_release_date", read_only=True
    )
    rake_type = serializers.CharField(source="rake.rake_type", read_only=True)
    free_time = serializers.DecimalField(
        source="unloading_details.free_time",
        max_digits=20,
        decimal_places=2,
        read_only=True,
    )
    material_cleaning_date = serializers.DateField(
        source="unloading_details.material_cleaning_date", read_only=True
    )
    placement_date = serializers.DateTimeField(
        source="unloading_details.placement_date", read_only=True
    )
    rk_unload_id = serializers.IntegerField(
        source="unloading_details.rk_unload_id", read_only=True
    )

    class Meta:
        model = TgtRakeLoadingDetails
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
            # "segment",
            # "org_id",
            # "inventory_item_id",
            # "rake_point",
            # "ship_to_depot",
            # "qty_dispatch_frm_plant",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        user_id = self.context.get("request").user.id
        auto_generated_field = {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
        unloading = TgtRakeUnloadingDetails(
            rld=instance, rake=instance.rake, **auto_generated_field
        )
        unloading.save()
        rake_charges = TgtRakeCharges(rld=instance, **auto_generated_field)
        rake_charges.save()
        return instance

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if (
            self.Meta.model.objects.filter(rake_id=attrs.get("rake", 0)).aggregate(
                total_no_of_wagons=functions.Coalesce(
                    Sum("no_of_wagons"), 0, output_field=IntegerField()
                )
            )["total_no_of_wagons"]
            > attrs.get("rake").no_of_wagons
        ):
            raise serializers.ValidationError(
                {"no_of_wagons": "wagon count for given rake detail exceeding its rake"}
            )
        return attrs


class TgtRakeUnloadingDetailsSerializer(AutoGenerateFieldsSerializer):
    rld = serializers.SlugRelatedField(
        slug_field="rld_id", queryset=TgtRakeLoadingDetails.objects.all()
    )
    org_id = OptionChoiceField(
        source="rld.org_id", read_only=True, choices=LpModelDfFnlBrandChoices.choices
    )
    inventory_item_id = OptionChoiceField(
        source="rld.inventory_item_id",
        read_only=True,
        choices=InventoryItemIdChoices.choices,
    )
    no_of_wagons = serializers.IntegerField(source="rld.no_of_wagons", read_only=True)
    segment = serializers.CharField(source="rld.segment", read_only=True)
    ship_to_depot = serializers.CharField(source="rld.ship_to_depot", read_only=True)
    qty_dispatch_frm_plant = serializers.DecimalField(
        source="rld.qty_dispatch_frm_plant",
        read_only=True,
        max_digits=20,
        decimal_places=2,
    )
    rake = serializers.IntegerField(source="rld.rake.rake_id", read_only=True)
    rake_type = serializers.CharField(source="rld.rake.rake_type", read_only=True)
    rr_no = serializers.CharField(source="rld.rr_no", read_only=True)
    rake_point = serializers.CharField(source="rld.rake_point", read_only=True)
    rake_point_code = serializers.CharField(
        source="rld.rake_point_code", read_only=True
    )
    dispatch_from_plant = serializers.CharField(
        source="rld.rake.dispatch_from_plant", read_only=True
    )
    packing_type = serializers.CharField(source="rld.packing_type", read_only=True)

    actual_release_date = serializers.DateTimeField(
        source="rld.rake.actual_release_date", read_only=True
    )
    excise_invoice_no = serializers.CharField(
        source="rld.excise_invoice_no", read_only=True
    )
    qty_available = serializers.SerializerMethodField()
    total_demurrage_amount = serializers.SerializerMethodField()
    rake_details = serializers.SerializerMethodField()

    class Meta:
        model = TgtRakeUnloadingDetails
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )

    def validate_rld(self, value):
        if hasattr(value, "unloading_details"):
            raise serializers.ValidationError(
                f"Unloading details for {value} already exists."
            )
        return value

    def get_qty_available(self, obj):
        qty_placed = (
            getattr(obj, "qty_placed", 0)
            if getattr(obj, "qty_placed", 0) is not None
            else 0
        )
        total_lifting_qty = obj.daywise_liftings.aggregate(
            total_lifting_qty=Coalesce(
                Sum("lifting_qty"), 0, output_field=DecimalField()
            )
        )["total_lifting_qty"]
        return qty_placed - total_lifting_qty

    def get_total_demurrage_amount(self, obj):
        return obj.rld.rake_charges.total_demurrage_amount

    def get_rake_details(self, value):
        rake_id = TgtRakeLoadingDetails.objects.filter(rld_id=value.rld_id).first()
        if TgtRakeLoading.objects.filter(rake_id=rake_id.rake_id).values():
            return TgtRakeLoading.objects.filter(rake_id=rake_id.rake_id).values()
        return None


class TgtRakeDisposalsSerializer(AutoGenerateFieldsSerializer):
    rk_unload = serializers.SlugRelatedField(
        slug_field="rk_unload_id", queryset=TgtRakeUnloadingDetails.objects.all()
    )
    org_id = OptionChoiceField(
        source="rk_unload.rld.org_id",
        read_only=True,
        choices=LpModelDfFnlBrandChoices.choices,
    )
    inventory_item_id = OptionChoiceField(
        source="rk_unload.rld.inventory_item_id",
        read_only=True,
        choices=InventoryItemIdChoices.choices,
    )
    segment = serializers.CharField(source="rk_unload.rld.segment", read_only=True)

    class Meta:
        model = TgtRakeDisposals
        fields = "__all__"
        read_only_fields = ("created_by", "last_updated_by", "last_update_login")


class TgtDayWiseLiftingSerializer(AutoGenerateFieldsSerializer):
    rk_unload = serializers.SlugRelatedField(
        slug_field="rk_unload_id", queryset=TgtRakeUnloadingDetails.objects.all()
    )
    org_id = OptionChoiceField(
        source="rk_unload.rld.org_id",
        read_only=True,
        choices=LpModelDfFnlBrandChoices.choices,
    )
    inventory_item_id = OptionChoiceField(
        source="rk_unload.rld.inventory_item_id",
        read_only=True,
        choices=InventoryItemIdChoices.choices,
    )
    segment = serializers.CharField(source="rk_unload.rld.segment", read_only=True)
    excise_invoice_no = serializers.CharField(
        source="rk_unload.rld.excise_invoice_no", read_only=True
    )

    class Meta:
        model = TgtDayWiseLifting
        fields = "__all__"
        read_only_fields = ("created_by", "last_updated_by", "last_update_login")


class FreightChangeInitiationListSerializer(
    BulkCreateListSerializer, BulkUpdateListSerializer
):
    def update(self, instances, validated_data):
        objects_updated = list()
        # route_master_updated_objects = list()
        # route_master_created_objects = list()
        try:
            for index, attrs in enumerate(validated_data):
                updated_instance = self.child.update(instances[index], attrs)
                objects_updated.append(updated_instance)

            # Route Master operations to be handled in ERP API so below code commented.
            #     if attrs.get("status") == ApprovalStatusChoices.APPROVED.value:
            #         route_master = TOebsSclRouteMaster.objects.filter(
            #             active_flag="Y", route_id=instances[index].route_code
            #         ).first()
            #         route_master.end_date = instances[index].applicability_date.replace(
            #             day=instances[index].applicability_date.day - 1
            #         )
            #         route_master_updated_objects.append(route_master)

            #         new_route = TOebsSclRouteMaster()
            #         for attr, value in route_master.__dict__.items():
            #             if not value:
            #                 continue
            #             setattr(new_route, attr, value)
            #         new_route.id = None
            #         new_route.freight_amount = (instances[index].to_be_freight,)
            #         new_route.from_date = (instances[index].applicability_date,)
            #         new_route.distance = instances[index].to_be_distance
            #         route_master_created_objects.append(new_route)

            # TOebsSclRouteMaster.objects.bulk_update(
            #     route_master_updated_objects, fields=["end_date"]
            # )
            # TOebsSclRouteMaster.objects.bulk_create(route_master_created_objects)

            self.child.Meta.model.objects.bulk_update(
                objects_updated,
                fields=[*getattr(self.child.Meta, "editable_fields", None)],
            )
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": f"Data not saved, original exception was: {e}"}
            )
        except IndexError as e:
            raise serializers.ValidationError(
                {
                    "message": f"Some of the IDs provided are not available in the database, original exception was: {e}."
                }
            )

        return objects_updated


class FreightChangeInitiationSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    status = OptionChoiceField(choices=ApprovalStatusChoices.choices)

    class Meta:
        model = FreightChangeInitiation
        exclude = (
            # "created_by",
            # "creation_date",
            # "last_updated_by",
            # "last_update_date",
            "last_update_login",
        )
        list_serializer_class = FreightChangeInitiationListSerializer
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        editable_fields = {"status"}

    def create(self, validated_data):
        obj = (
            ApprovalThreshold.objects.filter(
                approval=validated_data["approval_type"],
                min__lte=validated_data["contribution"],
                max__gte=validated_data["contribution"],
            )
            .values("persona")
            .first()
        )

        persona = obj["persona"]
        validated_data["persona"] = persona
        validated_data.update(self.get_auto_generated_fields())
        route_master = TOebsSclRouteMaster.objects.filter(
            active_flag="Y", route_id=validated_data.pop("route_code", 0)
        ).first()

        # threshold = validated_data.get("to_be_freight", 0) - validated_data.get(
        # "current_freight", 0
        # )
        # validated_data["persona"] = "PLH" if threshold <= 10 else "ZLH"

        instance = self.Meta.model(
            **validated_data,
            route_code=route_master.route_id,
            plant=route_master.whse,
            ship_city=route_master.to_city,
            ship_state=route_master.state_name,
            ship_district=route_master.dist_name,
            ship_taluka=route_master.tehsil_name,
            mode=route_master.mode_of_transport,
            segment=route_master.nt_tr,
            dispatch_type=route_master.primary_secondary_route,
            pack_type=route_master.attribute3,
            current_freight=route_master.freight_amount,
            description=route_master.route_description,
            current_distance=route_master.distance,
        )

        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance

    def update(self, instance, validated_data):
        if validated_data.get("status") != ApprovalStatusChoices.APPROVED.value:
            return super().update(instance, validated_data)

        validated_data["approved_by"] = self.context.get("request").user.id
        erp_payload = {
            "data": {
                "P_ROUTE_ID": instance.route_code,
                "PFREIGHT": float(
                    validated_data.get("to_be_freight", instance.to_be_freight)
                ),
                "PDISTANCE": validated_data.get(
                    "to_be_distance", instance.to_be_distance
                ),
                "PFROMDATE": str(
                    validated_data.get(
                        "applicability_date", instance.applicability_date
                    )
                ),
                "PUSERNAME": "02039",
            }
        }

        response = requests.post(
            "http://192.168.100.68:9001/soa-infra/resources/Shree_Customer_App/SCL_ROUTE_UPDATE/Routeupdate/",
            json=erp_payload,
        )
        response_body = json.loads(response.content)

        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise serializers.ValidationError("Error in response of ERP API")

        if response_body.get("P_ERROR_CODE") == "E":
            raise serializers.ValidationError(
                f"Error in response of ERP API: {response_body.get('P_ERROR_MESSAGE', '')}"
            )

        return super().update(instance, validated_data)


class NewFreightInitiationSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    status = OptionChoiceField(choices=ApprovalStatusChoices.choices)

    class Meta:
        model = NewFreightInitiation
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "created_by",
            "last_updated_by",
            "last_update_login",
        )
        editable_fields = {"status"}


class EpodDataSerializer(serializers.ModelSerializer):
    tgt_dispatch_data = serializers.SerializerMethodField()

    class Meta:
        model = EpodData
        fields = "__all__"

    def get_tgt_dispatch_data(self, data):
        epod_obj = (
            TgtPlantDispatchData.objects.filter(delivery_id=data.delivery_id)
            .values()
            .first()
        )
        return epod_obj


class ReasonsForDemurrageWharfageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonsForDemurrageWharfage
        fields = "__all__"


class TgtRakeLoadingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtRakeLoading
        fields = "__all__"


class WharfageSlabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WharfageSlabs
        fields = "__all__"


class DemurrageSlabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemurrageSlabs
        fields = "__all__"


class CrwcChargesMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrwcChargesMaster
        fields = "__all__"


class WaiverCommissionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiverCommissionMaster
        fields = "__all__"


class RailExpensesDetailsSerializer(serializers.ModelSerializer):
    wagon_under_dm_average = serializers.SerializerMethodField()
    rate_per_wagon_cal = serializers.SerializerMethodField()
    dm_amount_wth_gst_sum = serializers.SerializerMethodField()
    dm_hours_sum = serializers.SerializerMethodField()
    total_dm_amount_sum = serializers.SerializerMethodField()
    total_gst_amount = serializers.SerializerMethodField()

    # dm_cgst_percent_per=serializers.SerializerMethodField()
    # dm_igst_percent_per=serializers.SerializerMethodField()
    # dm_sgst_percent_per=serializers.SerializerMethodField()
    class Meta:
        model = RailExpensesDetails
        # fields="__all__"
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "wf_hours",
            "wagon_under_wf",
            "wf_rate_per_wagon",
            "wf_amount_wth_gst",
            "wf_cgst_percent",
            "wf_igst_percent",
            "wf_sgst_percent",
            "total_wf_gst_amount",
            "total_wf_amount",
        )

    def get_dm_hours_sum(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            dm_hours_sum = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(Sum("dm_hours"))
            return dm_hours_sum

    def get_rate_per_wagon_cal(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            rate_per_wagon_cal = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(
                rate_per_wagon_cal=ExpressionWrapper(
                    Sum("dm_amount_wth_gst")
                    / (Sum("rate_per_wagon") * Sum("dm_hours")),
                    output_field=DecimalField(),
                )
            )
            return rate_per_wagon_cal

    def get_wagon_under_dm_average(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            wagon_under_dm_average = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(Avg("wagon_under_dm"))
            return wagon_under_dm_average

    def get_dm_amount_wth_gst_sum(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            dm_amount_wth_gst_sum = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(Sum("dm_amount_wth_gst"))
            return dm_amount_wth_gst_sum

    def get_total_gst_amount(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            total_gst_amount = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(Sum("total_gst_amount"))
            return total_gst_amount

    def get_total_dm_amount_sum(self, obj):
        total_depots = settings.USER_DEPOT_MAPPING.get(
            f"{self.context.get('request').user.email}", []
        )
        rake_id = obj.rake_id
        if rake_id:
            total_dm_amount_sum = RailExpensesDetails.objects.filter(
                rake_id=rake_id, ship_to_depot__in=total_depots
            ).aggregate(Sum("total_dm_amount"))
            return total_dm_amount_sum


class RailExpensesSerializerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class RailExpensesDetailsPostSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = RailExpensesDetails
    #     fields = "__all__"
    class Meta:
        model = RailExpensesDetails
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = RailExpensesSerializerListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class HourlyLiftingEfficiencyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyLiftingEfficiencyMaster
        fields = "__all__"


class HourlyLiftingEfficiencySerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = HourlyLiftingEfficiency
        # fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "rake_id",
            "dm_hours",
            "wagon_under_dm",
            "rate_per_wagon",
            "dm_amount_wth_gst",
            "dm_cgst_percent",
            "dm_igst_percent",
            "dm_sgst_percent",
            "total_gst_amount",
            "total_dm_amount",
        }
        read_only_fields = ("id",)


class SidingConstraintsSerializerListSerializer(serializers.ListSerializer):
    """Parent list serializer class for MarketMappingStateClassification."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class SidingConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SidingConstraints
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = SidingConstraintsSerializerListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class CostsMasterDetailSerializer(serializers.ModelSerializer):
    def modify_packing_type(self, obj):
        if obj.packing_type != "PAPER":
            return "HDPE"
        return obj.packing_type

    packing_type = serializers.SerializerMethodField(method_name="modify_packing_type")
    transferring_cost = serializers.SerializerMethodField()
    road_handling_per_mt = serializers.SerializerMethodField()
    average_freight = serializers.SerializerMethodField()
    liasioning_agent = serializers.SerializerMethodField()

    class Meta:
        model = TgtRakeLoadingDetails
        fields = [
            "rake_point",
            "rake_point_code",
            "packing_type",
            "ship_to_depot",
            "transferring_cost",
            "road_handling_per_mt",
            "average_freight",
            "liasioning_agent",
            "qty_dispatch_frm_plant",
            "qty_net_received",
        ]

    def get_transferring_cost(self, data):
        packaging = data.packing_type
        if data.packing_type != "PAPER":
            packaging = "HDPE"
        rail_obj = RailHeadToGodownShiftingCartageCosts.objects.filter(
            rake_point=data.rake_point, godown=data.ship_to_depot, packaging=packaging
        ).aggregate(Avg("transferring_cost"))
        return rail_obj["transferring_cost__avg"]

    def get_road_handling_per_mt(self, data):
        packaging = data.packing_type
        if data.packing_type != "PAPER":
            packaging = "HDPE"
        road_obj = RoadHandlingMaster.objects.filter(
            godown=data.ship_to_depot, packaging=packaging
        ).aggregate(Avg("road_handling_per_mt"))
        return road_obj["road_handling_per_mt__avg"]

    def get_average_freight(self, data):
        packaging = data.packing_type
        if data.packing_type != "PAPER":
            packaging = "HDPE"
        godown = None
        if data.ship_to_depot:
            godown = data.ship_to_depot[:3]
        freight_obj = DepoWiseFreightMaster.objects.filter(
            pack_mat=packaging, depo_code=godown
        ).aggregate(Avg("average_freight"))
        return freight_obj["average_freight__avg"]

    def get_liasioning_agent(self, instance):
        # Access the siding_name and siding_code from the instance
        siding_name = instance.rake_point
        siding_code = instance.rake_point_code

        # Query the SidingWiseLiasioningAgent model based on the siding_name and siding_code
        agent_obj = SidingWiseLiasioningAgent.objects.filter(
            siding_name=siding_name, siding_code=siding_code
        ).first()
        if agent_obj:
            return agent_obj.liasioning_agent

        return None


class LiftingPatternSerializerListSerializer(serializers.ListSerializer):
    """Parent list serializer class for LiftingPatternSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


# class LiftingPatternSerializer(AutoGenerateFieldsSerializer):
#     class Meta(AutoGenerateFieldsSerializer.Meta):
#         model = LiftingPattern
#         # fields = "__all__"
#         list_serializer_class = LiftingPatternSerializerListSerializer

#     def create(self, validated_data):
#         validated_data.update(
#             {
#                 "created_by": self.context.get("request_user"),
#                 "last_updated_by": self.context.get("request_user"),
#                 "last_update_login": self.context.get("request_user"),
#             }
#         )

#         instance = self.Meta.model(**validated_data)
#         if isinstance(self._kwargs.get("data"), dict):
#             instance.save()

#         return instance


class LiftingPatternSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = LiftingPattern
        exclude = ()
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "run_id",
            "rake_id",
            "rake_point",
            "rake_point_code",
            "min_time",
            "max_time",
            "time_range",
            "brand",
            "packaging",
            "lifting_qty",
        }
        read_only_fields = (
            "id",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )


class TgtRakeLoadingDetailsSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgtRakeLoadingDetails
        fields = "__all__"


class WaiverCommissionMasterSerializer(serializers.ModelSerializer):
    siding_code_and_name = serializers.SerializerMethodField()

    class Meta:
        model = WaiverCommissionMaster
        fields = "__all__"

    def get_siding_code_and_name(self, instance):
        # Access the siding_name and siding_code from the instance
        agent = instance.agent

        # Query the SidingWiseLiasioningAgent model based on the siding_name and siding_code
        agent_obj = SidingWiseLiasioningAgent.objects.filter(
            liasioning_agent=agent
        ).first()
        if agent_obj:
            data_dict = {
                "siding_code": agent_obj.siding_code,
                "siding_name": agent_obj.siding_name,
            }
            return data_dict
        data_dict = {"siding_code": None, "siding_name": None}

        return data_dict


class RailExpensesDetailsWfSerializer(serializers.ModelSerializer):
    class Meta:
        model = RailExpensesDetailsWarfage
        # fields="__all__"
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )


class RailExpenseswWarfageSerializerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class RailExpensesDetailsWfPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RailExpensesDetailsWarfage
        # fields = "__all__"

        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = RailExpenseswWarfageSerializerListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class HandlingMastersSerializer(AutoGenerateFieldsSerializer):
    class Meta(AutoGenerateFieldsSerializer.Meta):
        model = HandlingMasters


class GdVsWharfageInputSerializer(serializers.ModelSerializer):
    """GdVsWharfageInputSerializer serializer class."""

    class Meta:
        model = GdWharfageRunInput
        fields = "__all__"


class GdWharfageOutputListSerializer(serializers.ListSerializer):
    """Parent list serializer class for GdVsWharfageInputSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class GdVsWhargfageOutputSerializer(serializers.ModelSerializer):
    """GdVsWharfageInputSerializer Serializer class."""

    class Meta:
        model = GdWharfageOutput
        exclude = ("run_id", "created_by", "last_updated_by", "last_update_login")
        list_serializer_class = GdWharfageOutputListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "run_id": self.context.get("run_id"),
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class GdVsWharfageModelRunOutputByRunidSerializer(serializers.ModelSerializer):
    cost_demurrage_total = serializers.SerializerMethodField()
    cost_wharfage_total = serializers.SerializerMethodField()
    cost_crwc_total = serializers.SerializerMethodField()
    cost_gd_total = serializers.SerializerMethodField()
    avg_demurrage_ammount = serializers.SerializerMethodField()
    avg_wharfage_ammount = serializers.SerializerMethodField()
    avg_crwc_ammount = serializers.SerializerMethodField()
    avg_gd_ammount = serializers.SerializerMethodField()
    qty_to_be_plt = serializers.SerializerMethodField()
    qty_to_be_crwc = serializers.SerializerMethodField()
    qty_to_be_gd = serializers.SerializerMethodField()
    total_cost_per_mt = serializers.SerializerMethodField()
    matrix_total_demurrage = serializers.SerializerMethodField()
    matrix_total_demurrage_rake_handling = serializers.SerializerMethodField()
    matrix_total_demurrage_freight_cost = serializers.SerializerMethodField()
    matrix_total_wharfage = serializers.SerializerMethodField()
    matrix_total_wharfage_rake_handling = serializers.SerializerMethodField()
    matrix_total_wharfage_freight_cost = serializers.SerializerMethodField()
    matrix_total_crwc_cost = serializers.SerializerMethodField()
    matrix_total_crwc_rake_handling_cost = serializers.SerializerMethodField()
    matrix_total_crwc_freight_cost = serializers.SerializerMethodField()
    matrix_total_crwc_handling_charges_cost = serializers.SerializerMethodField()
    matrix_total_gd_rake_handling_cost = serializers.SerializerMethodField()
    matrix_total_gd_transfer_cost = serializers.SerializerMethodField()
    matrix_total_gd_freight_cost = serializers.SerializerMethodField()
    matrix_total_gd_handling_charges = serializers.SerializerMethodField()
    qty_demurrage_end_time = serializers.SerializerMethodField()
    qty_wharfage_end_time = serializers.SerializerMethodField()
    qty_crwc_end_time = serializers.SerializerMethodField()
    qty_gd_end_time = serializers.SerializerMethodField()
    demurrage_qty_sum = serializers.SerializerMethodField()
    wharfage_qty_sum = serializers.SerializerMethodField()
    crwc_qty_sum = serializers.SerializerMethodField()
    gd_qty_sum = serializers.SerializerMethodField()
    total_cost_sum = serializers.SerializerMethodField()

    class Meta:
        model = GdWharfageOutput
        fields = "__all__"

    def get_data(self, obj):
        run_id = self.context.get("run_id")
        return GdWharfageOutput.objects.filter(run_id=run_id)

    def get_cost_demurrage_total(self, obj):
        objects = self.get_data(obj).aggregate(cost_demurrage=Sum("cost_demurrage"))
        return objects["cost_demurrage"]

    def get_total_cost_sum(self, obj):
        objects = self.get_data(obj).aggregate(total_cost_sum=Sum("total_cost"))
        return objects["total_cost_sum"]

    def get_cost_wharfage_total(self, obj):
        objects = self.get_data(obj).aggregate(cost_wharfage=Sum("cost_wharfage"))
        return objects["cost_wharfage"]

    def get_cost_crwc_total(self, obj):
        objects = self.get_data(obj).aggregate(cost_crwc=Sum("cost_crwc"))
        return objects["cost_crwc"]

    def get_cost_gd_total(self, obj):
        objects = self.get_data(obj).aggregate(cost_gd=Sum("cost_gd"))
        return objects["cost_gd"]

    def get_avg_demurrage_ammount(self, obj):
        objects = self.get_data(obj).aggregate(
            total_cost=Sum("cost_demurrage"), total_qty=Sum("qty_demurrage")
        )
        return objects["total_cost"] / objects["total_qty"]

    def get_avg_wharfage_ammount(self, obj):
        objects = self.get_data(obj).aggregate(
            total_cost=Sum("cost_wharfage"), total_qty=Sum("qty_wharfage")
        )
        return objects["total_cost"] / objects["total_qty"]

    def get_avg_crwc_ammount(self, obj):
        objects = self.get_data(obj).aggregate(
            total_cost=Sum("cost_crwc"), total_qty=Sum("qty_crwc")
        )
        if int(objects["total_qty"]) != 0:
            return objects["total_cost"] / objects["total_qty"]
        return 0

    def get_avg_gd_ammount(self, obj):
        objects = self.get_data(obj).aggregate(
            total_cost=Sum("cost_gd"), total_qty=Sum("qty_gd")
        )
        if int(objects["total_qty"]) != 0:
            return objects["total_cost"] / objects["total_qty"]
        return 0
        # return int(objects["total_cost"]) / int(objects["total_qty"])

    def get_qty_to_be_plt(self, obj):
        objects = self.get_data(obj).aggregate(
            qty_demurrage=Sum("qty_demurrage"), qty_wharfage=Sum("qty_wharfage")
        )
        return objects["qty_demurrage"] + objects["qty_wharfage"]

    def get_qty_to_be_crwc(self, obj):
        objects = self.get_data(obj).aggregate(qty_crwc=Sum("qty_crwc"))
        return objects["qty_crwc"]

    def get_qty_to_be_gd(self, obj):
        objects = self.get_data(obj).aggregate(qty_gd=Sum("qty_gd"))
        return objects["qty_gd"]

    def get_total_cost_per_mt(self, obj):
        objects = self.get_data(obj).aggregate(
            cost_demurrage=Sum("cost_demurrage"),
            cost_wharfage=Sum("cost_wharfage"),
            cost_crwc=Sum("cost_crwc"),
            cost_gd=Sum("cost_gd"),
        )
        objects_1 = self.get_data(obj).aggregate(
            qty_demurrage=Sum("qty_demurrage"),
            qty_wharfage=Sum("qty_wharfage"),
            qty_crwc=Sum("qty_crwc"),
            qty_gd=Sum("qty_gd"),
        )
        sum_objects = (
            objects["cost_demurrage"]
            + objects["cost_wharfage"]
            + objects["cost_crwc"]
            + objects["cost_gd"]
        )
        sum_objects_1 = (
            objects_1["qty_demurrage"]
            + objects_1["qty_wharfage"]
            + objects_1["qty_crwc"]
            + objects_1["qty_gd"]
        )
        return sum_objects / sum_objects_1

    def get_matrix_total_demurrage(self, obj):
        objects = self.get_data(obj).aggregate(
            total_demurrage=Sum("total_demurrage"), qty_demurrage=Sum("qty_demurrage")
        )
        if int(objects["qty_demurrage"]) != 0:
            return objects["total_demurrage"] / objects["qty_demurrage"]
        return 0

    def get_matrix_total_demurrage_rake_handling(self, obj):
        objects = self.get_data(obj).aggregate(
            total_demurrage_rake_handling=Sum("total_demurrage_rake_handling"),
            qty_demurrage=Sum("qty_demurrage"),
        )
        if int(objects["qty_demurrage"]) != 0:
            return objects["total_demurrage_rake_handling"] / objects["qty_demurrage"]
        return 0

    def get_matrix_total_demurrage_freight_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_demurrage_freight_cost=Sum("total_demurrage_freight_cost"),
            qty_demurrage=Sum("qty_demurrage"),
        )
        if int(objects["qty_demurrage"]) != 0:
            return objects["total_demurrage_freight_cost"] / objects["qty_demurrage"]
        return 0

    def get_matrix_total_wharfage(self, obj):
        objects = self.get_data(obj).aggregate(
            total_wharfage=Sum("total_wharfage"), qty_wharfage=Sum("qty_wharfage")
        )
        if int(objects["qty_wharfage"]) != 0:
            return objects["total_wharfage"] / objects["qty_wharfage"]
        return 0

    def get_matrix_total_wharfage_rake_handling(self, obj):
        objects = self.get_data(obj).aggregate(
            total_wharfage_rake_handling=Sum("total_wharfage_rake_handling"),
            qty_wharfage=Sum("qty_wharfage"),
        )
        if int(objects["qty_wharfage"]) != 0:
            return objects["total_wharfage_rake_handling"] / objects["qty_wharfage"]
        return 0

    def get_matrix_total_wharfage_freight_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_wharfage_freight_cost=Sum("total_wharfage_freight_cost"),
            qty_wharfage=Sum("qty_wharfage"),
        )
        if int(objects["qty_wharfage"]) != 0:
            return objects["total_wharfage_freight_cost"] / objects["qty_wharfage"]
        return 0

    def get_matrix_total_crwc_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_crwc_cost=Sum("total_crwc_cost"), qty_crwc=Sum("qty_crwc")
        )
        if int(objects["qty_crwc"]) != 0:
            return objects["total_crwc_cost"] / objects["qty_crwc"]
        return 0

    def get_matrix_total_crwc_rake_handling_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_crwc_rake_handling_cost=Sum("total_crwc_rake_handling_cost"),
            qty_crwc=Sum("qty_crwc"),
        )
        if int(objects["qty_crwc"]) != 0:
            return objects["total_crwc_rake_handling_cost"] / objects["qty_crwc"]
        return 0

    def get_matrix_total_crwc_freight_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_crwc_freight_cost=Sum("total_crwc_freight_cost"),
            qty_crwc=Sum("qty_crwc"),
        )
        if int(objects["qty_crwc"]) != 0:
            return objects["total_crwc_freight_cost"] / objects["qty_crwc"]
        return 0

    def get_matrix_total_crwc_handling_charges_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_crwc_handling_charges_cost=Sum("total_crwc_handling_charges_cost"),
            qty_crwc=Sum("qty_crwc"),
        )
        if int(objects["qty_crwc"]) != 0:
            return objects["total_crwc_handling_charges_cost"] / objects["qty_crwc"]
        return 0

    def get_matrix_total_gd_rake_handling_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_gd_rake_handling_cost=Sum("total_gd_rake_handling_cost"),
            qty_gd=Sum("qty_gd"),
        )
        if int(objects["qty_gd"]) != 0:
            return objects["total_gd_rake_handling_cost"] / objects["qty_gd"]
        return 0

    def get_matrix_total_gd_transfer_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_gd_transfer_cost=Sum("total_gd_transfer_cost"), qty_gd=Sum("qty_gd")
        )
        if int(objects["qty_gd"]) != 0:
            return objects["total_gd_transfer_cost"] / objects["qty_gd"]
        return 0

    def get_matrix_total_gd_freight_cost(self, obj):
        objects = self.get_data(obj).aggregate(
            total_gd_freight_cost=Sum("total_gd_freight_cost"), qty_gd=Sum("qty_gd")
        )
        if int(objects["qty_gd"]) != 0:
            return objects["total_gd_freight_cost"] / objects["qty_gd"]
        return 0

    def get_matrix_total_gd_handling_charges(self, obj):
        objects = self.get_data(obj).aggregate(
            total_gd_handling_charges=Sum("total_gd_handling_charges"),
            qty_gd=Sum("qty_gd"),
        )
        if int(objects["qty_gd"]) != 0:
            return objects["total_gd_handling_charges"] / objects["qty_gd"]
        return 0

    def get_qty_wharfage_end_time(self, obj):
        objects = self.get_data(obj).order_by("-qty_wharfage")
        if objects:
            for dem_obj in objects:
                if dem_obj.qty_demurrage > 0:
                    req_obj = dem_obj.end_time
                    return req_obj
        return None

    def get_qty_demurrage_end_time(self, obj):
        objects = self.get_data(obj).order_by("-qty_demurrage")
        if objects:
            for dem_obj in objects:
                if dem_obj.qty_demurrage > 0:
                    req_obj = dem_obj.end_time
                    return req_obj
        return None

    def get_qty_crwc_end_time(self, obj):
        objects = self.get_data(obj).order_by("-qty_crwc")
        if objects:
            for dem_obj in objects:
                if dem_obj.qty_crwc > 0:
                    req_obj = dem_obj.end_time
                    return req_obj
        return None

    def get_qty_gd_end_time(self, obj):
        objects = self.get_data(obj).order_by("-qty_gd")
        if objects:
            for dem_obj in objects:
                if dem_obj.qty_gd > 0:
                    req_obj = dem_obj.end_time
                    return req_obj
        return None

    def get_demurrage_qty_sum(self, obj):
        objects = self.get_data(obj).aggregate(qty_demurrage=Sum("qty_demurrage"))
        return objects["qty_demurrage"]

    def get_wharfage_qty_sum(self, obj):
        objects = self.get_data(obj).aggregate(qty_wharfage=Sum("qty_wharfage"))
        return objects["qty_wharfage"]

    def get_crwc_qty_sum(self, obj):
        objects = self.get_data(obj).aggregate(qty_crwc=Sum("qty_crwc"))
        return objects["qty_crwc"]

    def get_gd_qty_sum(self, obj):
        objects = self.get_data(obj).aggregate(qty_gd=Sum("qty_gd"))
        return objects["qty_gd"]
