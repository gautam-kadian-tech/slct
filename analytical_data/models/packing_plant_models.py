""" Models for Packing Plants - AAC and Cement """
from django.db import models

from accounts.models import User
from analytical_data.models.daily_scheduling_models import (
    LpSchedulingOrderMaster,
)


class TgtTatData(models.Model):
    stage_of_plant = models.CharField(
        db_column="STAGE_OF_PLANT", max_length=300, blank=True, null=True
    )
    truck_no = models.CharField(
        db_column="TRUCK_NO", max_length=100, blank=True, null=True
    )
    delivery_number = models.DecimalField(
        db_column="DELIVERY_NUMBER",
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True,
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=350, blank=True, null=True
    )
    organization_code = models.CharField(
        db_column="ORGANIZATION_CODE", max_length=350, blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=2400, blank=True, null=True
    )
    distance = models.CharField(
        db_column="DISTANCE", max_length=100, blank=True, null=True
    )
    inv_no = models.CharField(db_column="INV_NO", max_length=100, blank=True, null=True)
    item = models.CharField(db_column="ITEM", max_length=500, blank=True, null=True)
    tax_invoice_date = models.CharField(
        db_column="TAX_INVOICE_DATE", max_length=500, blank=True, null=True
    )
    shipped_quantity = models.DecimalField(
        db_column="SHIPPED_QUANTITY",
        max_digits=16,
        decimal_places=0,
        blank=True,
        null=True,
    )
    city = models.CharField(db_column="CITY", max_length=500, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=500, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=500, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=500, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=500, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=500, blank=True, null=True
    )
    diret_sale_or_iso = models.CharField(
        db_column="DIRET_SALE_OR_ISO", max_length=300, blank=True, null=True
    )
    sub_segment = models.CharField(
        db_column="SUB_SEGMENT", max_length=300, blank=True, null=True
    )
    token_id = models.CharField(
        db_column="TOKEN_ID", max_length=300, blank=True, null=True
    )
    transporter_code = models.CharField(
        db_column="TRANSPORTER_CODE", max_length=300, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=300, blank=True, null=True
    )
    di_generated = models.CharField(
        db_column="DI_GENERATED", max_length=300, blank=True, null=True
    )
    dilink = models.CharField(db_column="DILINK", max_length=300, blank=True, null=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=500, blank=True, null=True
    )
    customer_catg = models.CharField(
        db_column="CUSTOMER_CATG", max_length=150, blank=True, null=True
    )
    customer_sub_catg = models.CharField(
        db_column="CUSTOMER_SUB_CATG", max_length=150, blank=True, null=True
    )
    ppcal_in = models.CharField(
        db_column="PPCAL_IN", max_length=500, blank=True, null=True
    )
    sec_in = models.CharField(db_column="SEC_IN", max_length=500, blank=True, null=True)
    tare = models.CharField(db_column="TARE", max_length=500, blank=True, null=True)
    pp_in = models.CharField(db_column="PP_IN", max_length=500, blank=True, null=True)
    pp_out = models.CharField(db_column="PP_OUT", max_length=500, blank=True, null=True)
    gross_wt_time = models.CharField(
        db_column="GROSS_WT_TIME", max_length=400, blank=True, null=True
    )
    ppcal_out = models.CharField(
        db_column="PPCAL_OUT", max_length=400, blank=True, null=True
    )
    sec_out = models.CharField(
        db_column="SEC_OUT", max_length=400, blank=True, null=True
    )
    egp_dt = models.CharField(db_column="EGP_DT", max_length=400, blank=True, null=True)
    gate_out = models.CharField(
        db_column="GATE_OUT", max_length=400, blank=True, null=True
    )
    tare_wt = models.DecimalField(
        db_column="TARE_WT", max_digits=15, decimal_places=0, blank=True, null=True
    )
    gross_wt = models.DecimalField(
        db_column="GROSS_WT", max_digits=15, decimal_places=0, blank=True, null=True
    )
    bid_id = models.DecimalField(
        db_column="BID_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    bid_allocation_time = models.CharField(
        db_column="BID_ALLOCATION_TIME", max_length=500, blank=True, null=True
    )
    total_time = models.CharField(
        db_column="TOTAL_TIME", max_length=50, blank=True, null=True
    )
    gate_entry_time = models.CharField(
        db_column="GATE_ENTRY_TIME", max_length=500, blank=True, null=True
    )
    gate_exit_time = models.CharField(
        db_column="GATE_EXIT_TIME", max_length=500, blank=True, null=True
    )
    diff = models.DecimalField(
        db_column="DIFF", max_digits=15, decimal_places=0, blank=True, null=True
    )
    order_line_id = models.DecimalField(
        db_column="ORDER_LINE_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    order_line_creation_date = models.CharField(
        db_column="ORDER_LINE_CREATION_DATE", max_length=500, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=500, blank=True, null=True)
    delivery_confirm_date = models.CharField(
        db_column="DELIVERY_CONFIRM_DATE", max_length=500, blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TGT_TAT_DATA"


class PackingPlantAacTatReasons(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=20)
    date = models.DateField(db_column="DATE")
    yard_reg_to_di_link_reason = models.CharField(
        db_column="YARD_REG_TO_DI_LINK_REASON", max_length=100, blank=True, null=True
    )
    di_link_to_pp_call_reason = models.CharField(
        db_column="DI_LINK_TO_PP_CALL_REASON", max_length=100, blank=True, null=True
    )
    pp_call_to_sec_in_time_reason = models.CharField(
        db_column="PP_CALL_TO_SEC_IN_TIME_REASON", max_length=100, blank=True, null=True
    )
    sec_in_to_tare_reason = models.CharField(
        db_column="SEC_IN_TO_TARE_REASON", max_length=100, blank=True, null=True
    )
    tare_to_pp_in_reason = models.CharField(
        db_column="TARE_TO_PP_IN_REASON", max_length=100, blank=True, null=True
    )
    pp_in_to_pp_out_reason = models.CharField(
        db_column="PP_IN_TO_PP_OUT_REASON", max_length=100, blank=True, null=True
    )
    pp_out_to_gross_wt_reason = models.CharField(
        db_column="PP_OUT_TO_GROSS_WT_REASON", max_length=100, blank=True, null=True
    )
    gross_wt_to_invoice_reason = models.CharField(
        db_column="GROSS_WT_TO_INVOICE_REASON", max_length=100, blank=True, null=True
    )
    invoice_to_sec_out_reason = models.CharField(
        db_column="INVOICE_TO_SEC_OUT_REASON", max_length=100, blank=True, null=True
    )
    sec_out_to_plant_out_reason = models.CharField(
        db_column="SEC_OUT_TO_PLANT_OUT_REASON", max_length=100, blank=True, null=True
    )
    # plant_time_reason = models.CharField(db_column="PLANT_TIME_REASON", max_length=100)
    # yard_time_reason = models.CharField(db_column="YARD_TIME_REASON", max_length=100)
    other_activity_name = models.CharField(
        db_column="OTHER_ACTIVITY_NAME",
        max_length=20,
        null=True,
        blank=True,
    )
    other_activity_time = models.DecimalField(
        db_column="OTHER_ACTIVITY_TIME",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    other_activity_reason = models.CharField(
        db_column="OTHER_ACTIVITY_REASON",
        max_length=100,
        null=True,
        blank=True,
    )
    date_of_creation = models.DateField(db_column="DATE_OF_CREATION", auto_now_add=True)
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKING_PLANT_AAC_TAT_REASONS"


class PackingPlantCementTatReasons(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=20)
    date = models.DateField(db_column="DATE")
    yard_reg_to_di_link_reason = models.CharField(
        db_column="YARD_REG_TO_DI_LINK_REASON", max_length=100, blank=True, null=True
    )
    di_link_to_pp_call_reason = models.CharField(
        db_column="DI_LINK_TO_PP_CALL_REASON", max_length=100, blank=True, null=True
    )
    pp_call_to_sec_in_time_reason = models.CharField(
        db_column="PP_CALL_TO_SEC_IN_TIME_REASON", max_length=100, blank=True, null=True
    )
    sec_in_to_tare_reason = models.CharField(
        db_column="SEC_IN_TO_TARE_REASON", max_length=100, blank=True, null=True
    )
    tare_to_pp_in_reason = models.CharField(
        db_column="TARE_TO_PP_IN_REASON", max_length=100, blank=True, null=True
    )
    pp_in_to_pp_out_reason = models.CharField(
        db_column="PP_IN_TO_PP_OUT_REASON", max_length=100, blank=True, null=True
    )
    pp_out_to_gross_wt_reason = models.CharField(
        db_column="PP_OUT_TO_GROSS_WT_REASON", max_length=100, blank=True, null=True
    )
    gross_wt_to_invoice_reason = models.CharField(
        db_column="GROSS_WT_TO_INVOICE_REASON", max_length=100, blank=True, null=True
    )
    invoice_to_sec_out_reason = models.CharField(
        db_column="INVOICE_TO_SEC_OUT_REASON", max_length=100, blank=True, null=True
    )
    sec_out_to_plant_out_reason = models.CharField(
        db_column="SEC_OUT_TO_PLANT_OUT_REASON", max_length=100, blank=True, null=True
    )
    # plant_time_reason = models.CharField(db_column="PLANT_TIME_REASON", max_length=100)
    # yard_time_reason = models.CharField(db_column="YARD_TIME_REASON", max_length=100)
    other_activity_name = models.CharField(
        db_column="OTHER_ACTIVITY_NAME",
        max_length=20,
        null=True,
        blank=True,
    )
    other_activity_time = models.DecimalField(
        db_column="OTHER_ACTIVITY_TIME",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    other_activity_reason = models.CharField(
        db_column="OTHER_ACTIVITY_REASON",
        max_length=100,
        null=True,
        blank=True,
    )
    date_of_creation = models.DateField(db_column="DATE_OF_CREATION", auto_now_add=True)
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKING_PLANT_CEMENT_TAT_REASONS"


# class PackingPlantCementTatReasons(models.Model):
#     id = models.BigIntegerField(db_column='ID', primary_key=True)
#     plant = models.CharField(db_column='PLANT', max_length=20)
#     date = models.DateField(db_column='DATE')
#     yard_reg_to_di_link_reason = models.CharField(db_column='YARD_REG_TO_DI_LINK_REASON', max_length=100, blank=True, null=True)
#     di_link_to_pp_call_reason = models.CharField(db_column='DI_LINK_TO_PP_CALL_REASON', max_length=100, blank=True, null=True)
#     pp_call_to_sec_in_time_reason = models.CharField(db_column='PP_CALL_TO_SEC_IN_TIME_REASON', max_length=100, blank=True, null=True)
#     sec_in_to_tare_reason = models.CharField(db_column='SEC_IN_TO_TARE_REASON', max_length=100, blank=True, null=True)
#     tare_to_pp_in_reason = models.CharField(db_column='TARE_TO_PP_IN_REASON', max_length=100, blank=True, null=True)
#     pp_in_to_pp_out_reason = models.CharField(db_column='PP_IN_TO_PP_OUT_REASON', max_length=100, blank=True, null=True)
#     pp_out_to_gross_wt_reason = models.CharField(db_column='PP_OUT_TO_GROSS_WT_REASON', max_length=100, blank=True, null=True)
#     gross_wt_to_invoice_reason = models.CharField(db_column='GROSS_WT_TO_INVOICE_REASON', max_length=100, blank=True, null=True)
#     invoice_to_sec_out_reason = models.CharField(db_column='INVOICE_TO_SEC_OUT_REASON', max_length=100, blank=True, null=True)
#     sec_out_to_plant_out_reason = models.CharField(db_column='SEC_OUT_TO_PLANT_OUT_REASON', max_length=100, blank=True, null=True)
#     other_activity_name = models.CharField(db_column='OTHER_ACTIVITY_NAME', max_length=20, blank=True, null=True)
#     other_activity_time = models.DecimalField(db_column='OTHER_ACTIVITY_TIME', max_digits=5, decimal_places=2, blank=True, null=True)
#     other_activity_reason = models.CharField(db_column='OTHER_ACTIVITY_REASON', max_length=100, blank=True, null=True)
#     date_of_creation = models.DateField(db_column='DATE_OF_CREATION')
#     created_by = models.IntegerField(db_column='CREATED_BY', blank=True, null=True)
#     last_updated_by = models.IntegerField(db_column='LAST_UPDATED_BY', blank=True, null=True)
#     last_update_date = models.DateField(db_column='LAST_UPDATE_DATE', blank=True, null=True)
#     last_update_login = models.IntegerField(db_column='LAST_UPDATE_LOGIN', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'PACKING_PLANT_CEMENT_TAT_REASONS'


class PlantStorage(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=150, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=150, blank=True, null=True
    )
    organization_id = models.BigIntegerField(db_column="ORGANIZATION_ID")
    inventory_item_id = models.BigIntegerField(db_column="INVENTORY_ITEM_ID")
    org_id = models.BigIntegerField(db_column="ORG_ID")
    min_inv_capacity = models.DecimalField(
        db_column="MIN_INV_CAPACITY", max_digits=20, decimal_places=2
    )
    max_inv_capacity = models.DecimalField(
        db_column="MAX_INV_CAPACITY", max_digits=20, decimal_places=2
    )
    effective_start_date = models.DateTimeField(db_column="EFFECTIVE_START_DATE")
    effective_end_date = models.DateTimeField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PLANT_STORAGE"


class PlantDepoSla(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inventory_item_id = models.DecimalField(
        db_column="INVENTORY_ITEM_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    di_link_sla = models.IntegerField(db_column="DI_LINK_SLA", blank=True, null=True)
    dispatch_sla = models.IntegerField(db_column="DISPATCH_SLA", blank=True, null=True)
    product_cat = models.CharField(
        db_column="PRODUCT_CAT", max_length=120, blank=True, null=True
    )
    effective_start_date = models.DateTimeField(
        db_column="EFFECTIVE_START_DATE", blank=True, null=True
    )
    effective_end_date = models.DateTimeField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PLANT_DEPO_SLA"


class ClinkerDispatchPlan(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    shipped_from_plant = models.CharField(
        db_column="SHIPPED_FROM_PLANT", max_length=50, blank=True, null=True
    )
    shipped_to_plant = models.CharField(
        db_column="SHIPPED_TO_PLANT", max_length=50, blank=True, null=True
    )
    shipping_date = models.DateField(db_column="SHIPPING_DATE", blank=True, null=True)
    dispatch_plan_qty_mt = models.DecimalField(
        db_column="DISPATCH_PLAN_QTY_(MT)",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CLINKER_DISPATCH_PLAN"


class PackingPlantBagsStock(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    supplier_code = models.DecimalField(
        db_column="SUPPLIER_CODE", max_digits=20, decimal_places=2
    )
    supplier_name = models.CharField(db_column="SUPPLIER_NAME", max_length=10)
    brand = models.CharField(db_column="BRAND", max_length=10)
    grade = models.CharField(db_column="GRADE", max_length=10)
    packing = models.CharField(db_column="PACKING", max_length=10)
    date_of_procurement = models.DateField(db_column="DATE_OF_PROCUREMENT")
    date_of_receipt = models.DateField(db_column="DATE_OF_RECEIPT")
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2
    )
    original_bill_status = models.CharField(
        db_column="ORIGINAL_BILL_STATUS", max_length=10
    )
    plant = models.CharField(db_column="PLANT", max_length=10)
    remarks = models.TextField(db_column="REMARKS")

    class Meta:
        managed = False
        db_table = "PACKING_PLANT_BAGS_STOCK"


class PackerBagBurstingDesc(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=100, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    nozzle_rounding = models.DecimalField(
        db_column="NOZZLE_ROUNDING",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    problem_at_belt = models.DecimalField(
        db_column="PROBLEM_AT_BELT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bag_quality_issues = models.DecimalField(
        db_column="BAG_QUALITY_ISSUES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bursting_at_loading_point = models.DecimalField(
        db_column="BURSTING_AT_LOADING_POINT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    other = models.DecimalField(
        db_column="OTHER", max_digits=20, decimal_places=2, blank=True, null=True
    )
    total_bursting = models.DecimalField(
        db_column="TOTAL_BURSTING",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=100, blank=True, null=True
    )
    todays_dispatch = models.DecimalField(
        db_column="TODAYS_DISPATCH",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bags_consumption = models.DecimalField(
        db_column="BAGS_CONSUMPTION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bag_bursting_percentage = models.DecimalField(
        db_column="BAG_BURSTING_PERCENTAGE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PACKER_BAG_BURSTING_DESC"


class PackerShiftLevelStoppages(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=50)
    date = models.DateField(db_column="DATE")
    shift = models.IntegerField(db_column="SHIFT")
    packer_code = models.CharField(db_column="PACKER_CODE", max_length=50)
    tl_code = models.CharField(db_column="TL_CODE", max_length=50)
    mech_hrs = models.DecimalField(
        db_column="MECH_HRS", max_digits=20, decimal_places=2
    )
    elec_hrs = models.DecimalField(
        db_column="ELEC_HRS", max_digits=20, decimal_places=2
    )
    inst_hrs = models.DecimalField(
        db_column="INST_HRS", max_digits=20, decimal_places=2
    )
    sch_maintainence = models.DecimalField(
        db_column="SCH_MAINTAINENCE", max_digits=20, decimal_places=2
    )
    mat_extraction = models.DecimalField(
        db_column="MAT_EXTRACTION", max_digits=20, decimal_places=2
    )
    compressor_down = models.DecimalField(
        db_column="COMPRESSOR_DOWN", max_digits=20, decimal_places=2
    )
    mg_changeover = models.DecimalField(
        db_column="MG_CHANGEOVER", max_digits=20, decimal_places=2
    )
    no_trucks = models.DecimalField(
        db_column="NO_TRUCKS", max_digits=20, decimal_places=2
    )
    other_misc = models.DecimalField(
        db_column="OTHER_MISC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    shift_change_or_tea_break_or_truck_placement = models.DecimalField(
        db_column="SHIFT_CHANGE_OR_TEA_BREAK_OR_TRUCK_PLACEMENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    other = models.DecimalField(
        db_column="OTHER", max_digits=20, decimal_places=2, blank=True, null=True
    )
    stoppage_hrs = models.DecimalField(
        db_column="STOPPAGE_HRS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    running_hrs = models.DecimalField(
        db_column="RUNNING_HRS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    tph = models.DecimalField(
        db_column="TPH", max_digits=20, decimal_places=2, blank=True, null=True
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=250, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    labour_unavailability = models.BigIntegerField(
        db_column="LABOUR_UNAVAILABILITY", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKER_SHIFT_LEVEL_STOPPAGES"


class ShiftWiseAdhocPercentage(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=100, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    planned_qty = models.DecimalField(
        db_column="PLANNED_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    adhoc_percent = models.DecimalField(
        db_column="ADHOC_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rail_planned_qty = models.DecimalField(
        db_column="RAIL_PLANNED_QTY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    shift = models.CharField(db_column="SHIFT", max_length=50, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SHIFTWISE_ADHOC_PERCENTAGE"


class PpMaster(models.Model):
    run_id = models.AutoField(db_column="RUN_ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=200, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    shift = models.DecimalField(
        db_column="SHIFT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PP_MASTER"


class PpShiftDetails(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("PpMaster", models.DO_NOTHING, db_column="RUN_ID")
    number_of_packer = models.DecimalField(
        db_column="NUMBER_OF_PACKER",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    number_of_tl = models.DecimalField(
        db_column="NUMBER_OF_TL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    no_of_packer_workers = models.DecimalField(
        db_column="NO_OF_PACKER_WORKERS",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    no_of_loader_workers = models.DecimalField(
        db_column="NO_OF_LOADER_WORKERS",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY", null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY", null=True)
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN", null=True)

    class Meta:
        managed = False
        db_table = "PP_SHIFT_DETAILS"


class PpOrderTagging(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("PpMaster", models.DO_NOTHING, db_column="RUN_ID")
    order_master_id = models.ForeignKey(
        LpSchedulingOrderMaster,
        models.DO_NOTHING,
        db_column="ORDER_MASTER_ID",
        related_name="pp_order_tagging",
    )
    packer_code = models.CharField(
        db_column="PACKER_CODE", max_length=100, blank=True, null=True
    )
    tl_code = models.CharField(
        db_column="TL_CODE", max_length=100, blank=True, null=True
    )
    order_processing_time = models.DecimalField(
        db_column="ORDER_PROCESSING_TIME",
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
    )
    new_time = models.DateTimeField(db_column="NEW_TIME", blank=True, null=True)
    pp_call_rank = models.DecimalField(
        db_column="PP_CALL_RANK", max_digits=20, decimal_places=3, blank=True, null=True
    )
    pp_call_sequence = models.CharField(
        db_column="PP_CALL_SEQUENCE", max_length=100, blank=True, null=True
    )
    tentative_pp_in_time = models.DateTimeField(
        db_column="TENTATIVE_PP_IN_TIME", blank=True, null=True
    )
    token_no = models.BigIntegerField(db_column="TOKEN_NO", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY", null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY", null=True)
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN", null=True)

    class Meta:
        managed = False
        db_table = "PP_ORDER_TAGGING"


class PpDowntime(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=240, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    shift = models.DecimalField(
        db_column="SHIFT", max_digits=25, decimal_places=2, blank=True, null=True
    )
    packer = models.CharField(db_column="PACKER", max_length=240, blank=True, null=True)
    packer_rated_output = models.CharField(
        db_column="PACKER_RATED_OUTPUT", max_length=240, blank=True, null=True
    )
    packer_downtime_hrs = models.DecimalField(
        db_column="PACKER_DOWNTIME_HRS",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    tl_name = models.CharField(
        db_column="TL_NAME", max_length=240, blank=True, null=True
    )
    tl_rated_output = models.CharField(
        db_column="TL_RATED_OUTPUT", max_length=240, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    tl_downtime_hrs = models.DecimalField(
        db_column="TL_DOWNTIME_HRS",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "PP_DOWNTIME"


class PackerRatedCapacity(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=10, blank=True, null=True)
    packer = models.CharField(db_column="PACKER", max_length=50, blank=True, null=True)
    workers_req_for_packer = models.IntegerField(
        db_column="WORKERS_REQ_FOR_PACKER", blank=True, null=True
    )
    packer_rated_capacity_mt_hr = models.DecimalField(
        db_column="PACKER_RATED_CAPACITY_MT/HR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    truck_loader = models.CharField(
        db_column="TRUCK_LOADER", max_length=20, blank=True, null=True
    )
    tl_rated_capacity_mt_hr = models.DecimalField(
        db_column="TL_RATED_CAPACITY_MT/HR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    workers_req_for_tl = models.IntegerField(
        db_column="WORKERS_REQ_FOR_TL", blank=True, null=True
    )
    can_run_multiple_brands = models.CharField(
        db_column="CAN_RUN_MULTIPLE_BRANDS", max_length=10, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    effective_start_date = models.DateTimeField(
        db_column="EFFECTIVE_START_DATE", blank=True, null=True
    )
    effective_end_date = models.DateTimeField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKER_RATED_CAPACITY"


class LpSchedulingDpc(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=100, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=100, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    inv_qty = models.DecimalField(
        db_column="INV_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    plant = models.CharField(db_column="PLANT", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "LP_SCHEDULING_DPC"


class PlantDepoSlaNew(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=360, blank=True, null=True
    )
    organization_id = models.BigIntegerField(
        db_column="ORGANIZATION_ID", blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    inventory_item_id = models.BigIntegerField(
        db_column="INVENTORY_ITEM_ID", blank=True, null=True
    )
    di_link_sla = models.CharField(
        db_column="DI_LINK_SLA", max_length=50, blank=True, null=True
    )
    dispatch_sla = models.CharField(
        db_column="DISPATCH_SLA", max_length=50, blank=True, null=True
    )
    product_cat = models.CharField(
        db_column="PRODUCT_CAT", max_length=50, blank=True, null=True
    )
    effective_start_date = models.DateField(
        db_column="EFFECTIVE_START_DATE", blank=True, null=True
    )
    effective_end_date = models.DateField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )
    sla_to_di_link = models.CharField(
        db_column="SLA_TO_DI_LINK", max_length=50, blank=True, null=True
    )
    yard_to_di_link = models.CharField(
        db_column="YARD_TO_DI_LINK", max_length=50, blank=True, null=True
    )
    sla_to_dispatch = models.CharField(
        db_column="SLA_TO_DISPATCH", max_length=50, blank=True, null=True
    )
    di_link_to_pp_call = models.CharField(
        db_column="DI_LINK_TO_PP_CALL", max_length=50, blank=True, null=True
    )
    pp_call_to_sec_in = models.CharField(
        db_column="PP_CALL_TO_SEC_IN", max_length=50, blank=True, null=True
    )
    sec_in_to_tare = models.CharField(
        db_column="SEC_IN_TO_TARE", max_length=50, blank=True, null=True
    )
    tare_to_pp_in = models.CharField(
        db_column="TARE_TO_PP_IN", max_length=50, blank=True, null=True
    )
    pp_in_to_pp_out = models.CharField(
        db_column="PP_IN_TO_PP_OUT", max_length=50, blank=True, null=True
    )
    pp_out_to_invoice = models.CharField(
        db_column="PP_OUT_TO_INVOICE", max_length=50, blank=True, null=True
    )
    invoice_to_gross = models.CharField(
        db_column="INVOICE_TO_GROSS", max_length=50, blank=True, null=True
    )
    gross_to_sec_out = models.CharField(
        db_column="GROSS_TO_SEC_OUT", max_length=50, blank=True, null=True
    )
    sec_out_to_plant_out = models.CharField(
        db_column="SEC_OUT_TO_PLANT_OUT", max_length=50, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "PLANT_DEPO_SLA_NEW"


class ShiftwiseAdhocQty(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=100, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    planned_qty = models.DecimalField(
        db_column="PLANNED_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    adhoc_qty = models.DecimalField(
        db_column="ADHOC_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rail_planned_qty = models.DecimalField(
        db_column="RAIL_PLANNED_QTY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)
    shift = models.IntegerField(db_column="SHIFT", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now_add=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SHIFTWISE_ADHOC_QTY"


class PpRailOrderTagging(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("PpMaster", models.DO_NOTHING, db_column="RUN_ID")
    rail_order = models.ForeignKey(
        "ShiftwiseAdhocQty", models.DO_NOTHING, db_column="RAIL_ORDER_ID"
    )
    packer_code = models.CharField(
        db_column="PACKER_CODE", max_length=100, blank=True, null=True
    )
    tl_code = models.CharField(
        db_column="TL_CODE", max_length=100, blank=True, null=True
    )
    order_processing_time = models.DecimalField(
        db_column="ORDER_PROCESSING_TIME",
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
    )
    new_time = models.DateTimeField(db_column="NEW_TIME", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now_add=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    brand = models.CharField(db_column="BRAND", max_length=20, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=20, blank=True, null=True)
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=10, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=20, default="RAIL")
    executable_shift = models.DecimalField(
        db_column="EXECUTABLE_SHIFT",
        max_digits=30,
        decimal_places=10,
        blank=True,
        null=True,
    )
    pp_call_rank = models.DecimalField(
        db_column="PP_CALL_RANK", max_digits=20, decimal_places=0, blank=True, null=True
    )
    pp_call_sequence = models.CharField(
        db_column="PP_CALL_SEQUENCE", max_length=100, blank=True, null=True
    )
    tentative_pp_in_time = models.DateTimeField(
        db_column="TENTATIVE_PP_IN_TIME", blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=240, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "PP_RAIL_ORDER_TAGGING"


class MvPendingReasonsForDelay(models.Model):
    delivery_id = models.IntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    delivery_detail_id = models.IntegerField(
        db_column="DELIVERY_DETAIL_ID", primary_key=True
    )
    customer_id = models.CharField(
        db_column="CUSTOMER_ID", max_length=300, blank=True, null=True
    )
    order_number = models.CharField(
        db_column="ORDER_NUMBER", max_length=10050, blank=True, null=True
    )
    source_header_id = models.DecimalField(
        db_column="SOURCE_HEADER_ID",
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
    )
    source_line_id = models.DecimalField(
        db_column="SOURCE_LINE_ID",
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
    )
    ordered_qty = models.DecimalField(
        db_column="ORDERED_QTY",
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
    )
    order_line_creation_date = models.DateTimeField(
        db_column="ORDER_LINE_CREATION_DATE", blank=True, null=True
    )
    delay = models.DecimalField(
        db_column="DELAY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    weighted_delay = models.DecimalField(
        db_column="WEIGHTED_DELAY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.TextField(db_column="STATUS", blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=240, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=240, blank=True, null=True
    )
    segment = models.CharField(
        db_column="SEGMENT", max_length=150, blank=True, null=True
    )
    order_type = models.TextField(db_column="ORDER_TYPE", blank=True, null=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=360, blank=True, null=True
    )
    ship_to_state = models.CharField(
        db_column="SHIP_TO_STATE", max_length=60, blank=True, null=True
    )
    ship_to_district = models.CharField(
        db_column="SHIP_TO_DISTRICT", max_length=60, blank=True, null=True
    )
    ship_to_city = models.CharField(
        db_column="SHIP_TO_CITY", max_length=60, blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=360, blank=True, null=True)
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=240, blank=True, null=True
    )
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=2000, blank=True, null=True
    )
    reasons_for_delay = models.TextField(
        db_column="REASONS_FOR_DELAY", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MV_PENDING_REASONS_FOR_DELAY"


class PpOrderStatus(models.Model):
    delivery_id = models.IntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    delivery_detail_id = models.IntegerField(
        db_column="DELIVERY_DETAIL_ID", blank=True, null=True
    )
    order_type = models.TextField(db_column="ORDER_TYPE", blank=True, null=True)
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=300, blank=True, null=True
    )
    order_id = models.CharField(
        db_column="ORDER_ID", max_length=10050, blank=True, null=True
    )
    order_header_id = models.DecimalField(
        db_column="ORDER_HEADER_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_line_id = models.DecimalField(
        db_column="ORDER_LINE_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    org_id = models.DecimalField(
        db_column="ORG_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inventory_item_id = models.DecimalField(
        db_column="INVENTORY_ITEM_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dispatched_quantity = models.DecimalField(
        db_column="Dispatched Quantity",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_quantity = models.DecimalField(
        db_column="ORDER_QUANTITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    auto_tagged_mode = models.CharField(
        db_column="AUTO_TAGGED_MODE", max_length=240, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=240, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=240, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=2000, blank=True, null=True)
    order_date = models.DateTimeField(db_column="ORDER_DATE", blank=True, null=True)
    request_date = models.DateTimeField(db_column="REQUEST_DATE", blank=True, null=True)
    di_generated = models.DateTimeField(db_column="DI_GENERATED", blank=True, null=True)
    dilink_creation_dt = models.DateTimeField(
        db_column="DILINK_CREATION_DT", blank=True, null=True
    )
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    order_status = models.TextField(db_column="ORDER_STATUS", blank=True, null=True)
    cust_name = models.CharField(
        db_column="CUST_NAME", max_length=360, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=150, blank=True, null=True
    )
    cust_sub_cat = models.CharField(
        db_column="CUST_SUB_CAT", max_length=150, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=60, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=60, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=60, blank=True, null=True
    )
    full_address = models.TextField(db_column="Full Address", blank=True, null=True)
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=150, blank=True, null=True
    )
    vehicle_number = models.CharField(
        db_column="VEHICLE_NUMBER", max_length=150, blank=True, null=True
    )
    auto_tagged_source = models.TextField(
        db_column="AUTO_TAGGED_SOURCE", blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=360, blank=True, null=True
    )
    ship_from_zone = models.CharField(
        db_column="Ship_from_zone", max_length=100, blank=True, null=True
    )
    warehouse = models.DecimalField(
        db_column="WAREHOUSE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ship_to_org_id = models.DecimalField(
        db_column="SHIP_TO_ORG_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    freightterms = models.CharField(
        db_column="FREIGHTTERMS", max_length=3000, blank=True, null=True
    )
    fob = models.CharField(db_column="FOB", max_length=3000, blank=True, null=True)
    token_id = models.DecimalField(
        db_column="TOKEN_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    route = models.CharField(db_column="ROUTE", max_length=150, blank=True, null=True)
    source_location_id = models.DecimalField(
        db_column="SOURCE_LOCATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    shipinglocation = models.DecimalField(
        db_column="SHIPINGLOCATION",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    sales_order_type = models.CharField(
        db_column="SALES_ORDER_TYPE", max_length=240, blank=True, null=True
    )
    released_date = models.DateTimeField(
        db_column="RELEASED_DATE", blank=True, null=True
    )
    delivery_due_date = models.DateTimeField(
        db_column="DELIVERY_DUE_DATE", blank=True, null=True
    )
    pp_call_time = models.DateTimeField(db_column="PP_CALL_TIME", blank=True, null=True)
    tokenno = models.DecimalField(
        db_column="TOKENNO", max_digits=20, decimal_places=0, blank=True, null=True
    )
    status = models.TextField(db_column="STATUS", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "PP_ORDER_STATUS"


class TgtBridgingCost(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    route_id = models.CharField(
        db_column="ROUTE_ID", max_length=10, blank=True, null=True
    )  # this is a foreign key on TOebsSclRouteMaster model class.
    plant = models.CharField(db_column="PLANT", max_length=50, blank=True, null=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=50, blank=True, null=True
    )
    to_org = models.CharField(db_column="TO_ORG", max_length=20, blank=True, null=True)
    rail_bridging_rs_pmt_field = models.DecimalField(
        db_column="RAIL_BRIDGING (Rs.PMT)",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    year = models.DecimalField(
        db_column="YEAR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    effective_start_date = models.DateField(
        db_column="EFFECTIVE_START_DATE", blank=True, null=True
    )
    effective_end_date = models.DateField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )
    active_flag = models.IntegerField(db_column="ACTIVE_FLAG", default=0)

    class Meta:
        managed = False
        db_table = "TGT_BRIDGING_COST"


class TgtTruckCycleTat(models.Model):
    stage_of_plant = models.CharField(
        db_column="STAGE_OF_PLANT", max_length=300, blank=True, null=True
    )
    truck_no = models.CharField(
        db_column="TRUCK_NO", max_length=100, blank=True, null=True
    )
    delivery_number = models.DecimalField(
        db_column="DELIVERY_NUMBER",
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True,
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=350, blank=True, null=True
    )
    organization_code = models.CharField(
        db_column="ORGANIZATION_CODE", max_length=350, blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=2400, blank=True, null=True
    )
    distance = models.CharField(
        db_column="DISTANCE", max_length=100, blank=True, null=True
    )
    inv_no = models.CharField(db_column="INV_NO", max_length=100, blank=True, null=True)
    item = models.CharField(db_column="ITEM", max_length=500, blank=True, null=True)
    tax_invoice_date = models.CharField(
        db_column="TAX_INVOICE_DATE", max_length=500, blank=True, null=True
    )
    shipped_quantity = models.DecimalField(
        db_column="SHIPPED_QUANTITY",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
    )
    ordered_quantity = models.DecimalField(
        db_column="ORDERED_QUANTITY",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
    )
    city = models.CharField(db_column="CITY", max_length=500, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=500, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=500, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=500, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=500, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=500, blank=True, null=True
    )
    diret_sale_or_iso = models.CharField(
        db_column="DIRET_SALE_OR_ISO", max_length=300, blank=True, null=True
    )
    sub_segment = models.CharField(
        db_column="SUB_SEGMENT", max_length=300, blank=True, null=True
    )
    token_id = models.CharField(
        db_column="TOKEN_ID", max_length=300, blank=True, null=True
    )
    transporter_code = models.CharField(
        db_column="TRANSPORTER_CODE", max_length=300, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=300, blank=True, null=True
    )
    di_generated = models.CharField(
        db_column="DI_GENERATED", max_length=300, blank=True, null=True
    )
    dilink = models.CharField(db_column="DILINK", max_length=300, blank=True, null=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=500, blank=True, null=True
    )
    customer_catg = models.CharField(
        db_column="CUSTOMER_CATG", max_length=150, blank=True, null=True
    )
    customer_sub_catg = models.CharField(
        db_column="CUSTOMER_SUB_CATG", max_length=150, blank=True, null=True
    )
    ppcal_in = models.CharField(
        db_column="PPCAL_IN", max_length=500, blank=True, null=True
    )
    sec_in = models.CharField(db_column="SEC_IN", max_length=500, blank=True, null=True)
    tare = models.CharField(db_column="TARE", max_length=500, blank=True, null=True)
    pp_in = models.CharField(db_column="PP_IN", max_length=500, blank=True, null=True)
    pp_out = models.CharField(db_column="PP_OUT", max_length=500, blank=True, null=True)
    gross_wt_time = models.CharField(
        db_column="GROSS_WT_TIME", max_length=400, blank=True, null=True
    )
    ppcal_out = models.CharField(
        db_column="PPCAL_OUT", max_length=400, blank=True, null=True
    )
    sec_out = models.CharField(
        db_column="SEC_OUT", max_length=400, blank=True, null=True
    )
    egp_dt = models.CharField(db_column="EGP_DT", max_length=400, blank=True, null=True)
    gate_out = models.CharField(
        db_column="GATE_OUT", max_length=400, blank=True, null=True
    )
    tare_wt = models.DecimalField(
        db_column="TARE_WT", max_digits=15, decimal_places=0, blank=True, null=True
    )
    gross_wt = models.DecimalField(
        db_column="GROSS_WT", max_digits=15, decimal_places=0, blank=True, null=True
    )
    bid_id = models.DecimalField(
        db_column="BID_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    order_header_id = models.DecimalField(
        db_column="ORDER_HEADER_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    bid_allocation_time = models.CharField(
        db_column="BID_ALLOCATION_TIME", max_length=500, blank=True, null=True
    )
    total_time = models.CharField(
        db_column="TOTAL_TIME", max_length=50, blank=True, null=True
    )
    gate_entry_time = models.CharField(
        db_column="GATE_ENTRY_TIME", max_length=500, blank=True, null=True
    )
    gate_exit_time = models.CharField(
        db_column="GATE_EXIT_TIME", max_length=500, blank=True, null=True
    )
    diff = models.DecimalField(
        db_column="DIFF", max_digits=15, decimal_places=0, blank=True, null=True
    )
    order_line_id = models.DecimalField(
        db_column="ORDER_LINE_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    order_line_creation_date = models.CharField(
        db_column="ORDER_LINE_CREATION_DATE", max_length=500, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=500, blank=True, null=True)
    delivery_confirm_date = models.CharField(
        db_column="DELIVERY_CONFIRM_DATE", max_length=500, blank=True, null=True
    )
    route_id = models.CharField(
        db_column="ROUTE_ID", max_length=20, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TGT_TRUCK_CYCLE_TAT"


class TOebsSclRouteMaster(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    route = models.CharField(db_column="ROUTE", max_length=80, blank=True, null=True)
    route_id = models.IntegerField(db_column="ROUTE_ID", blank=True, null=True)
    route_description = models.CharField(
        db_column="ROUTE_DESCRIPTION", max_length=240, blank=True, null=True
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=240, blank=True, null=True
    )
    freight_amount = models.CharField(
        db_column="FREIGHT_AMOUNT", max_length=20, blank=True, null=True
    )
    from_city = models.CharField(
        db_column="FROM_CITY", max_length=50, blank=True, null=True
    )
    to_city = models.CharField(
        db_column="TO_CITY", max_length=50, blank=True, null=True
    )  # to_city -> rake_point in TgtBridgingCost
    tehsil_name = models.CharField(
        db_column="TEHSIL_NAME", max_length=50, blank=True, null=True
    )
    dist_name = models.CharField(
        db_column="DIST_NAME", max_length=50, blank=True, null=True
    )
    state_name = models.CharField(
        db_column="STATE_NAME", max_length=100, blank=True, null=True
    )
    country = models.CharField(
        db_column="COUNTRY", max_length=100, blank=True, null=True
    )
    distance = models.CharField(
        db_column="DISTANCE", max_length=100, blank=True, null=True
    )
    route_type = models.CharField(
        db_column="ROUTE_TYPE", max_length=240, blank=True, null=True
    )
    transit_time_hours = models.CharField(
        db_column="TRANSIT_TIME_HOURS", max_length=20, blank=True, null=True
    )
    transit_time_mins = models.CharField(
        db_column="TRANSIT_TIME_MINS", max_length=20, blank=True, null=True
    )
    lead_time = models.CharField(
        db_column="LEAD_TIME", max_length=20, blank=True, null=True
    )
    whse = models.CharField(db_column="WHSE", max_length=100, blank=True, null=True)
    route_flag = models.CharField(
        db_column="ROUTE_FLAG", max_length=10, blank=True, null=True
    )
    from_date = models.DateTimeField(db_column="FROM_DATE", blank=True, null=True)
    end_date = models.DateTimeField(db_column="END_DATE", blank=True, null=True)
    active_flag = models.CharField(
        db_column="ACTIVE_FLAG", max_length=10, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=15, decimal_places=0, blank=True, null=True
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=50, blank=True, null=True
    )
    from_city_id = models.DecimalField(
        db_column="FROM_CITY_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    to_city_id = models.DecimalField(
        db_column="TO_CITY_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=100, blank=True, null=True
    )
    inactive_date = models.DateTimeField(
        db_column="INACTIVE_DATE", blank=True, null=True
    )
    secondary_freight_rake_point = models.DecimalField(
        db_column="SECONDARY_FREIGHT_RAKE_POINT",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=500, blank=True, null=True
    )
    route_details = models.CharField(
        db_column="ROUTE_DETAILS", max_length=500, blank=True, null=True
    )
    bulk_update = models.CharField(
        db_column="BULK_UPDATE", max_length=1, blank=True, null=True
    )
    bulk_taluka = models.CharField(
        db_column="BULK_TALUKA", max_length=100, blank=True, null=True
    )
    bulk_dis = models.CharField(
        db_column="BULK_DIS", max_length=100, blank=True, null=True
    )
    bulk_state = models.CharField(
        db_column="BULK_STATE", max_length=100, blank=True, null=True
    )
    bulk_amount = models.DecimalField(
        db_column="BULK_AMOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    bulk_amount_per = models.DecimalField(
        db_column="BULK_AMOUNT_PER",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=100, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=100, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=100, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=100, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=100, blank=True, null=True
    )
    nt_tr = models.CharField(db_column="NT_TR", max_length=100, blank=True, null=True)
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=100, blank=True, null=True
    )
    diesel_qty = models.DecimalField(
        db_column="DIESEL_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    key = models.BigIntegerField(db_column="Key", blank=True, null=True)
    active = models.IntegerField(db_column="Active", blank=True, null=True)
    activestarttime = models.DateTimeField(
        db_column="ActiveStartTime", blank=True, null=True
    )
    activeendtime = models.DateTimeField(
        db_column="ActiveEndTime", blank=True, null=True
    )
    dw_insert_pid = models.CharField(max_length=100, blank=True, null=True)
    dw_insert_tms = models.DateTimeField(blank=True, null=True)
    dw_update_pid = models.CharField(max_length=100, blank=True, null=True)
    dw_update_tms = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "T_OEBS_SCL_ROUTE_MASTER"


class BackUnloadingEnrouteMarketsMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=540, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=540, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=540, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=540, blank=True, null=True
    )
    passing_district = models.CharField(
        db_column="PASSING_DISTRICT", max_length=540, blank=True, null=True
    )
    passing_state = models.CharField(
        db_column="PASSING_STATE", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "BACKUNLOADING_ENROUTE_MARKETS_MASTER"


class L1SourceMapping(models.Model):
    id = models.BigIntegerField(db_column="ID", primary_key=True)
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=50, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=50, blank=True, null=True
    )
    source_id = models.CharField(
        db_column="SOURCE_ID", max_length=50, blank=True, null=True
    )
    from_city_id = models.BigIntegerField(
        db_column="FROM_CITY_ID", blank=True, null=True
    )
    source_city = models.CharField(
        db_column="SOURCE_CITY", max_length=240, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=240, blank=True, null=True
    )
    source_taluka = models.CharField(
        db_column="SOURCE_TALUKA", max_length=240, blank=True, null=True
    )
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=240, blank=True, null=True
    )
    source_type = models.CharField(
        db_column="SOURCE_TYPE", max_length=50, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=50, blank=True, null=True)
    to_city_id = models.BigIntegerField(db_column="TO_CITY_ID", blank=True, null=True)
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=240, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=240, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=240, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=100, blank=True, null=True
    )
    contribution_per_mt = models.DecimalField(
        db_column="CONTRIBUTION_PER_MT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    tlc_per_mt = models.DecimalField(
        db_column="TLC_PER_MT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    sla = models.DecimalField(
        db_column="SLA", max_digits=20, decimal_places=2, blank=True, null=True
    )
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=100, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=50, blank=True, null=True)
    priority = models.IntegerField(db_column="PRIORITY", blank=True, null=True)
    destination_taluka = models.CharField(
        db_column="DESTINATION_TALUKA", max_length=240, blank=True, null=True
    )
    route_id_secondary = models.BigIntegerField(
        db_column="ROUTE_ID_SECONDARY", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "L1_SOURCE_MAPPING"


class SourceChangeMode(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
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
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=200, blank=True, null=True
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
    club_id = models.BigIntegerField(db_column="CLUB_ID", blank=True, null=True)
    di_generated = models.BooleanField(db_column="DI_GENERATED", blank=True, null=True)
    order_executable = models.BooleanField(
        db_column="ORDER_EXECUTABLE", blank=True, null=True
    )
    self_consumption_flag = models.BooleanField(
        db_column="SELF_CONSUMPTION_FLAG", blank=True, null=True
    )
    pp_call = models.BooleanField(db_column="PP_CALL", blank=True, null=True)
    remarks = models.CharField(
        db_column="REMARKS", max_length=1000, blank=True, null=True
    )
    reason = models.CharField(db_column="REASON", max_length=500, blank=True, null=True)
    delivery_id = models.BigIntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    delivery_detail_id = models.BigIntegerField(
        db_column="DELIVERY_DETAIL_ID", blank=True, null=True
    )
    org_id = models.BigIntegerField(db_column="ORG_ID", blank=True, null=True)
    organization_id = models.BigIntegerField(
        db_column="ORGANIZATION_ID", blank=True, null=True
    )
    inventory_item_id = models.BigIntegerField(
        db_column="INVENTORY_ITEM_ID", blank=True, null=True
    )
    dispatched_quantity = models.BigIntegerField(
        db_column="DISPATCHED QUANTITY", blank=True, null=True
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
    full_address = models.TextField(db_column="FULL_ADDRESS", blank=True, null=True)
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
        db_column="SHIP_FROM_ZONE", max_length=50, blank=True, null=True
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
    shipping_location = models.BigIntegerField(
        db_column="SHIPPING_LOCATION", blank=True, null=True
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
    total_quantity = models.DecimalField(
        db_column="TOTAL_QUANTITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    original_tlc = models.DecimalField(
        db_column="ORIGINAL_TLC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    original_sla = models.DecimalField(
        db_column="ORIGINAL_SLA", max_digits=20, decimal_places=2, blank=True, null=True
    )
    changed_tlc = models.DecimalField(
        db_column="CHANGED_TLC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    changed_sla = models.DecimalField(
        db_column="CHANGED_SLA", max_digits=20, decimal_places=2, blank=True, null=True
    )
    planned_node_city = models.CharField(
        db_column="PLANNED_NODE_CITY", max_length=200, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=200, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=200, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=200, blank=True, null=True
    )
    planned_mode = models.CharField(
        db_column="PLANNED_MODE", max_length=200, blank=True, null=True
    )
    planned_sale_type = models.CharField(
        db_column="PLANNED_SALE_TYPE", max_length=200, blank=True, null=True
    )
    planned_source = models.CharField(
        db_column="PLANNED_SOURCE", max_length=200, blank=True, null=True
    )
    # created_by = models.BigIntegerField(db_column="CREATED_BY")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="CREATED_BY"
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SOURCE_CHANGE_MODE"


class TOebsApSuppliers(models.Model):
    vendor_id = models.BigIntegerField(
        db_column="VENDOR_ID", unique=True, primary_key=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    vendor_name = models.CharField(
        db_column="VENDOR_NAME", max_length=240, blank=True, null=True
    )
    vendor_name_alt = models.CharField(
        db_column="VENDOR_NAME_ALT", max_length=320, blank=True, null=True
    )
    segment1 = models.CharField(
        db_column="SEGMENT1", unique=True, max_length=30, blank=True, null=True
    )
    summary_flag = models.CharField(
        db_column="SUMMARY_FLAG", max_length=1, blank=True, null=True
    )
    enabled_flag = models.CharField(
        db_column="ENABLED_FLAG", max_length=1, blank=True, null=True
    )
    segment2 = models.CharField(
        db_column="SEGMENT2", max_length=30, blank=True, null=True
    )
    segment3 = models.CharField(
        db_column="SEGMENT3", max_length=30, blank=True, null=True
    )
    segment4 = models.CharField(
        db_column="SEGMENT4", max_length=30, blank=True, null=True
    )
    segment5 = models.CharField(
        db_column="SEGMENT5", max_length=30, blank=True, null=True
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=15, decimal_places=0, blank=True, null=True
    )
    employee_id = models.DecimalField(
        db_column="EMPLOYEE_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    vendor_type_lookup_code = models.CharField(
        db_column="VENDOR_TYPE_LOOKUP_CODE", max_length=30, blank=True, null=True
    )
    customer_num = models.CharField(
        db_column="CUSTOMER_NUM", max_length=25, blank=True, null=True
    )
    one_time_flag = models.CharField(
        db_column="ONE_TIME_FLAG", max_length=1, blank=True, null=True
    )
    parent_vendor_id = models.DecimalField(
        db_column="PARENT_VENDOR_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    min_order_amount = models.DecimalField(
        db_column="MIN_ORDER_AMOUNT",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ship_to_location_id = models.DecimalField(
        db_column="SHIP_TO_LOCATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    bill_to_location_id = models.DecimalField(
        db_column="BILL_TO_LOCATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ship_via_lookup_code = models.CharField(
        db_column="SHIP_VIA_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    freight_terms_lookup_code = models.CharField(
        db_column="FREIGHT_TERMS_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    fob_lookup_code = models.CharField(
        db_column="FOB_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    terms_id = models.DecimalField(
        db_column="TERMS_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    set_of_books_id = models.DecimalField(
        db_column="SET_OF_BOOKS_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    credit_status_lookup_code = models.CharField(
        db_column="CREDIT_STATUS_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    credit_limit = models.DecimalField(
        db_column="CREDIT_LIMIT", max_digits=15, decimal_places=0, blank=True, null=True
    )
    always_take_disc_flag = models.CharField(
        db_column="ALWAYS_TAKE_DISC_FLAG", max_length=1, blank=True, null=True
    )
    pay_date_basis_lookup_code = models.CharField(
        db_column="PAY_DATE_BASIS_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    pay_group_lookup_code = models.CharField(
        db_column="PAY_GROUP_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    payment_priority = models.DecimalField(
        db_column="PAYMENT_PRIORITY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    invoice_currency_code = models.CharField(
        db_column="INVOICE_CURRENCY_CODE", max_length=15, blank=True, null=True
    )
    payment_currency_code = models.CharField(
        db_column="PAYMENT_CURRENCY_CODE", max_length=15, blank=True, null=True
    )
    invoice_amount_limit = models.DecimalField(
        db_column="INVOICE_AMOUNT_LIMIT",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    exchange_date_lookup_code = models.CharField(
        db_column="EXCHANGE_DATE_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    hold_all_payments_flag = models.CharField(
        db_column="HOLD_ALL_PAYMENTS_FLAG", max_length=1, blank=True, null=True
    )
    hold_future_payments_flag = models.CharField(
        db_column="HOLD_FUTURE_PAYMENTS_FLAG", max_length=1, blank=True, null=True
    )
    hold_reason = models.CharField(
        db_column="HOLD_REASON", max_length=240, blank=True, null=True
    )
    distribution_set_id = models.DecimalField(
        db_column="DISTRIBUTION_SET_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    accts_pay_code_combination_id = models.DecimalField(
        db_column="ACCTS_PAY_CODE_COMBINATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    disc_lost_code_combination_id = models.DecimalField(
        db_column="DISC_LOST_CODE_COMBINATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    disc_taken_code_combination_id = models.DecimalField(
        db_column="DISC_TAKEN_CODE_COMBINATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    expense_code_combination_id = models.DecimalField(
        db_column="EXPENSE_CODE_COMBINATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    prepay_code_combination_id = models.DecimalField(
        db_column="PREPAY_CODE_COMBINATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_1099 = models.CharField(
        db_column="NUM_1099", max_length=30, blank=True, null=True
    )
    type_1099 = models.CharField(
        db_column="TYPE_1099", max_length=10, blank=True, null=True
    )
    withholding_status_lookup_code = models.CharField(
        db_column="WITHHOLDING_STATUS_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    withholding_start_date = models.DateTimeField(
        db_column="WITHHOLDING_START_DATE", blank=True, null=True
    )
    organization_type_lookup_code = models.CharField(
        db_column="ORGANIZATION_TYPE_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    vat_code = models.CharField(
        db_column="VAT_CODE", max_length=30, blank=True, null=True
    )
    start_date_active = models.DateTimeField(
        db_column="START_DATE_ACTIVE", blank=True, null=True
    )
    end_date_active = models.DateTimeField(
        db_column="END_DATE_ACTIVE", blank=True, null=True
    )
    minority_group_lookup_code = models.CharField(
        db_column="MINORITY_GROUP_LOOKUP_CODE", max_length=30, blank=True, null=True
    )
    payment_method_lookup_code = models.CharField(
        db_column="PAYMENT_METHOD_LOOKUP_CODE", max_length=25, blank=True, null=True
    )
    bank_account_name = models.CharField(
        db_column="BANK_ACCOUNT_NAME", max_length=80, blank=True, null=True
    )
    bank_account_num = models.CharField(
        db_column="BANK_ACCOUNT_NUM", max_length=30, blank=True, null=True
    )
    bank_num = models.CharField(
        db_column="BANK_NUM", max_length=25, blank=True, null=True
    )
    bank_account_type = models.CharField(
        db_column="BANK_ACCOUNT_TYPE", max_length=25, blank=True, null=True
    )
    women_owned_flag = models.CharField(
        db_column="WOMEN_OWNED_FLAG", max_length=1, blank=True, null=True
    )
    small_business_flag = models.CharField(
        db_column="SMALL_BUSINESS_FLAG", max_length=1, blank=True, null=True
    )
    standard_industry_class = models.CharField(
        db_column="STANDARD_INDUSTRY_CLASS", max_length=25, blank=True, null=True
    )
    hold_flag = models.CharField(
        db_column="HOLD_FLAG", max_length=1, blank=True, null=True
    )
    purchasing_hold_reason = models.CharField(
        db_column="PURCHASING_HOLD_REASON", max_length=240, blank=True, null=True
    )
    hold_by = models.DecimalField(
        db_column="HOLD_BY", max_digits=9, decimal_places=0, blank=True, null=True
    )
    hold_date = models.DateTimeField(db_column="HOLD_DATE", blank=True, null=True)
    terms_date_basis = models.CharField(
        db_column="TERMS_DATE_BASIS", max_length=25, blank=True, null=True
    )
    price_tolerance = models.DecimalField(
        db_column="PRICE_TOLERANCE",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    inspection_required_flag = models.CharField(
        db_column="INSPECTION_REQUIRED_FLAG", max_length=1, blank=True, null=True
    )
    receipt_required_flag = models.CharField(
        db_column="RECEIPT_REQUIRED_FLAG", max_length=1, blank=True, null=True
    )
    qty_rcv_tolerance = models.DecimalField(
        db_column="QTY_RCV_TOLERANCE",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    qty_rcv_exception_code = models.CharField(
        db_column="QTY_RCV_EXCEPTION_CODE", max_length=25, blank=True, null=True
    )
    enforce_ship_to_location_code = models.CharField(
        db_column="ENFORCE_SHIP_TO_LOCATION_CODE", max_length=25, blank=True, null=True
    )
    days_early_receipt_allowed = models.DecimalField(
        db_column="DAYS_EARLY_RECEIPT_ALLOWED",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    days_late_receipt_allowed = models.DecimalField(
        db_column="DAYS_LATE_RECEIPT_ALLOWED",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    receipt_days_exception_code = models.CharField(
        db_column="RECEIPT_DAYS_EXCEPTION_CODE", max_length=25, blank=True, null=True
    )
    receiving_routing_id = models.DecimalField(
        db_column="RECEIVING_ROUTING_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    allow_substitute_receipts_flag = models.CharField(
        db_column="ALLOW_SUBSTITUTE_RECEIPTS_FLAG", max_length=1, blank=True, null=True
    )
    allow_unordered_receipts_flag = models.CharField(
        db_column="ALLOW_UNORDERED_RECEIPTS_FLAG", max_length=1, blank=True, null=True
    )
    hold_unmatched_invoices_flag = models.CharField(
        db_column="HOLD_UNMATCHED_INVOICES_FLAG", max_length=1, blank=True, null=True
    )
    exclusive_payment_flag = models.CharField(
        db_column="EXCLUSIVE_PAYMENT_FLAG", max_length=1, blank=True, null=True
    )
    ap_tax_rounding_rule = models.CharField(
        db_column="AP_TAX_ROUNDING_RULE", max_length=1, blank=True, null=True
    )
    auto_tax_calc_flag = models.CharField(
        db_column="AUTO_TAX_CALC_FLAG", max_length=1, blank=True, null=True
    )
    auto_tax_calc_override = models.CharField(
        db_column="AUTO_TAX_CALC_OVERRIDE", max_length=1, blank=True, null=True
    )
    amount_includes_tax_flag = models.CharField(
        db_column="AMOUNT_INCLUDES_TAX_FLAG", max_length=1, blank=True, null=True
    )
    tax_verification_date = models.DateTimeField(
        db_column="TAX_VERIFICATION_DATE", blank=True, null=True
    )
    name_control = models.CharField(
        db_column="NAME_CONTROL", max_length=4, blank=True, null=True
    )
    state_reportable_flag = models.CharField(
        db_column="STATE_REPORTABLE_FLAG", max_length=1, blank=True, null=True
    )
    federal_reportable_flag = models.CharField(
        db_column="FEDERAL_REPORTABLE_FLAG", max_length=1, blank=True, null=True
    )
    attribute_category = models.CharField(
        db_column="ATTRIBUTE_CATEGORY", max_length=30, blank=True, null=True
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=150, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=150, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=150, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=150, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=150, blank=True, null=True
    )
    attribute6 = models.CharField(
        db_column="ATTRIBUTE6", max_length=150, blank=True, null=True
    )
    attribute7 = models.CharField(
        db_column="ATTRIBUTE7", max_length=150, blank=True, null=True
    )
    attribute8 = models.CharField(
        db_column="ATTRIBUTE8", max_length=150, blank=True, null=True
    )
    attribute9 = models.CharField(
        db_column="ATTRIBUTE9", max_length=150, blank=True, null=True
    )
    attribute10 = models.CharField(
        db_column="ATTRIBUTE10", max_length=150, blank=True, null=True
    )
    attribute11 = models.CharField(
        db_column="ATTRIBUTE11", max_length=150, blank=True, null=True
    )
    attribute12 = models.CharField(
        db_column="ATTRIBUTE12", max_length=150, blank=True, null=True
    )
    attribute13 = models.CharField(
        db_column="ATTRIBUTE13", max_length=150, blank=True, null=True
    )
    attribute14 = models.CharField(
        db_column="ATTRIBUTE14", max_length=150, blank=True, null=True
    )
    attribute15 = models.CharField(
        db_column="ATTRIBUTE15", max_length=150, blank=True, null=True
    )
    request_id = models.DecimalField(
        db_column="REQUEST_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    program_application_id = models.DecimalField(
        db_column="PROGRAM_APPLICATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    program_id = models.DecimalField(
        db_column="PROGRAM_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    program_update_date = models.DateTimeField(
        db_column="PROGRAM_UPDATE_DATE", blank=True, null=True
    )
    offset_vat_code = models.CharField(
        db_column="OFFSET_VAT_CODE", max_length=20, blank=True, null=True
    )
    vat_registration_num = models.CharField(
        db_column="VAT_REGISTRATION_NUM", max_length=20, blank=True, null=True
    )
    auto_calculate_interest_flag = models.CharField(
        db_column="AUTO_CALCULATE_INTEREST_FLAG", max_length=1, blank=True, null=True
    )
    validation_number = models.DecimalField(
        db_column="VALIDATION_NUMBER",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    exclude_freight_from_discount = models.CharField(
        db_column="EXCLUDE_FREIGHT_FROM_DISCOUNT", max_length=1, blank=True, null=True
    )
    tax_reporting_name = models.CharField(
        db_column="TAX_REPORTING_NAME", max_length=80, blank=True, null=True
    )
    check_digits = models.CharField(
        db_column="CHECK_DIGITS", max_length=30, blank=True, null=True
    )
    bank_number = models.CharField(
        db_column="BANK_NUMBER", max_length=30, blank=True, null=True
    )
    allow_awt_flag = models.CharField(
        db_column="ALLOW_AWT_FLAG", max_length=1, blank=True, null=True
    )
    awt_group_id = models.DecimalField(
        db_column="AWT_GROUP_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    global_attribute1 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE1", max_length=150, blank=True, null=True
    )
    global_attribute2 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE2", max_length=150, blank=True, null=True
    )
    global_attribute3 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE3", max_length=150, blank=True, null=True
    )
    global_attribute4 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE4", max_length=150, blank=True, null=True
    )
    global_attribute5 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE5", max_length=150, blank=True, null=True
    )
    global_attribute6 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE6", max_length=150, blank=True, null=True
    )
    global_attribute7 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE7", max_length=150, blank=True, null=True
    )
    global_attribute8 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE8", max_length=150, blank=True, null=True
    )
    global_attribute9 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE9", max_length=150, blank=True, null=True
    )
    global_attribute10 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE10", max_length=150, blank=True, null=True
    )
    global_attribute11 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE11", max_length=150, blank=True, null=True
    )
    global_attribute12 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE12", max_length=150, blank=True, null=True
    )
    global_attribute13 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE13", max_length=150, blank=True, null=True
    )
    global_attribute14 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE14", max_length=150, blank=True, null=True
    )
    global_attribute15 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE15", max_length=150, blank=True, null=True
    )
    global_attribute16 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE16", max_length=150, blank=True, null=True
    )
    global_attribute17 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE17", max_length=150, blank=True, null=True
    )
    global_attribute18 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE18", max_length=150, blank=True, null=True
    )
    global_attribute19 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE19", max_length=150, blank=True, null=True
    )
    global_attribute20 = models.CharField(
        db_column="GLOBAL_ATTRIBUTE20", max_length=150, blank=True, null=True
    )
    global_attribute_category = models.CharField(
        db_column="GLOBAL_ATTRIBUTE_CATEGORY", max_length=30, blank=True, null=True
    )
    edi_transaction_handling = models.CharField(
        db_column="EDI_TRANSACTION_HANDLING", max_length=25, blank=True, null=True
    )
    edi_payment_method = models.CharField(
        db_column="EDI_PAYMENT_METHOD", max_length=25, blank=True, null=True
    )
    edi_payment_format = models.CharField(
        db_column="EDI_PAYMENT_FORMAT", max_length=25, blank=True, null=True
    )
    edi_remittance_method = models.CharField(
        db_column="EDI_REMITTANCE_METHOD", max_length=25, blank=True, null=True
    )
    edi_remittance_instruction = models.CharField(
        db_column="EDI_REMITTANCE_INSTRUCTION", max_length=256, blank=True, null=True
    )
    bank_charge_bearer = models.CharField(
        db_column="BANK_CHARGE_BEARER", max_length=1, blank=True, null=True
    )
    bank_branch_type = models.CharField(
        db_column="BANK_BRANCH_TYPE", max_length=25, blank=True, null=True
    )
    match_option = models.CharField(
        db_column="MATCH_OPTION", max_length=25, blank=True, null=True
    )
    future_dated_payment_ccid = models.DecimalField(
        db_column="FUTURE_DATED_PAYMENT_CCID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    create_debit_memo_flag = models.CharField(
        db_column="CREATE_DEBIT_MEMO_FLAG", max_length=25, blank=True, null=True
    )
    offset_tax_flag = models.CharField(
        db_column="OFFSET_TAX_FLAG", max_length=1, blank=True, null=True
    )
    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    parent_party_id = models.DecimalField(
        db_column="PARENT_PARTY_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ni_number = models.CharField(
        db_column="NI_NUMBER", max_length=30, blank=True, null=True
    )
    tca_sync_num_1099 = models.CharField(
        db_column="TCA_SYNC_NUM_1099", max_length=30, blank=True, null=True
    )
    tca_sync_vendor_name = models.CharField(
        db_column="TCA_SYNC_VENDOR_NAME", max_length=360, blank=True, null=True
    )
    tca_sync_vat_reg_num = models.CharField(
        db_column="TCA_SYNC_VAT_REG_NUM", max_length=50, blank=True, null=True
    )
    unique_tax_reference_num = models.DecimalField(
        db_column="UNIQUE_TAX_REFERENCE_NUM",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    partnership_utr = models.DecimalField(
        db_column="PARTNERSHIP_UTR",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    partnership_name = models.CharField(
        db_column="PARTNERSHIP_NAME", max_length=240, blank=True, null=True
    )
    cis_enabled_flag = models.CharField(
        db_column="CIS_ENABLED_FLAG", max_length=1, blank=True, null=True
    )
    first_name = models.CharField(
        db_column="FIRST_NAME", max_length=240, blank=True, null=True
    )
    second_name = models.CharField(
        db_column="SECOND_NAME", max_length=240, blank=True, null=True
    )
    last_name = models.CharField(
        db_column="LAST_NAME", max_length=240, blank=True, null=True
    )
    salutation = models.CharField(
        db_column="SALUTATION", max_length=30, blank=True, null=True
    )
    trading_name = models.CharField(
        db_column="TRADING_NAME", max_length=240, blank=True, null=True
    )
    work_reference = models.CharField(
        db_column="WORK_REFERENCE", max_length=30, blank=True, null=True
    )
    company_registration_number = models.CharField(
        db_column="COMPANY_REGISTRATION_NUMBER", max_length=30, blank=True, null=True
    )
    national_insurance_number = models.CharField(
        db_column="NATIONAL_INSURANCE_NUMBER", max_length=30, blank=True, null=True
    )
    verification_number = models.CharField(
        db_column="VERIFICATION_NUMBER", max_length=30, blank=True, null=True
    )
    verification_request_id = models.DecimalField(
        db_column="VERIFICATION_REQUEST_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    match_status_flag = models.CharField(
        db_column="MATCH_STATUS_FLAG", max_length=1, blank=True, null=True
    )
    cis_verification_date = models.DateTimeField(
        db_column="CIS_VERIFICATION_DATE", blank=True, null=True
    )
    individual_1099 = models.CharField(
        db_column="INDIVIDUAL_1099", max_length=30, blank=True, null=True
    )
    pay_awt_group_id = models.DecimalField(
        db_column="PAY_AWT_GROUP_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cis_parent_vendor_id = models.DecimalField(
        db_column="CIS_PARENT_VENDOR_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    bus_class_last_certified_date = models.DateTimeField(
        db_column="BUS_CLASS_LAST_CERTIFIED_DATE", blank=True, null=True
    )
    bus_class_last_certified_by = models.DecimalField(
        db_column="BUS_CLASS_LAST_CERTIFIED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    key = models.BigIntegerField(db_column="Key", blank=True, null=True)
    active = models.IntegerField(db_column="Active", blank=True, null=True)
    activestarttime = models.DateTimeField(
        db_column="ActiveStartTime", blank=True, null=True
    )
    activeendtime = models.DateTimeField(
        db_column="ActiveEndTime", blank=True, null=True
    )
    dw_insert_pid = models.CharField(max_length=100, blank=True, null=True)
    dw_insert_tms = models.DateTimeField(blank=True, null=True)
    dw_update_pid = models.CharField(max_length=100, blank=True, null=True)
    dw_update_tms = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "T_OEBS_AP_SUPPLIERS"


class LogisticsForecastRun(models.Model):
    run_id = models.BigAutoField(db_column="RUN_ID", primary_key=True)
    run_type = models.CharField(
        db_column="RUN_TYPE", max_length=240, blank=True, null=True
    )
    run_date = models.DateField(db_column="RUN_DATE", blank=True, null=True)
    forecast_month = models.DateField(db_column="FORECAST_MONTH", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "LOGISTICS_FORECAST_RUN"


class LogisticsForecastRunDtl(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey(
        "LogisticsForecastRun",
        models.DO_NOTHING,
        db_column="RUN_ID",
        blank=True,
        null=True,
    )
    forecast_demurrage = models.DecimalField(
        db_column="FORECAST_DEMURRAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    forecast_wharfage = models.DecimalField(
        db_column="FORECAST_WHARFAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    source = models.CharField(db_column="SOURCE", max_length=360, blank=True, null=True)
    avg_demurrage = models.DecimalField(
        db_column="AVG_DEMURRAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    min_demurrage = models.DecimalField(
        db_column="MIN_DEMURRAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_demurrage = models.DecimalField(
        db_column="MAX_DEMURRAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    median_demurrage = models.DecimalField(
        db_column="MEDIAN_DEMURRAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    median_wharfage = models.DecimalField(
        db_column="MEDIAN_WHARFAGE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    avg_wharfage = models.DecimalField(
        db_column="AVG_WHARFAGE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    min_wharfage = models.DecimalField(
        db_column="MIN_WHARFAGE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    max_wharfage = models.DecimalField(
        db_column="MAX_WHARFAGE", max_digits=22, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LOGISTICS_FORECAST_RUN_DTL"
