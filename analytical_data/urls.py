"""Analytical data urls module"""
from django.urls import path

from analytical_data.views import *
from analytical_data.views.state_head_views import (
    RevisedBucketsApprovalViewset,
    TradeOrderPlacementApprovalViewset,
)

urlpatterns = [
    # Demand urls:
    path(
        "demands-list/",
        DemandListView.as_view({"get": "list"}),
        name="demands_list",
    ),
    path(
        "demands-list/<int:id>",
        DemandListView.as_view({"patch": "partial_update"}),
        name="demands_list",
    ),
    path(
        "get-demands-data-by-id/",
        GetDemandDataByIdViewSet.as_view({"get": "get"}),
        name="get_demands_data_by_id",
    ),
    path(
        "demands-download-upload/",
        DemandListView.as_view({"get": "download"}),
        name="demands_list_download_upload",
    ),
    path(
        "demands-dropdown/",
        DemandDropdownView.as_view(),
        name="demands_dropdown",
    ),
    # Godown master urls:
    path(
        "godown-master-list/",
        GodownMasterListView.as_view({"get": "list"}),
        name="godown_master_list",
    ),
    path(
        "godown-master-download-upload/",
        GodownMasterListView.as_view({"get": "download"}),
        name="godown_master_list",
    ),
    path(
        "godown-master/<int:id>",
        GodownMasterViewSet.as_view({"put": "put"}),
        name="godown_master",
    ),
    path(
        "godown-master-dropdown",
        GodownMasterDropdownView.as_view(),
        name="godown-master-dropdown",
    ),
    # Links master urls:
    path(
        "links-master/",
        LinksMasterViewSet.as_view({"get": "list"}),
        name="links_master",
    ),
    path(
        "links-master/<int:pk>",
        LinksMasterViewSet.as_view({"patch": "partial_update"}),
        name="links_master",
    ),
    path(
        "links-master-upload-download/",
        LinksMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="links_master_upload_download",
    ),
    path(
        "links-master-dropdown/",
        LinksMasterDropdownView.as_view(),
        name="links_master_dropdown",
    ),
    # Packaging master urls:
    path(
        "packaging-master/",
        PackagingMasterViewSet.as_view({"get": "list"}),
        name="packaging_master",
    ),
    path(
        "packaging-master/<int:id>",
        PackagingMasterViewSet.as_view({"patch": "partial_update"}),
        name="packaging_master",
    ),
    path(
        "packaging-master-download-upload/",
        PackagingMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="packaging_master_download_upload",
    ),
    path(
        "packaging-master-dropdown/",
        PackagingMasterDropdownView.as_view(),
        name="packaging_master_dropdown",
    ),
    # Packer constraints master urls:
    path(
        "packer-constraints-master/",
        PackerConstraintsMViewSet.as_view({"post": "create", "get": "list"}),
        name="packer_constraints_master",
    ),
    path(
        "packer-constraints-master/<int:id>",
        PackerConstraintsMViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="packer_constraints_master",
    ),
    # Packer shift constraint urls:
    path(
        "packer-shift-constraints/",
        PackerShiftConstraintViewSet.as_view({"post": "create", "get": "list"}),
        name="packer_shift_constraints",
    ),
    path(
        "packer-shift-constraints/<int:id>",
        PackerShiftConstraintViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="packer_shift_constraints",
    ),
    # Plant constraints master urls:
    path(
        "plant-constraints-master/",
        PlantConstraintsMViewSet.as_view({"post": "create", "get": "list"}),
        name="plant_constraints_master",
    ),
    path(
        "plant-constraints-master/<int:id>",
        PlantConstraintsMViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="plant_constraints_master",
    ),
    # Plant product master urls:
    path(
        "plant-products-master/",
        PlantProductsMasterViewSet.as_view({"get": "list"}),
        name="plant_products_master",
    ),
    path(
        "plant-products-master/<int:id>",
        PlantProductsMasterViewSet.as_view({"patch": "partial_update"}),
        name="plant_products_master",
    ),
    path(
        "plant-products-master-download-upload/",
        PlantProductsMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="plant_products_master_download_upload",
    ),
    path(
        "plant-product-master-dropdown/",
        PlantProductMasterDropdownView.as_view(),
        name="plants_products_master_dropdown",
    ),
    # Price master urls:
    path(
        "price-master/",
        PriceMasterViewSet.as_view({"get": "list"}),
        name="price_master",
    ),
    path(
        "price-master-download-upload/",
        PriceMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="price_master",
    ),
    path(
        "price-master/<int:id>",
        PriceMasterViewSet.as_view({"patch": "partial_update"}),
        name="price_master",
    ),
    # Route restrictions urls:
    path(
        "route-restrictions/",
        RouteRestrictionsViewSet.as_view({"post": "create", "get": "list"}),
        name="route_restrictions",
    ),
    path(
        "route-restrictions/<int:id>",
        RouteRestrictionsViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="route_restrictions",
    ),
    # Service level sla urls:
    path(
        "service-level-sla/",
        ServiceLevelSlaViewSet.as_view({"post": "create", "get": "list"}),
        name="service_level_sla",
    ),
    path(
        "service-level-sla/<int:id>",
        ServiceLevelSlaViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="service_level_sla",
    ),
    path(
        "service-level-sla-download-upload/",
        ServiceLevelSlaViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="service_level_sla_download_upload",
    ),
    path(
        "service-level-sla-dropdown/",
        ServiceLevelSlaDropdownView.as_view(),
        name="service_level_sla_dropdown",
    ),
    # Vehicle availability urls:
    path(
        "vehicle-availability/",
        VehicleAvailabilityViewSet.as_view({"post": "create", "get": "list"}),
        name="vehicle_availability",
    ),
    path(
        "vehicle-availability/<int:id>",
        VehicleAvailabilityViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="vehicle_availability",
    ),
    path(
        "vehicle-availability-download-upload/",
        VehicleAvailabilityViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="vehicle_availability_download_upload",
    ),
    path(
        "vehicle-availability-dropdown/",
        VehicleAvailabilityDropdownView.as_view(),
        name="vehicle_availability_dropdown",
    ),
    path(
        "route-restriction-dropdown/",
        RouteRestrictionDropdownView.as_view(),
        name="route_restriction_dropdown",
    ),
    # Lp model run urls:
    path(
        "lp-model-run-list/",
        LpModelRunListView.as_view(),
        name="lp_model_run_list",
    ),
    # lp model df fnl url:
    path(
        "lp-model-df-fnl-list/<int:run_id>",
        LpModelDfFnlBaseListAPIView.as_view(),
        name="lp_model_df_fnl_list",
    ),
    path(
        "lp-model-df-fnl/",
        LpModelDfFnlView.as_view(),
        name="lp_model_df_fnl",
    ),
    path(
        "getting_data_based_on_state/",
        StateViewSet.as_view({"get": "get"}),
        name="getting_data_based_on_state",
    ),
    path("states-cities/", StatesCities.as_view(), name="states_cities"),
    # Output screen urls:
    path(
        "road-vs-rake/<int:run_id>",
        RoadVsRakeView.as_view(),
        name="road_vs_rake",
    ),
    path(
        "rake-transfer-details/<int:run_id>",
        RakeTransferDetails.as_view(),
        name="rake_transfer_details",
    ),
    path(
        "dispatches/<int:run_id>",
        DispatchAPIView.as_view(),
        name="dispatch_view",
    ),
    path(
        "freight-based-quantity/<int:run_id>",
        FreightBasedQuantity.as_view(),
        name="freight_based_quantity",
    ),
    path(
        "tlc-breakup/<int:run_id>",
        TLCBreakupView.as_view(),
        name="tlc_breakup",
    ),
    path(
        "export-data/<int:run_id>",
        ExportToExcelView.as_view(),
        name="export_data",
    ),
    path(
        "lp-model-df-fnl-scenario-analysis/",
        LpModelDfFnlScenarioAnalysisView.as_view(),
        name="lp_model_df_fnl_scenario_analysis",
    ),
    path(
        "export-scenario-analysis/",
        LpModelScenarioAnalysisExportView.as_view(),
        name="export_scenario_analysis",
    ),
    path(
        "output-screen-dropdown/",
        OutputScreenDropdown.as_view(),
        name="output_screen_dropdown",
    ),
    path(
        "plant-dispatch-plan/<int:run_id>",
        PlantDispatchPlan.as_view(),
        name="plant_dispatch_plan",
    ),
    path(
        "plant-dispatch-plan-analysis/<int:run_id1>/<int:run_id2>",
        PlantDispatchPlanAnalysis.as_view(),
        name="plant_dispatch_plan",
    ),
    # path(
    #     "clinker-allocation/<int:run_id>",
    #     ClinkerALlocation.as_view(),
    #     name="clinker_allocation",
    # ),
    path(
        "clinker-allocation-analysis/<int:run_id1>/<int:run_id2>",
        ClinkerALlocationAnalysis.as_view(),
        name="clinker_allocation_analysis",
    ),
    # Lp scheduling vehicle constraint urls:
    path(
        "lp-scheduling-vehicle-constraint/",
        LpSchedulingVehicleConstraintView.as_view({"post": "create", "get": "list"}),
        name="lp_scheduling_vehicle_constraint",
    ),
    path(
        "lp-scheduling-vehicle-constraint-upload-download/",
        LpSchedulingVehicleConstraintView.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="lp_scheduling_vehicle_constraint_upload_download",
    ),
    path(
        "lp-scheduling-vehicle-constraint-dropdown/",
        LpSchedulingVehicleConstraintDropdownView.as_view(),
        name="lp_scheduling_vehicle_constraint_dropdown",
    ),
    path(
        "lp-scheduling-vehicle-constraint/<int:id>",
        LpSchedulingVehicleConstraintView.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="lp_scheduling_vehicle_constraint",
    ),
    # Lp scheduling plant constraint urls:
    path(
        "lp-scheduling-plant-constraint/",
        LpSchedulingPlantConstraintViewSet.as_view({"post": "create", "get": "list"}),
        name="lp_scheduling_plant_constraint",
    ),
    path(
        "lp-scheduling-plant-constraint/<int:id>",
        LpSchedulingPlantConstraintViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="lp_scheduling_plant_constraint",
    ),
    path(
        "lp-scheduling-plant-constraint-download-upload/",
        LpSchedulingPlantConstraintViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="lp_scheduling_plant_constraint_download_upload",
    ),
    path(
        "lp-scheduling-plant-constraint-dropdown/",
        LpSchedulingPlantConstraintDropdownView.as_view(),
        name="lp_scheduling_plant_constraint_dropdown",
    ),
    # Lp scheduling packer constraint urls:
    path(
        "lp-scheduling-packer-constraint/",
        LpSchedulingPackerConstraintView.as_view({"post": "create", "get": "list"}),
        name="lp_scheduling_packer_constraint",
    ),
    path(
        "lp-scheduling-packer-constraint-dropdown/",
        LpSchedulingPackerConstraintDropdownView.as_view(),
        name="lp_scheduling_packer_constraint_dropdown",
    ),
    path(
        "lp-scheduling-packer-constraint/<int:id>",
        LpSchedulingPackerConstraintView.as_view(
            {"patch": "partial_update", "delete": "destroy"}
        ),
        name="lp_scheduling_packer_constraint",
    ),
    #  Lp scheduling order master urls:
    path(
        "lp-scheduling-order-master/",
        LpSchedulingOrderMasterViewSet.as_view({"get": "list", "put": "update"}),
        name="lp_scheduling_order_master",
    ),
    path(
        "lp-scheduling-order-master-edit-dropdown/",
        LpSchedulingOrderMasterEditDropdownViewSet.as_view(),
        name="lp_scheduling_order_master_edit_dropdown",
    ),
    path(
        "lp-scheduling-order-master-update/<int:id>",
        LpSchedulingOrderMasterUpdateView.as_view({"patch": "partial_update"}),
        name="lp_scheduling_order_master",
    ),
    path(
        "lp-scheduling-order-master-dropdown/",
        LpSchedulingOrderMasterDropdownView.as_view({"get": "get"}),
        name="lp_scheduling_order_master_dropdown",
    ),
    path(
        "lp-scheduling-order-master-district-dropdown/",
        LpSchedulingOrderMasterDistrictDropdownView.as_view(),
        name="lp_scheduling_order_master_district_dropdown",
    ),
    path(
        "lp-scheduling-order-master-city-dropdown/",
        LpSchedulingOrderMasterCityDropdownView.as_view(),
        name="lp_scheduling_order_master_city_dropdown",
    ),
    path(
        "get-clinker-demand-run-data/",
        GetCLinkerDemandRunDataViewSet.as_view(),
        name="get-clinker-demand-run-data",
    ),
    path(
        "clinker-dispatch-gu-plant-dropdown/",
        ClinkerDispatchGUPlantDropdown.as_view(),
        name="clinker-dispatch-gu-plant-dropdown",
    ),
    path(
        "lp-scheduling-order-executable/",
        LpSchedulingOrderExecutableView.as_view(
            {"get": "list", "patch": "patch"},
        ),
        name="lp_scheduling_order_executable",
    ),
    path(
        "lp-scheduling-order-executable-download/",
        LpSchedulingOrderExecutableView.as_view(
            {"get": "download"},
        ),
        name="lp_scheduling_order_executable_download",
    ),
    path(
        "lp-scheduling-order-non-executable/",
        LpSchedulingOrderNonExecutableView.as_view({"get": "list"}),
        name="lp_scheduling_order_non_executable",
    ),
    path(
        "lp-scheduling-order-non-executable-download/",
        LpSchedulingOrderNonExecutableView.as_view({"get": "download"}),
        name="lp_scheduling_order_non_executable_download",
    ),
    path(
        "lp-scheduling-order-pp-sequence/",
        LpSchedulingPpSequenceView.as_view({"get": "list"}),
        name="lp_scheduling_order_pp_sequence/",
    ),
    path(
        "lp-scheduling-order-executable-dropdown/<int:id>",
        LpSchedulingOrderExecutableDropdownView.as_view(),
        name="lp_scheduling_order_executable_dropdown",
    ),
    path(
        "lp-scheduling-pp-sequence-dropdown/",
        LpSchedulingPpSequenceDropdown.as_view(),
        name="lp_scheduling_pp_sequence_dropdown",
    ),
    path(
        "order-executable-quantity-sum/",
        OrderExecutableQuantitySumView.as_view({"get": "get"}),
        name="order_executable_quantity_sum",
    ),
    # Clinker links master urls:
    path(
        "clinker-links-master/",
        CLinkerLinksMasterViewSet.as_view({"get": "list"}),
        name="clinker_links_master",
    ),
    path(
        "clinker-links-master/<int:id>",
        CLinkerLinksMasterViewSet.as_view({"patch": "partial_update"}),
        name="clinker_links_master",
    ),
    path(
        "clinker-links-master-download-upload/",
        CLinkerLinksMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="clinker_links_master",
    ),
    path(
        "clinker-links-master-dropdown/",
        ClinkerLinksMasterDropDownView.as_view(),
        name="clinker_links_master_dropdown",
    ),
    # DJP urls:
    path(
        "djp-counter-score/",
        DjpCounterScoreViewSet.as_view(),
        name="djp_counter_score",
    ),
    path(
        "djp-route-score/",
        DjpRouteScoreViewSet.as_view(),
        name="djp_route_score",
    ),
    path(
        "djp-run/",
        DjpRunViewSet.as_view(),
        name="djp_counter_score",
    ),
    # Third party API callings:
    path("update-route/", RouteUpdateView.as_view(), name="update_route"),
    path("create-delivery/", DeliveryCreationView.as_view(), name="create_delivery"),
    path("pp-call/", PpCallView.as_view(), name="pp_call"),
    path("order-update/", OrderUpdateView.as_view(), name="order-update"),
    # LpTargetSetting API View:
    path(
        "lp-target-setting/",
        LpTargetSettingView.as_view({"get": "list"}),
        name="lp_target_setting",
    ),
    path(
        "lp-target-setting-download-upload/",
        LpTargetSettingView.as_view({"get": "download", "put": "upload_update"}),
        name="lp_target_setting_download_upload",
    ),
    path(
        "lp-target-setting/<int:id>",
        LpTargetSettingView.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="lp_target_setting",
    ),
    path(
        "lp-target-setting-dropdown/",
        LpTargetSettingsDropdownViewSet.as_view({"get": "get"}),
        name="lp_target_setting_dropdown",
    ),
    # clinker demand run urls:
    path(
        "clinker-demand-run/", ClinkerDemandRunView.as_view(), name="lp_target_setting"
    ),
    # Rail handling urls:
    path(
        "rail-handling/",
        RailHandlingView.as_view({"get": "list"}),
        name="rail_handling",
    ),
    path(
        "rail-handling/<int:id>",
        RailHandlingView.as_view({"patch": "partial_update"}),
        name="rail_handling",
    ),
    path(
        "rail-handling-download-upload/",
        RailHandlingView.as_view({"get": "download", "put": "upload_update"}),
        name="rail_handling_download_upload",
    ),
    path(
        "rail-handling-dropdown/",
        RailHandlingDownView.as_view(),
        name="rail_handling_drop_down",
    ),
    path(
        "update-status-lp-model-run/",
        LpModelRunUpdate.as_view(),
        name="update-status-lp-model-run",
    ),
    # Kacha pakka conversion rate urls:
    path(
        "kacha-pakka-conversion-rate/",
        KachaPakkaConversionRateViewSet.as_view({"get": "list", "put": "update"}),
        name="kacha_pakka_conversion_rate",
    ),
    path(
        "kacha-pakka-conversion-rate-download-upload/",
        KachaPakkaConversionRateViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="kacha_pakka_conversion_rate_download_upload",
    ),
    # Annual urbanization rate urls:
    path(
        "annual-urbanization-rate/",
        AnnualUrbanizationRateViewSet.as_view({"get": "list", "put": "update"}),
        name="annual_urbanization_rate",
    ),
    path(
        "annual-urbanization-rate-download-upload/",
        AnnualUrbanizationRateViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="annual_urbanization_rate_download_upload",
    ),
    # Average flat size urls:
    path(
        "average-flat-size/",
        AverageFlatSizeViewSet.as_view({"get": "list", "put": "update"}),
        name="average_flat_size",
    ),
    path(
        "average-flat-size-download-upload/",
        AverageFlatSizeViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="average_flat_size_download_upload",
    ),
    # Urban rural household size urls:
    path(
        "urban-rural-household-size/",
        UrbanRuralHouseholdSizeViewSet.as_view({"get": "list", "put": "update"}),
        name="urban_rural_household_size",
    ),
    path(
        "urban-rural-household-size-download-upload/",
        UrbanRuralHouseholdSizeViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="urban_rural_household_size_download_upload",
    ),
    # Cement consumption urls:
    path(
        "cement-consumption/",
        CementConsumptionViewSet.as_view({"get": "list", "put": "update"}),
        name="cement_consumption",
    ),
    path(
        "cement-consumption-download-upload/",
        CementConsumptionViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="cement_consumption_download_upload",
    ),
    # Project database urls:
    path(
        "project-database/",
        ProjectDbViewSet.as_view({"get": "list", "put": "update"}),
        name="project_database",
    ),
    path(
        "project-database-download-upload/",
        ProjectDbViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="project_database_download_upload",
    ),
    # Desired market share urls:
    path(
        "desired-market-share/",
        DesiredMarketShareViewSet.as_view({"get": "list", "put": "update"}),
        name="desired_market_share",
    ),
    path(
        "get-desired-market-share-states/",
        GetDesiredMarketShareStatesViewSet.as_view(),
        name="get_desired_market_share_states",
    ),
    path(
        "get-geographical-presence-states/",
        GetGeographicalPresenceStatesViewSet.as_view(),
        name="get_geographical_presence_states",
    ),
    path(
        "desired-market-share-download-upload/",
        DesiredMarketShareViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="desired_market_share_download_upload",
    ),
    # Geographical presence urls:
    path(
        "geographical-presence/",
        GeographicalPresenceViewSet.as_view({"get": "list", "put": "update"}),
        name="geographical_presence",
    ),
    path(
        "geographical-presence-download-upload/",
        GeographicalPresenceViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="geographical_presence_download_upload",
    ),
    # Seasonality urls:
    path(
        "seasonality/",
        SeasonalityViewSet.as_view({"get": "list", "put": "update"}),
        name="seasonality",
    ),
    path(
        "seasonality-download-upload/",
        SeasonalityViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="seasonality_download_upload",
    ),
    # High rise low rise split urls:
    path(
        "high-rise-low-rise-split/",
        HighRiseLowRiseSplitViewSet.as_view({"get": "list", "put": "update"}),
        name="high_rise_low_rise_split",
    ),
    path(
        "high-rise-low-rise-split-download-upload/",
        HighRiseLowRiseSplitViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="high_rise_low_rise_split_download_upload",
    ),
    # Demand forecast run detail urls:
    path(
        "demand-forecast-run-download-upload/",
        DemandForecastRunViewSet.as_view({"get": "download"}),
        name="demand_forecast_run_download_upload",
    ),
    # Macro output final urls:
    path(
        "macro-output-final-download-upload/",
        DfMacroOutputFinalViewSet.as_view({"get": "download"}),
        name="macro_output_final_download_upload",
    ),
    path(
        "macro-analysis-script/",
        MacroAnalysisScriptRunView.as_view(),
        name="macro_analysis_script",
    ),
    # Top down targets detail urls:
    path(
        "top-down-targets-download-upload/",
        TopDownTargetsViewSet.as_view({"get": "download"}),
        name="top_down_targets_download_upload",
    ),
    path(
        "top-down-targets-dropdown/",
        TopDownTargetsDropdownView.as_view(),
        name="kacha_pakka_dropdown",
    ),
    # Sale consensus target urls:
    path(
        "consensus-target/",
        ConsensusTargetViewSet.as_view(),
        name="consensus_target",
    ),
    path(
        "consensus-target-update/",
        ConsensusTargetUpdateDownloadViewSet.as_view({"put": "update"}),
        name="consensus_target",
    ),
    path(
        "consensus-target-download-upload/",
        ConsensusTargetUpdateDownloadViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="consensus_target",
    ),
    path(
        "consensus-target-dropdown/",
        ConsensusTargetDropdownView.as_view(),
        name="consensus_target_dropdown",
    ),
    path(
        "lp-min-capacity/",
        LpMinCapacityViewSet.as_view({"get": "list"}),
        name="lp-min-capacity",
    ),
    path(
        "lp-min-capacity/<int:id>",
        LpMinCapacityViewSet.as_view({"patch": "partial_update"}),
        name="lp-min-capacity",
    ),
    # Testing pending on credit-limit-nt/
    path(
        "credit-limit-nt/",
        CreditLimitNtView.as_view({"get": "list", "post": "create"}),
        name="credit_limit_nt",
    ),
    path(
        "credit-limit-nt/<int:id>",
        CreditLimitNtView.as_view({"patch": "partial_update", "get": "retrieve"}),
        name="credit_limit_nt",
    ),
    path(
        "credit-limit-nt-change-status/",
        CreditLimitNtChangeStatus.as_view(),
        name="credit_limit_nt_change_status",
    ),
    # Testing pending on customer-accounts/
    path(
        "customer-accounts/",
        TOebsHzCustAccountsView.as_view(),
        name="customer_accounts",
    ),
    path(
        "nt-ncr-threshold/",
        NtNcrThresholdView.as_view(),
        name="nt_ncr_threshold",
    ),
    path(
        "nt-ncr-threshold-dropdown/",
        NtNcrThresholdDropdownView.as_view(),
        name="nt_ncr_threshold_dropdown",
    ),
    path(
        "nt-ncr-threshold-district-dropdown/",
        NtNcrThresholdDistrictsDropdownView.as_view(),
        name="nt_ncr_threshold_dropdown",
    ),
    path(
        "nt-ncr-threshold-city-dropdown/",
        NtNcrThresholdCityDropdownView.as_view(),
        name="nt_ncr_threshold_dropdown",
    ),
    path(
        "monthly-nt-ncr-sales/",
        NtNcrMonthlySales.as_view(),
        name="monthly_nt_ncr_sales",
    ),
    path(
        "brand-approval/",
        BrandApprovalViewSet.as_view({"get": "list", "post": "create"}),
        name="brand_approval",
    ),
    path(
        "brand-approval/<int:id>",
        BrandApprovalViewSet.as_view({"patch": "partial_update", "get": "retrieve"}),
        name="brand_approval",
    ),
    path(
        "brand-approval-dropdown/",
        BrandApprovalDropdownView.as_view(),
        name="brand_approval_dropdown",
    ),
    path(
        "lp-scheduling-dpc-dropdown/",
        LpSchedulingDpcDropdownView.as_view(),
        name="lp_scheduling_dpc_dropdown",
    ),
    path(
        "nt-communication/",
        NtCommunicationView.as_view({"post": "create", "get": "list"}),
        name="nt_communication",
    ),
    path(
        "nt-communication/<int:id>",
        NtCommunicationView.as_view({"get": "retrieve"}),
        name="nt_communication",
    ),
    path(
        "nt-communication-download/<int:id>",
        NtCommunicationView.as_view({"get": "download"}),
        # name="nt_notes_communications",
    ),
    path(
        "nt-notes-communications/",
        NtNotesView.as_view({"post": "create", "get": "list"}),
        name="nt_notes_communications",
    ),
    path(
        "nt-notes-communications/<int:id>",
        NtNotesView.as_view({"get": "retrieve"}),
        name="nt_notes_communications",
    ),
    path(
        "nt-notes-communications-download/<int:id>",
        NtNotesView.as_view({"get": "download"}),
        # name="nt_notes_communications",
    ),
    path(
        "packing-plant-aac/avg",
        TgtTruckCycleTatAacView.as_view(),
        name="packing-plant-aac-avg",
    ),
    path(
        "packing-plant-cement/avg",
        TgtTruckCycleTatCementView.as_view(),
        name="packing-plant-cement-avg",
    ),
    path(
        "packing-plant-aac/reasons",
        PackingPlantAacTatReasonsView.as_view(),
        name="packing-plant-aac-reasons",
    ),
    path(
        "packing-plant-cement/reasons",
        PackingPlantCementTatReasonsView.as_view(),
        name="packing-plant-cement-reasons",
    ),
    path(
        "packing-plant-aac/reasons/<int:id>",
        PackingPlantAacTatReasonsView.as_view(),
        name="packing-plant-aac-reasons",
    ),
    path(
        "packing-plant-aac/reasons-download/",
        PackingPlantAacTatReasonsDownloadView.as_view({"get": "download"}),
        name="packing_plant_aac_reasons_download",
    ),
    path(
        "packing-plant-cement/reasons/<int:id>",
        PackingPlantCementTatReasonsView.as_view(),
        name="packing-plant-cement-reasons",
    ),
    path(
        "packing-plant-aac-dropdown",
        AacPlantDropdownView.as_view(),
        name="packing-plant-aac-dropdown",
    ),
    path(
        "packing-plant-cement-dropdown",
        CementPlantDropdownView.as_view(),
        name="packing-plant-cement-dropdown",
    ),
    # NSH Non-trade urls:
    path(
        "non-trade-sales-dropdown/",
        NonTradeSalesDropdown.as_view(),
        name="non_trade_sales_dropdown",
    ),
    path(
        "dim-period-years-dropdown/",
        DimPeriodYearsDropdown.as_view(),
        name="dim_period_years_dropdown",
    ),
    path(
        "dim-period-months-dropdown/",
        DimPeriodMonthsDropdown.as_view(),
        name="dim_period_months_dropdown",
    ),
    path("ncr-calculator/", NcrCalculator.as_view(), name="ncr_calculator"),
    path(
        "ncr-calculator/<int:id>",
        NcrCalculator.as_view(),
        name="ncr_calculator",
    ),
    path(
        "ncr-calculator-dropdown/",
        NcrCalculatorDropdown.as_view(),
        name="ncr_calculator_dropdown",
    ),
    path(
        "annual-sales-target/",
        AnnualSalesTargetStateView.as_view({"put": "update", "get": "list"}),
        name="annual_sales_target",
    ),
    path(
        "annual-sales-target-ntso-kam/",
        AnnualSalesTargetNtsoKamView.as_view({"put": "update", "get": "list"}),
        name="annual_sales_target_ntso_kam",
    ),
    path(
        "annual-sales-plan-product/",
        AnnualSalesTargetProductView.as_view({"put": "update", "get": "list"}),
        name="annual_sales_target_product",
    ),
    path(
        "annual-sales-plan-account/",
        AnnualSalesTargetAccountView.as_view({"put": "update", "get": "list"}),
        name="annual_sales_target_account",
    ),
    path("dim-resources/", DimResourcesListView.as_view(), name="dim_resources"),
    path(
        "dim-resource-designation-dropdown/",
        DimResourceDesignationDropdown.as_view(),
        name="dim-resource-designation-dropdown",
    ),
    path(
        "dim-resource-dropdown/",
        DimResourceDropdown.as_view(),
        name="dim-resource-dropdown",
    ),
    path(
        "dim-account-name-dropdown/",
        DimAccountNameDropdown.as_view(),
        name="dim-account-name-dropdown",
    ),
    path(
        "fact-nt-sales-planning-get-data/",
        FactNtSalesPlanningViewSet.as_view({"get": "list"}),
        name="fact-nt-sales-planning",
    ),
    path(
        "tdt-multiplier/",
        TdtMultiplierViewSet.as_view({"get": "list", "put": "update"}),
        name="tdt-multiplier",
    ),
    path(
        "tdt-multiplier-download-upload/",
        TdtMultiplierViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="tdt-multiplier-download-upload",
    ),
    path(
        "tdt-multiplier-state-dropdown/",
        TdtMultiplierDropdown.as_view(),
        name="tdt-multiplier-state-dropdown",
    ),
    path(
        "get-data-based-on-month-actual/",
        NshNonTradeSalesActualViewSet.as_view({"get": "list"}),
        name="get-data-based-on-month",
    ),
    path(
        "sum-api-for-year/",
        SumApi.as_view({"get": "get"}),
        name="get-data-based-on-month",
    ),
    path(
        "nt-credit-limit-dropdown-data/",
        NtCreditLimitDropdown.as_view(),
        name="get-data-based-on-month",
    ),
    path("dim-customers/", DimCustomersView.as_view(), name="dim_customers"),
    path(
        "transfer-accounts/",
        TransferAccounts.as_view({"get": "list", "post": "create", "patch": "update"}),
        name="transfer_accounts",
    ),
    path(
        "transfer-officers-all-accounts/",
        TransferOfficersAllAccounts.as_view(),
        name="transfer_officers_all_accounts",
    ),
    path(
        "transfer-accounts/<int:id>",
        TransferAccounts.as_view({"get": "retrieve"}),
        name="transfer_accounts",
    ),
    path(
        "three-months-old-customer-data/",
        ThreeMonthsOldCustomerData.as_view(),
        name="three_months_old_customer_data",
    ),
    path(
        "plant-storage/",
        PlantStorageView.as_view({"get": "list"}),
        name="plant-storage",
    ),
    path(
        "plant-storage/<int:id>",
        PlantStorageView.as_view({"patch": "partial_update"}),
        name="plant-storage",
    ),
    path(
        "plant-depo-sla/",
        PlantDepoSlaView.as_view({"get": "list"}),
        name="plant-depo-sla",
    ),
    path(
        "plant-depo-sla/<int:id>",
        PlantDepoSlaView.as_view({"patch": "partial_update"}),
        name="plant-depo-sla",
    ),
    path(
        "clinker-dispatch-plan/",
        ClinkerDispatchPlanViewSet.as_view({"get": "list", "post": "post"}),
        name="clinker-dispatch-plan/",
    ),
    path(
        "clinker-dispatch-plan/<int:id>",
        ClinkerDispatchPlanViewSet.as_view({"patch": "partial_update"}),
        name="clinker-dispatch-plan/",
    ),
    path(
        "packing-plant-bags-stock/",
        PackingPlantBagsStockViewSet.as_view({"get": "list", "post": "create"}),
        name="packing-plant-bags-stock/",
    ),
    path(
        "packing-plant-bags-stock/<int:id>",
        PackingPlantBagsStockViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="packing-plant-bags-stock/",
    ),
    path(
        "packing-plant-bags-dropdown/",
        PackingPlantBagsStockDropdownView.as_view(),
        name="packing-plant-bags-dropdown/",
    ),
    path(
        "packer-bag-bursting-desc/",
        PackerBagBurstingDescViewSet.as_view({"get": "list", "post": "post"}),
        name="packer-bag-bursting-desc/",
    ),
    path(
        "packer-bag-bursting-desc/<int:id>",
        PackerBagBurstingDescViewSet.as_view({"patch": "partial_update"}),
        name="packer_bag_bursting_desc",
    ),
    path(
        "get-packer-bag-bursting-desc-by-id/",
        PackerBagBurstingDescDataByIdViewSet.as_view({"get": "get"}),
        name="get-packer-bag-bursting-desc-by-id",
    ),
    path(
        "packer-shift-level-stoppages/",
        PackerShiftLevelStoppagesViewSet.as_view({"get": "list", "post": "create"}),
        name="packer-shift-level-stoppages/",
    ),
    path(
        "packer-shift-level-stoppages-main-list/",
        PackerShiftLevelStoppagesMainListViewSet.as_view({"get": "get"}),
        name="packer-shift-level-stoppages_main_list",
    ),
    path(
        "packer-shift-level-stoppages-dropdown/",
        PackerShiftLevelStoppagesDropdownView.as_view(),
        name="packer-shift-level-stoppages-dropdown/",
    ),
    path(
        "getting-customer-data-based-on-resource/",
        GetCustomerBasedOnResource.as_view({"get": "get"}),
        name="getting-data-based-on-resource/",
    ),
    path(
        "shiftwise-adhoc-percentage/",
        ShiftWiseAdhocPercentageViewSet.as_view(
            {"get": "list", "patch": "partial_update"}
        ),
        name="shiftwise-adhoc-percentage",
    ),
    # Influencer manager urls:
    path(
        "case-study-window-state/",
        StateCaseStudyViewSet.as_view({"post": "post"}),
        name="state_case_study",
    ),
    path(
        "get-case-study-state-data/",
        GetStateCaseStudyDataViewSet.as_view({"get": "list", "patch": "patch"}),
        name="get_state_case_study_data",
    ),
    path(
        "get-case-study-state-data/<int:id>",
        GetStateCaseStudyDataViewSet.as_view({"patch": "partial_update"}),
        name="get_state_case_study_data",
    ),
    path(
        "get-case-study-state-data-by-id/",
        StateCaseStudyDataByIdViewSet.as_view({"get": "get"}),
        name="get_state_case_study_data_by_id",
    ),
    path(
        "create_scheme_entry/",
        SchemeViewSet.as_view({"post": "post"}),
        name="create_scheme_entry",
    ),
    path(
        "view_scheme_entry/",
        GetStateSchemeViewSet.as_view({"get": "list"}),
        name="view_scheme_entry",
    ),
    path(
        "view-scheme-entry-by-id/",
        GetStateSchemeByIdViewSet.as_view({"get": "get"}),
        name="view_scheme_entry_by_id",
    ),
    path(
        "last-year-meet-plan-avg/",
        LastYearMeetPlanAvg.as_view(),
        name="last_year_meet_plan_avg",
    ),
    path(
        "get-crm-infl-assist-req-data/",
        GetCrmInflAssistReqDataViewSet.as_view({"get": "list"}),
        name="get_crm_infl_assist_req_data",
    ),
    path(
        "get-crm-infl-assist-req-data/<int:id>",
        GetCrmInflAssistReqDataViewSet.as_view({"patch": "partial_update"}),
        name="get_crm_infl_assist_req_data",
    ),
    path(
        "get-prvyr-select-month-crm-nth-activity-data/<int:id>",
        GetPrvYrSelectdMnthCrmNthActivityPlanViewSet.as_view(
            {"patch": "partial_update"}
        ),
        name="get-prvyr-select-month-crm-activity-data",
    ),
    path(
        "get-crm-infl-assist-req-by-id/",
        CrmInflAssistReqDataByIdViewSet.as_view({"get": "get"}),
        name="get-crm-infl-assist-req-by-id",
    ),
    path(
        "get-crm-infl-chg-req-data/",
        GetCrmInflChgReqDataViewSet.as_view({"get": "list"}),
        name="get_crm_infl_chg_req_data",
    ),
    path(
        "get-crm-infl-chg-req-data/<int:id>",
        GetCrmInflChgReqDataViewSet.as_view({"patch": "partial_update"}),
        name="get_crm_infl_chg_req_data",
    ),
    path(
        "get-crm-infl-chg-req-by-id/",
        CrmInflChgReqDataByIdViewSet.as_view({"get": "get"}),
        name="get-crm-chg-req-by-id",
    ),
    path(
        "create-pp-master/",
        PpMasterViewSet.as_view({"post": "post"}),
        name="create_pp_master",
    ),
    path(
        "get-packing-plant-output-data/",
        GetPackingPlanOutputViewSet.as_view({"get": "get"}),
        name="get_packing_plant_output_data",
    ),
    path(
        "order-tagging-dropdown/",
        PpOrderTaggingDropdown.as_view(),
        name="order_tagging_dropdown",
    ),
    path(
        "get-prv-yr-selected-month-mgr-meet-plan-data/",
        GetPrvYrSelectdMnthMgrMeetPlanDataViewSet.as_view({"get": "get"}),
        name="get_prv_yr_selected_month_mgr_meet_plan_data",
    ),
    # path(
    #     "create-pp-downtime/",
    #     PpDowntimeViewSet.as_view({"post": "post"}),
    #     name="create_pp_downtime",
    # ),
    path(
        "get-packer-created-capacity-viewset-data/",
        GetPackerRatedCapacityViewSet.as_view({"get": "list"}),
        name="get_packer_created_capacity_viewSet_data",
    ),
    path(
        "get-packer-created-capacity-viewset-data/<int:id>",
        GetPackerRatedCapacityViewSet.as_view({"patch": "partial_update"}),
        name="get_packer_created_capacity_viewSet_data",
    ),
    path(
        "create-annual-meet-plan-yearly/",
        CreateAnnualMeetPlanYearly.as_view({"post": "post"}),
        name="annual_meet_plan_yearly/",
    ),
    path(
        "annual-influncer-plan-last-year-avg/",
        AnnualInfluencerManagerPLanLastYearAvg.as_view(),
        name="annual_influncer_plan_last_year_avg",
    ),
    path(
        "create-annual-influencer-plan-yearly/",
        CreateAnnualInflncrPlnYearly.as_view({"post": "post"}),
        name="create_annual_influencer_plan_yearly/",
    ),
    path(
        "get-prv-yr-selected-month-crm-annual-data/",
        GetPrvYrSelectdMnthCrmAnnualPlanViewSet.as_view({"get": "get"}),
        name="get_packing_plant_output_data",
    ),
    # National Technical Head Work
    path(
        "crm-complaints/",
        CrmComplaintsViewSet.as_view({"get": "list"}),
        name="crm-complaints",
    ),
    path(
        "crm-complaints/<int:id>",
        CrmComplaintsViewSet.as_view({"patch": "partial_update"}),
        name="crm-complaints",
    ),
    path(
        "get-crm-complaints-by-id",
        GetCrmComplaintsByIdViewSet.as_view({"get": "get"}),
        name="crm-complaints-by-id",
    ),
    path(
        "create-crm-complaints/",
        CreateCrmComplaintsViewSet.as_view({"post": "post"}),
        name="create_crm_complaints",
    ),
    path(
        "crm-nthproduct-approve/",
        CrmNthProductApprovalViewSet.as_view({"get": "list"}),
        name="crm_nthproduct_approve",
    ),
    path(
        "crm-ann-site-conv-plan/",
        CrmAnnualSiteConvPlanViewSet.as_view({"post": "post", "get": "list"}),
        name="crm_ann_site_conv_plan",
    ),
    path(
        "crm-ann-site-conv-plan/<int:id>",
        CrmAnnualSiteConvPlanViewSet.as_view({"patch": "partial_update"}),
        name="crm_ann_site_conv_plan",
    ),
    path(
        "get-last-year-avg-crm-ann-site-conv-plan/",
        GetLstYrAvgCrmAnnualSiteConvPlanViewSet.as_view({"get": "get"}),
        name="get_last_year_avg_crm_ann_site_conv_plan/",
    ),
    path("crm-ann-site-conv-dropdown/", CrmAnnualSiteConvDropdown.as_view()),
    path(
        "crm-material-test-certificate/",
        CrmMaterialtestCertificateViewSet.as_view({"post": "post", "get": "list"}),
        name="crm_material_test_certificate",
    ),
    path(
        "crm-material-test-certificate/<int:id>",
        CrmMaterialtestCertificateViewSet.as_view({"patch": "partial_update"}),
        name="crm_material_test_certificate",
    ),
    path(
        "nth-budget-plan/",
        NthBudgetPlanViewSet.as_view(
            {"post": "create", "get": "list", "put": "update"}
        ),
        name="nth_budget_plan",
    ),
    path(
        "get-prv-yr-selected-month-crm-nth-budget-plan-data/",
        GetPrvYrSelectdMnthNthBudgetPlanViewSet.as_view({"get": "get"}),
        name="get_prv_yr_selected_month_crm_nth_budget_plan_data",
    ),
    path(
        "crm-nth-activity-plan/",
        CrmNthActivityPlanView.as_view({"post": "post", "get": "list"}),
        name="crm_nth_activity_plan",
    ),
    path(
        "get-crm-nth-activity-data-by-id/",
        CrmNthActivityPlanByIdViewSet.as_view({"get": "get"}),
        name="get_crm_nth_activity_data_by_id",
    ),
    path(
        "crm-nth-activity-plan/<int:id>",
        CrmNthActivityPlanView.as_view({"patch": "partial_update"}),
        name="crm_nth_activity_plan",
    ),
    path(
        "get-prv-yr-selected-month-crm-nth-activity-plan-data/",
        GetPrvYrSelectdMnthCrmNthActivityPlanViewSet.as_view({"get": "get"}),
        name="get_prv_yr_selected_month_crm_nth_activity_plan_data",
    ),
    # Marketing Branding Urls
    path(
        "crm-mab-branding-approval-data/",
        CrmMabBrandingApprViewSet.as_view({"get": "list"}),
        name="crm_mab_branding_approval_data",
    ),
    path(
        "crm-mab-branding-approval-data-by-id/",
        CrmMabBrandingApprByIdViewSet.as_view({"get": "get", "patch": "patch"}),
        name="get_crm_mab_bt_planning_data_by_id",
    ),
    path(
        "crm-mab-branding-approval-data/<int:id>",
        CrmMabBrandingApprViewSet.as_view({"patch": "partial_update"}),
        name="crm_mab_branding_approval_data",
    ),
    path(
        "get-vendors-by-state/",
        GetVendorsByStateViewSet.as_view({"get": "get"}),
        name="get_vendors_by_state",
    ),
    path(
        "crm-mab-bt-planning-data/",
        CrmMabBtlPlanningViewSet.as_view({"get": "list", "put": "update"}),
        name="crm_mab_bt_planning_data",
    ),
    path(
        "crm-mab-bt-planning-data-by-id/",
        CrmMabBtlPlanningByIdViewSet.as_view({"get": "get"}),
        name="get_crm_mab_bt_planning_data_by_id",
    ),
    path(
        "crm-mab-bt-planning-data/<int:id>",
        CrmMabBtlPlanningViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="crm_mab_bt_planning_data",
    ),
    path(
        "crm-nth-quot-ncr-excp-appr-data/",
        CrmNthQuotNcrExcpApprViewSet.as_view({"get": "list"}),
        name="crm_nth_quot_ncr_excp_appr_data",
    ),
    path(
        "crm-nth-so-ncr-excp-appr-data/",
        CrmNthSoNcrExcpApprViewSet.as_view({"get": "list"}),
        name="crm_nth_so_ncr_excp_appr_data",
    ),
    path(
        "crm-nth-source-change-request-data/",
        CrmNthSourceChgReqViewSet.as_view({"get": "list"}),
        name="crm_nth_source_change_request_data",
    ),
    path(
        "crm-nth-extended-validity-data/",
        CrmNthExtendValidityViewSet.as_view({"get": "list"}),
        name="crm_nth_extended_validity_data",
    ),
    path(
        "crm-nth-order-canc-appr-data/",
        CrmNthOrderCancApprViewSet.as_view({"get": "list"}),
        name="crm_nth_order_canc_appr_data",
    ),
    path(
        "crm-nth-bank-guart-appr-data/",
        CrmNthBankGuartApprViewSet.as_view({"get": "list"}),
        name="crm_nth_bank_guart_appr_data",
    ),
    path(
        "crm-nth-lead-form-data/",
        CrmNthLeadFormViewSet.as_view({"get": "list", "post": "post"}),
        name="crm_nth_lead_form_data",
    ),
    path(
        "crm-nth-lead-form-data/<int:id>",
        CrmNthLeadFormViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="crm_nth_lead_form_data",
    ),
    path(
        "crm-nth-refund-request-data/",
        CrmNthRefuReqViewSet.as_view({"get": "list"}),
        name="crm_nth_refund_request_data",
    ),
    path(
        "crm-nth-customer-code-cre-data/",
        CrmNthCustCodeCreViewSet.as_view({"get": "list"}),
        name="crm_nth_customer_code_cre_data",
    ),
    path(
        "crm-markrequisitionset-branding-past--data/",
        CrmMabPastRequisitionsViewSet.as_view({"get": "list"}),
        name="crm_market_branding_past_requisitions_data",
    ),
    path(
        "crm-market-branding-past-requisitions-data/<int:id>",
        CrmMabPastRequisitionsViewSet.as_view({"patch": "partial_update"}),
        name="crm_market_branding_past_requisitions_data",
    ),
    path(
        "crm-market-branding-past-requisitions-data-by-id/",
        CrmMabPastRequisitionsByIdViewSet.as_view({"get": "get"}),
        name="crm_market_branding_past_requisitions_data_by_id",
    ),
    path(
        "crm-market-branding-initiate-requisition-data/",
        CrmMabInitReqViewSet.as_view({"post": "post"}),
        name="crm_market_branding_initiate_requisition_data",
    ),
    # CRM Rate List URLs:
    path(
        "crm-mab-rate-list/",
        CrmMabRateListUploadDownloadAPIView.as_view({"get": "list"}),
        name="crm_mab_rate_list",
    ),
    path(
        "crm-mab-rate-list-upload-download/",
        CrmMabRateListUploadDownloadAPIView.as_view(
            {"post": "upload_create", "get": "download"}
        ),
        name="crm_mab_rate_list_upload_download",
    ),
    path(
        "packing-plant-run-model/",
        PackingPlantScriptRunModel.as_view(),
        name="packing-plant-run-model",
    ),
    path("lp-script-view-set/", LpScriptViewSet.as_view(), name="lp-script-view-set"),
    path(
        "unique-value-packing-plant/",
        UniqueValueViewSet.as_view(),
        name="unique-value-packing-plant",
    ),
    path(
        "lp-scheduling-dpc-data/",
        LpSchedulingDpcViewSet.as_view({"get": "list", "post": "create"}),
        name="lp_scheduling_dpc_data",
    ),
    path(
        "lp-scheduling-dpc-data-upload-data/",
        LpSchedulingDpcViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="lp_scheduling_dpc_data-upload-data",
    ),
    path(
        "lp-scheduling-dpc-data/<int:id>",
        LpSchedulingDpcViewSet.as_view({"patch": "partial_update"}),
        name="lp_scheduling_dpc_data",
    ),
    path(
        "Lp-scheduling-dpc-data-by-id/",
        LpSchedulingDpcByIdViewSet.as_view({"get": "get"}),
        name="Lp_scheduling_dpc_data_by_id",
    ),
    path(
        "tn-mox-scheme-data/",
        TNmOmxSchemesViewSet.as_view({"get": "get"}),
        name="tn_mox_scheme_data",
    ),
    path(
        "market-mapping-market-potential/",
        MarketMappingMarketPotentialViewSet.as_view({"get": "list", "put": "update"}),
        name="market_mapping_market_potential",
    ),
    path(
        "market-mapping-market-potential-upload-download/",
        MarketMappingMarketPotentialViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="market_mapping_market_potential_upload_download",
    ),
    path(
        "market-mapping-market-potential-dropdown/",
        MarketMappingMarketPotentialDropdown.as_view(),
        name="market_mapping_market_potential_dropdown",
    ),
    path(
        "market-mapping-growth-potential-dropdown/",
        MarketMappingGrowthPotentialDropdown.as_view(),
        name="market_mapping_growth_potential_dropdown",
    ),
    path(
        "plant-depo-sla-new-data/",
        PlantDepoSlaNewViewSet.as_view({"get": "list"}),
        name="plant_depo_sla_new_data",
    ),
    path(
        "plant-depo-sla-new-data/<int:id>",
        PlantDepoSlaNewViewSet.as_view({"patch": "partial_update"}),
        name="plant_depo_sla_new_data",
    ),
    path(
        "market-mapping-growth-potential/",
        MarketMappingGrowthPotentialViewSet.as_view({"get": "list", "put": "update"}),
        name="market_mapping_growth_potential",
    ),
    path(
        "market-mapping-growth-potential-upload-download/",
        MarketMappingGrowthPotentialViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="market_mapping_growth_potential_upload_download",
    ),
    path(
        "slct-party-wise-scheme-props-data/",
        SlctPartyWiseSchemePropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_party_wise_scheme_props_data",
    ),
    path(
        "slct-party-wise-scheme-props-data/<int:id>",
        SlctPartyWiseSchemePropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_party_wise_scheme_props_data",
    ),
    path(
        "slct-cash-disc-props/",
        SlctCashDiscPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_cash_disc_props",
    ),
    path(
        "update-slct-cash-disc-props/",
        UpdateSlctCashDiscPropseViewSet.as_view({"post": "post"}),
        name="update_slct_cash_disc_props",
    ),
    path(
        "update-slct-party-wise-scheme-props/",
        UpdateSlctPartyWiseSchemePropsViewSet.as_view({"post": "post"}),
        name="update_slct_party_wise_scheme_props",
    ),
    path(
        "update-slct-quantity-slab-props/",
        UpdateSlctQuantitySlabPropsViewSet.as_view({"post": "post"}),
        name="update_slct_quantity_slab_props",
    ),
    path(
        "update-slct-annual-disc-slab-based/",
        UpdateSlctAnnualDiscSlabBasedViewSet.as_view({"post": "post"}),
        name="update_slct_annual_disc_slab_based",
    ),
    path(
        "update-slct-annual-disc-target-based/",
        UpdateSlctAnnualDiscTargetBasedViewSet.as_view({"post": "post"}),
        name="update_slct_annual_disc_target_based",
    ),
    path(
        "update-slct-booster-per-day-target-scheme/",
        UpdateSlctBoosterPerDayTargetSchemeViewSet.as_view({"post": "post"}),
        name="update_slct_booster_per_day_target_scheme",
    ),
    path(
        "update-slct-booster-per-day-growth-scheme/",
        UpdateSlctBoosterPerDayGrowthSchemeViewSet.as_view({"post": "post"}),
        name="update_slct_booster_per_day_growth_scheme",
    ),
    path(
        "update-slct-inkind-tour-propsal/",
        UpdateSlctInKindTourPropsalViewSet.as_view({"post": "post"}),
        name="update_slct_inkind_tour_proposal",
    ),
    path(
        "update-slct-inkind-booster-scheme-props/",
        UpdateSlctInKindBoosterSchemePropsViewSet.as_view({"post": "post"}),
        name="update_slct_inkind_booster_scheme_props",
    ),
    path(
        "update-slct-prm-prdcombo-scm-props/",
        UpdateSlctPrmPrdComboScmPropsViewSet.as_view({"post": "post"}),
        name="update_slct_prm_prdcombo_scm_props",
    ),
    path(
        "update-slct-dir-plt-billing-props/",
        UpdateSlctDirPltBilngDiscPropsViewSet.as_view({"post": "post"}),
        name="update_slct_dir_plt_billing_props",
    ),
    path(
        "update-slct-border-disc-props/",
        UpdateSlctBorderDiscPropsViewSet.as_view({"post": "post"}),
        name="update_slct_border_disc_props",
    ),
    path(
        "update-slct-activity-props/",
        UpdateSlctActivityPropsViewSet.as_view({"post": "post"}),
        name="update_slct_activity_props",
    ),
    path(
        "update-slct-vol-cutter-slab-based-props/",
        UpdateSlctVolCutterSlabBasedProposalViewSet.as_view({"post": "post"}),
        name="update_slct_vol_cutter_slab_based_props",
    ),
    path(
        "update-slct-vol-cutter-target-based-props/",
        UpdateSlctVolCutterTargetBasedViewSet.as_view({"post": "post"}),
        name="update_slct_vol_cutter_target_based_props",
    ),
    path(
        "update-slct-eng-cash-sch-props/",
        UpdateSlctEngCashSchPtPropsViewSet.as_view({"post": "post"}),
        name="update_slct_eng_cash_sch_props",
    ),
    path(
        "update-slct-mason-kind-sch-props/",
        UpdateSlctMasonKindSchPropsViewSet.as_view({"post": "post"}),
        name="update_slct_mason_kind_sch_props",
    ),
    path(
        "update-slct-dealer-linkind-sch-props/",
        UpdateSlctDealerLinkedSchPropsViewSet.as_view({"post": "post"}),
        name="update_slct_linked_sch_props",
    ),
    path(
        "update-slct-vechile-sch-props/",
        UpdateSlctVehicleSchPropsViewSet.as_view({"post": "post"}),
        name="update_slct_vechile_sch_props",
    ),
    path(
        "update-slct-dealer-outs-based-props/",
        UpdateSlctDealerOutsBasedPropsViewSet.as_view({"post": "post"}),
        name="update_slct_dealer_out_based_props",
    ),
    path(
        "update-slct-rail-based-sch-props/",
        UpdateSlctRailBasedSchPropsViewSet.as_view({"post": "post"}),
        name="update_slct_rail_based_sch_props",
    ),
    path(
        "update-slct-price-change-req-exist-markt/",
        UpdateSlctPriceChangeRequestExistingMarktViewSet.as_view({"post": "post"}),
        name="update_slct_price_change_req_exist_markt",
    ),
    path(
        "update-slct-bench-mark-change-req/",
        UpdateSlctBenchmarkChangeRequestViewSet.as_view({"post": "post"}),
        name="update_slct_bench_mark_change_req",
    ),
    path(
        "update-slct-markt-pricing-req/",
        UpdateSlctNewMarketPricingRequestViewSet.as_view({"post": "post"}),
        name="update_slct_markt_pricing_req",
    ),
    path(
        "slct-cash-disc-props/<int:id>",
        SlctCashDiscPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_cash_disc_props",
    ),
    path(
        "slct-quantity-slab-props/",
        SlctQuantitySlabPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_quantity_slab_props",
    ),
    path(
        "slct-quantity-slab-props/<int:id>",
        SlctQuantitySlabPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_quantity_slab_props",
    ),
    path(
        "slct-direct-plant-billing-discount-props/",
        SlctDirPltBilngDiscPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_direct_plant_billing_disc_props/",
    ),
    path(
        "slct-direct-plant-billing-discount-props/<int:id>",
        SlctDirPltBilngDiscPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_direct_plant_billing_disc_props/",
    ),
    path(
        "slct-premium-product-combo-scheme-props/",
        SlctPrmPrdComboScmPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_premium_product_combo_scheme_props/",
    ),
    path(
        "slct-premium-product-combo-scheme-props/<int:id>",
        SlctPrmPrdComboScmPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_premium_product_combo_scheme_props/",
    ),
    path(
        "slct-vehicle-scheme-proposal/",
        SlctVehicleSchPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_vehicle_scheme_proposal/",
    ),
    path(
        "slct-vehicle-scheme-proposal/<int:id>",
        SlctVehicleSchPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_vehicle_scheme_proposal/",
    ),
    path(
        "crm-infl-mgr-meet-plan/",
        CrmInflMgrMeetPlanViewSet.as_view({"get": "list"}),
        name="crm_infl_mgr_meet_plan/",
    ),
    path(
        "crm-infl-mgr-annual-plan/",
        CrmInflMgrAnnualPlanViewSet.as_view({"get": "list"}),
        name="crm_infl_mgr_annual_plan/",
    ),
    path(
        "crm-infl-mgr-meet-plan/<int:id>",
        CrmInflMgrMeetPlanViewSet.as_view({"patch": "partial_update"}),
        name="crm_infl_mgr_meet_plan/",
    ),
    path(
        "crm-infl-mgr-annual-plan/<int:id>",
        CrmInflMgrAnnualPlanViewSet.as_view({"patch": "partial_update"}),
        name="crm_infl_mgr_annual_plan/",
    ),
    path(
        "shiftwise-adhoc-quantity/",
        ShiftWiseAdhocQtyViewSet.as_view({"get": "list"}),
        name="shiftwise_adhoc_quantity/",
    ),
    path(
        "shiftwise-adhoc-quantity/<int:id>",
        ShiftWiseAdhocQtyViewSet.as_view({"patch": "partial_update"}),
        name="shiftwise_adhoc_quantity/",
    ),
    path(
        "slct-border-discount-prop/",
        SlctBorderDiscPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_border_discount_prop/",
    ),
    path(
        "slct-border-discount-prop/<int:id>",
        SlctBorderDiscPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_border_discount_prop/",
    ),
    path(
        "slct-activity-props-data/",
        SlctActivityPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_activity_props_data/",
    ),
    path(
        "slct-activity-props-data/<int:id>",
        SlctActivityPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_activity_props_data/",
    ),
    path(
        "slct-mason-kind-sch-props/",
        SlctMasonKindSchPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_mason_kind_sch_props/",
    ),
    path(
        "slct-mason-kind-sch-props/<int:id>",
        SlctMasonKindSchPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_mason_kind_sch_props/",
    ),
    path(
        "nt_head_annual_sales_plan/",
        FactNtSalesPlanAnnualViewSet.as_view({"post": "create"}),
        name="nt_head_annual_sales_plan",
    ),
    path(
        "consensus_target_for_nt_head_annual_sales_plan/",
        ConsensusTargetForNtViewSet.as_view({"post": "create"}),
        name="consensus_target_for_nt_head_annual_sales_plan",
    ),
    path(
        "fact-nt-sales-planning-ncr/",
        FactNtSalesPlanningNcrViewSet.as_view({"get": "list"}),
        name="fact_nt_sales_planning_ncr",
    ),
    path(
        "fact_nt_sales_planning_monthly/",
        FactNtSalesPlanningMonthViewSet.as_view({"get": "list", "post": "post"}),
        name="fact_nt_sales_planning_monthly",
    ),
    path(
        "fact_nt_sales_planning_month_previous_month_data/",
        FactNtSalesPlanningMonthGetPreviousMonthDataViewSet.as_view({"get": "get"}),
        name="fact_nt_sales_planning_month_previous_month_data",
    ),
    path(
        "fact_nt_sales_planning_ncr_previous_month_data/",
        FactNtSalesPlanningNcrGetPreviousMonthDataViewSet.as_view({"get": "get"}),
        name="fact_nt_sales_planning_ncr_previous_month_data",
    ),
    path(
        "consensus_target_total_target_by_month/",
        ConsensusTargetForNtTargetSumViewSet.as_view({"get": "get"}),
        name="consensus_target_total_target_by_month/",
    ),
    path(
        "sum_od_every_month_annualy/",
        SumForAnnualTargetColumnWise.as_view(),
        name="sum_od_every_month_annual",
    ),
    path(
        "slct-engineer-scheme-point-proposal-data/",
        SlctEngCashSchPtPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_engineer_scheme_point_proposal_data/",
    ),
    path(
        "slct-engineer-scheme-point-proposal-data/<int:id>",
        SlctEngCashSchPtPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_engineer_scheme_point_proposal_data/",
    ),
    path(
        "crm-influencer-manager-scheme-budget/",
        CrmInflMgrSchemeBudgetViewSet.as_view({"get": "list", "post": "post"}),
        name="crm_influencer_manager_scheme_budget",
    ),
    path(
        "crm-influencer-manager-scheme-budget/<int:id>",
        CrmInflMgrSchemeBudgetViewSet.as_view({"patch": "partial_update"}),
        name="crm_influencer_manager_scheme_budget",
    ),
    path(
        "slct-rail-based-sch-props/",
        SlctRailBasedSchPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_rail_based_sch_props/",
    ),
    path(
        "slct-rail-based-sch-props/<int:id>",
        SlctRailBasedSchPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_rail_based_sch_props/",
    ),
    path(
        "slct-dealer-outstanding-scheme-proposal/",
        SlctDealerOutsBasedPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_dealer_outstanding_scheme_proposal/",
    ),
    path(
        "slct-dealer-outstanding-scheme-proposal/<int:id>",
        SlctDealerOutsBasedPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_dealer_outstanding_scheme_proposal/",
    ),
    path(
        "slct-dealer-linked-sch-props/",
        SlctDealerLinkedSchPropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_dealer_linked_sch_props/",
    ),
    path(
        "slct-dealer-linked-sch-props/<int:id>",
        SlctDealerLinkedSchPropsViewSet.as_view({"patch": "partial_update"}),
        name="slct_dealer_linked_sch_props/",
    ),
    path(
        "slct-annual-disc-proposal-target/",
        SlctAnnualDiscTargetBasedViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_annual_disc_proposal_target/",
    ),
    path(
        "slct-annual-disc-proposal-target/<int:id>",
        SlctAnnualDiscTargetBasedViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="slct_annual_disc_proposal_target/",
    ),
    path(
        "slct-annual-disc-slab-based/",
        SlctAnnualDiscSlabBasedViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_annual_disc_slab_based/",
    ),
    path(
        "slct-annual-disc-slab-based/<int:id>",
        SlctAnnualDiscSlabBasedViewSet.as_view({"patch": "partial_update"}),
        name="slct_annual_disc_slab_based/",
    ),
    path(
        "sales-planning-market-mapping-run-model/",
        MarketMappingRunRunModel.as_view(),
        name="sales-planning-market-mapping-run-model",
    ),
    path(
        "demand-spilit-run-view/", DemandSplitView.as_view(), name="demand=spilit-view/"
    ),
    # SLCT_COMB_SLAB_GROWTH_PROPS api urls:
    path(
        "slab-growth-based-scheme-proposal/",
        SlctCombSlabGrowthPropsViewSet.as_view({"post": "post", "get": "list"}),
        name="slab_growth_brased_scheme_proposal",
    ),
    path(
        "slab-growth-based-scheme-proposal/<int:id>",
        SlctCombSlabGrowthPropsViewSet.as_view({"get": "retrieve"}),
        name="slab_growth_brased_scheme_proposal",
    ),
    path(
        "update-slab-growth-based-scheme-proposal/",
        UpdateSlctCombSlabGrowthPropsViewSet.as_view({"post": "post"}),
        name="update_slab_growth_brased_scheme_proposal",
    ),
    path(
        "slct-vol-cutter-target-based/",
        SlctVolCutterTargetBasedViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_vol_cutter_target_based",
    ),
    path(
        "slct-vol-cutter-slab-based-proposal/",
        SlctVolCutterSlabBasedProposalViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_vol_cutter_slab_based_proposal",
    ),
    path(
        "slct-vol-cutter-slab-based-proposal/<int:id>",
        SlctVolCutterSlabBasedProposalViewSet.as_view({"patch": "partial_update"}),
        name="slct_vol_cutter_slab_based_proposal/",
    ),
    path(
        "slct-vol-cutter-target-based/<int:id>",
        SlctVolCutterTargetBasedViewSet.as_view({"patch": "partial_update"}),
        name="slct_vol_cutter_target_based/",
    ),
    path(
        "market-mapping-sales-target-download/",
        MarketMappingSalesTargetViewSet.as_view({"get": "download"}),
        name="market_mapping_sales_target_download_upload",
    ),
    # market mapping download APIs:
    path(
        "market-mapping-pricing-output-download/",
        MarketMappingPricingOutputViewSet.as_view({"get": "download"}),
        name="sales_planning_market_mapping_run_model_download",
    ),
    path(
        "market-mapping-branding-output-download/",
        MarketMappingBrandingOuputViewSet.as_view({"get": "download"}),
        name="market_mapping_target_download",
    ),
    path(
        "market-mapping-channel-strategy-download/",
        MarketMappingChannelStrategyViewSet.as_view({"get": "download"}),
        name="market_mapping_channel_strategy_download",
    ),
    path(
        "market-mapping-counter-strategy-download/",
        MarketMappingCounterStrategyViewSet.as_view({"get": "download"}),
        name="market_mapping_counter_strategy_download",
    ),
    path(
        "market-mapping-district-classification-download/",
        MarketMappingDistrictClassificationViewSet.as_view({"get": "download"}),
        name="market_mapping_district_classification_download",
    ),
    path(
        "market-mapping-state-classification-download/",
        MarketMappingStateClassificationViewSet.as_view({"get": "download"}),
        name="market_mapping_state_classification_download",
    ),
    path(
        "bottom-up-targets-monthly-2-download-upload/",
        DfBottomUpTargetsMonthly2ViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="bottom_up_targets_monthly_2_download_upload",
    ),
    path(
        "bottom-up-nt-download-upload/",
        BottomUpNtViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="bottom_up_nt_download_upload",
    ),
    path(
        "bottom-up-nt/",
        BottomUpNtViewSet.as_view({"get": "list", "put": "update"}),
        name="bottom_up_nt",
    ),
    path(
        "get-downtime-data/",
        GetDowntimeDataViewSet.as_view({"get": "get"}),
        name="get-downtime-data/",
    ),
    # path(
    #     "save-downtime-data/",
    #     PpDowntimeEntryViewSet.as_view(),
    #     name="save_downtime_data/",
    # ),
    path(
        "save-adhoc-qty-data/",
        ShiftWiseAdhocQtyBulkCreateViewSet.as_view(),
        name="save_downtime_data/",
    ),
    path(
        "get-adhoc-qty-data/",
        GetAdhocQtyListViewSet.as_view(),
        name="get_adhoc_qty_data",
    ),
    path(
        "update-adhoc-qty-data/",
        UpdateAdhocQtyListViewSet.as_view(),
        name="update_adhoc_qty_data",
    ),
    # path(
    #     "update-pp-downtime-data/",
    #     UpdatePpDowntimeListViewSet.as_view(),
    #     name="update_pp_downtime_data",
    # ),
    path(
        "slct-booster-per-day-target-based/",
        SlctBoosterPerDayTargetSchemeViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_booster_per_day_target_based",
    ),
    path(
        "slct-booster-per-day-target-based/<int:id>",
        SlctBoosterPerDayTargetSchemeViewSet.as_view({"patch": "partial_update"}),
        name="slct_vol_cutter_target_based/",
    ),
    path(
        "slct-booster-per-day-growth-based/",
        SlctBoosterPerDayGrowthSchemeViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_booster_per_day_growth_based",
    ),
    path(
        "slct-booster-per-day-growth-based/<int:id>",
        SlctBoosterPerDayGrowthSchemeViewSet.as_view({"patch": "partial_update"}),
        name="slct_vol_cutter_growth_based/",
    ),
    path(
        "slct-bench-mark-change-request/",
        SlctBenchmarkChangeRequestViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_bench_mark_change_request/",
    ),
    path(
        "slct-bench-mark-change-request/<int:id>",
        SlctBenchmarkChangeRequestViewSet.as_view({"patch": "partial_update"}),
        name="slct_bench_mark_change_request/",
    ),
    path(
        "slct-price-change-request-existing-mrkt/",
        SlctPriceChangeRequestExistingMarktViewSet.as_view(
            {"get": "list", "post": "post"}
        ),
        name="slct_price_change_request_existing_mrkt/",
    ),
    path(
        "in-kind-tour-proposal/",
        SlctInKindTourProposalViewSet.as_view({"post": "create", "get": "list"}),
        name="in_kind_tour_proposal",
    ),
    path(
        "in-kind-tour-proposal/<int:id>",
        SlctInKindTourProposalViewSet.as_view({"get": "retrieve"}),
        name="in_kind_tour_proposal",
    ),
    path(
        "pp-rail-order-tagging-value-packing-plant/",
        PpRailOrderTaggingValueViewSet.as_view(),
        name="pp_rail_order_tagging_value_packing_plant",
    ),
    path(
        "get-all-vendors/",
        GetAllVendorsViewSet.as_view({"get": "get"}),
        name="get_all_vendors",
    ),
    path(
        "slct-scheme-discount-proposal/",
        SlctSchemeDiscountProposalViewSet.as_view({"post": "create", "get": "list"}),
        name="slct_scheme_discount_proposal",
    ),
    path(
        "update-slct-scheme-discount-proposal/",
        UpdateSlctSchemeDiscountProposalViewSet.as_view({"post": "post"}),
        name="udate_slct_scheme_discount_proposal",
    ),
    path(
        "slct-scheme-discount-proposal/<int:pk>/",
        SlctSchemeDiscountProposalViewSet.as_view({"get": "retrieve"}),
        name="slct_scheme_discount_proposal",
    ),
    path(
        "get-cash-disc-props-by-id/",
        SlctCashDiscPropsByIDViewSet.as_view({"get": "get"}),
        name="get_state_case_study_data_by_id",
    ),
    path(
        "get-slct-quantity-props-by-id/",
        SlctQuantitySlabPropsByIdViewSet.as_view({"get": "get"}),
        name="get_slct_quantity_props_by_id",
    ),
    path(
        "slct-party-wise-scheme-props-data-by-id/",
        SlctPartyWiseSchemePropsByIdViewSet.as_view({"get": "get"}),
        name="slct_party_wise_scheme_props_data_by_id",
    ),
    path(
        "slct-new-market-pricing-request/",
        SlctNewMarketPricingRequestViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_new_market_pricing_request/",
    ),
    path(
        "slct-branding-request/",
        SlctBrandingRequestsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_branding_request/",
    ),
    path(
        "slct-inkind-booster-scheme/",
        SlctInKindBoosterSchemePropsViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_inkind_booster_scheme/",
    ),
    path(
        "slct-annual-sales-plan-data/",
        SlctAnnualSalesPlanViewSet.as_view({"get": "list", "post": "post"}),
        name="slct_annual_sales_plan_data/",
    ),
    path(
        "slct-annual-sales-plan-data/<int:id>",
        SlctAnnualSalesPlanViewSet.as_view({"patch": "partial_update"}),
        name="slct_annual_sales_plan_data",
    ),
    # path(
    #     "slct-monthly-sales-plan-data/",
    #     SlctMonthlySalesPlanViewSet.as_view({"get": "list", "post": "post"}),
    #     name="slct_monthly_sales_plan_data/",
    # ),
    # path(
    #     "slct-monthly-sales-plan-data/<int:id>",
    #     SlctMonthlySalesPlanViewSet.as_view({"patch": "partial_update"}),
    #     name="slct_monthly_sales_plan_data",
    # ),
    path(
        "reason-for-delay-get/",
        MvPendingReasonsForDelayViewSet.as_view({"get": "list"}),
        name="reason-for-delay-get",
    ),
    path(
        "reason-for-delay-dropdown/",
        MvPendingReasonsForDelayDropdown.as_view(),
        name="reason_for_delay_dropdown",
    ),
    path(
        "reason-for-delay-get/<int:delivery_detail_id>",
        MvPendingReasonsForDelayViewSet.as_view({"patch": "partial_update"}),
        name="reason-for-delay-get",
    ),
    path(
        "get-plant-depo-sla-plant-and-product/",
        GetPlantDepoSlaPlantAndProductList.as_view({"get": "get"}),
        name="get-plant-depo-sla-plant-and-product",
    ),
    path(
        "get-slct-activity-props-data-by-id/",
        SlctActivityPropsByIdViewSet.as_view({"get": "get"}),
        name="get_slct_activity_props_data_by_id",
    ),
    path(
        "get-slct-annual-sales-plan-data-by-id/",
        SlctAnnualSalesPlanByIdViewSet.as_view({"get": "get"}),
        name="get_slct_annual_sales_plan_data_by_id",
    ),
    path(
        "get-border-discount-data-by-id/",
        SlctBorderDiscPropsByIdViewSet.as_view({"get": "get"}),
        name="get_border_discount_data_by_id",
    ),
    path(
        "get-vehicle-scheme-data-by-id/",
        SlctVehicleSchPropsByIdViewSet.as_view({"get": "get"}),
        name="get_vehicle_scheme_data_by_id",
    ),
    path(
        "get-branding-request-data-by-id/",
        SlctBrandingRequestsByIdViewSet.as_view({"get": "get"}),
        name="get_branding_request_data_by_id",
    ),
    path(
        "get-monthly-sales-plan-data-by-id/",
        SlctMonthlySalesPlanByIdViewSet.as_view({"get": "get"}),
        name="get_monthly_sales_plan_data_by_id",
    ),
    path(
        "vehicle-data-dropdown/",
        TOebsXxsclVehicleMasterViewSet.as_view(),
        name="vhecile-data_dropdown",
    ),
    path(
        "get-engineer-cash-scheme-data-by-id/",
        SlctEngCashSchPtPropsByIdViewSet.as_view({"get": "get"}),
        name="get_engineer_cash_scheme_data_by_id",
    ),
    path(
        "get-mason-kind-scheme-data-by-id/",
        SlctMasonKindSchPropsByIdViewSet.as_view({"get": "get"}),
        name="get_mason_kind_scheme_data_by_id",
    ),
    path(
        "get-rail-based-scheme-data-by-id/",
        SlctRailBasedSchPropsByIdViewSet.as_view({"get": "get"}),
        name="get_rail_based_scheme_data_by_id",
    ),
    path(
        "get-inkind-tour-props-data-by-id/",
        SlctInKindTourProposalByIdViewSet.as_view({"get": "get"}),
        name="get_inkind_tour_props_data_by_id",
    ),
    path(
        "get-annual-disc-slab-based-data-by-id/",
        SlctAnnualDiscSlabBasedByIdViewSet.as_view({"get": "get"}),
        name="get_annual_disc_slab_based_data_by_id",
    ),
    path(
        "get-comb-slab-growth-data-by-id/",
        SlctCombSlabGrowthPropsByIdViewSet.as_view({"get": "get"}),
        name="get_comb_slab_growth_data_by_id",
    ),
    path(
        "get-gap-with-other-product-data-by-id/",
        SlctGapWithOtherProductByIdViewSet.as_view({"get": "get"}),
        name="get_gap_with_other_product_data_by_id",
    ),
    path(
        "get-premium-product-combo-data-by-id/",
        SlctPrmPrdComboScmPropsByIdViewSet.as_view({"get": "get"}),
        name="get_premium_product_combo_data_by_id",
    ),
    path(
        "get-dealer-linked-scheme-data-by-id/",
        SlctDealerLinkedSchPropsByIdViewSet.as_view({"get": "get"}),
        name="get_dealer_linked_scheme_data_by_id",
    ),
    path(
        "get-dealer-outstanding-data-by-id/",
        SlctDealerOutsBasedPropsByIdViewSet.as_view({"get": "get"}),
        name="get_dealer_outstanding_data_by_id",
    ),
    path(
        "get-direct-plant-billing-data-by-id/",
        SlctDirPltBilngDiscPropsByIdViewSet.as_view({"get": "get"}),
        name="get_direct_plant_billing_data_by_id",
    ),
    path(
        "get-volume-cutter-target-based-data-by-id/",
        SlctVolCutterTargetBasedByIdViewSet.as_view({"get": "get"}),
        name="get_volume_cutter_target_based_data_by_id",
    ),
    path(
        "get-annual-discount-target-based-data-by-id/",
        SlctAnnualDiscTargetBasedByIdViewSet.as_view({"get": "get"}),
        name="get_annual_discount_target_based_data_by_id",
    ),
    path(
        "get-benchmark-change-request-data-by-id/",
        SlctBenchmarkChangeRequestByIdViewSet.as_view({"get": "get"}),
        name="get_benchmark_change_request_data_by_id",
    ),
    path(
        "get-new-market-pricing-request-data-by-id/",
        SlctNewMarketPricingRequestByIdViewSet.as_view({"get": "get"}),
        name="get_new_market_pricing_request_data_by_id",
    ),
    path(
        "get-inkind-booster-scheme-data-by-id/",
        SlctInKindBoosterSchemePropsByIdViewSet.as_view({"get": "get"}),
        name="get_inkind_booster_scheme_data_by_id",
    ),
    path(
        "get-booster-growth-scheme-data-by-id/",
        SlctBoosterPerDayGrowthSchemeByIdViewSet.as_view({"get": "get"}),
        name="get_booster_growth_scheme_data_by_id",
    ),
    path(
        "get-booster-target-scheme-data-by-id/",
        SlctBoosterPerDayTargetSchemeByIdViewSet.as_view({"get": "get"}),
        name="get_booster_target_scheme_data_by_id",
    ),
    path(
        "get-volume-cutter-slab-based-data-by-id/",
        SlctVolCutterSlabBasedProposalByIdViewSet.as_view({"get": "get"}),
        name="get_volume_cutter_slab_based_data_by_id",
    ),
    path(
        "get-price-change-request-existing-market-data-by-id/",
        SlctPriceChangeRequestExistingMarktByIdViewSet.as_view({"get": "get"}),
        name="get_price_change_request_existing_market_data_by_id",
    ),
    path(
        "handling-agent-dashboard-dropdown/",
        HandingAgentDashboardDropdown.as_view(),
        name="handling_agent_dashboard_dropdown",
    ),
    path(
        "handling-agent-dashboard/",
        HandlingAgentDashboard.as_view(),
        name="handling_agent_dashboard",
    ),
    path("monthly-nth-budget/", MonthlyNthBudget.as_view(), name="monthly_nth_budget"),
    path(
        "dim-product-test-dropdown/",
        DimProductTestDropdown.as_view(),
        name="dim_product_test_dropdown",
    ),
    path(
        "missing-demand-sample-download/",
        SampleDownloadView.as_view(),
        name="missing_demand_sample_download",
    ),
    path(
        "zone-mapping-new-dropdown/",
        ZoneMappingNewDropdown.as_view(),
        name="zone_mapping_new_dropdown",
    ),
    path(
        "demand-spilit-missing-run-view/",
        DemandSplitMissingView.as_view(),
        name="demand-spilit-missing-run-view",
    ),
    path(
        "tgt-plant-silo-capacity/",
        TGTPlantSiloCapacityViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_plant_silo_capacity",
    ),
    path(
        "tgt-mrn-data/",
        TgtMrnDataViewSet.as_view({"get": "list"}),
        name="tgt_mrn_data",
    ),
    path(
        "tgt-mrn-data/<int:pk>",
        TgtMrnDataViewSet.as_view({"get": "retrieve"}),
        name="tgt_mrn_data",
    ),
    path(
        "tgt-plant-silo-capacity/<int:id>",
        TGTPlantSiloCapacityViewSet.as_view({"patch": "partial_update"}),
        name="tgt_plant_silo_capacity",
    ),
    path(
        "tgt-plant-silo-capacity-dropdown/",
        TgtPlantSiloCapacityDropdown.as_view(),
        name="tgt_plant_silo_capacity_dropdown",
    ),
    path(
        "godown-performance/",
        GodownPerformance.as_view(),
        name="godown_performance",
    ),
    path(
        "godown-tat/",
        GodownTat.as_view(),
        name="godown_tat",
    ),
    path(
        "road-rake-coordinator-freight-discovery/",
        RoadRakeCoordinatorAPIView.as_view({"post": "create"}),
        name="road_rake_coordinator_freight_discovery",
    ),
    path(
        "road-rake-coordinator-freight-discovery-download/<int:id>",
        RoadRakeCoordinatorAPIView.as_view({"get": "download"}),
        name="road_rake_coordinator_freight_discovery_download",
    ),
    path(
        "road-rake-coordinator-freight-discovery/<int:id>",
        RoadRakeCoordinatorAPIView.as_view({"put": "update", "get": "retrieve"}),
        name="road_rake_coordinator_freight_discovery",
    ),
    path(
        "waterfall-chart-inventory/",
        WaterfallChartInventoryViewSet.as_view(),
        name="waterfall_chart_inventory",
    ),
    path(
        "waterfall-chart-inventory-product-dropdown/",
        WaterFallChartInventoryDropdownViewSet.as_view({"get": "get"}),
        name="waterfall_chart_inventory",
    ),
    path(
        "tgt-slh-service-level-depo/",
        TgtSlhServiceLevelDepoAPIView.as_view(),
        name="tgt_slh_service_level_depo",
    ),
    path(
        "product-wise-inventory-data/",
        ProductWiseInventory.as_view({"get": "get"}),
        name="product_wise_inventory_data",
    ),
    path(
        "monthly-inventory-data/",
        MonthlyInventory.as_view({"get": "get"}),
        name="monthly_inventory_data",
    ),
    path(
        "date-wise-inventory-data/",
        DayWiseInventory.as_view({"get": "get"}),
        name="date_wise_inventory_data",
    ),
    path(
        "plant-depo-master-dropdown/",
        PlantDepoMasterDropdownView.as_view(),
        name="plant_depo_master_dropdown",
    ),
    # rake report urls:
    path(
        "tgt-rake-loading/",
        TgtRakeLoadingViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_rake_loading",
    ),
    path(
        "tgt-rake-loading/<int:rake_id>",
        TgtRakeLoadingViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="tgt_rake_loading",
    ),
    path(
        "tgt-rake-loading-details/",
        TgtRakeLoadingDetailsViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_rake_loading_details",
    ),
    path(
        "tgt-rake-loading-details/<int:rld_id>",
        TgtRakeLoadingDetailsViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="tgt_rake_loading_details",
    ),
    path(
        "tgt-rake-charges/",
        TgtRakeChargesViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_rake_charges",
    ),
    path(
        "tgt-rake-charges/<int:rc_id>",
        TgtRakeChargesViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="tgt_rake_charges",
    ),
    path(
        "tgt-rake-unloading-details/",
        TgtRakeUnloadingDetailsViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_rake_unloading_details",
    ),
    path(
        "tgt-rake-unloading-details/<int:rk_unload_id>",
        TgtRakeUnloadingDetailsViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="tgt_rake_unloading_details",
    ),
    path(
        "tgt-rake-disposals/",
        TgtRakeDisposalsViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_disposal_charges",
    ),
    path(
        "tgt-rake-disposals/<int:rd_rk_unload_id>",
        TgtRakeDisposalsViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="tgt_disposal_charges",
    ),
    path(
        "tgt-daywise-lifting/",
        TgtDayWiseLiftingViewSet.as_view({"post": "create", "get": "list"}),
        name="tgt_daywise_lifting",
    ),
    path(
        "tgt-daywise-lifting/<int:daywise_lifting_id>",
        TgtDayWiseLiftingViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
        name="tgt_daywise_lifting",
    ),
    path(
        "toebs-scl-address-link-dropdown/",
        TOebsSclAddressLinkDropdown.as_view(),
        name="toebs_scl_address_link_dropdown",
    ),
    path(
        "vendor-detail-master-dropdown/",
        VendorDetailMasterDropdown.as_view(),
        name="vendor-detail-master-dropdown",
    ),
    path(
        "dim-customer-test-data/",
        DimCustomersTestViewSet.as_view({"get": "list"}),
        name="dim_customer_test_data",
    ),
    path(
        "stock-availability-data/",
        StockAvailabilityViewSet.as_view(),
        name="stock_availability_data",
    ),
    path(
        "stock-availability-in-depo-data/",
        StockAvailabilityindepot.as_view(),
        name="stock_availability_in_depo_data",
    ),
    path(
        "tgt-slh-order-pendency/",
        TgtSlhOrderPendencyViewSet.as_view({"get": "list"}),
        name="tgt_slh_order_pendency",
    ),
    path(
        "lp-scheduling-di-detail/",
        LpSchedulingDiDtlViewSet.as_view(),
        name="lp_scheduling_di_detail",
    ),
    path(
        "lp-scheduling-di-detail-dropdown/",
        LpSchedulingDiDtlDropdownViewSet.as_view(),
        name="lp_scheduling_di_detail_dropdown",
    ),
    path(
        "tgt-bridging-cost/",
        TgtBridgingCostViewSet.as_view({"get": "list", "post": "create"}),
        name="tgt_bridging_cost",
    ),
    path(
        "tgt-bridging-cost/<int:id>",
        TgtBridgingCostViewSet.as_view({"put": "update"}),
        name="tgt_bridging_cost",
    ),
    path(
        "tgt-bridging-cost-dropdown/",
        TgtBridgingCostAPIView.as_view(),
        name="tgt_bridging_cost_dropdown",
    ),
    path(
        "slct-download-excel/",
        SlctDownloadExcel.as_view(),
        name="slct_download_excel",
    ),
    path(
        "district-classification-run/",
        DistrictClassification.as_view(),
        name="district-classification-run",
    ),
    path(
        "influncer-manager-run-model/",
        InfluencerMeetFreeRunInputView.as_view(),
        name="influncer-manager-run-model",
    ),
    path(
        "get-stoppage-description-list/",
        GetStoppageDescriptionList.as_view({"get": "get"}),
        name="get_stoppage_description_list",
    ),
    path(
        "update-packer-shift-stoppage-data/",
        UpdatePackerShiftLevelStoppagesListViewSet.as_view(),
        name="update_packer_shift_stoppage_data",
    ),
    path(
        "crm-influencer-output-data/",
        InfluencerOutputViewSet.as_view({"get": "get"}),
        name="crm_influencer_output_data/",
    ),
    path(
        "influencer-tech-activity-dropdown/",
        InfluencerTechActivityMasterDropdown.as_view({"get": "get"}),
        name="influencer_tech_activity_dropdown",
    ),
    path(
        "influencer-output-download-api/",
        InfluencerOutputView.as_view({"get": "download"}),
        name="influencer_output_data",
    ),
    path(
        "influencer-meet-budget-output/",
        InfluencerMeetBudgetOutputAPIView.as_view(),
        name="influencer_meet_budget_output",
    ),
    path(
        "back-unloading-enroute-market-master/",
        BackUnloadingEnrouteMarketsMasterViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="back_unloading_enroute_market_master",
    ),
    path(
        "back-unloading-enroute-market-master/<int:id>",
        BackUnloadingEnrouteMarketsMasterViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="back_unloading_enroute_market_master",
    ),
    path(
        "back-unloading-enroute-market-master-dropdown/",
        BackUnloadingEnrouteMarketsMasterDropdownView.as_view(),
        name="back_unloading_enroute_market_master_dropdown",
    ),
    path(
        "backhualing-process-detail-dropdown/",
        BackhaulingProcessDropdownViewSet.as_view({"get": "list", "post": "post"}),
        name="backhualing_process_detail_dropdown",
    ),
    path(
        "demand-backhualing-process-detail-dropdown/",
        DemandBackhaulingProcessViewSet.as_view({"get": "get"}),
        name="demand_backhualing_process_detail_dropdown",
    ),
    path(
        "competition-price-download-api/",
        CompetitionPriceNewMarketsDownloadUploadViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="competition_price_download_data",
    ),
    path(
        "competition-price-new-market/",
        CompetitionPriceNewMarketsDownloadUploadViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="competition-price-new-market",
    ),
    path(
        "price-benchmarks-download-api/",
        PriceBenchmarksDownloadUploadViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="price_benchmarks_download_api",
    ),
    path(
        "price-benchmarks-data/",
        PriceBenchmarksDownloadUploadViewSet.as_view({"get": "list", "put": "update"}),
        name="price_benchmarks_data",
    ),
    path(
        "iframes/",
        IFramesUrlMapping.as_view(),
        name="iframes",
    ),
    path(
        "depot-addition-master/",
        DepotAdditionMasterViewSet.as_view({"get": "list", "post": "create"}),
        name="depo_addition_master",
    ),
    path(
        "depot-addition-master-download-upload/",
        DepotAdditionMasterViewSet.as_view({"get": "download", "put": "upload_update"}),
        name="depot_addition_master_download_upload",
    ),
    path(
        "depot-addition-master/<int:id>",
        DepotAdditionMasterViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="depo_addition_master",
    ),
    path(
        "new-price-computation/",
        NewPriceComputationViewSet.as_view(
            {"post": "post", "get": "list", "patch": "update"}
        ),
        name="new_price_computation",
    ),
    path(
        "new-price-computation-get-benchmark-data/",
        NewPriceComputationGetBenchmarkViewSet.as_view(),
        name="new_price_computation_get_benchmark_data",
    ),
    path(
        "depot-addition-master-dropdown/",
        DepotAdditionMasterDropdownViewSet.as_view(),
        name="depot_addition_master_dropdown",
    ),
    path(
        "depot-addition-output/",
        DepotAdditionOutputViewSet.as_view({"get": "list"}),
        name="depot_addition_output",
    ),
    path(
        "depot-addition-output-dropdown/",
        DepotAdditionOutputDropdownViewSet.as_view(),
        name="depot_addition_output_dropdown",
    ),
    path(
        "average-depot-addition-output/",
        AverageDepotAdditionOutputView.as_view(),
        name="average_depot_addition_output",
    ),
    path(
        "bag-burst-dispatch-qty-by-plant/",
        BagBurstDispatchQty.as_view(),
        name="bag_burst_dispatch_qty_by_plant",
    ),
    path(
        "influencer-meeting-output-data/",
        InfluencerMeetingOutputViewSet.as_view({"get": "list"}),
        name="influencer_meeting_output_data",
    ),
    path(
        "so-augmentation-run-view/",
        SoAugmentationRunView.as_view(),
        name="so-augmentation-run-view",
    ),
    path(
        "depot-addition-run/",
        DepotAdditionOutputRunView.as_view(),
        name="depot-addition-run",
    ),
    path(
        "depot-addition-output-view-data/",
        DepotAdditionOutputViewViewSet.as_view({"get": "list"}),
        name="depot_addition_output_view_data",
    ),
    path(
        "slct-monthly-sales-plan-upload-download/",
        SlctMonthlySalesPlanDownloadViewSet.as_view(
            {"put": "upload_update", "get": "download"}
        ),
        name="slct_monthly_sales_plan_upload_download",
    ),
    path(
        "slct-monthly-sales-plan-data/",
        SlctMonthlySalesPlanDownloadViewSet.as_view(
            {"get": "list", "put": "update", "post": "create"}
        ),
        name="slct-monthly-sales-plan-data",
    ),
    path(
        "slct-annual-sales-plan-upload-download/",
        SlctAnnualSalesPlanDownloadViewSet.as_view(
            {"put": "upload_update", "get": "download"}
        ),
        name="slct_annual_sales_plan_upload_download",
    ),
    path(
        "new-freight-intitiation-status-count-view/",
        NewFreightInitiationStatusCountViewSet.as_view(),
        name="new_freight_intitiations_view",
    ),
    path(
        "freight-change-init-status-count-view/",
        FreightChangeInitiationStatusCountViewSet.as_view(),
        name="new_freight_intitiations_view",
    ),
    path(
        "new-freight-initiative-dropdown/",
        NewFreightInitiationDropdown.as_view(),
        name="new_freight_initiative_dropdown",
    ),
    path(
        "freight-initiation-dropdown/",
        FreightChangeInitiationDropdown.as_view(),
        name="freight_initiation_dropdown",
    ),
    path(
        "all_product-dropdown/",
        AllproductsDropdown.as_view(),
        name="all_product_dropdown",
    ),
    path(
        "freight-change-initiation/",
        FreightChangeInitiationViewSet.as_view(
            {"post": "create", "get": "list", "put": "update"}
        ),
        name="freight_change_initiation",
    ),
    path(
        "freight-change-initiation-dropdown/",
        FreightChangeInitiationDropdown.as_view(),
        name="FreightChangeInitiationDropdown",
    ),
    path(
        "freight-change-initiation-download-uplaod/",
        FreightChangeInitiationViewSet.as_view(
            {"put": "freight_change_upload_create", "get": "download"}
        ),
    ),
    path(
        "freight-change-initiation-request-count/",
        FreightChangeInitiationViewSet.as_view({"get": "request_count"}),
    ),
    path(
        "new-freight-initiation/",
        NewFreightInitiationViewSet.as_view(
            {"post": "create", "get": "list", "put": "update"}
        ),
        name="new_freight_initiation",
    ),
    path(
        "new-freight-initiation-request-count/",
        NewFreightInitiationViewSet.as_view({"get": "request_count"}),
    ),
    path(
        "scl-route-master-data/",
        TOebsSclRouteMasterViewSet.as_view({"get": "list"}),
        name="scl_route_master_data",
    ),
    path(
        "source-mapping-route-id-dropdown/",
        L1SourceMappingRouteIdDropdown.as_view(),
        name="source_mapping_route_id_dropdown",
    ),
    path(
        "source-mapping-data/",
        L1SourceMappingViewSet.as_view({"get": "list"}),
        name="source_mapping_data",
    ),
    path(
        "tgt-plant-depo-master-dropdown/",
        TgtPlantDepoMasterDropdown.as_view(),
        name="tgt-plant-depo-master-dropdown",
    ),
    path(
        "competition-price-new-market-dropdown/",
        CompetitionPriceNewMarketsDropdown.as_view(),
        name="competition-price-new-market-dropdown",
    ),
    path(
        "price-benchmarks-dropdown/",
        PriceBenchmarksDropdown.as_view(),
        name="price-benchmarks-dropdown",
    ),
    path(
        "new-price-computation-dropdown/",
        NewPriceComputationDropdown.as_view(),
        name="new-price-computation-dropdown",
    ),
    path(
        "augmentation-output-download-api/",
        AugmentationOutputTableDownloadAPIView.as_view({"get": "download"}),
        name="augmentation-output-download-api",
    ),
    path(
        "consensus-target-monthly-sales/",
        ConsensusTargetMonthlysalesplan.as_view(),
        name="consensus_target_monthly_sales",
    ),
    path(
        "nth-consensus-target-monthly-sales/",
        NTHConsensusTargetMonthlySalesPlan.as_view(),
        name="nth_consensus_target_monthly_sales",
    ),
    # path(
    #     "change-source-mode-total-impact/",
    #     SourceChangeModeTotalImpact.as_view(),
    #     name="change_source_mode_total_impact",
    # ),
    path(
        "change-source-mode/",
        SourceChangeModeViewSet.as_view({"get": "list"}),
        name="change_source_mode",
    ),
    path(
        "vpc-historical-dropdown/",
        VpcHistoricalDropdown.as_view(),
        name="vpc-historical-dropdown",
    ),
    path(
        "get-vpc-by-plant/",
        GetVpcByPlant.as_view(),
        name="get_vpc_by_plant",
    ),
    path(
        "crm-nth-prod-appr-dropdown/",
        CrmNthProductApprovalDropdown.as_view(),
        name="crm_nth_prod_appr_dropdown",
    ),
    # path(
    #     "godown-dispatch-data/",
    #     GodownDispatchViewSet.as_view(),
    #     name="godown_data",
    # ),
    path(
        "rail-road-flag-dropdown-data/",
        RailRoadFlagDropdownViewSet.as_view(),
        name="godown_data",
    ),
    path(
        "rail-road-flag-data/",
        RailRoadFlagViewSet.as_view(),
        name="godown_data",
    ),
    # path(
    #     "crossing-dispatch-data/",
    #     CrossingDataViewSet.as_view(),
    #     name="crossing_data",
    # ),
    path(
        "order-status/",
        OrderStatusViewSet.as_view(),
        name="order_status",
    ),
    # path(
    #     "diversions-dispatch-data/",
    #     DiversionsViewSet.as_view(),
    #     name="diversion_data",
    # ),
    # path(
    #     "rh-firing-dispatch-data/",
    #     RhFiringViewSet.as_view(),
    #     name="rh_firing_data",
    # ),
    path(
        "order-pendency-quantity-sum-and-count/",
        TgtSlhOrderPendencyQuantitySumAndCount.as_view(),
    ),
    path(
        "service-level-depo-quantity-sum-and-count/",
        TgtSlhServiceLevelDepoQuantitySumAndCount.as_view(),
    ),
    path(
        "nm-market-share-potential-download-api/",
        NmMarketSharePotentialViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="nm_market_share_potential_download_api",
    ),
    path(
        "nm-market-share-potential-data/",
        NmMarketSharePotentialViewSet.as_view({"get": "list", "put": "update"}),
        name="nm_market_share_potential_data",
    ),
    # path(
    #     "plan-data-for-month/",
    #     PlanDataForMonthViewSet.as_view({"get": "get"}),
    #     name="plan_data_for_month",
    # ),
    path(
        "order-status-recieved/",
        OrderStatusRecievedViewSet.as_view({"get": "get"}),
        name="order_status_recieved",
    ),
    path(
        "depo-operations-data/",
        DepotOperationsViewSet.as_view({"get": "get"}),
        name="depo_operations_data",
    ),
    path(
        "nm-market-share-potential-dropdown/",
        NmMarketSharePotentialDropdown.as_view(),
        name="nm_market_share_potential_dropdown",
    ),
    path(
        "previous-year-month-annual-site-conversion-plan/",
        PreviousYearMonthAnnualSiteConvPlan.as_view(),
    ),
    path(
        "product-wise-inventory-data/",
        ProductWiseInventory.as_view({"get": "get"}),
        name="product-wise-inventory-data",
    ),
    path(
        "previous-year-month-annual-site-conversion-plan/",
        PreviousYearMonthAnnualSiteConvPlan.as_view(),
    ),
    path(
        "product-wise-dropdown-data/",
        ProductWiseDropdown.as_view({"get": "get"}),
        name="product-wise-dropdown-data",
    ),
    path(
        "pricing_run_model/", PricingModelRunView.as_view(), name="pricing_run_model/"
    ),
    path(
        "nm-market-4x4-output-data/",
        NmMarket4X4OutputViewSet.as_view({"get": "list"}),
        name="nm-market-4x4-output-data",
    ),
    path(
        "monthly-wise-inventory-data/",
        MonthlyWiseInventory.as_view({"get": "get"}),
        name="monthly_wise_inventory_data",
    ),
    path(
        "so-league-weightage/",
        SoLeagueWeightageViewSet.as_view({"get": "list", "put": "update"}),
        name="so-league-weightage",
    ),
    path(
        "nsh-contribution-scenario/",
        NshContributionScenarioViewSet.as_view({"post": "post", "get": "list"}),
        name="nsh_contribution_scenario",
    ),
    path(
        "nsh-scenario-analysis-contribution-data/",
        NshScenarioAnalysisContributionData.as_view({"get": "get"}),
        name="nsh_scenario_analysis_contribution_data",
    ),
    path(
        "price-computation-base-segment-dropdown/",
        PriceComputationBaseSegmentDropdown.as_view(),
        name="price-computation-base-segment-dropdown",
    ),
    path(
        "toebs-scl-ncr-advance-calc-tab2-dropdown/",
        TOebsSclArNcrAdvanceCalcTabDropdown.as_view(),
        name="toebs-scl-ncr-advance-calc-tab2-dropdown",
    ),
    path(
        "order-pool-source-change-dropdown/",
        OrderPoolSourceChangeDropdown.as_view(),
        name="order-pool-source-change-dropdown",
    ),
    path(
        "source-change-freight-master/",
        SourceChangeFreightMasterViewSet.as_view({"get": "get"}),
        name="source-change-freight-master",
    ),
    path(
        "gift-master-dropdown/",
        GiftMasterDropdown.as_view({"get": "get"}),
        name="gift-master-dropdown",
    ),
    path(
        "product-brand-dropdown/",
        SchemeProductDropdown.as_view({"get": "get"}),
        name="product_brand_dropdown",
    ),
    path(
        "district-classification-run-download/",
        DistrictClassification.as_view(),
        name="district-classification-run-download",
    ),
    path(
        "non-trade-sales-planning-adherence-data/",
        NonTradeSalesPlanningAdherence.as_view({"get": "get"}),
        name="non-trade-sales-planning-adherence-data",
    ),
    path(
        "resource-name-dropdown-data/",
        ResourcesNameDropdown.as_view({"get": "get"}),
        name="resource-name-dropdown-data",
    ),
    path(
        "nt-input-sales-planning-consensus-target-data/",
        NTInputSPConsensusTarget.as_view(),
        name="nt-input-sales-planning-consensus-target-data",
    ),
    path(
        "premium-product-master-dropdown/",
        NTPremiumProductsMasterTmpDropdown.as_view(),
        name="premium-product-master-dropdown",
    ),
    path(
        "nt-resource-target/",
        NtResourceTargetViewSet.as_view(
            {"post": "create", "put": "update", "get": "list"}
        ),
        name="nt-resource-target",
    ),
    path(
        "nt-market-target-bulk-create/",
        NtMarketTargetBulkCreateViewSet.as_view(),
        name="nt-market-target-bulk-create",
    ),
    path(
        "tgt-plant-dispatch-data-dropdown/",
        TgtPlantDispatchDataDropdownAPIView.as_view(),
        name="tgt_plant_dispatch_data_dropdown",
    ),
    path(
        "influencer-tech-activity-master/",
        InfluencerTechActivityMasterViewSet.as_view({"get": "list", "post": "create"}),
        name="influencer_tech_activity_master",
    ),
    path(
        "influencer-tech-activity-master/<int:id>",
        InfluencerTechActivityMasterViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="influencer_tech_activity_master",
    ),
    path(
        "suppliers-vendor-data/",
        TOebsApSuppliersViewSet.as_view({"get": "get"}),
        name="change_source_mode",
    ),
    path(
        "vpc-historical-plant-dropdown/",
        VpcHistoricalPlantDropdown.as_view(),
        name="vpc-historical-plant-dropdown",
    ),
    path(
        "nt-monthly-sales-plan-ncr/",
        NtMonthlySalesPlanNcrData.as_view({"get": "get"}),
        name="nt_monthly_sales_plan_ncr",
    ),
    path(
        "monthly-target-setting-data/",
        MonthlyTargetSettingTargetSum.as_view(),
        name="monthly-target-setting-data",
    ),
    path(
        "monthly-target-setting-viewset-data/",
        MonthlyTargetSettingViewSet.as_view({"get": "list"}),
        name="monthly-target-setting-viewset-data",
    ),
    path(
        "nt-monthly-sales-plan-contribution/",
        NtMonthlySalesPlanContributionData.as_view({"get": "get"}),
        name="nt-monthly-sales-plan-contribution",
    ),
    path(
        "sales-plan-approval/",
        SalesPlanApproval.as_view({"get": "get"}),
        name="sales-plan-approval/",
    ),
    path(
        "get-warehouse-id/",
        GetWarehouseId.as_view(),
        name="get_warehouse_id",
    ),
    path(
        "crm-market-mapping-pricing-download-upload/",
        CrmMarketMappingPricingViewSet.as_view(
            {"get": "download_by_state", "put": "upload_update"}
        ),
        name="crm_market_mapping_pricing_download_upload_api",
    ),
    path(
        "crm-market-mapping-pricing/",
        CrmMarketMappingPricingViewSet.as_view(
            {"get": "list_by_state", "put": "update"}
        ),
        name="crm_market_mapping_pricing",
    ),
    path(
        "crm-pricing-download-upload/",
        CrmPricingViewSet.as_view({"get": "download_by_state", "put": "upload_update"}),
        name="crm_pricing_download_upload_api",
    ),
    path(
        "crm-pricing/",
        CrmPricingViewSet.as_view({"get": "list_by_state", "put": "update"}),
        name="crm_pricing",
    ),
    path(
        "pricing-input-crm-pricing-list/",
        PricingInputCrmPricingListViewSet.as_view({"get": "get"}),
        name="pricing_input_crm_pricing_list",
    ),
    path(
        "crm-market-mapping-pricing-dropdown/",
        CrmMarketMappingPricingDropdown.as_view(),
        name="crm-market-mapping-pricing-dropdown",
    ),
    path("branding-activity-budget-expense/", ActivityBudgetExpenseAPI.as_view()),
    path("sponsorship-budget-get-data/", SponsorshipBudgetGetView.as_view()),
    path(
        "calc-tab-dealer-name-dropdown/",
        CalcTabDealerNameDropdown.as_view(),
        name="calc-tab-dealer-name-dropdown",
    ),
    path(
        "vendor-detail-master-vendor-code-dropdown/",
        VendorDetailMasterVendorCodeDropdown.as_view(),
        name="vendor-detail-master-vendor-code-dropdown",
    ),
    path(
        "t-nm-material-transaction-dropdown/",
        TnmMaterialTransactionDropdown.as_view(),
        name="t-nm-material-transaction-dropdown",
    ),
    path(
        "branding-activity-viewset/",
        BrandingActivityViewSet.as_view(
            {"get": "list", "post": "post", "patch": "update"}
        ),
        name="branding-activity-viewset",
    ),
    path(
        "branding-activity-viewset/<int:id>",
        BrandingActivityViewSet.as_view({"patch": "partial_update", "get": "retrieve"}),
        name="branding-activity-viewset",
    ),
    path(
        "AutomatedModelsRunStatus/",
        AutomatedModelsRunStatusView.as_view({"post": "post"}),
        name="AutomatedModelsRunStatusView",
    ),
    path(
        "market-mapping-branding-budget-viewset/",
        MarketMappingBrandingBudgetViewSet.as_view({"get": "list", "put": "update"}),
        name="market-mapping-branding-budget-viewset",
    ),
    path(
        "market-mapping-branding-budget-viewset/<int:id>",
        MarketMappingBrandingBudgetViewSet.as_view(
            {"patch": "partial_update", "get": "retrieve"}
        ),
        name="market-mapping-branding-budget-viewset",
    ),
    path(
        "market-mapping-branding-budget-dropdown/",
        MarketMappingBrandingBudgetDropDown.as_view(),
        name="market-mapping-branding-budget-dropdown/",
    ),
    path(
        "branding-activity-dropdown/",
        BrandingActivityDropDown.as_view(),
        name="branding-activity-dropdown/",
    ),
    path(
        "market-potetial-and-market-share-monthly-data/",
        MarketPotentialAndShareMonthlyViewSet.as_view({"get": "get"}),
        name="market-potetial-and-market-share-monthly-data",
    ),
    path(
        "nth-market-potetial-and-market-share-monthly-data/",
        NTHMarketPotentialAndShareMonthlyViewSet.as_view({"get": "get"}),
        name="market-potetial-and-market-share-monthly-data",
    ),
    path(
        "state-head-monthly-sales-data/",
        StateHeadMonthlySalesData.as_view({"get": "list"}),
        name="state-head-monthly-sales-data",
    ),
    path(
        "state-head-monthly-sales-data-download-upload/",
        StateHeadMonthlySalesData.as_view({"get": "download"}),
        name="state-head-monthly-sales-data-download-upload",
    ),
    path(
        "state-head-monthly-sales-state-dropdown/",
        StateHeadMonthlySalesStateDropdown.as_view(),
        name="state-head-monthly-sales-state-dropdown/",
    ),
    path(
        "get-last-updated-date/",
        GetLastUpdatedDate.as_view(),
        name="get_last_updated_date",
    ),
    path(
        "demmurage-and-wharfage-forecast/",
        DemurrageAndWharfageForecastViewSet.as_view(),
        name="demmurage-and-wharfage-forecast",
    ),
    path(
        "lp-scheduling-order-master-source-change/",
        LpSchedulingOrderMasterSourceChange.as_view({"patch": "patch"}),
        name="lp_scheduling_order_maste_source_change",
    ),
    path(
        "crm-complaints-dropdown/",
        CrmComplaintsDropdown.as_view(),
        name="crm_complaints_dropdown",
    ),
    path(
        "crm-infl-chg-req-dropdown/",
        CrmInflChgReqDropdown.as_view(),
        name="crm_infl_chg_req_dropdown",
    ),
    path(
        "premium-product-master-bgp-dropdown/",
        PremiumProductsMasterTmpBGPDropdown.as_view(),
        name="premium_product_master_bgp_dropdown",
    ),
    path(
        "backhauling-opportunities/",
        BackhaulingOpportunitiesViewSet.as_view({"get": "list"}),
        name="backhauling_opportunities",
    ),
    path(
        "epod-data-viewset/",
        EpodDataViewSet.as_view({"get": "get"}),
        name="epod-data-viewset",
    ),
    path(
        "epod-data-viewset/<int:id>",
        EpodDataViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="epod-data-viewset",
    ),
    path(
        "tgt-rake-loading-details-dropdown/",
        TgtRakeLoadingDetailsViewSet.as_view({"get": "dropdown"}),
        name="tgt_rake_loading_details_dropdown",
    ),
    path(
        "backhauling-opportunities/<int:id>",
        BackhaulingOpportunitiesViewSet.as_view({"patch": "partial_update"}),
        name="backhauling_opportunities",
    ),
    path(
        "backhauling-opportunities-dropdown/",
        BackhaulingOpportunitiesDropdown.as_view({"get": "get"}),
        name="backhauling_opportunities_dropdown",
    ),
    path(
        "backhauling-opportunities-cards-data/",
        BackhaulingOpportunitiesCardsViewSet.as_view(),
        name="backhauling_opportunities_cards_data",
    ),
    path("tgt-plant-dispatch-data/", TgtPlantDispatchDataAPIView.as_view()),
    path(
        "backhauling-inbound-truck/",
        BackhaulingInboundTruckViewSet.as_view({"get": "list", "put": "update"}),
        name="backhauling_inbound_truck",
    ),
    path(
        "backhauling-inbound-truck-download-upload/",
        BackhaulingInboundTruckViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="backhauling_inbound_truck_download_upload",
    ),
    path(
        "backhauling-inbound-truck-dropdown/",
        BackhaulingInboundTruckDropdown.as_view({"get": "get"}),
        name="backhauling_inbound_truck_dropdown",
    ),
    path(
        "backhauling-model-run/",
        BackhaulingRunView.as_view(),
        name="backhauling-model-run",
    ),
    path(
        "crm-infl-assist-req-dropdown/",
        CrmInflAssistReqDropdown.as_view(),
        name="crm_infl_assist_req_dropdown",
    ),
    path(
        "non-trade-head-monthly-target-sales-data/",
        NonTradeHeadMonthlySalesData.as_view({"get": "list"}),
        name="non-trade-head-monthly-target-sales-data",
    ),
    path(
        "non-trade-head-monthly-target-sales-data-download-upload/",
        NonTradeHeadMonthlySalesData.as_view({"get": "download"}),
        name="non-trade-head-monthly-target-sales-data-download-upload",
    ),
    path(
        "non-trade-head-monthly-sales-dropdown/",
        NonTradeHeadMonthlySalesDropdown.as_view(),
        name="non_trade_head_monthly_sales_dropdown",
    ),
    path(
        "crm-influencer-scheme/",
        CrmInflSchemeViewSet.as_view({"get": "list", "post": "create"}),
        name="crm_influencer_scheme/",
    ),
    path(
        "source-change-contribution-difference/",
        SourceChangeContributionDifference.as_view(),
        name="source_change_contribution_difference",
    ),
    path(
        "crm-infl-gift-scheme/",
        CrmInflGiftSchemeviewset.as_view({"get": "list", "post": "create"}),
        name="Crm-Infl-Gift-Scheme",
    ),
    path(
        "crm-nth-lead-form-dropdown/",
        CrmNthLeadFormDropDown.as_view(),
        name="crm_nth_lead_form_dropdown",
    ),
    path(
        "change-source-approval-request/",
        ChangeSourceApprovalRequest.as_view(
            {"get": "list", "post": "create", "put": "update"}
        ),
    ),
    path(
        "change-source-approval-request/<int:id>",
        ChangeSourceApprovalRequest.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
    ),
    path(
        "change-source-approval-request-count/",
        ChangeSourceApprovalRequest.as_view({"get": "request_count"}),
    ),
    path(
        "change-source-approval-request-dropdown/",
        ChangeSourceApprovalRequest.as_view({"get": "dropdown"}),
    ),
    # path(
    #     "change-source-approval-request-total-impact/",
    #     SourceChangeModeTotalImpact.as_view(),
    # ),
    path(
        "crm-infl-mgr-meet-Plan-monthly-download-upload/",
        CrmInflMgrMeetPlanMonthlyViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="crm_infl_mgr_meet_Plan_monthly_download_upload_api",
    ),
    path(
        "crm-infl-mgr-meet-Plan-monthly/",
        CrmInflMgrMeetPlanMonthlyViewSet.as_view({"get": "list", "put": "update"}),
        name="crm_infl_mgr_meet_Plan_monthly",
    ),
    path(
        "nth-budget-plan-monthly-download-upload/",
        NthBudgetPlanMonthlyViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="nth_budget_Plan_monthly_download_upload_api",
    ),
    path(
        "nth-budget-plan-monthly/",
        NthBudgetPlanMonthlyViewSet.as_view({"get": "list", "put": "update"}),
        name="nth_budget_plan_monthly",
    ),
    path(
        "crm-annual-site-conv-plan-monthly-download-upload/",
        CrmAnnualSiteConvPlanMonthlyViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="crm_annual_site_conv_plan_monthly_download_upload_api",
    ),
    path(
        "crm-annual-site-conv-plan-monthly/",
        CrmAnnualSiteConvPlanMonthlyViewSet.as_view({"get": "list", "put": "update"}),
        name="crm_annual_site_conv_plan_monthly",
    ),
    path(
        "crm-infl-mgr-annual-plan-monthly-download-upload/",
        CrmInflMgrAnnualPlanMonthlyViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="crm_infl_mgr_annual_plan_monthly_download_upload_api",
    ),
    path(
        "crm-infl-mgr-annual-plan-monthly/",
        CrmInflMgrAnnualPlanMonthlyViewSet.as_view({"get": "list", "put": "update"}),
        name="crm_infl_mgr_annual_plan_monthly",
    ),
    path(
        "crm-infl-mgr-meet-plan-download-upload/",
        CrmInflMgrMeetPlanDownloadUploadViewset.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="crm_infl_mgr_meet_plan_download_upload",
    ),
    path(
        "crm-infl-mgr-annual-plan-download-upload/",
        CrmInflMgrAnnualPlanDownloadUploadViewset.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="crm_infl_mgr_annual_plan_download_upload/",
    ),
    path(
        "new-market-pricing-viewset/",
        NewMarketPricingApprovalViewSet.as_view({"get": "list", "post": "post"}),
        name="new_market_pricing_viewset",
    ),
    path(
        "new-market-pricing-viewset/<int:id>",
        NewMarketPricingApprovalViewSet.as_view(
            {"patch": "partial_update", "get": "retrieve"}
        ),
        name="new_market_pricing__viewset",
    ),
    path(
        "sponsorship-budget-viewset/",
        SponsorshipBudgetViewSet.as_view(
            {"get": "list", "put": "update", "post": "post"}
        ),
        name="sponsorship_budget_viewset",
    ),
    path(
        "last-yr-infl-mgr-scheme-budget-avg/",
        LstYrBudgetAvgCrmInflMgrSchemeBudgetViewSet.as_view(),
        name="last_yr_infl_mgr_scheme_budget_avg",
    ),
    path(
        "system-recommendation-technical-activities/",
        SystemRecommendationTechicalActivities.as_view(),
        name="",
    ),
    path(
        "market-mapping-branding-budget-download-upload/",
        MarketMappingBrandingBudgetViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="market-mapping-branding-budget-download-upload",
    ),
    path(
        "crm-sales-planning-bottom-up-target-viewset",
        CrmSalesPlanningBottomUpTargetViewset.as_view({"get": "list"}),
        name="CrmSalesPlanningBottomUpTargetViewset",
    ),
    path(
        "nt-product-target-by-state/",
        NtProductTargetByState.as_view(),
        name="nt_product_target_by_state",
    ),
    path(
        "crm-sales-planning-bottomup-target-cards/",
        CrmSalesPlanningBottomUpTargetSum.as_view(),
        name="CrmSalesPlanningBottomUpTarget",
    ),
    path(
        "non-trade-sales-planning-state-data/",
        NonTradeSalesPlanningStateViewSet.as_view({"get": "list", "put": "update"}),
        name="non_trade_sales_planning_state_data",
    ),
    path(
        "non-trade-sales-planning-account-data/",
        NonTradeSalesPlanningAccountViewSet.as_view({"get": "list", "put": "update"}),
        name="non_trade_sales_planning_account_data",
    ),
    path(
        "non-trade-sales-planning-designation-data/",
        NonTradeSalesPlanningDesignationViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_designation_data",
    ),
    path(
        "non-trade-sales-planning-product-data/",
        NonTradeSalesPlanningProductViewSet.as_view({"get": "list", "put": "update"}),
        name="non_trade_sales_planning_product_data",
    ),
    path(
        "non-trade-sales-planning-state-monthly-data/",
        NonTradeSalesPlanningStateMonthlyViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_state_monthly_data",
    ),
    path(
        "non-trade-sales-planning-account-monthly-data/",
        NonTradeSalesPlanningAccountMonthlyViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_account_monthly_data",
    ),
    path(
        "non-trade-sales-planning-designation-monthly-data/",
        NonTradeSalesPlanningDesignationMonthlyViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_designation_monthly_data",
    ),
    path(
        "non-trade-sales-planning-product-monthly-data/",
        NonTradeSalesPlanningProductMonthlyViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_product_monthly_data",
    ),
    path(
        "siding-code-mapping-dropdown/",
        SidingCodeMappingDropdown.as_view(),
        name="siding_code_mapping_dropdow",
    ),
    path(
        "target-sales-planning-monthly/",
        TargetSalesPlanningMonthlyViewSet.as_view({"get": "list", "put": "update"}),
        name="target_sales_planning_monthly/",
    ),
    path(
        "nt-sales-planning-monthly-quantity-historical-actuals/",
        NtSalesPlanningMonthlyQuantityHistoricalActuals.as_view(),
        name="nt_sales_planning_monthly_quantity_historical_actuals",
    ),
    path(
        "crm-sales-plan-and-adherence-viewset",
        CrmSalesPlanAndAdherenceViewset.as_view(),
        name="CrmSalesPlanAndAdherenceViewset/",
    ),
    path(
        "nt-sales-planning-monthly-quantity-ncr-month-actual/",
        NtSalesPlanningMonthlyNCRMonthActual.as_view(),
        name="nt_sales_planning_monthly_quantity_ncr_month_actual",
    ),
    path(
        "nt-bottom-up-annual-cards/",
        NtBottomUpAnnualCards.as_view(),
        name="nt_bottom_up_annual_cards",
    ),
    path(
        "non-trade-sales-planning-monthly-ncr-target/",
        NonTradeSalesPlanningMonthlyNcrTargetViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="non_trade_sales_planning_monthly_ncr_target",
    ),
    path(
        "non-trade-top-down-monthly-target/",
        NonTradeTopDownMonthlyTargetViewSet.as_view({"get": "list", "put": "update"}),
        name="non_trade_top_down_monthly_target",
    ),
    path(
        "reason-for-freight-change-dropdown",
        ReasonForFreightChangeDropdown.as_view(),
        name="ReasonForFreightChnageDropdown",
    ),
    path(
        "rake-types-dropdown/",
        RakeTypesDropdown.as_view(),
        name="rake_types_dropdow",
    ),
    path(
        "non-trade-sp-selected-year-monthly-target/",
        NonTradeSalesPlanningSelectedYearTotalMonthTargetsViewSet.as_view(
            {"get": "get"}
        ),
        name="non_trade_sp_selected_year_monthly_target",
    ),
    path(
        "target-sales-planning-sum-card/",
        TargetsalesPlanningSumCard.as_view(),
        name="TargetsalesPlanningSumCard",
    ),
    path(
        "reasons-for-demurrage-wharfage/",
        ReasonsForDemurrageWharfageView.as_view({"get": "get"}),
        name="TargetsalesPlanningSumCard",
    ),
    path(
        "district-wise-pricing-proposal/",
        DistrictWisePricingProposalViewSet.as_view({"get": "list", "post": "post"}),
        name="district_wise_pricing_proposal",
    ),
    path(
        "price-change-req-approval/",
        PriceChangeReqApproval.as_view({"get": "list", "put": "update"}),
        name="PriceChangeReqApproval",
    ),
    path(
        "price-change-req-approval-get/",
        PriceChangeApprovalGet.as_view(),
        name="price_change_approval_get",
    ),
    path(
        "price-change-request-approval-dropdown/",
        PriceChangeRequestApprovalDropdown.as_view(),
        name="price-change-request-dropdown",
    ),
    path(
        "network-addition-plan/",
        NetworkAdditionPlanViewSet.as_view({"get": "list", "put": "update"}),
        name="network_addition_plan",
    ),
    path(
        "network-addition-plan-state/",
        NetworkAdditionPlanStateViewSet.as_view({"get": "list", "put": "put"}),
        name="network_addition_plan_state",
    ),
    path(
        "epod-data-vehicle-no-and-delivery-id-dropdown/",
        EpodDataVehicleNoAndDeliveryIdDropdown.as_view(),
        name="epod-data-vehicle-no-and-delivery-id-dropdown",
    ),
    path(
        "alert-transaction/",
        AlertTransactionViewSet.as_view({"get": "get", "put": "update"}),
        name="alert_transaction",
    ),
    path(
        "alert-transaction-count/",
        AlertTransactionViewSet.as_view({"get": "alerts_count"}),
    ),
    path(
        "trade-order-placement-approval/",
        TradeOrderPlacementApprovalViewset.as_view({"get": "list"}),
        name="trade_order_placement_approval",
    ),
    path(
        "trade-order-placement-approval/<int:id>",
        TradeOrderPlacementApprovalViewset.as_view({"patch": "partial_update"}),
        name="trade_order_placement_approval",
    ),
    path(
        "annual-state-level-target-dropdown/",
        AnnualStateLevelTargetDropdown.as_view(),
        name="annual_state_level_target_dropdown",
    ),
    path(
        "annual-district-level-target-download-upload/",
        AnnualDistrictLevelTargetViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="annual_district_level_target_download_upload",
    ),
    path(
        "annual-district-level-target/",
        AnnualDistrictLevelTargetViewSet.as_view({"get": "list", "put": "update"}),
        name="annual_district_level_target",
    ),
    path(
        "annual-state-level-target/",
        AnnualStateLevelTargetViewSet.as_view({"get": "list", "put": "update"}),
        name="annual_state_level_target",
    ),
    path(
        "revised-buckets-approval-viewset/",
        RevisedBucketsApprovalViewset.as_view({"get": "list"}),
        name="RevisedBucketsApprovalViewset",
    ),
    path(
        "revised-buckets-approval-viewset/<int:id>",
        RevisedBucketsApprovalViewset.as_view({"patch": "partial_update"}),
        name="RevisedBucketsApprovalViewset",
    ),
    path(
        "crm-exception-approval-for-replacement-of-product-viewset/",
        CrmExceptionApprovalForReplacementOfProductViewset.as_view({"get": "list"}),
        name="Crm_Exception_Approval_For_Replacement_OfProduct_Viewset",
    ),
    path(
        "crm-exception-approval-for-replacement-of-product-viewset/<int:id>",
        CrmExceptionApprovalForReplacementOfProductViewset.as_view(
            {"patch": "partial_update"}
        ),
        name="Crm_Exception_Approval_For_Replacement_OfProduct_Viewset",
    ),
    path(
        "annual-district-level-target-dropdown/",
        AnnualDistrictLevelTargetDropdown.as_view(),
        name="AnnualDistrictLevelTargetDropdown",
    ),
    path(
        "nt-sales-planning-designation-actuals/",
        NtSalesPlanningDesignationActuals.as_view(),
        name="nt_sales_planning_desgnation_actuals",
    ),
    path(
        "state-head-state-wise-target/",
        StateHeadStateWiseTarget.as_view(),
        name="state_head_state_wise_target",
    ),
    path(
        "revised-buckets-approvalt-dropdown/",
        RevisedBucketsApprovalDropdown.as_view(),
        name="RevisedBucketsApprovaltDropdown",
    ),
    path(
        "network-addition-cards-data/",
        NetworkAdditionCardsData.as_view(),
        name="network_addition_cards_data",
    ),
    path(
        "crm-exception-approval-for-replacement-of-product-dropdown/",
        CrmExceptionApprovalForReplacementOfProductDropdown.as_view(),
        name="crm_exception_approval_for_replacement_of_product_dropdown",
    ),
    path(
        "annual-state-level-target-comment-and-status/",
        AnnualStateLevelTargetCommentAndStatus.as_view(),
        name="annual_state_level_target_comment_and_status",
    ),
    path(
        "crm-verification-and-approval-of-dealer-sp-form/",
        CrmVerificationAndApprovalOfDealerSpFormViewSet.as_view(
            {"get": "list", "put": "update"}
        ),
        name="crm_verification_and_approval_of_dealer_sp_form",
    ),
    path(
        "crm-verification-and-approval-of-dealer-sp-form/<int:id>",
        CrmVerificationAndApprovalOfDealerSpFormViewSet.as_view({"get": "retrieve"}),
        name="crm-verification-and-approval-of-dealer-sp-form",
    ),
    path(
        "nt-top-down-month-product-actual/",
        NTTopDownMonthProductActual.as_view(),
        name="nt-top-down-month-product-actual",
    ),
    path(
        "sh-annual-state-level-target-approval-cards/",
        SHAnnualStateLevelTargetApprovalCards.as_view(),
        name="sh-annual-state-level-target-approval-cards",
    ),
    path(
        "annual-state-level-target-dropdown/",
        AnnualStateLevelTargetDropdown.as_view(),
        name="annual_state_level_target_dropdown",
    ),
    path(
        "target-setting-download-script/",
        TaregtSettingDownload.as_view(),
        name="target-setting-download-script",
    ),
    path(
        "exception-disbursement-approval/",
        ExceptionDisbursementApprovalViewSet.as_view({"get": "list", "put": "update"}),
        name="exception_disbursement_approval",
    ),
    path(
        "exception-disbursement-approval/<int:id>",
        ExceptionDisbursementApprovalViewSet.as_view({"get": "retrieve"}),
        name="exception_disbursement_approval",
    ),
    path(
        "gift-redeem-request-approval/",
        GiftRedeemRequestApprovalViewSet.as_view({"get": "list", "put": "update"}),
        name="gift_redeem_request_approval",
    ),
    path(
        "gift-redeem-request-approval/<int:id>",
        GiftRedeemRequestApprovalViewSet.as_view({"get": "retrieve"}),
        name="gift_redeem_request_approval",
    ),
    path(
        "order-executable-detail-update-create/",
        OrderExecutableDetailUpdateOrCreate.as_view(),
        name="order_executable_detail_update_create/",
    ),
    path(
        "crm-approval-stage-gates-viewset/",
        CrmApprovalStageGatesViewSet.as_view({"get": "list", "put": "update"}),
        name="crm_approval_stage_gates_viewset",
    ),
    path(
        "tgt-rake-loading-get/",
        TgtRakeLoadingGetViewSet.as_view({"get": "list"}),
        name="tgt_rake_loading_get",
    ),
    path(
        "existing-depot-locations-viewset/",
        ExistingDepotLocationsViewSet.as_view({"get": "list", "put": "update"}),
        name="existing_depot_locations_viewset",
    ),
    path(
        "existing-depot-locations-viewset/<int:id>",
        ExistingDepotLocationsViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="existing_depot_locations_viewset",
    ),
    path(
        "existing-depot-locations-viewset-download-upload/",
        ExistingDepotLocationsViewSet.as_view(
            {"get": "download", "put": "upload_update"}
        ),
        name="existing_depot_locations_download_upload",
    ),
    path(
        "depo-addition-run-id-list/",
        DepoAdditionRunListViewSet.as_view({"get": "get"}),
        name="tgt_rake_loading_get",
    ),
    path(
        "exception-disbursement-approval-dropdown/",
        ExceptionDisbursementApprovalDropdown.as_view(),
        name="exception_disbursement_approval_dropdown",
    ),
    path(
        "tgt-rake-loading-detail-dropdown/",
        TgtRakeLoadingDetailDropdown.as_view(),
        name="tgt_rake_loading_detail_dropdown",
    ),
    path(
        "tgt-rake-loading-dropdown/",
        TgtRakeLoadingDropdown.as_view(),
        name="tgt_rake_loading_dropdown",
    ),
    path(
        "tgt-day-wise-lifting-closing-sum/",
        SumOfClosingPointView.as_view({"get": "get"}),
        name="tgt-day-wise-lifting-closing-sum",
    ),
    path(
        "gift-redeem-request-approval-dropdown/",
        GiftRedeemRequestApprovalDropdown.as_view(),
        name="gift_redeem_request_approval_dropdown",
    ),
    path(
        "wharfage-slabs/",
        WharfageSlabsViewSet.as_view({"get": "list"}),
        name="wharfage_slabs",
    ),
    path(
        "wharfage-slabs-download-upload/",
        WharfageSlabsViewSet.as_view({"get": "download"}),
        name="wharfage_slabs_download_upload",
    ),
    path(
        "demurrage-slabs/",
        DemurrageSlabsViewSet.as_view({"get": "list"}),
        name="demurrage_slabs",
    ),
    path(
        "demurrage-slabs-download-upload/",
        DemurrageSlabsViewSet.as_view({"get": "download"}),
        name="demurrage_slabs_download_upload",
    ),
    path(
        "crwc-charges-master/",
        CrwcChargesMasterViewSet.as_view({"get": "list"}),
        name="crwc_charges_master",
    ),
    path(
        "crwc-charges-master-download-upload/",
        CrwcChargesMasterViewSet.as_view({"get": "download"}),
        name="crwc_charges_master_download_upload",
    ),
    path(
        "waiver-commission-master/",
        WaiverCommissionMasterViewSet.as_view({"get": "list"}),
        name="waiver_commission_master",
    ),
    path(
        "waiver-commission-master-download-upload/",
        WaiverCommissionMasterViewSet.as_view({"get": "download"}),
        name="waiver_commission_master_download_upload",
    ),
    path(
        "rail-expenses-details/",
        RailExpensesDetailsViewSet.as_view({"get": "list", "post": "create"}),
        name="rail_expenses_details",
    ),
    path(
        "waiver-commission-master-dropdown/",
        WaiverCommissionMasterDropdown.as_view(),
        name="waiver-commission-master-dropdown",
    ),
    path(
        "crwc-charges-master-dropdown/",
        CrwcChargesMasterDropdown.as_view(),
        name="crwc-charges-master-dropdown",
    ),
    path(
        "network-addition-state-cards-data/",
        NetworkAdditionStateCardsData.as_view(),
        name="network_addition_state_cards_data",
    ),
    path(
        "hourly-lifting-efficiency-master/",
        HourlyLiftingEfficiencyMasterViewSet.as_view({"get": "list"}),
        name="hourly_lifting_efficiency_master",
    ),
    path(
        "hourly-lifting-efficiency/",
        HourlyLiftingEfficiencyViewSet.as_view({"get": "list", "post": "create"}),
        name="hourly_lifting_efficiency",
    ),
    path(
        "hourly-lifting-efficiency/<int:id>",
        HourlyLiftingEfficiencyViewSet.as_view({"patch": "partial_update"}),
        name="hourly_lifting_efficiency",
    ),
    path(
        "siding-constraints-create/",
        SidingConstraintsViewSet.as_view({"post": "create", "get": "list"}),
        name="siding-constraints-create/",
    ),
    path(
        "cost-master-detail-viewset/",
        CostsMasterDetailViewSet.as_view({"get": "get"}),
        name="cost-master-detail-viewset",
    ),
    path(
        "cost-master-cost-head-viewset/",
        CostMasterCostHeadViewSet.as_view(),
        name="cost-master-cost-head-viewset",
    ),
    # path(
    #     "lifting-pattern-viewset/",
    #     LiftingPatternViewSet.as_view({"get": "list", "post": "create"}),
    #     name="lifting_pattern_viewset",
    # ),
    path(
        "lifting-pattern-viewset/",
        LiftingPatternViewSet.as_view({"get": "list", "put": "update"}),
        name="lifting_pattern_viewset",
    ),
    path(
        "lifting-pattern-viewset/<int:id>",
        LiftingPatternViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="lifting_pattern_viewset",
    ),
    path(
        "time-combination/",
        GetTimeCombination.as_view({"get": "get"}),
        name="time-combination",
    ),
    path(
        "rail-expenses-details-wf-viewSet/",
        RailExpensesDetailsWfViewSet.as_view({"get": "list", "post": "create"}),
        name="rail_expenses_details_wf_viewSet",
    ),
    path(
        "tpc-customer-mapping/",
        TpcCustomerMappingViewSet.as_view(
            {"get": "list", "post": "create", "patch": "update"}
        ),
        name="tpc_customer_mapping",
    ),
    path(
        "tgt-order-data-customer-and-tpc-dropdown/",
        TgtOrderDataApCustomerAndTPCDropdown.as_view(),
        name="tgt-order-data-customer-and-tpc-dropdown",
    ),
    path("epod-data-reached/", EpodDataReachedViewSet.as_view({"get": "get"})),
    path(
        "tgt-plant-dispatch-data-dropdown-api-view-new/",
        TgtPlantDispatchDataDropdownAPIViewnew.as_view(),
        name="TgtPlantDispatchDataDropdownAPIViewnew",
    ),
    path(
        "packer-rated-capacity-dropdown/",
        PackerRatedCapacityDropdown.as_view(),
        name="packer_rated_capacity_dropdown",
    ),
    path(
        "siding-constraints-check/",
        SidingConstraintsCheckViewSet.as_view(),
        name="siding_constraints_check",
    ),
    path(
        "trade-order-placement-approval-dropdown/",
        TradeOrderPlacementApprovalDropdown.as_view(),
        name="trade-order-placement-approval-dropdown",
    ),
    path(
        "handling-masters/",
        HandlingMastersViewSet.as_view({"get": "get"}),
        name="handling-masters",
    ),
    path(
        "network-addition-plan-state-send-to-nsh-button/",
        NetworkAdditionPlanStateSendToNshButtonViewSet.as_view(),
        name="network_addition_plan_state_send_to_nsh_button",
    ),
    path(
        "target-sales-planning-monthly-target-sum/",
        TargetSalesPlanningMonthlyTargetSum.as_view(),
        name="target_sales_planning_monthly_target_sum/",
    ),
    path(
        "target-sales-planning-monthly-adherence/",
        TargetSalesPlanningMonthlyAdherenceViewswet.as_view(),
        name="target_sales_planning_monthly_adherence/",
    ),
    path(
        "non-trade-sp-selected-year-selected-month-total-target/",
        NonTradeSalesPlanningSelectedYearSelectedMonthTotalMonthTargetsViewSet.as_view(
            {"get": "get"}
        ),
        name="non_trade_sp_selected_year_selected_month_total_target",
    ),
    path(
        "gd-vs-wharfage-model-view/",
        GdVsWharfageModelRunView.as_view(),
        name="gd-vs-wharfage-model-view",
    ),
    path(
        "gd-wharfage-output-view/",
        GdWharfageOutputViewSet.as_view({"get": "get"}),
        name="gd_wharfage_output_view",
    ),
    path(
        "gd-wharfage-slab-code/",
        GetSlabsCode.as_view(),
        name="gd-wharfage-slab-code",
    ),
    path(
        "gd-warfhage-run-list-view/",
        GdWarfhageRunListView.as_view(),
        name="gd_warfhage_run_list_view",
    ),
    path(
        "freight-change-format-download/",
        FreightChangeFormatDownloadView.as_view({"get": "get"}),
        name="freight_change_format_download",
    ),
    path(
        "tgt-order-data-ap-tpc-dropdown/",
        TgtOrderDataApTPCDropdown.as_view(),
        name="tgt_order_data_ap_tpc_dropdown",
    ),
]
