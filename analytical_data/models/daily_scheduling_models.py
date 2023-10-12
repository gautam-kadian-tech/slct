"""Analytical data daily scheduling models module."""
from django.db import models

from accounts.models import User
from analytical_data.enum_classes import ApprovalStatusChoices
from analytical_data.models.monthly_scheduling_models import LpModelDfRank


class LpSchedulingOrderMaster(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    order_id = models.BigIntegerField(db_column="ORDER_ID", blank=True, null=True)
    order_header_id = models.BigIntegerField(
        db_column="ORDER_HEADER_ID", blank=True, null=True
    )
    order_line_id = models.BigIntegerField(
        db_column="ORDER_LINE_ID", blank=True, null=True
    )
    order_date = models.DateTimeField(db_column="ORDER_DATE", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=200, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=200, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=200, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=200, blank=True, null=True
    )
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=200, blank=True, null=True
    )
    order_quantity = models.DecimalField(
        db_column="ORDER_QUANTITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=200, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=200, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=200, blank=True, null=True
    )
    customer_code = models.BigIntegerField(
        db_column="CUSTOMER_CODE", blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=200, blank=True, null=True
    )
    cust_sub_cat = models.CharField(
        db_column="CUST_SUB_CAT", max_length=200, blank=True, null=True
    )
    cust_name = models.CharField(
        db_column="CUST_NAME", max_length=200, blank=True, null=True
    )
    auto_tagged_source = models.CharField(
        db_column="AUTO_TAGGED_SOURCE", max_length=200, blank=True, null=True
    )
    auto_tagged_mode = models.CharField(
        db_column="AUTO_TAGGED_MODE", max_length=200, blank=True, null=True
    )
    sales_officer_changed_source = models.BooleanField(
        db_column="SALES_OFFICER_CHANGED_SOURCE", blank=True, null=True
    )
    delivery_due_date = models.DateTimeField(
        db_column="DELIVERY_DUE_DATE", blank=True, null=True
    )
    dispatch_due_date = models.DateTimeField(
        db_column="DISPATCH_DUE_DATE", blank=True, null=True
    )
    order_status = models.CharField(
        db_column="ORDER_STATUS", max_length=200, blank=True, null=True
    )
    full_truck_load = models.BooleanField(
        db_column="FULL_TRUCK_LOAD", blank=True, null=True
    )
    order_clubbed = models.BooleanField(
        db_column="ORDER_CLUBBED", blank=True, null=True
    )
    club_id = models.IntegerField(db_column="CLUB_ID", blank=True, null=True)
    di_generated = models.BooleanField(db_column="DI_GENERATED", blank=True, null=True)
    order_executable = models.BooleanField(
        db_column="ORDER_EXECUTABLE", blank=True, null=True
    )
    self_consumption_flag = models.BooleanField(
        db_column="SELF_CONSUMPTION_FLAG", blank=True, null=True
    )
    pp_call = models.BooleanField(db_column="PP_CALL", blank=True, null=True)
    remarks = models.BooleanField(db_column="REMARKS", blank=True, null=True)
    created_at = models.DateField(db_column="CREATED_AT", blank=True, null=True)
    updated_at = models.DateTimeField(db_column="UPDATED_AT", blank=True, null=True)
    reason = models.CharField(db_column="Reason", max_length=500, blank=True, null=True)
    delivery_id = models.BigIntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    delivery_detail_id = models.BigIntegerField(
        db_column="DELIVERY_DETAIL_ID", unique=True, blank=True, null=True
    )
    org_id = models.BigIntegerField(db_column="ORG_ID", blank=True, null=True)
    organization_id = models.BigIntegerField(
        db_column="ORGANIZATION_ID", blank=True, null=True
    )
    inventory_item_id = models.BigIntegerField(
        db_column="INVENTORY_ITEM_ID", blank=True, null=True
    )
    dispatched_quantity = models.BigIntegerField(
        db_column="Dispatched Quantity", blank=True, null=True
    )
    dilink_creation_dt = models.DateTimeField(
        db_column="DILINK_CREATION_DT", blank=True, null=True
    )
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    ship_taluka = models.CharField(
        db_column="SHIP_TALUKA", max_length=50, blank=True, null=True
    )
    full_address = models.TextField(db_column="Full Address", blank=True, null=True)
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=50, blank=True, null=True
    )
    vehicle_number = models.CharField(
        db_column="VEHICLE_NUMBER", max_length=50, blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=50, blank=True, null=True
    )
    ship_from_zone = models.CharField(
        db_column="Ship_from_zone", max_length=50, blank=True, null=True
    )
    warehouse = models.BigIntegerField(db_column="WAREHOUSE", blank=True, null=True)
    ship_to_org_id = models.BigIntegerField(
        db_column="SHIP_TO_ORG_ID", blank=True, null=True
    )
    freightterms = models.CharField(
        db_column="FREIGHTTERMS", max_length=50, blank=True, null=True
    )
    fob = models.CharField(db_column="FOB", max_length=50, blank=True, null=True)
    token_id = models.BigIntegerField(db_column="TOKEN_ID", blank=True, null=True)
    route = models.CharField(db_column="ROUTE", max_length=200, blank=True, null=True)
    source_location_id = models.BigIntegerField(
        db_column="SOURCE_LOCATION_ID", blank=True, null=True
    )
    shipinglocation = models.BigIntegerField(
        db_column="SHIPINGLOCATION", blank=True, null=True
    )
    sales_order_type = models.CharField(
        db_column="SALES_ORDER_TYPE", max_length=50, blank=True, null=True
    )
    changed_source = models.CharField(
        db_column="CHANGED_SOURCE", max_length=200, blank=True, null=True
    )
    changed_mode = models.CharField(
        db_column="CHANGED_MODE", max_length=200, blank=True, null=True
    )
    transferred_to_depot = models.BooleanField(
        db_column="TRANSFERRED_TO_DEPOT", blank=True, null=True
    )
    request_date = models.CharField(
        db_column="REQUEST_DATE", max_length=50, blank=True, null=True
    )
    released_date = models.CharField(
        db_column="RELEASED_DATE", max_length=50, blank=True, null=True
    )
    source_change_time = models.DateTimeField(
        db_column="SOURCE_CHANGE_TIME", blank=True, null=True
    )
    source_change_route_id = models.BigIntegerField(
        db_column="SOURCE_CHANGE_ROUTE_ID", blank=True, null=True
    )
    current_source = models.CharField(
        db_column="CURRENT_SOURCE", max_length=100, blank=True, null=True
    )
    contribution_impact = models.DecimalField(
        db_column="CONTRIBUTION_IMPACT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    changed_inco_terms = models.CharField(
        db_column="CHANGED_INCO_TERMS", max_length=360, blank=True, null=True
    )
    changed_freight_terms = models.CharField(
        db_column="CHANGED_FREIGHT_TERMS", max_length=360, blank=True, null=True
    )
    changed_route_id = models.CharField(
        db_column="CHANGED_ROUTE_ID", max_length=360, blank=True, null=True
    )
    changed_fob = models.CharField(
        db_column="CHANGED_FOB", max_length=360, blank=True, null=True
    )
    changed_run_id_for_changed_source = models.BigIntegerField(
        db_column="CHANGED_RUN_ID_FOR_CHANGED_SOURCE", blank=True, null=True
    )
    total_impact = models.BigIntegerField(
        db_column="TOTAL_IMPACT", blank=True, null=True
    )
    attribute16_remarks = models.CharField(
        db_column="ATTRIBUTE16_REMARKS", max_length=100, blank=True, null=True
    )
    executable_comment = models.TextField(
        db_column="EXECUTABLE_COMMENT", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_ORDER_MASTER"


class LpSchedulingCrmChecks(models.Model):
    """Lp scheduling crm checks model class."""

    id = models.IntegerField(db_column="ID", primary_key=True)
    order_master = models.ForeignKey(
        LpSchedulingOrderMaster,
        db_column="ORDER_MASTER_ID",
        on_delete=models.CASCADE,
        related_name="lp_scheduling_crm_checks",
    )
    credit_limit_check = models.CharField(
        db_column="CREDIT_LIMIT_CHECK", max_length=200, blank=True, null=True
    )
    dealer_own_truck = models.BooleanField(
        db_column="DEALER_OWN_TRUCK", blank=True, null=True
    )
    dealer_truck_number = models.CharField(
        db_column="DEALER_TRUCK_NUMBER", max_length=200, blank=True, null=True
    )
    dealer_truck_contact_number = models.CharField(
        db_column="DEALER_TRUCK_CONTACT_NUMBER", max_length=200, blank=True, null=True
    )
    order_below_qc = models.BooleanField(
        db_column="ORDER_BELOW_QC", blank=True, null=True
    )
    trucks_pending_for_epod_confirmation = models.IntegerField(
        db_column="TRUCKS_PENDING_FOR_EPOD_CONFIRMATION", blank=True, null=True
    )
    market_operating_hours = models.CharField(
        db_column="MARKET_OPERATING_HOURS", max_length=200, blank=True, null=True
    )
    created_at = models.DateField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_CRM_CHECKS"


class LpSchedulingDiDetails(models.Model):
    """Lp scheduling DI details model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    remarks = models.CharField(
        db_column="REMARKS", max_length=200, blank=True, null=True
    )
    order_master = models.ForeignKey(
        LpSchedulingOrderMaster,
        db_column="ORDER_MASTER_ID",
        on_delete=models.CASCADE,
        related_name="lp_scheduling_di_details",
    )
    di_number = models.BigIntegerField(db_column="DI_NUMBER", blank=True, null=True)
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=200, blank=True, null=True
    )
    di_quantity = models.DecimalField(
        db_column="DI_QUANTITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    truck_number = models.CharField(
        db_column="TRUCK_NUMBER", max_length=200, blank=True, null=True
    )
    driver_contact_number = models.CharField(
        db_column="DRIVER_CONTACT_NUMBER", max_length=200, blank=True, null=True
    )
    transporter = models.CharField(
        db_column="TRANSPORTER", max_length=200, blank=True, null=True
    )
    token_no = models.BigIntegerField(db_column="TOKEN_NO", blank=True, null=True)
    order_line_id = models.BigIntegerField(
        db_column="ORDER_LINE_ID", blank=True, null=True
    )
    order_id = models.BigIntegerField(db_column="ORDER_ID", blank=True, null=True)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(db_column="UPDATED_AT", auto_now=True)

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_DI_DETAILS"


class LpSchedulingPpCallDtl(models.Model):
    """Daily scheduling PP call details model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    order_master = models.ForeignKey(
        LpSchedulingOrderMaster,
        db_column="ORDER_MASTER_ID",
        on_delete=models.CASCADE,
        related_name="lp_scheduling_pp_call_dtl",
    )
    pp_calling_sequence = models.IntegerField(
        db_column="PP_CALLING_SEQUENCE", blank=True, null=True
    )
    prioritized_order = models.BooleanField(
        db_column="PRIORITIZED_ORDER", blank=True, null=True
    )
    pp_call_date = models.DateField(db_column="PP_CALL_DATE", blank=True, null=True)
    pp_call_shift = models.CharField(
        db_column="PP_CALL_SHIFT", max_length=200, blank=True, null=True
    )
    time_remaining_to_deliver = models.DecimalField(
        db_column="TIME_REMAINING_TO_DELIVER",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rank_on_delivery_time = models.IntegerField(
        db_column="RANK_ON_DELIVERY_TIME", blank=True, null=True
    )
    rank_on_order_in_pending_time = models.IntegerField(
        db_column="RANK_ON_ORDER_IN_PENDING_TIME", blank=True, null=True
    )
    ncr_quartile = models.IntegerField(db_column="NCR_QUARTILE", blank=True, null=True)
    customer_categorization_score = models.IntegerField(
        db_column="CUSTOMER_CATEGORIZATION_SCORE", blank=True, null=True
    )
    total_score = models.IntegerField(db_column="TOTAL_SCORE", blank=True, null=True)
    created_at = models.DateField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    exec_calling_sequence = models.BigIntegerField(
        db_column="EXEC_CALLING_SEQUENCE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_PP_CALL_DTL"


class LpSchedulingExecutableDtl(models.Model):
    """Daily scheduling executable details model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    order_master = models.ForeignKey(
        LpSchedulingOrderMaster,
        db_column="ORDER_MASTER_ID",
        on_delete=models.CASCADE,
        related_name="lp_scheduling_executable_dtl",
    )
    executable_date = models.DateField(
        db_column="EXECUTABLE_DATE", blank=True, null=True
    )
    executable_shift = models.IntegerField(
        db_column="EXECUTABLE_SHIFT", blank=True, null=True
    )
    original_source = models.CharField(
        db_column="ORIGINAL_SOURCE", max_length=200, blank=True, null=True
    )
    original_mode = models.CharField(
        db_column="ORIGINAL_MODE", max_length=200, blank=True, null=True
    )
    changed_source = models.CharField(
        db_column="CHANGED_SOURCE", max_length=200, blank=True, null=True
    )
    changed_mode = models.CharField(
        db_column="CHANGED_MODE", max_length=200, blank=True, null=True
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=200, blank=True, null=True
    )
    created_at = models.DateField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    reason = models.CharField(db_column="Reason", max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_EXECUTABLE_DTL"
        ordering = ["id"]


class LpSchedulingVehicleConstraints(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    plant = models.CharField(db_column="PLANT", max_length=1000, blank=True, null=True)
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=1000, blank=True, null=True
    )
    vehicle_size = models.DecimalField(
        db_column="VEHICLE_SIZE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    no_of_vehicles = models.IntegerField(
        db_column="NO_OF_VEHICLES", blank=True, null=True
    )
    current_vehicles = models.IntegerField(
        db_column="CURRENT_VEHICLES", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_VEHICLE_CONSTRAINTS"


class LpSchedulingPlantConstraints(models.Model):
    """Daily Scheduling plant constraints table."""

    id = models.AutoField(db_column="ID", primary_key=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    capacity = models.DecimalField(
        db_column="CAPACITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    current_capacity = models.DecimalField(
        db_column="CURRENT_CAPACITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_PLANT_CONSTRAINTS"
        ordering = ["id"]


class LpSchedulingPackerConstraints(models.Model):
    """Daily Scheduling Packer Constraints table"""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=1000, blank=True, null=True)
    packer_no = models.CharField(
        db_column="PACKER_NO", max_length=1000, blank=True, null=True
    )
    packer_rated_output = models.CharField(
        db_column="PACKER_RATED_OUTPUT", max_length=1000, blank=True, null=True
    )
    truck_loader_number = models.CharField(
        db_column="TRUCK_LOADER_NUMBER", max_length=1000, blank=True, null=True
    )
    loader_rated_output = models.CharField(
        db_column="LOADER_RATED_OUTPUT", max_length=1000, blank=True, null=True
    )
    packer_planned_downtime = models.DateField(
        db_column="PACKER_PLANNED_DOWNTIME", blank=True, null=True
    )
    loader_planned_downtime = models.DateField(
        db_column="LOADER_PLANNED_DOWNTIME", blank=True, null=True
    )
    packer_available = models.BooleanField(
        db_column="PACKER_AVAILABLE", blank=True, null=True
    )
    loader_available = models.BooleanField(
        db_column="LOADER_AVAILABLE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_PACKER_CONSTRAINTS"


class RouteRestrictions(models.Model):
    """Model class for route restrictions data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    link_id = models.DecimalField(
        db_column="LINK_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    max_size = models.DecimalField(
        db_column="MAX_SIZE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    start_time = models.TimeField(db_column="START_TIME")
    end_time = models.TimeField(db_column="END_TIME")
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ROUTE_RESTRICTIONS"
        ordering = ["id"]


class PackerShiftConstraint(models.Model):
    """Model class for packer shift constraint data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant_id = models.CharField(db_column="PLANT_ID", max_length=50)
    rated_output = models.CharField(db_column="RATED_OUTPUT", max_length=50)
    shift = models.CharField(db_column="SHIFT", max_length=50)
    shift_efficiency = models.CharField(db_column="SHIFT_EFFICIENCY", max_length=50)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKER_SHIFT_CONSTRAINT"
        ordering = ["id"]


class BackhaulingProcess(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    inbound_plant = models.CharField(
        db_column="INBOUND_PLANT", max_length=100, blank=True, null=True
    )
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=540, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=540, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=150, blank=True, null=True
    )
    week = models.CharField(db_column="WEEK", max_length=360, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "BACKHAULING_PROCESS"


class DepotAdditionRun(models.Model):
    run_id = models.BigAutoField(db_column="RUN_ID", primary_key=True)
    run_date = models.DateField(db_column="RUN_DATE", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    depot_cost = models.DecimalField(
        db_column="DEPOT_COST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    max_taluka_per_depot = models.DecimalField(
        db_column="MAX_TALUKA_PER_DEPOT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "DEPOT_ADDITION_RUN"


class DepotAdditionOutputView(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    existing_depo_lead = models.DecimalField(
        db_column="EXISTING_DEPO_LEAD",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    recommended_depo_lead = models.DecimalField(
        db_column="RECOMMENDED_DEPO_LEAD",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    run = models.ForeignKey(
        DepotAdditionRun, models.DO_NOTHING, db_column="RUN_ID", blank=True, null=True
    )
    lat = models.DecimalField(
        db_column="LAT", max_digits=22, decimal_places=2, blank=True, null=True
    )
    long = models.DecimalField(
        db_column="LONG", max_digits=22, decimal_places=2, blank=True, null=True
    )
    potential = models.DecimalField(
        db_column="POTENTIAL", max_digits=22, decimal_places=2, blank=True, null=True
    )
    depot_lat = models.DecimalField(
        db_column="DEPOT_LAT", max_digits=22, decimal_places=2, blank=True, null=True
    )
    depot_long = models.DecimalField(
        db_column="DEPOT_LONG", max_digits=22, decimal_places=2, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    depot_opening_cost = models.DecimalField(
        db_column="DEPOT_OPENING_COST",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    no_of_taluka = models.BigIntegerField(
        db_column="NO_OF_TALUKA", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DEPOT_ADDITION_OUTPUT_VIEW"


class SourceChangeFreightMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    brand = models.BigIntegerField(db_column="BRAND", blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    org_type = models.CharField(
        db_column="ORG_TYPE", max_length=360, blank=True, null=True
    )
    incoterm = models.CharField(
        db_column="INCOTERM", max_length=360, blank=True, null=True
    )
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SOURCE_CHANGE_FREIGHT_MASTER"


class SourceChangeApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    changed_source = models.CharField(
        db_column="CHANGED_SOURCE", max_length=360, blank=True, null=True
    )
    changed_mode = models.CharField(
        db_column="CHANGED_MODE", max_length=360, blank=True, null=True
    )
    order = models.ForeignKey(
        LpSchedulingOrderMaster, models.CASCADE, db_column="ORDER"
    )
    rank = models.ForeignKey(LpModelDfRank, models.CASCADE, db_column="RANK")
    persona = models.CharField(
        db_column="PERSONA", max_length=360, blank=True, null=True
    )
    status = models.CharField(
        db_column="STATUS",
        max_length=360,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING.value,
    )
    total_impact = models.BigIntegerField(
        db_column="TOTAL_IMPACT", blank=True, null=True
    )
    approved_at = models.DateTimeField(db_column="APPROVED_AT", blank=True, null=True)
    approver_action_reason = models.CharField(
        db_column="APPROVER_ACTION_REASON", max_length=360, blank=True, null=True
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CREATED_BY", blank=True, null=True
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    changed_inco_terms = models.CharField(
        db_column="CHANGED_INCO_TERMS", max_length=360, blank=True, null=True
    )
    changed_freight_terms = models.CharField(
        db_column="CHANGED_FREIGHT_TERMS", max_length=360, blank=True, null=True
    )
    changed_route_id = models.CharField(
        db_column="CHANGED_ROUTE_ID", max_length=360, blank=True, null=True
    )
    changed_fob = models.CharField(
        db_column="CHANGED_FOB", max_length=360, blank=True, null=True
    )
    changed_run_id_for_changed_source = models.BigIntegerField(
        db_column="CHANGED_RUN_ID_FOR_CHANGED_SOURCE", blank=True, null=True
    )
    approval_type = models.CharField(
        db_column="APPROVAL_TYPE", max_length=360, blank=True, null=True
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=22, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SOURCE_CHANGE_APPROVAL"


class ApprovalThreshold(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    min = models.BigIntegerField(db_column="MIN", blank=True, null=True)
    max = models.BigIntegerField(db_column="MAX", blank=True, null=True)
    persona = models.CharField(
        db_column="PERSONA", max_length=360, blank=True, null=True
    )
    approval = models.CharField(
        db_column="APPROVAL", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "APPROVAL_THRESHOLD"
