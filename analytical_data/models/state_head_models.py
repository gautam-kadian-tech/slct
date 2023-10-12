from django.db import models

from analytical_data.enum_classes import ApprovalStatusChoices
from analytical_data.utils.send_email import EmailService


class SlctCashDiscProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    schemetype = models.CharField(
        db_column="Schemetype", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=200, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="Packaging", max_length=50, blank=True, null=True
    )
    slabscheme = models.CharField(
        db_column="SlabScheme", max_length=50, blank=True, null=True
    )
    dealerscheme = models.CharField(
        db_column="DealerScheme", max_length=50, blank=True, null=True
    )
    periodstartdate = models.DateField(
        db_column="PeriodStartDate", blank=True, null=True
    )
    periodenddate = models.DateField(db_column="PeriodEndDate", blank=True, null=True)
    invtype = models.CharField(
        db_column="INVType", max_length=50, blank=True, null=True
    )
    gstsource = models.CharField(
        db_column="GstSource", max_length=50, blank=True, null=True
    )
    outflowimpact = models.DecimalField(
        db_column="OutFlowImpact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    dispatchtype = models.CharField(
        db_column="DispatchType", max_length=10, blank=True, null=True
    )
    billto_shipto = models.CharField(
        db_column="BillTo_ShipTo", max_length=10, blank=True, null=True
    )
    saletype = models.CharField(
        db_column="SaleType", max_length=200, blank=True, null=True
    )
    schemetype_0 = models.CharField(
        db_column="SchemeType", max_length=50, blank=True, null=True
    )
    holidayexclude = models.CharField(
        db_column="HolidayExclude", max_length=10, blank=True, null=True
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_CASH_DISC_PROPS"


class AutomatedModelsRunStatus(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    model_name = models.CharField(
        db_column="MODEL_NAME", max_length=255, blank=True, null=True
    )
    run_date = models.DateTimeField(db_column="RUN_DATE", blank=True, null=True)
    run_successful = models.BooleanField(
        db_column="RUN_SUCCESSFUL", blank=True, null=True
    )
    error_msg = models.TextField(db_column="ERROR_MSG", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "AUTOMATED_MODELS_RUN_STATUS"


class SlctCashDiscDaysIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    no_of_days_lower = models.IntegerField(
        db_column="NO_OF_DAYS_LOWER", blank=True, null=True
    )
    no_of_days_upper = models.IntegerField(
        db_column="NO_OF_DAYS_UPPER", blank=True, null=True
    )
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cash_disc = models.ForeignKey(
        "SlctCashDiscProps",
        models.DO_NOTHING,
        db_column="CASH_DISC",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_CASH_DISC_DAYS_INCENTIVE"


class TNmOmxSchemes(models.Model):
    scheme_id = models.BigIntegerField(db_column="SCHEME_ID", primary_key=True)
    scheme_name = models.CharField(
        db_column="SCHEME_NAME", max_length=100, blank=True, null=True
    )
    scheme_short_description = models.CharField(
        db_column="SCHEME_SHORT_DESCRIPTION", max_length=240, blank=True, null=True
    )
    scheme_long_description = models.CharField(
        db_column="SCHEME_LONG_DESCRIPTION", max_length=4000, blank=True, null=True
    )
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=4, blank=True, null=True
    )
    scheme_user_types = models.CharField(
        db_column="SCHEME_USER_TYPES", max_length=200, blank=True, null=True
    )
    quantity_reward_ratio = models.DecimalField(
        db_column="QUANTITY_REWARD_RATIO",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    bag_reward_ratio = models.DecimalField(
        db_column="BAG_REWARD_RATIO",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    start_date = models.DateTimeField(db_column="START_DATE", blank=True, null=True)
    end_date = models.DateTimeField(db_column="END_DATE", blank=True, null=True)
    org_id = models.DecimalField(
        db_column="ORG_ID", max_digits=65535, decimal_places=10, blank=True, null=True
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", auto_now_add=True, blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now=True, blank=True, null=True
    )
    scheme_url = models.CharField(
        db_column="SCHEME_URL", max_length=150, blank=True, null=True
    )
    scheme_status = models.CharField(
        db_column="SCHEME_STATUS", max_length=1, blank=True, null=True
    )
    multi_flag = models.CharField(
        db_column="MULTI_FLAG", max_length=1, blank=True, null=True
    )
    result_date = models.DateTimeField(db_column="RESULT_DATE", blank=True, null=True)
    active_flag = models.CharField(
        db_column="ACTIVE_FLAG", max_length=1, blank=True, null=True
    )
    scheme_number = models.CharField(
        db_column="SCHEME_NUMBER", max_length=150, blank=True, null=True
    )
    scheme_image = models.CharField(
        db_column="SCHEME_IMAGE", max_length=150, blank=True, null=True
    )
    scheme_faq = models.CharField(
        db_column="SCHEME_FAQ", max_length=4000, blank=True, null=True
    )
    scheme_tnc = models.CharField(
        db_column="SCHEME_TNC", max_length=4000, blank=True, null=True
    )
    states = models.CharField(
        db_column="STATES", max_length=4000, blank=True, null=True
    )
    districts = models.CharField(
        db_column="DISTRICTS", max_length=4000, blank=True, null=True
    )
    talukas = models.CharField(
        db_column="TALUKAS", max_length=4000, blank=True, null=True
    )
    cities = models.CharField(
        db_column="CITIES", max_length=4000, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=65535, decimal_places=10, blank=True, null=True
    )
    uom = models.CharField(db_column="UOM", max_length=25, blank=True, null=True)
    base_target = models.DecimalField(
        db_column="BASE_TARGET",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    mitra_types = models.CharField(
        db_column="MITRA_TYPES", max_length=200, blank=True, null=True
    )
    inventory_item_ids = models.CharField(
        db_column="INVENTORY_ITEM_IDS", max_length=200, blank=True, null=True
    )
    packing_types = models.CharField(
        db_column="PACKING_TYPES", max_length=200, blank=True, null=True
    )
    cust_depots = models.CharField(
        db_column="CUST_DEPOTS", max_length=1000, blank=True, null=True
    )
    last_processed_date = models.DateTimeField(
        db_column="LAST_PROCESSED_DATE", blank=True, null=True
    )
    last_processed_by = models.DecimalField(
        db_column="LAST_PROCESSED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    final_processed_date = models.DateTimeField(
        db_column="FINAL_PROCESSED_DATE", blank=True, null=True
    )
    final_processed_by = models.DecimalField(
        db_column="FINAL_PROCESSED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    redemption_start_date = models.DateTimeField(
        db_column="REDEMPTION_START_DATE", blank=True, null=True
    )
    redemption_end_date = models.DateTimeField(
        db_column="REDEMPTION_END_DATE", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=2, blank=True, null=True)
    approval_status = models.CharField(
        db_column="APPROVAL_STATUS", max_length=2, blank=True, null=True
    )
    last_communication_date = models.DateTimeField(
        db_column="LAST_COMMUNICATION_DATE", blank=True, null=True
    )
    last_communication_by = models.DecimalField(
        db_column="LAST_COMMUNICATION_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    last_communication_batch_id = models.DecimalField(
        db_column="LAST_COMMUNICATION_BATCH_ID",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=4000, blank=True, null=True
    )
    parent_scheme_id = models.DecimalField(
        db_column="PARENT_SCHEME_ID",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    last_prepared_date = models.DateTimeField(
        db_column="LAST_PREPARED_DATE", blank=True, null=True
    )
    last_prepared_by = models.DecimalField(
        db_column="LAST_PREPARED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    final_prepared_date = models.DateTimeField(
        db_column="FINAL_PREPARED_DATE", blank=True, null=True
    )
    final_prepared_by = models.DecimalField(
        db_column="FINAL_PREPARED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    approved_by = models.DecimalField(
        db_column="APPROVED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    approved_date = models.DateTimeField(
        db_column="APPROVED_DATE", blank=True, null=True
    )
    released_date = models.DateTimeField(
        db_column="RELEASED_DATE", blank=True, null=True
    )
    released_by = models.DecimalField(
        db_column="RELEASED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    closed_by = models.DecimalField(
        db_column="CLOSED_BY",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    closed_date = models.DateTimeField(db_column="CLOSED_DATE", blank=True, null=True)
    catalogue_id = models.DecimalField(
        db_column="CATALOGUE_ID",
        max_digits=65535,
        decimal_places=10,
        blank=True,
        null=True,
    )
    inventory_item_names = models.CharField(
        db_column="INVENTORY_ITEM_NAMES", max_length=200, blank=True, null=True
    )
    scheme_level = models.CharField(
        db_column="SCHEME_LEVEL", max_length=1, blank=True, null=True
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
        db_table = "T_NM_OMX_SCHEMES"


class SlctPartyWiseSchemeProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    schemetype = models.CharField(
        db_column="Schemetype", max_length=50, blank=True, null=True
    )
    incentive = models.CharField(
        db_column="Incentive", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=200, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_scheme = models.CharField(
        db_column="Slab_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_invoice = models.CharField(
        db_column="On_Invoice", max_length=50, blank=True, null=True
    )
    gst_deductable = models.CharField(
        db_column="GST_Deductable", max_length=50, blank=True, null=True
    )
    outflow_overall = models.DecimalField(
        db_column="Outflow_Overall",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    dispatchtype = models.CharField(
        db_column="DispatchType", max_length=10, blank=True, null=True
    )
    billto_shipto = models.CharField(
        db_column="BillTo_ShipTo", max_length=10, blank=True, null=True
    )
    saletype = models.CharField(
        db_column="SaleType", max_length=200, blank=True, null=True
    )
    schemetype_0 = models.CharField(
        db_column="SchemeType", max_length=50, blank=True, null=True
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_PARTY_WISE_SCHEME_PROPS"


class SlctPartyWiseSchemePropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_code = models.DecimalField(
        db_column="CUSTOMER_CODE", max_digits=20, decimal_places=0
    )
    customer_name = models.CharField(db_column="CUSTOMER_NAME", max_length=20)
    target_incentive_slab1 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab1 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB1", max_length=20, blank=True, null=True
    )
    target_incentive_slab2 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab2 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB2", max_length=20, blank=True, null=True
    )
    target_incentive_slab3 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab3 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB3", max_length=20, blank=True, null=True
    )
    target_incentive_slab4 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB4",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab4 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB4", max_length=20, blank=True, null=True
    )
    target_incentive_slab5 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB5",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab5 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB5", max_length=20, blank=True, null=True
    )
    target_incentive_slab6 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB6",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab6 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB6", max_length=20, blank=True, null=True
    )
    target_incentive_slab7 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB7",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab7 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB7", max_length=20, blank=True, null=True
    )
    target_incentive_slab8 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB8",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab8 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB8", max_length=20, blank=True, null=True
    )
    party_wise_scheme = models.ForeignKey(
        "SlctPartyWiseSchemeProps",
        models.DO_NOTHING,
        db_column="PARTY_WISE_SCHEME",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_PARTY_WISE_SCHEME_PROPS_INCENTIVE"


class SlctQuantitySlabProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    schemetype = models.CharField(
        db_column="Schemetype", max_length=50, blank=True, null=True
    )
    incentivetype = models.CharField(
        db_column="Incentivetype", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=200, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_scheme = models.CharField(
        db_column="Slab_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_invoice = models.CharField(
        db_column="On_Invoice", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_Ded_source", max_length=50, blank=True, null=True
    )
    outflow_over_impact = models.DecimalField(
        db_column="Outflow_Over_Impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    dispatchtype = models.CharField(
        db_column="DispatchType", max_length=10, blank=True, null=True
    )
    billto_shipto = models.CharField(
        db_column="BillTo_ShipTo", max_length=10, blank=True, null=True
    )
    saletype = models.CharField(
        db_column="SaleType", max_length=200, blank=True, null=True
    )
    schemetype_0 = models.CharField(
        db_column="SchemeType", max_length=50, blank=True, null=True
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_QUANTITY_SLAB_PROPS"


class SlctQuantitySlabPropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.IntegerField(
        db_column="QUANTITY_SLAB_LOWER", blank=True, null=True
    )
    quantity_slab_upper = models.IntegerField(
        db_column="QUANTITY_SLAB_UPPER", blank=True, null=True
    )
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    incentive_kind = models.CharField(
        db_column="INCENTIVE_KIND", max_length=20, blank=True, null=True
    )
    quantity_slab = models.ForeignKey(
        "SlctQuantitySlabProps",
        models.DO_NOTHING,
        db_column="QUANTITY_SLAB",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_QUANTITY_SLAB_PROPS_INCENTIVE"


class SlctDirPltBilngDiscProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_dedt_source = models.CharField(
        db_column="GST_DedT_source", max_length=50, blank=True, null=True
    )
    dispatch_type = models.CharField(max_length=50, blank=True, null=True)
    outflow_impact = models.DecimalField(
        db_column="Outflow_Impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_DIR_PLT_BILNG_DISC_PROPS"


class SlctDirPltBilngDiscPropsIncentives(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    inc_district = models.CharField(db_column="INC_DISTRICT", max_length=20)
    plant = models.CharField(db_column="PLANT", max_length=20, blank=True, null=True)
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=10, decimal_places=2, blank=True, null=True
    )
    dir_plt_bilng = models.ForeignKey(
        SlctDirPltBilngDiscProps,
        models.DO_NOTHING,
        db_column="DIR_PLT_BILNG",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_DIR_PLT_BILNG_DISC_PROPS_INCENTIVES"


class SlctPrmPrdComboScmProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_Based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_Ded_source", max_length=50, blank=True, null=True
    )
    period_base_from_date = models.DateField(
        db_column="period_base_From_Date", blank=True, null=True
    )
    period_base_to_date = models.DateField(
        db_column="period_base_To_Date", blank=True, null=True
    )
    base_brand_target = models.CharField(
        db_column="Base_Brand_target", max_length=50, blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="Outflow_Overall_Imp",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_PRM_PRD_COMBO_SCM_PROPS"


class SlctPrmPrdComboScmPropsIncentives(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.IntegerField(db_column="QUANTITY_SLAB_LOWER")
    quantity_slab_upper = models.IntegerField(db_column="QUANTITY_SLAB_UPPER")
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=30, blank=True, null=True
    )
    prm_prdt_combo = models.ForeignKey(
        SlctPrmPrdComboScmProps,
        models.DO_NOTHING,
        db_column="PRM_PRDT_COMBO",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_PRM_PRD_COMBO_SCM_PROPS_INCENTIVES"


class SlctVehicleSchProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="Period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_dedt_at_source = models.CharField(
        db_column="GST_DedT_at_source", max_length=50, blank=True, null=True
    )
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=50, blank=True, null=True
    )
    scheme_appl_disp_type = models.CharField(
        db_column="Scheme_appl_disp_type", max_length=50, blank=True, null=True
    )
    sale_flag = models.CharField(
        db_column="Sale_Flag", max_length=50, blank=True, null=True
    )
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    outflow_overall = models.DecimalField(
        db_column="Outflow_Overall",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_VEHICLE_SCH_PROPS"


class SlctVehicleSchPropsIncentives(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=20)
    inc_district = models.CharField(db_column="INC_DISTRICT", max_length=20)
    city = models.CharField(db_column="CITY", max_length=20)
    inc_vehicle_type = models.CharField(db_column="INC_VEHICLE_TYPE", max_length=30)
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    vechicle_sch_props = models.ForeignKey(
        SlctVehicleSchProps,
        models.DO_NOTHING,
        db_column="VECHICLE_SCH_PROPS",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_VEHICLE_SCH_PROPS_INCENTIVES"


class SlctMasonKindSchProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    engineer_scheme = models.CharField(
        db_column="Engineer_Scheme", max_length=50, blank=True, null=True
    )
    points_to_value_conv = models.DecimalField(
        db_column="Points_to_Value_Conv",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    overflow_overall = models.DecimalField(
        db_column="Overflow_Overall",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    comments = models.CharField(
        db_column="Comments", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_MASON_KIND_SCH_PROPS"


class SlctMasonKindSchBagPointConv(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=20, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=20, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=20, blank=True, null=True
    )
    bags_point_conv_rto = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        db_column="BAGS_POINT_CONV_RTO",
        blank=True,
        null=True,
    )
    mason_kind_sch = models.ForeignKey(
        SlctMasonKindSchProps,
        models.DO_NOTHING,
        db_column="MASON_KIND_SCH",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_MASON_KIND_SCH_BAG_POINT_CONV"


class SlctMasonKindSchPropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    point_slab_lower = models.IntegerField(
        db_column="POINT_SLAB_LOWER", blank=True, null=True
    )
    point_slab_upper = models.IntegerField(
        db_column="POINT_SLAB_UPPER", blank=True, null=True
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    cash_incentive = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        db_column="CASH_INCENTIVE",
        blank=True,
        null=True,
    )
    mason_kind_sch = models.ForeignKey(
        SlctMasonKindSchProps,
        models.DO_NOTHING,
        db_column="MASON_KIND_SCH",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_MASON_KIND_SCH_PROPS_INCENTIVE"


class SlctBorderDiscProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_off_Invoice", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_Ded_source", max_length=50, blank=True, null=True
    )
    dispatch_type = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="Outflow_Overall_Imp",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BORDER_DISC_PROPS"


class SlctBorderDiscPropsIncentives(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=20)
    inc_district = models.CharField(db_column="INC_DISTRICT", max_length=20)
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    border_disc = models.ForeignKey(
        "SlctBorderDiscProps",
        models.DO_NOTHING,
        db_column="BORDER_DISC",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_BORDER_DISC_PROPS_INCENTIVES"


class SlctActivityProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_ACTIVITY_PROPS"


class SlctActivityPropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    cost_head = models.CharField(
        db_column="COST_HEAD", max_length=70, blank=True, null=True
    )
    no_of_pax = models.IntegerField(db_column="NO_OF_PAX", blank=True, null=True)
    cost_per_head = models.IntegerField(
        db_column="COST_PER_HEAD", blank=True, null=True
    )
    total_expense = models.IntegerField(
        db_column="TOTAL_EXPENSE", blank=True, null=True
    )
    activity_props = models.ForeignKey(
        "SlctActivityProps",
        models.DO_NOTHING,
        db_column="ACTIVITY_PROPS",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_ACTIVITY_PROPS_INCENTIVE"


class SlctEngCashSchPtProps(models.Model):
    """select engineer cash scheme props model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    engineer_scheme = models.CharField(
        db_column="Engineer_Scheme", max_length=50, blank=True, null=True
    )
    points_conv_ratio = models.DecimalField(
        db_column="Points_Conv_Ratio",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    overflow_overall_impact = models.DecimalField(
        db_column="Overflow_Overall_impact",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    comments = models.CharField(
        db_column="Comments", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_ENG_CASH_SCH_PT_PROPS"


class SlctEngCashSchPtBagPointConv(models.Model):
    """select engineer cash scheme bag point conv model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=20)
    product = models.CharField(db_column="PRODUCT", max_length=20)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=20, blank=True, null=True
    )
    bags_point_conv_rto = models.DecimalField(
        db_column="BAGS_POINT_CONV_RTO",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    eng_cash_sch_pt = models.ForeignKey(
        "SlctEngCashSchPtProps",
        models.DO_NOTHING,
        db_column="ENG_CASH_SCH_PT",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_ENG_CASH_SCH_PT_BAG_POINT_CONV"


class SlctEngCashSchPtPropsIncentive(models.Model):
    """select engineer cash scheme proposal incentive model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    point_slab_lower = models.DecimalField(
        db_column="POINT_SLAB_LOWER", max_digits=20, decimal_places=2
    )
    point_slab_upper = models.DecimalField(
        db_column="POINT_SLAB_UPPER", max_digits=20, decimal_places=2
    )
    in_kind_incentive = models.CharField(
        db_column="IN_KIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    cash_incentive = models.DecimalField(
        db_column="CASH_INCENTIVE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    eng_cash_sch_pt = models.ForeignKey(
        "SlctEngCashSchPtProps",
        models.DO_NOTHING,
        db_column="ENG_CASH_SCH_PT",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_ENG_CASH_SCH_PT_PROPS_INCENTIVE"


class SlctRailBasedSchProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_dedt_source = models.CharField(
        db_column="GST_DedT_source", max_length=50, blank=True, null=True
    )
    railhead = models.CharField(
        db_column="Railhead", max_length=50, blank=True, null=True
    )
    outflow_overall_impact = models.DecimalField(
        db_column="Outflow_overall_impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comments = models.CharField(
        db_column="Comments", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_RAIL_BASED_SCH_PROPS"


class SlctRailBasedSchPropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    point_slab_lower = models.DecimalField(
        db_column="POINT_SLAB_LOWER", max_digits=20, decimal_places=2
    )
    point_slab_upper = models.DecimalField(
        db_column="POINT_SLAB_UPPER", max_digits=20, decimal_places=2
    )
    incentive_total_sales = models.DecimalField(
        db_column="INCENTIVE_TOTAL_SALES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    in_kind_incentive = models.CharField(
        db_column="IN_KIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    rail_based_sch = models.ForeignKey(
        "SlctRailBasedSchProps",
        models.DO_NOTHING,
        db_column="RAIL_BASED_SCH",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_RAIL_BASED_SCH_PROPS_INCENTIVE"


class SlctDealerOutsBasedProps(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_dedt_source = models.CharField(
        db_column="GST_DedT_source", max_length=50, blank=True, null=True
    )
    period_outs_from_date = models.DateField(
        db_column="Period_Outs_From_Date", blank=True, null=True
    )
    period_outs_to_date = models.DateField(
        db_column="Period_Outs_To_Date", blank=True, null=True
    )
    outflow_overall_impact = models.DecimalField(
        db_column="Outflow_Overall_Impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_DEALER_OUTS_BASED_PROPS"


class SlctDealerOutsBasedPropsIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    outstanding_threshold = models.DecimalField(
        db_column="OUTSTANDING_THRESHOLD", max_digits=20, decimal_places=2
    )
    target_incentive = models.DecimalField(
        db_column="TARGET_INCENTIVE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    in_kind_incentive = models.CharField(
        db_column="IN_KIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    dealer_outs = models.ForeignKey(
        SlctDealerOutsBasedProps,
        models.DO_NOTHING,
        db_column="DEALER_OUTS",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_DEALER_OUTS_BASED_PROPS_INCENTIVE"


class SlctDealerLinkedSchProps(models.Model):
    """slct dealer linked scheme proposal model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    scheme_application = models.CharField(
        db_column="SCHEME_APPLICATION", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_off_Invoice", max_length=50, blank=True, null=True
    )
    gst_dedt_source = models.CharField(
        db_column="GST_dedt_source", max_length=50, blank=True, null=True
    )
    target_type = models.CharField(
        db_column="Target_Type", max_length=50, blank=True, null=True
    )
    outflow_overall_impact = models.DecimalField(
        db_column="Outflow_Overall_Impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_DEALER_LINKED_SCH_PROPS"


class SlctDealerLinkedSchPropsIncentive(models.Model):
    """slct dealer linked scheme proposal incentive model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER", max_digits=20, decimal_places=2
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER", max_digits=20, decimal_places=2
    )
    incentive_on_t_sale = models.DecimalField(
        db_column="INCENTIVE_ON_T_SALE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    points = models.DecimalField(
        db_column="POINTS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    add_incentive_thres = models.DecimalField(
        db_column="ADD_INCENTIVE_THRES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    add_incentive = models.DecimalField(
        db_column="ADD_INCENTIVE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    add_inkind_incentive = models.CharField(
        db_column="ADD_INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    add_points = models.DecimalField(
        db_column="ADD_POINTS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    dealer_linked_sch = models.ForeignKey(
        "SlctDealerLinkedSchProps",
        models.DO_NOTHING,
        db_column="DEALER_LINKED_SCH",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_DEALER_LINKED_SCH_PROPS_INCENTIVE"


class SlctCombSlabGrowthProps(models.Model):
    """Slct comb slab growth props model class."""

    id = models.BigAutoField(primary_key=True)
    scheme_type = models.CharField(max_length=50, blank=True, null=True)
    incentive_type = models.CharField(max_length=50, blank=True, null=True)
    zone = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    packaging = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    slab_scheme = models.CharField(max_length=50, blank=True, null=True)
    period_from_date = models.DateField(blank=True, null=True)
    period_to_date = models.DateField(blank=True, null=True)
    dealer_scheme = models.CharField(max_length=50, blank=True, null=True)
    gst_deduct = models.BooleanField(blank=True, null=True)
    scheme_period_from = models.DateField(blank=True, null=True)
    scheme_period_to = models.DateField(blank=True, null=True)
    base_brand = models.CharField(max_length=50, blank=True, null=True)
    on_invoice = models.CharField(max_length=50, blank=True, null=True)
    outflow_overall = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True
    )
    comment = models.CharField(max_length=500, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    dispatchtype = models.CharField(
        db_column="DispatchType", max_length=10, blank=True, null=True
    )
    billto_shipto = models.CharField(
        db_column="BillTo_ShipTo", max_length=10, blank=True, null=True
    )
    saletype = models.CharField(
        db_column="SaleType", max_length=200, blank=True, null=True
    )
    schemetype = models.CharField(
        db_column="SchemeType", max_length=50, blank=True, null=True
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )
    created_by = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)
    last_updated_by = models.IntegerField()
    last_update_date = models.DateField(auto_now=True)
    last_update_login = models.IntegerField()

    class Meta:
        managed = False
        db_table = "SLCT_COMB_SLAB_GROWTH_PROPS"


class SlctCombSlabGrowthPropsIncentive(models.Model):
    """Slct comb slab growth props incentives model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER", max_digits=20, decimal_places=2
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER", max_digits=20, decimal_places=2
    )
    target_incentive_slab1 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab1 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB1", max_length=20, blank=True, null=True
    )
    target_incentive_slab2 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab2 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB2", max_length=20, blank=True, null=True
    )
    target_incentive_slab3 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab3 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB3", max_length=20, blank=True, null=True
    )
    target_incentive_slab4 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB4",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab4 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB4", max_length=20, blank=True, null=True
    )
    target_incentive_slab5 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB5",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab5 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB5", max_length=20, blank=True, null=True
    )
    target_incentive_slab6 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB6",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab6 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB6", max_length=20, blank=True, null=True
    )
    target_incentive_slab7 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB7",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab7 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB7", max_length=20, blank=True, null=True
    )
    target_incentive_slab8 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB8",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab8 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB8", max_length=20, blank=True, null=True
    )
    comb_slab_props = models.ForeignKey(
        "SlctCombSlabGrowthProps",
        models.CASCADE,
        db_column="COMB_SLAB_PROPS",
        related_name="incentives",
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_COMB_SLAB_GROWTH_PROPS_INCENTIVE"


class SlctVolCutterTargetBased(models.Model):
    """slct vol cutter target based model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    scheme_sub_type = models.CharField(
        db_column="SCHEME_SUB_TYPE", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="INCENTIVE_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    packing = models.CharField(
        db_column="PACKING", max_length=50, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    slab_scheme = models.CharField(
        db_column="SLAB_SCHEME", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="PERIOD_FROM_DATE", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="PERIOD_TO_DATE", blank=True, null=True)
    dealer_scheme = models.CharField(
        db_column="DEALER_SCHEME", max_length=50, blank=True, null=True
    )
    on_invoice = models.CharField(
        db_column="ON_INVOICE", max_length=50, blank=True, null=True
    )
    outflow_overall = models.DecimalField(
        db_column="OUTFLOW_OVERALL",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_VOL_CUTTER_TARGET_BASED"


class SlctVolCutterTargetBasedIncentive(models.Model):
    """slct vol cutter target based incentive model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_code = models.DecimalField(
        db_column="CUSTOMER_CODE", max_digits=20, decimal_places=0
    )
    customer_name = models.CharField(db_column="CUSTOMER_NAME", max_length=20)
    target_incentive_slab1 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab1 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB1", max_length=20, blank=True, null=True
    )
    target_incentive_slab2 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab2 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB2", max_length=20, blank=True, null=True
    )
    target_incentive_slab3 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab3 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB3", max_length=20, blank=True, null=True
    )
    target_incentive_slab4 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB4",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab4 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB4", max_length=20, blank=True, null=True
    )
    target_incentive_slab5 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB5",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab5 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB5", max_length=20, blank=True, null=True
    )
    target_incentive_slab6 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB6",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab6 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB6", max_length=20, blank=True, null=True
    )
    target_incentive_slab7 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB7",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab7 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB7", max_length=20, blank=True, null=True
    )
    target_incentive_slab8 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB8",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab8 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB8", max_length=20, blank=True, null=True
    )
    vol_cutter_slab_basd = models.ForeignKey(
        "SlctVolCutterTargetBased",
        models.DO_NOTHING,
        db_column="VOL_CUTTER_SLAB_BASD",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_VOL_CUTTER_TARGET_BASED_INCENTIVE"


class SlctVolCutterSlabBasedProposal(models.Model):
    """slct vol cutter slab based proposal model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    scheme_sub_type = models.CharField(
        db_column="SCHEME_SUB_TYPE", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="INCENTIVE_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    packing = models.CharField(
        db_column="PACKING", max_length=50, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    slab_scheme = models.CharField(
        db_column="SLAB_SCHEME", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="PERIOD_FROM_DATE", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="PERIOD_TO_DATE", blank=True, null=True)
    dealer_scheme = models.CharField(
        db_column="DEALER_SCHEME", max_length=50, blank=True, null=True
    )
    on_invoice = models.CharField(
        db_column="ON_INVOICE", max_length=50, blank=True, null=True
    )
    outflow_overall = models.DecimalField(
        db_column="OUTFLOW_OVERALL",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_VOL_CUTTER_SLAB_BASED_PROPOSAL"


class SlctVolCutterSlabBasedProposalIncentives(models.Model):
    """slct vol cutter slab based proposal incentives model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER",
        max_digits=65,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER",
        max_digits=65,
        decimal_places=2,
        blank=True,
        null=True,
    )
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    vol_cutter_slab_bsd = models.ForeignKey(
        "SlctVolCutterSlabBasedProposal",
        models.DO_NOTHING,
        db_column="VOL_CUTTER_SLAB_BSD",
        blank=True,
        null=True,
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=65, decimal_places=2
    )
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY", max_digits=65, decimal_places=2
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN", max_digits=65, decimal_places=2
    )

    class Meta:
        managed = False
        db_table = "SLCT_VOL_CUTTER_SLAB_BASED_PROPOSAL_INCENTIVES"


class SlctBoosterPerDayTargetScheme(models.Model):
    """slct booster per day target scheme model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="INCENTIVE_TYPE", max_length=50, blank=True, null=True
    )
    sub_scheme_type = models.CharField(
        db_column="SUB_SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    slab_based_scheme = models.CharField(
        db_column="SLAB_BASED_SCHEME", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="DEALER_SCHEME", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="PERIOD_FROM_DATE", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="PERIOD_TO_DATE", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="ON_OFF_INVOICE", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_DED_SOURCE", max_length=50, blank=True, null=True
    )
    scheme_target_parameters = models.CharField(
        db_column="SCHEME_TARGET_PARAMETERS", max_length=50, blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="OUTFLOW_OVERALL_IMP",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BOOSTER_PER_DAY_TARGET_SCHEME"


class SlctBoosterPerDayTargetSchemeIncentive(models.Model):
    """slct booster per day target scheme incentive model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER",
        max_digits=65535,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER",
        max_digits=65535,
        decimal_places=2,
        blank=True,
        null=True,
    )
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    booster_per_day_target = models.ForeignKey(
        "SlctBoosterPerDayTargetScheme",
        models.DO_NOTHING,
        db_column="BOOSTER_PER_DAY_TARGET",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    additional_incentive = models.DecimalField(
        db_column="ADDITIONAL_INCENTIVE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    additional_inkind_incentive = models.CharField(
        db_column="ADDITIONAL_INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BOOSTER_PER_DAY_TARGET_SCHEME_INCENTIVE"


class SlctBoosterPerDayGrowthScheme(models.Model):
    """slct booster per day growth scheme model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="INCENTIVE_TYPE", max_length=50, blank=True, null=True
    )
    sub_scheme_type = models.CharField(
        db_column="SUB_SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    slab_based_scheme = models.CharField(
        db_column="SLAB_BASED_SCHEME", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="DEALER_SCHEME", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="PERIOD_FROM_DATE", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="PERIOD_TO_DATE", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="ON_OFF_INVOICE", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_DED_SOURCE", max_length=50, blank=True, null=True
    )
    scheme_target_parameters = models.CharField(
        db_column="SCHEME_TARGET_PARAMETERS", max_length=50, blank=True, null=True
    )
    base_brand_for_target = models.CharField(
        db_column="BASE_BRAND_FOR_TARGET", max_length=50, blank=True, null=True
    )
    period_base_tgt_from_date = models.DateField(
        db_column="PERIOD_BASE_TGT_FROM_DATE", blank=True, null=True
    )
    period_base_tgt_to_date = models.DateField(
        db_column="PERIOD_BASE_TGT_TO_DATE", blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="OUTFLOW_OVERALL_IMP",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BOOSTER_PER_DAY_GROWTH_SCHEME"


class SlctBoosterPerDayGrowthSchemeIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_1 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_inkind_incentive_slab_1 = models.CharField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_1", max_length=20, blank=True, null=True
    )
    booster_per_growth_target = models.ForeignKey(
        "SlctBoosterPerDayGrowthScheme",
        models.DO_NOTHING,
        db_column="BOOSTER_PER_GROWTH_TARGET",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    target_incentive_slab_2 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_3 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_4 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_4",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_5 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_5",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_6 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_6",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_7 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_7",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_incentive_slab_8 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB_8",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_inkind_incentive_slab_2 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_2", blank=True, null=True
    )
    target_inkind_incentive_slab_3 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_3", blank=True, null=True
    )
    target_inkind_incentive_slab_4 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_4", blank=True, null=True
    )
    target_inkind_incentive_slab_5 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_5", blank=True, null=True
    )
    target_inkind_incentive_slab_6 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_6", blank=True, null=True
    )
    target_inkind_incentive_slab_7 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_7", blank=True, null=True
    )
    target_inkind_incentive_slab_8 = models.TextField(
        db_column="TARGET_INKIND_INCENTIVE_SLAB_8", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BOOSTER_PER_DAY_GROWTH_SCHEME_INCENTIVE"


class SlctBenchmarkChangeRequest(models.Model):
    """slct benchmark change request model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_type = models.CharField(
        db_column="REQUEST_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    price_chg_efft_date = models.DateField(
        db_column="PRICE_CHG_EFFT_DATE", blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    price_list = models.DecimalField(
        db_column="PRICE_LIST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BENCHMARK_CHANGE_REQUEST"


class SlctBenchmarkChangeRequestBillingGap(models.Model):
    """slct benchmarkchange request billing gap model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    average_volume = models.DecimalField(
        db_column="AVERAGE_VOLUME",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share = models.DecimalField(
        db_column="MARKET_SHARE",
        max_digits=65535,
        decimal_places=2,
        blank=True,
        null=True,
    )
    benchmark_current_brand = models.CharField(
        db_column="BENCHMARK_CURRENT_BRAND", max_length=50, blank=True, null=True
    )
    benchmark_current_gap = models.DecimalField(
        db_column="BENCHMARK_CURRENT_GAP",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    benchmark_proposed_brand = models.CharField(
        db_column="BENCHMARK_PROPOSED_BRAND", max_length=50, blank=True, null=True
    )
    benchmark_proposed_gap = models.DecimalField(
        db_column="BENCHMARK_PROPOSED_GAP",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pricing_current = models.DecimalField(
        db_column="PRICING_CURRENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pricing_current_proposed = models.DecimalField(
        db_column="PRICING_CURRENT_PROPOSED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand_wsp_current = models.DecimalField(
        db_column="BRAND_WSP_CURRENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand_wsp_current_proposed = models.DecimalField(
        db_column="BRAND_WSP_CURRENT_PROPOSED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ncr_current = models.DecimalField(
        db_column="NCR_CURRENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ncr_current_proposed = models.DecimalField(
        db_column="NCR_CURRENT_PROPOSED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sale_proposed = models.DecimalField(
        db_column="SALE_PROPOSED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bench_mark_chq_req = models.ForeignKey(
        "SlctBenchmarkChangeRequest",
        models.DO_NOTHING,
        db_column="BENCH_MARK_CHQ_REQ",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_BENCHMARK_CHANGE_REQUEST_BILLING_GAP"


class SlctPriceChangeRequestExistingMarkt(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_type = models.CharField(
        db_column="REQUEST_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    price_chg_effect_date = models.DateField(
        db_column="PRICE_CHG_EFFECT_DATE", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    price_list = models.CharField(
        db_column="PRICE_LIST", max_length=50, blank=True, null=True
    )
    brand_wsp_profit_based_on_benchmark = models.DecimalField(
        db_column="BRAND_WSP_PROFIT_BASED_ON_BENCHMARK",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    standard_wsp_profit_margin = models.DecimalField(
        db_column="STANDARD_WSP_PROFIT_MARGIN",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_reduction_as_per_benchmark = models.DecimalField(
        db_column="PRICE_REDUCTION_AS_PER_BENCHMARK",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="GRADE", max_length=50, blank=True, null=True
    )
    price_reduction_bill_price = models.DecimalField(
        db_column="PRICE_REDUCTION_BILL_PRICE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_reduction_bd = models.DecimalField(
        db_column="PRICE_REDUCTION_BD",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_reduction_rd = models.DecimalField(
        db_column="PRICE_REDUCTION_RD",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    schemes = models.CharField(
        db_column="SCHEMES", max_length=120, blank=True, null=True
    )
    reason = models.CharField(db_column="REASON", max_length=50, blank=True, null=True)
    comment = models.TextField(db_column="COMMENT", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_PRICE_CHANGE_REQUEST_EXISTING_MARKT"


class SlctPriceChangeRequestBrandVsCompetitors(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    slct_price_change_request_existing_markt = models.ForeignKey(
        "SlctPriceChangeRequestExistingMarkt",
        models.DO_NOTHING,
        db_column="SLCT_PRICE_CHANGE_REQUEST_EXISTING_MARKT",
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    billing = models.DecimalField(
        db_column="BILLING", max_digits=20, decimal_places=2, blank=True, null=True
    )
    discount = models.DecimalField(
        db_column="DISCOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rd = models.DecimalField(
        db_column="RD", max_digits=20, decimal_places=2, blank=True, null=True
    )
    freight_benifit = models.DecimalField(
        db_column="FREIGHT_BENIFIT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    nod = models.DecimalField(
        db_column="NOD", max_digits=20, decimal_places=2, blank=True, null=True
    )
    retailer_scheme = models.DecimalField(
        db_column="RETAILER_SCHEME",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    mason_scheme = models.DecimalField(
        db_column="MASON_SCHEME", max_digits=20, decimal_places=2, blank=True, null=True
    )
    effective_nod = models.DecimalField(
        db_column="EFFECTIVE_NOD",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wsp = models.DecimalField(
        db_column="WSP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rsp = models.DecimalField(
        db_column="RSP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    wsp_margin = models.DecimalField(
        db_column="WSP_MARGIN", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rsp_margin = models.DecimalField(
        db_column="RSP_MARGIN", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_updated_date = models.DateField(
        db_column="LAST_UPDATED_DATE", blank=True, null=True, auto_now=True
    )
    last_updated_login = models.BigIntegerField(
        db_column="LAST_UPDATED_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_PRICE_CHANGE_REQUEST_BRAND_VS_COMPETITORS"


class SlctBenchmarkPriceWorking(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    slct_benchmark_price = models.ForeignKey(
        "SlctPriceChangeRequestExistingMarkt",
        models.DO_NOTHING,
        db_column="SLCT_BENCHMARK_PRICE",
        blank=True,
        null=True,
    )
    benchmark_brand = models.CharField(
        db_column="BENCHMARK_BRAND", max_length=50, blank=True, null=True
    )
    benchmark_wsp = models.DecimalField(
        db_column="BENCHMARK_WSP",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    parameter = models.DecimalField(
        db_column="PARAMETER", max_digits=20, decimal_places=2, blank=True, null=True
    )
    brand_wsp_based_on_benchmark = models.DecimalField(
        db_column="BRAND_WSP_BASED_ON_BENCHMARK",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand_wsp_wrt_desired_wso = models.DecimalField(
        db_column="BRAND_WSP_WRT_DESIRED_WSO",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_updated_date = models.DateField(db_column="LAST_UPDATED_DATE", auto_now=True)
    last_updated_login = models.BigIntegerField(
        db_column="LAST_UPDATED_LOGIN", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "SLCT_BENCHMARK_PRICE_WORKING"


class SlctInKindTourProposal(models.Model):
    """Slct inkind/tour proposal model class."""

    scheme_type = models.CharField(
        db_column="scheme_type", max_length=30, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="incentive_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="state", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="district", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="packaging", max_length=50, blank=True, null=True
    )
    slab_scheme = models.CharField(
        db_column="slab_scheme", max_length=50, blank=True, null=True
    )
    scheme_start_date = models.DateField(
        db_column="period_start_date", blank=True, null=True
    )
    scheme_end_date = models.DateField(
        db_column="period_end_date", blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="dealer_scheme", max_length=50, blank=True, null=True
    )
    sale_type_applicability = models.CharField(max_length=25)
    comment = models.CharField(max_length=100, blank=True, null=True)
    outflow_impact = models.DecimalField(
        db_column="out_flow_impact",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_IN_KIND_TOUR_PROPOSAL"


class SlctInKindQuantitySlabTourDestination(models.Model):
    """Quantity slab and tour destination model class."""

    in_kind_tour_prop = models.ForeignKey(
        SlctInKindTourProposal,
        on_delete=models.CASCADE,
        related_name="inkind_tour_destinations",
    )
    quantity_slab_lower = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    quantity_slab_upper = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    inkind_gift_detail = models.CharField(max_length=30, blank=True, null=True)
    tour_destination = models.CharField(max_length=30, blank=True, null=True)
    tour_cost = models.IntegerField(blank=True, null=True)
    inflation = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    tds = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    gst_lostt = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    effective_cost = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    per_bag_impact = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_IN_KIND_QUANTITY_SLAB_TOUR_DESTINATION"


class SlctSchemeDiscountProposal(models.Model):
    """Slct scheme discount proposal model class."""

    id = models.AutoField(primary_key=True)
    request_type = models.CharField(max_length=30, blank=True, null=True)
    price_change_effective_from = models.DateTimeField(blank=True, null=True)
    zone = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    price_list = models.CharField(max_length=50, blank=True, null=True)
    gap_for_state = models.CharField(max_length=20, null=True, blank=True)
    gap_for_district = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_SCHEME_DISCOUNT_PROPOSAL"


class SlctSchemeProposalGap(models.Model):
    """Slct scheme proposal gap data model class for scheme discount proposal."""

    id = models.AutoField(primary_key=True)
    scheme_discount_proposal = models.ForeignKey(
        SlctSchemeDiscountProposal,
        on_delete=models.CASCADE,
        related_name="scheme_proposal_gap",
    )
    opc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    opc_lpp = models.CharField(max_length=20, null=True, blank=True)
    ppc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    ppc_lpp = models.CharField(max_length=20, null=True, blank=True)
    psc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    psc_lpp = models.CharField(max_length=20, null=True, blank=True)
    cc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    cc_lpp = models.CharField(max_length=20, null=True, blank=True)
    premium_hdpe = models.CharField(max_length=20, null=True, blank=True)
    premium_lpp = models.CharField(max_length=20, null=True, blank=True)
    brand = models.CharField(max_length=20, null=True, blank=True)
    gap_type = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_SHCEME_PROPOSAL_GAP"


class SlctMarketInformation(models.Model):
    """Slct market informat model class for scheme discount proposal."""

    id = models.AutoField(primary_key=True)
    scheme_discount_proposal = models.ForeignKey(
        SlctSchemeDiscountProposal,
        on_delete=models.CASCADE,
        related_name="market_information",
    )
    opc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    opc_lpp = models.CharField(max_length=20, null=True, blank=True)
    ppc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    ppc_lpp = models.CharField(max_length=20, null=True, blank=True)
    psc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    psc_lpp = models.CharField(max_length=20, null=True, blank=True)
    cc_hdpe = models.CharField(max_length=20, null=True, blank=True)
    cc_lpp = models.CharField(max_length=20, null=True, blank=True)
    premium_hdpe = models.CharField(max_length=20, null=True, blank=True)
    premium_lpp = models.CharField(max_length=20, null=True, blank=True)
    brand = models.CharField(max_length=20, null=True, blank=True)
    information_type = models.CharField(max_length=20, null=True, blank=True)
    average_volume = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_MARKET_INFORMATION"


class SlctNewMarketPricingRequest(models.Model):
    """slct new market pricing request model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_type = models.CharField(
        db_column="REQUEST_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    price_chg_efft_date = models.DateField(
        db_column="PRICE_CHG_EFFT_DATE", blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    price_list = models.DecimalField(
        db_column="PRICE_LIST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    shree_product_brands = models.CharField(
        db_column="SHREE_PRODUCT_BRANDS", max_length=50, blank=True, null=True
    )
    product_shree = models.CharField(
        db_column="PRODUCT_SHREE", max_length=50, blank=True, null=True
    )
    packaging_shree = models.CharField(
        db_column="PACKAGING_SHREE", max_length=50, blank=True, null=True
    )
    benchmark_brand = models.CharField(
        db_column="BENCHMARK_BRAND", max_length=50, blank=True, null=True
    )
    product_benchmark = models.CharField(
        db_column="PRODUCT_BENCHMARK", max_length=50, blank=True, null=True
    )
    packaging_benchmark = models.CharField(
        db_column="PACKAGING_BENCHMARK", max_length=50, blank=True, null=True
    )
    bill_price = models.DecimalField(
        db_column="BILL_PRICE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rd = models.DecimalField(
        db_column="RD", max_digits=20, decimal_places=2, blank=True, null=True
    )
    discount = models.DecimalField(
        db_column="DISCOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    nod = models.DecimalField(
        db_column="NOD", max_digits=20, decimal_places=2, blank=True, null=True
    )
    gst = models.DecimalField(
        db_column="GST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    primary_freight = models.DecimalField(
        db_column="PRIMARY_FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    secondary_freight = models.DecimalField(
        db_column="SECONDARY FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    handling_charges = models.DecimalField(
        db_column="HANDLING CHARGES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sp_commission = models.DecimalField(
        db_column="SP COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    packing_charges = models.DecimalField(
        db_column="PACKING CHARGES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ncr = models.DecimalField(
        db_column="NCR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now_add=True
    )
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_NEW_MARKET_PRICING_REQUEST"


class SlctGapWithOtherProduct(models.Model):
    """slct gap with other product models"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    packing = models.CharField(
        db_column="PACKING", max_length=50, blank=True, null=True
    )
    gap = models.DecimalField(
        db_column="GAP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    new_market_pricing_request = models.ForeignKey(
        "SlctNewMarketPricingRequest",
        models.DO_NOTHING,
        db_column="NEW_MARKET_PRICING_REQUEST",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_GAP_WITH_OTHER_PRODUCT"


class SlctPricePackingInformation(models.Model):
    """slct price packing information model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    price_packaging_information_type = models.CharField(
        db_column="PRICE_PACKAGING_INFORMATION_TYPE",
        max_length=50,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    base_product = models.CharField(
        db_column="BASE_PRODUCT", max_length=50, blank=True, null=True
    )
    base_packaging = models.CharField(
        db_column="BASE_PACKAGING", max_length=50, blank=True, null=True
    )
    base_billing_price = models.DecimalField(
        db_column="BASE_BILLING_PRICE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    opc_hdpe = models.DecimalField(
        db_column="OPC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    opc_lpp = models.DecimalField(
        db_column="OPC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    ppc_hdpe = models.DecimalField(
        db_column="PPC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    ppc_lpp = models.DecimalField(
        db_column="PPC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    psc_hdpe = models.DecimalField(
        db_column="PSC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    psc_lpp = models.DecimalField(
        db_column="PSC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cc_hdpe = models.DecimalField(
        db_column="CC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cc_lpp = models.DecimalField(
        db_column="CC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    premium_hdpe = models.DecimalField(
        db_column="PREMIUM_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    premium_lpp = models.DecimalField(
        db_column="PREMIUM_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    pricing_packing_request = models.ForeignKey(
        "SlctNewMarketPricingRequest",
        models.DO_NOTHING,
        db_column="PRICING_PACKING_REQUEST",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_PRICE_PACKING_INFORMATION"


class SlctMarktingInformation(models.Model):
    """slct markting information model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="Brand", max_length=30, blank=True, null=True)
    marketing_information_type = models.CharField(
        db_column="MARKETING_INFORMATION_TYPE", max_length=20, blank=True, null=True
    )
    average = models.DecimalField(
        db_column="AVERAGE", max_digits=20, decimal_places=2, blank=True, null=True
    )

    opc_hdpe = models.DecimalField(
        db_column="OPC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    opc_lpp = models.DecimalField(
        db_column="OPC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    ppc_hdpe = models.DecimalField(
        db_column="PPC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    ppc_lpp = models.DecimalField(
        db_column="PPC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    psc_hdpe = models.DecimalField(
        db_column="PSC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    psc_lpp = models.DecimalField(
        db_column="PSC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cc_hdpe = models.DecimalField(
        db_column="CC_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cc_lpp = models.DecimalField(
        db_column="CC_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    premium_hdpe = models.DecimalField(
        db_column="PREMIUM_HDPE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    premium_lpp = models.DecimalField(
        db_column="PREMIUM_LPP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    marketing_information = models.ForeignKey(
        "SlctNewMarketPricingRequest",
        models.DO_NOTHING,
        db_column="MARKETING_INFORMATION",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_MARKTING_INFORMATION"


class SlctBrandingRequests(models.Model):
    """slct branding requests model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    branding_raised_for = models.CharField(
        db_column="BRANDING_RAISED_FOR", max_length=50, blank=True, null=True
    )
    dealer_code = models.DecimalField(
        db_column="DEALER_CODE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    dealer_name = models.CharField(
        db_column="DEALER_NAME", max_length=50, blank=True, null=True
    )
    dealer_state = models.CharField(
        db_column="DEALER_STATE", max_length=50, blank=True, null=True
    )
    dealer_district = models.CharField(
        db_column="DEALER_DISTRICT", max_length=50, blank=True, null=True
    )
    branding_objective = models.CharField(
        db_column="BRANDING_OBJECTIVE", max_length=50, blank=True, null=True
    )
    branding_objective_percentage = models.DecimalField(
        db_column="BRANDING_OBJECTIVE_PERCENTAGE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    calculated_amount = models.DecimalField(
        db_column="CALCULATED_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_amount = models.DecimalField(
        db_column="MANUAL_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date_of_raising_request = models.DateField(
        db_column="DATE_OF_RAISING_REQUEST", blank=True, null=True
    )
    val_per_from_date = models.DateField(
        db_column="VAL_PER_FROM_DATE", blank=True, null=True
    )
    val_per_to_date = models.DateField(
        db_column="VAL_PER_TO_DATE", blank=True, null=True
    )
    annual_budget_utilised = models.DecimalField(
        db_column="ANNUAL_BUDGET_UTILISED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    site_location_state = models.CharField(
        db_column="SITE_LOCATION_STATE", max_length=50, blank=True, null=True
    )
    site_location_district = models.CharField(
        db_column="SITE_LOCATION_DISTRICT", max_length=50, blank=True, null=True
    )
    site_location_pin_code = models.BigIntegerField(
        db_column="SITE_LOCATION_PIN_CODE", blank=True, null=True
    )
    photo_before_branding_activity = models.FileField(
        db_column="PHOTO_BEFORE_BRANDING_ACTIVITY",
        upload_to="static\media",
        max_length=500,
        blank=True,
        null=True,
    )
    vendor_selection = models.CharField(
        db_column="VENDOR_SELECTION", max_length=50, blank=True, null=True
    )
    buy_or_rent = models.CharField(
        db_column="BUY_OR_RENT", max_length=50, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "SLCT_BRANDING_REQUESTS"


class SlctAnnualDiscTargetBased(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    sub_scheme_type = models.CharField(
        db_column="Sub_scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_off_Invoice", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_Ded_source", max_length=50, blank=True, null=True
    )
    period_base_tgt_from_date = models.DateField(
        db_column="period_base_tgt_from_Date", blank=True, null=True
    )
    period_base_tgt_to_date = models.DateField(
        db_column="period_base_tgt_To_Date", blank=True, null=True
    )
    base_brand_tgt = models.CharField(
        db_column="Base_Brand_tgt", max_length=50, blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="Outflow_Overall_Imp",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_ANNUAL_DISC_TARGET_BASED"


class SlctBrandingActivity(models.Model):
    """slct branding activity models"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    branding_activity = models.CharField(
        db_column="BRANDING_ACTIVITY", max_length=20, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    size = models.DecimalField(
        db_column="SIZE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rate = models.DecimalField(
        db_column="RATE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    branding_request_activity = models.ForeignKey(
        "SlctBrandingRequests",
        models.DO_NOTHING,
        db_column="BRANDING_REQUEST_ACTIVITY",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_BRANDING_ACTIVITY"


class SlctBrandingAddress(models.Model):
    """slct branding address model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    site_address = models.TextField(db_column="SITE_ADDRESS", blank=True, null=True)
    branding_request = models.ForeignKey(
        "SlctBrandingRequests",
        models.DO_NOTHING,
        db_column="BRANDING_REQUEST",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(
        db_column="CREATION_DATE", blank=True, null=True, auto_now_add=True
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True, auto_now=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_BRANDING_ADDRESS"


class SlctAnnualDiscTargetBasedIncentives(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.IntegerField(
        db_column="QUANTITY_SLAB_LOWER", blank=True, null=True
    )
    quantity_slab_upper = models.IntegerField(
        db_column="QUANTITY_SLAB_UPPER", blank=True, null=True
    )
    incentive = models.DecimalField(
        db_column="INCENTIVE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    inkind_incentive = models.CharField(
        db_column="INKIND_INCENTIVE", max_length=20, blank=True, null=True
    )
    annual_disc_props_slab = models.ForeignKey(
        SlctAnnualDiscTargetBased,
        models.DO_NOTHING,
        db_column="ANNUAL_DISC_PROPS_SLAB",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_ANNUAL_DISC_TARGET_BASED_INCENTIVES"


class SlctAnnualDiscSlabBased(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="Scheme_type", max_length=50, blank=True, null=True
    )
    incentive_type = models.CharField(
        db_column="Incentive_type", max_length=50, blank=True, null=True
    )
    sub_scheme_type = models.CharField(
        db_column="Sub_scheme_type", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(max_length=50, blank=True, null=True)
    slab_based_scheme = models.CharField(
        db_column="Slab_based_Scheme", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="Dealer_Scheme", max_length=50, blank=True, null=True
    )
    period_from_date = models.DateField(
        db_column="period_From_Date", blank=True, null=True
    )
    period_to_date = models.DateField(db_column="period_To_Date", blank=True, null=True)
    on_off_invoice = models.CharField(
        db_column="On_OFF_Invoice", max_length=50, blank=True, null=True
    )
    gst_ded_source = models.CharField(
        db_column="GST_Ded_source", max_length=50, blank=True, null=True
    )
    period_base_tgt_from_date = models.DateField(
        db_column="period_base_tgt_From_date", blank=True, null=True
    )
    period_base_tgt_to_date = models.DateField(
        db_column="period_base_tgt_To_Date", blank=True, null=True
    )
    base_brand_target = models.CharField(
        db_column="Base_Brand_target", max_length=50, blank=True, null=True
    )
    outflow_overall_imp = models.DecimalField(
        db_column="Outflow_Overall_Imp",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="Comment", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_ANNUAL_DISC_SLAB_BASED"


class SlctAnnualDiscSlabBasedIncentive(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    dealer_type = models.CharField(
        db_column="DEALER_TYPE", max_length=20, blank=True, null=True
    )
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER", max_digits=20, decimal_places=2
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER", max_digits=20, decimal_places=2
    )
    target_incentive_slab1 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab1 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB1", max_length=20, blank=True, null=True
    )
    target_incentive_slab2 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab2 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB2", max_length=20, blank=True, null=True
    )
    target_incentive_slab3 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab3 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB3", max_length=20, blank=True, null=True
    )
    target_incentive_slab4 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB4",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab4 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB4", max_length=20, blank=True, null=True
    )
    target_incentive_slab5 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB5",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab5 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB5", max_length=20, blank=True, null=True
    )
    target_incentive_slab6 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB6",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab6 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB6", max_length=20, blank=True, null=True
    )
    target_incentive_slab7 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB7",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab7 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB7", max_length=20, blank=True, null=True
    )
    target_incentive_slab8 = models.DecimalField(
        db_column="TARGET_INCENTIVE_SLAB8",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_incentive_slab8 = models.CharField(
        db_column="INKIND_INCENTIVE_SLAB8", max_length=20, blank=True, null=True
    )
    disc_props_tgt = models.ForeignKey(
        SlctAnnualDiscSlabBased,
        models.DO_NOTHING,
        db_column="DISC_PROPS_TGT",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_ANNUAL_DISC_SLAB_BASED_INCENTIVE"


class SlctInKindBoosterSchemeProps(models.Model):
    """slct inkind booster scheme proposal model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme_type = models.CharField(
        db_column="SCHEME_TYPE", max_length=50, blank=True, null=True
    )
    scheme_sub_type = models.CharField(
        db_column="SCHEME_SUB_TYPE", max_length=50, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    dealer_scheme = models.CharField(
        db_column="DEALER_SCHEME", max_length=50, blank=True, null=True
    )
    base_target_period_from_date = models.DateField(
        db_column="BASE_TARGET_PERIOD_FROM_DATE", blank=True, null=True
    )
    base_target_period_to_date = models.DateField(
        db_column="BASE_TARGET_PERIOD_TO_DATE", blank=True, null=True
    )
    qualifier_1 = models.DecimalField(
        db_column="QUALIFIER 1", max_digits=5, decimal_places=2, blank=True, null=True
    )

    target_scheme_period_from = models.DateField(
        db_column="TARGET_SCHEME_PERIOD_FROM", blank=True, null=True
    )
    target_scheme_period_to = models.DateField(
        db_column="TARGET_SCHEME_PERIOD_TO", blank=True, null=True
    )
    qualifier_2 = models.DecimalField(
        db_column="QUALIFIER 2", max_digits=5, decimal_places=2, blank=True, null=True
    )

    outflow_overall = models.DecimalField(
        db_column="OUTFLOW_OVERALL",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=500, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        upload_to="static\media\state_head",
        max_length=500,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    approvals_comment = models.CharField(
        db_column="APPROVALS_COMMENT", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SLCT_IN_KIND_BOOSTER_SCHEME_PROPS"


class SlctInKindBoosterSchemePropsIncentive(models.Model):
    """slct inkind booster scheme proposal incentive model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    quantity_slab_lower = models.DecimalField(
        db_column="QUANTITY_SLAB_LOWER",
        max_digits=65535,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quantity_slab_upper = models.DecimalField(
        db_column="QUANTITY_SLAB_UPPER",
        max_digits=65535,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inkind_gift_detail = models.CharField(
        db_column="INKIND_GIFT_DETAIL", max_length=20, blank=True, null=True
    )
    in_kind_booster_scheme = models.ForeignKey(
        "SlctInKindBoosterSchemeProps",
        models.DO_NOTHING,
        db_column="IN_KIND_BOOSTER_SCHEME",
        blank=True,
        null=True,
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_IN_KIND_BOOSTER_SCHEME_PROPS_INCENTIVE"


class SlctAnnualSalesPlan(models.Model):
    """slct annual sales plan model set"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    district_potential = models.DecimalField(
        db_column="DISTRICT_POTENTIAL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    annual_sales_total_target = models.DecimalField(
        db_column="ANNUAL_SALES_TOTAL_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    ly_monthly_avg = models.DecimalField(
        db_column="LY_MONTHLY_AVG",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cur_yr_apr = models.DecimalField(
        db_column="CUR_YR_APR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_may = models.DecimalField(
        db_column="CUR_YR_MAY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_jun = models.DecimalField(
        db_column="CUR_YR_JUN", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_jul = models.DecimalField(
        db_column="CUR_YR_JUL", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_aug = models.DecimalField(
        db_column="CUR_YR_AUG", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_sep = models.DecimalField(
        db_column="CUR_YR_SEP", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_oct = models.DecimalField(
        db_column="CUR_YR_OCT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_nov = models.DecimalField(
        db_column="CUR_YR_NOV", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cur_yr_dec = models.DecimalField(
        db_column="CUR_YR_DEC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    nxt_yr_jan = models.DecimalField(
        db_column="NXT_YR_JAN", max_digits=20, decimal_places=2, blank=True, null=True
    )
    nxt_yr_feb = models.DecimalField(
        db_column="NXT_YR_FEB", max_digits=20, decimal_places=2, blank=True, null=True
    )
    nxt_yr_mar = models.DecimalField(
        db_column="NXT_YR_MAR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "SLCT_ANNUAL_SALES_PLAN"


class SlctMonthlySalesPlan(models.Model):
    """slct monthly sales plan"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    district_potential = models.DecimalField(
        db_column="DISTRICT_POTENTIAL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    current_month = models.CharField(
        db_column="CURRENT_MONTH", max_length=50, blank=True, null=True
    )
    current_month_total_sales = models.DecimalField(
        db_column="CURRENT_MONTH_TOTAL_SALES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_bucket1 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_bucket2 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_bucket3 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    next_month_total_target = models.DecimalField(
        db_column="NEXT_MONTH_TOTAL_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    next_month_bucket1 = models.DecimalField(
        db_column="NEXT_MONTH_BUCKET1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    next_month_bucket2 = models.DecimalField(
        db_column="NEXT_MONTH_BUCKET2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    next_month_bucket3 = models.DecimalField(
        db_column="NEXT_MONTH_BUCKET3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    premium = models.CharField(db_column="PREMIUM", max_length=1, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SLCT_MONTHLY_SALES_PLAN"


class ZoneMappingNew(models.Model):
    """State, district, city, zone dropdown data."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    so_code = models.TextField(db_column="SO_CODE", blank=True, null=True)
    org_id = models.CharField(db_column="ORG_ID", max_length=100, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    city_id = models.DecimalField(
        db_column="CITY_ID", max_digits=50, decimal_places=2, blank=True, null=True
    )
    pincode = models.CharField(
        db_column="PINCODE", max_length=100, blank=True, null=True
    )
    active = models.CharField(db_column="ACTIVE", max_length=100, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ZONE_MAPPING_NEW"


class TOebsXxsclVehicleMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    vechile_id = models.BigIntegerField(db_column="VECHILE_ID", blank=True, null=True)
    vehicle_no = models.CharField(
        db_column="VEHICLE_NO", max_length=150, blank=True, null=True
    )
    vehicle_model = models.CharField(
        db_column="VEHICLE_MODEL", max_length=150, blank=True, null=True
    )
    vehicle_make = models.CharField(
        db_column="VEHICLE_MAKE", max_length=150, blank=True, null=True
    )
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=150, blank=True, null=True
    )
    vehicle_tare_wt = models.DecimalField(
        db_column="VEHICLE_TARE_WT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vehicle_gross_wt = models.DecimalField(
        db_column="VEHICLE_GROSS_WT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    loading_capcity = models.DecimalField(
        db_column="LOADING_CAPCITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    insurance_issue_dt = models.DateTimeField(
        db_column="INSURANCE_ISSUE_DT", blank=True, null=True
    )
    insurance_expiry_dt = models.DateTimeField(
        db_column="INSURANCE_EXPIRY_DT", blank=True, null=True
    )
    puc_issue_dt = models.DateTimeField(db_column="PUC_ISSUE_DT", blank=True, null=True)
    puc_expiry_dt = models.DateTimeField(
        db_column="PUC_EXPIRY_DT", blank=True, null=True
    )
    fitness_issue_dt = models.DateTimeField(
        db_column="FITNESS_ISSUE_DT", blank=True, null=True
    )
    fitness_expiry_dt = models.DateTimeField(
        db_column="FITNESS_EXPIRY_DT", blank=True, null=True
    )
    transporter_name = models.CharField(
        db_column="TRANSPORTER_NAME", max_length=300, blank=True, null=True
    )
    vehicle_owner = models.CharField(
        db_column="VEHICLE_OWNER", max_length=50, blank=True, null=True
    )
    plant_org_id = models.DecimalField(
        db_column="PLANT_ORG_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    owner_name = models.CharField(
        db_column="OWNER_NAME", max_length=300, blank=True, null=True
    )
    telephone_no = models.CharField(
        db_column="TELEPHONE_NO", max_length=20, blank=True, null=True
    )
    mobile_no = models.CharField(
        db_column="MOBILE_NO", max_length=20, blank=True, null=True
    )
    black_listed = models.CharField(
        db_column="BLACK_LISTED", max_length=5, blank=True, null=True
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=150, blank=True, null=True
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=300, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=300, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=300, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=300, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=300, blank=True, null=True
    )
    attribute6 = models.CharField(
        db_column="ATTRIBUTE6", max_length=300, blank=True, null=True
    )
    attribute7 = models.CharField(
        db_column="ATTRIBUTE7", max_length=300, blank=True, null=True
    )
    attribute8 = models.CharField(
        db_column="ATTRIBUTE8", max_length=300, blank=True, null=True
    )
    attribute9 = models.CharField(
        db_column="ATTRIBUTE9", max_length=300, blank=True, null=True
    )
    attribute10 = models.CharField(
        db_column="ATTRIBUTE10", max_length=300, blank=True, null=True
    )
    attribute11 = models.CharField(
        db_column="ATTRIBUTE11", max_length=300, blank=True, null=True
    )
    attribute12 = models.CharField(
        db_column="ATTRIBUTE12", max_length=300, blank=True, null=True
    )
    attribute13 = models.CharField(
        db_column="ATTRIBUTE13", max_length=300, blank=True, null=True
    )
    attribute14 = models.CharField(
        db_column="ATTRIBUTE14", max_length=300, blank=True, null=True
    )
    attribute15 = models.CharField(
        db_column="ATTRIBUTE15", max_length=300, blank=True, null=True
    )
    driver_name = models.CharField(
        db_column="DRIVER_NAME", max_length=300, blank=True, null=True
    )
    driver_license = models.CharField(
        db_column="DRIVER_LICENSE", max_length=50, blank=True, null=True
    )
    driver_license_issue_dt = models.DateTimeField(
        db_column="DRIVER_LICENSE_ISSUE_DT", blank=True, null=True
    )
    driver_license_expiry_dt = models.DateTimeField(
        db_column="DRIVER_LICENSE_EXPIRY_DT", blank=True, null=True
    )
    truck_body_type = models.CharField(
        db_column="TRUCK_BODY_TYPE", max_length=60, blank=True, null=True
    )
    truck_body_length = models.CharField(
        db_column="TRUCK_BODY_LENGTH", max_length=20, blank=True, null=True
    )
    blacklist_till_date = models.DateTimeField(
        db_column="BLACKLIST_TILL_DATE", blank=True, null=True
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
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "T_OEBS_XXSCL_VEHICLE_MASTER"


class TgtStateHeadNsh(models.Model):
    employee_code = models.BigIntegerField(
        db_column="Employee Code", blank=True, null=True
    )
    name = models.CharField(db_column="Name", max_length=20, blank=True, null=True)
    email = models.CharField(db_column="Email", max_length=20, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TGT_STATE_HEAD_NSH"


class CrmMarketMappingPricing(models.Model):
    billing = models.DecimalField(
        db_column="BILLING", max_digits=22, decimal_places=2, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    counter_visit_id = models.BigIntegerField(
        db_column="COUNTER_VISIT_ID", blank=True, null=True
    )
    counter_visit_start_time = models.DateTimeField(
        db_column="COUNTER_VISIT_START_TIME", blank=True, null=True
    )
    discount = models.DecimalField(
        db_column="DISCOUNT", max_digits=22, decimal_places=2, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    employee_code_so = models.BigIntegerField(
        db_column="EMPLOYEE_CODE_SO", blank=True, null=True
    )
    id = models.BigIntegerField(db_column="ID", primary_key=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    retail_sales = models.DecimalField(
        db_column="RETAIL_SALES", max_digits=22, decimal_places=2, blank=True, null=True
    )
    retail_sale_price = models.DecimalField(
        db_column="RETAIL_SALE_PRICE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    stock = models.DecimalField(
        db_column="STOCK", max_digits=22, decimal_places=2, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    whole_sales = models.DecimalField(
        db_column="WHOLE_SALES", max_digits=22, decimal_places=2, blank=True, null=True
    )
    whole_sale_price = models.DecimalField(
        db_column="WHOLE_SALE_PRICE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    so_name = models.CharField(
        db_column="SO_NAME", max_length=540, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    erp_customer_no = models.CharField(
        db_column="ERP_CUSTOMER_NO", max_length=100, blank=True, null=True
    )
    crm_customer_code = models.CharField(
        db_column="CRM_CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    so_email_id = models.CharField(
        db_column="SO_EMAIL_ID", max_length=360, blank=True, null=True
    )
    so_brand = models.CharField(
        db_column="SO_BRAND", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_MARKET_MAPPING_PRICING"


class CrmPricing(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    wsp_price = models.DecimalField(
        db_column="WSP_PRICE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    rsp_price = models.DecimalField(
        db_column="RSP_PRICE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_PRICING"


class BrandingActivity(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=50, blank=True, null=True)
    city_id = models.CharField(
        db_column="CITY_ID", max_length=50, blank=True, null=True
    )
    activity_type = models.CharField(
        db_column="ACTIVITY_TYPE", max_length=50, blank=True, null=True
    )
    activity_for = models.CharField(
        db_column="ACTIVITY_FOR", max_length=50, blank=True, null=True
    )
    activity_code = models.CharField(
        db_column="ACTIVITY_CODE", max_length=50, blank=True, null=True
    )
    activity_category = models.CharField(
        db_column="ACTIVITY_CATEGORY", max_length=50, blank=True, null=True
    )
    activity_sub_category = models.CharField(
        db_column="ACTIVITY_SUB_CATEGORY", max_length=50, blank=True, null=True
    )
    activity_name = models.CharField(
        db_column="ACTIVITY_NAME", max_length=50, blank=True, null=True
    )
    site_name = models.CharField(
        db_column="SITE NAME", max_length=50, blank=True, null=True
    )
    site_type = models.CharField(
        db_column="SITE TYPE", max_length=50, blank=True, null=True
    )
    vendor_name = models.CharField(
        db_column="VENDOR NAME", max_length=50, blank=True, null=True
    )
    vendor_code = models.CharField(
        db_column="VENDOR CODE", max_length=50, blank=True, null=True
    )
    date_of_start = models.DateField(db_column="DATE OF START", blank=True, null=True)
    planned_date_of_completion = models.DateField(
        db_column="PLANNED DATE OF COMPLETION", blank=True, null=True
    )
    actual_date_of_completion = models.DateField(
        db_column="ACTUAL DATE OF COMPLETION", blank=True, null=True
    )
    quality_rating = models.DecimalField(
        db_column="QUALITY RATING",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    budget_planned = models.DecimalField(
        db_column="BUDGET_PLANNED",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    actual_spend = models.DecimalField(
        db_column="ACTUAL_SPEND",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status_of_scheme = models.CharField(
        db_column="STATUS_OF_SCHEME", max_length=50, blank=True, null=True
    )
    objective_of_activity = models.CharField(
        db_column="OBJECTIVE_OF_ACTIVITY", max_length=50, blank=True, null=True
    )
    objective_target = models.DecimalField(
        db_column="OBJECTIVE_TARGET",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    activity_feedback = models.DecimalField(
        db_column="ACTIVITY_FEEDBACK",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    qty_sold = models.DecimalField(
        db_column="QTY_SOLD",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    requision_raise_date_field = models.DateField(
        db_column="REQUISION_RAISE_DATE ", blank=True, null=True
    )
    last_mrn_date = models.DateField(db_column="LAST_MRN_DATE", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    raised_by = models.CharField(
        db_column="RAISED_BY", max_length=100, blank=True, null=True
    )
    requisition_number = models.CharField(
        db_column="REQUISITION_NUMBER", max_length=100, blank=True, null=True
    )
    po_number = models.CharField(
        db_column="PO_NUMBER", max_length=100, blank=True, null=True
    )
    date_of_po = models.DateField(db_column="DATE_OF_PO", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    general_activity_type = models.CharField(
        db_column="GENERAL_ACTIVITY_TYPE", max_length=360, blank=True, null=True
    )
    crm_requisition_number = models.BigIntegerField(
        db_column="CRM_REQUISITION_NUMBER", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "BRANDING_ACTIVITY"


class SoTalukaMappingDelhiHyd(models.Model):
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    org_id = models.IntegerField(db_column="ORG_ID", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    emp_code = models.BigIntegerField(db_column="EMP_CODE", blank=True, null=True)
    emp_name = models.CharField(
        db_column="EMP_NAME", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    mobile_number = models.DecimalField(
        db_column="MOBILE_NUMBER",
        max_digits=11,
        decimal_places=0,
        blank=True,
        null=True,
    )
    email_id_shree = models.CharField(
        db_column="EMAIL_ID_SHREE", max_length=100, blank=True, null=True
    )
    playstore_id = models.CharField(
        db_column="PLAYSTORE_ID", max_length=100, blank=True, null=True
    )
    ios_or_android = models.CharField(
        db_column="IOS_OR_ANDROID", max_length=100, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    id = models.BigAutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "SO_TALUKA_MAPPING_DELHI_HYD"


class CounterVisitList(models.Model):
    counter_type = models.CharField(
        db_column="COUNTER_TYPE", max_length=50, blank=True, null=True
    )
    crm_customer_code = models.CharField(
        db_column="CRM_CUSTOMER_CODE", max_length=50, blank=True, null=True
    )
    customer_no = models.CharField(
        db_column="CUSTOMER_NO", max_length=50, blank=True, null=True
    )
    deviation_comment = models.CharField(
        db_column="DEVIATION_COMMENT", max_length=2000, blank=True, null=True
    )
    deviation_reason = models.CharField(
        db_column="DEVIATION_REASON", max_length=2000, blank=True, null=True
    )
    end_visit_time = models.DateTimeField(
        db_column="END_VISIT_TIME", blank=True, null=True
    )
    crm_id = models.DecimalField(
        db_column="CRM_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    is_adhoc = models.CharField(
        db_column="IS_ADHOC", max_length=50, blank=True, null=True
    )
    start_visit_time = models.DateTimeField(
        db_column="START_VISIT_TIME", blank=True, null=True
    )
    system_recommended = models.CharField(
        db_column="SYSTEM_RECOMMENDED", max_length=50, blank=True, null=True
    )
    journey_visit_id = models.DecimalField(
        db_column="JOURNEY_VISIT_ID",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    counter_potential = models.DecimalField(
        db_column="COUNTER_POTENTIAL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    counter_sale = models.DecimalField(
        db_column="COUNTER_SALE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    counter_share = models.DecimalField(
        db_column="COUNTER_SHARE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    flagged_by = models.BigIntegerField(db_column="FLAGGED_BY", blank=True, null=True)
    is_bangur_counter = models.CharField(
        db_column="IS_BANGUR_COUNTER", max_length=10, blank=True, null=True
    )
    is_dealer_flag = models.CharField(
        db_column="IS_DEALER_FLAG", max_length=10, blank=True, null=True
    )
    is_rockstrong_counter = models.CharField(
        db_column="IS_ROCKSTRONG_COUNTER", max_length=10, blank=True, null=True
    )
    is_shree_counter = models.CharField(
        db_column="IS_SHREE_COUNTER", max_length=10, blank=True, null=True
    )
    network_type = models.CharField(
        db_column="NETWORK_TYPE", max_length=100, blank=True, null=True
    )
    order_generated = models.DecimalField(
        db_column="ORDER_GENERATED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    remark_for_flag = models.CharField(
        db_column="REMARK_FOR_FLAG", max_length=800, blank=True, null=True
    )
    remark_for_unflag = models.CharField(
        db_column="REMARK_FOR_UNFLAG", max_length=800, blank=True, null=True
    )
    total_sale = models.DecimalField(
        db_column="TOTAL_SALE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    unflag_time = models.DateTimeField(db_column="UNFLAG_TIME", blank=True, null=True)
    wholesale = models.DecimalField(
        db_column="WHOLESALE", max_digits=20, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "COUNTER_VISIT_LIST"


class CrmSalesPlanningBottomUpTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    emp_so_id = models.BigIntegerField(db_column="EMP_SO_ID", blank=True, null=True)
    crm_id = models.BigIntegerField(db_column="CRM_ID", blank=True, null=True)
    customer_number = models.CharField(
        db_column="CUSTOMER_NUMBER", max_length=120, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    bucket = models.CharField(db_column="BUCKET", max_length=360, blank=True, null=True)
    bottom_up_targets = models.DecimalField(
        db_column="BOTTOM_UP_TARGETS",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    planned = models.BigIntegerField(db_column="PLANNED", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_SALES_PLANNING_BOTTOM_UP_TARGET"


class TargetSalesPlanningMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    current_month_bucket1 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET1",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_bucket2 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET2",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_bucket3 = models.DecimalField(
        db_column="CURRENT_MONTH_BUCKET3",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_month_total_sales = models.DecimalField(
        db_column="CURRENT_MONTH_TOTAL_SALES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_bucket1 = models.DecimalField(
        db_column="TARGET_BUCKET1",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_bucket2 = models.DecimalField(
        db_column="TARGET_BUCKET2",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    target_bucket3 = models.DecimalField(
        db_column="TARGET_BUCKET3",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    bottom_up_targets_sum = models.DecimalField(
        db_column="BOTTOM_UP_TARGETS__SUM",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="STATUS",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=100,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    status_by_nsh = models.CharField(
        db_column="STATUS_BY_NSH",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=100,
    )
    deviation = models.DecimalField(
        db_column="DEVIATION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    planned = models.BigIntegerField(db_column="PLANNED", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TARGET_SALES_PLANNING_MONTHLY"


class TOebsXxsclCustomerMaster(models.Model):
    party_id = models.BigIntegerField(
        db_column="PARTY_ID", primary_key=True, null=False
    )
    party_name = models.CharField(
        db_column="PARTY_NAME", max_length=360, blank=True, null=True
    )
    category_code = models.CharField(
        db_column="CATEGORY_CODE", max_length=300, blank=True, null=True
    )
    cust_account_id = models.DecimalField(
        db_column="CUST_ACCOUNT_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    account_number = models.CharField(
        db_column="ACCOUNT_NUMBER", max_length=300, blank=True, null=True
    )
    customer_class_code = models.CharField(
        db_column="CUSTOMER_CLASS_CODE", max_length=300, blank=True, null=True
    )
    orig_system_reference = models.CharField(
        db_column="ORIG_SYSTEM_REFERENCE", max_length=240, blank=True, null=True
    )
    cust_cat = models.CharField(
        db_column="CUST_CAT", max_length=150, blank=True, null=True
    )
    cust_sub_cat = models.CharField(
        db_column="CUST_SUB_CAT", max_length=150, blank=True, null=True
    )
    party_site_id = models.DecimalField(
        db_column="PARTY_SITE_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cust_acct_site_id = models.DecimalField(
        db_column="CUST_ACCT_SITE_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    bill_to_flag = models.CharField(
        db_column="BILL_TO_FLAG", max_length=100, blank=True, null=True
    )
    depot_region = models.CharField(
        db_column="DEPOT_REGION", max_length=150, blank=True, null=True
    )
    cust_depot = models.CharField(
        db_column="CUST_DEPOT", max_length=150, blank=True, null=True
    )
    location_id = models.DecimalField(
        db_column="LOCATION_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    address1 = models.CharField(
        db_column="ADDRESS1", max_length=240, blank=True, null=True
    )
    address2 = models.CharField(
        db_column="ADDRESS2", max_length=240, blank=True, null=True
    )
    address3 = models.CharField(
        db_column="ADDRESS3", max_length=240, blank=True, null=True
    )
    address4 = models.CharField(
        db_column="ADDRESS4", max_length=240, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=60, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=560, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=60, blank=True, null=True
    )
    postal_code = models.CharField(
        db_column="POSTAL_CODE", max_length=60, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=600, blank=True, null=True)
    country = models.CharField(
        db_column="COUNTRY", max_length=600, blank=True, null=True
    )
    org_id = models.DecimalField(
        db_column="ORG_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    site_use_code = models.CharField(
        db_column="SITE_USE_CODE", max_length=300, blank=True, null=True
    )
    depot_type = models.CharField(
        db_column="DEPOT_TYPE", max_length=300, blank=True, null=True
    )
    mkt_link = models.CharField(
        db_column="MKT_LINK", max_length=150, blank=True, null=True
    )
    parent_id = models.CharField(
        db_column="PARENT_ID", max_length=150, blank=True, null=True
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
        db_table = "T_OEBS_XXSCL_CUSTOMER_MASTER"


class PricingProposalApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    crm_pricing_key = models.OneToOneField(
        "CrmPricing",
        models.DO_NOTHING,
        db_column="CRM_PRICING_KEY",
        blank=True,
        null=True,
    )
    price = models.IntegerField(db_column="PRICE", blank=True, null=True)
    status = models.CharField(
        db_column="STATUS",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=100,
    )
    comment = models.CharField(
        db_column="COMMENT", max_length=250, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    wsp_price = models.DecimalField(
        db_column="WSP_PRICE", max_digits=22, decimal_places=3, blank=True, null=True
    )
    rsp_price = models.DecimalField(
        db_column="RSP_PRICE", max_digits=22, decimal_places=3, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PRICING_PROPOSAL_APPROVAL"


class NetworkAdditionPlan(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_ts = models.DateTimeField(db_column="CREATED_TS", blank=True, null=True)
    modified_ts = models.DateTimeField(db_column="MODIFIED_TS", blank=True, null=True)
    type_pk_string = models.CharField(
        db_column="TYPE_PK_STRING", max_length=360, blank=True, null=True
    )
    owner_pk_string = models.CharField(
        db_column="OWNER_PK_STRING", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    total_counter = models.BigIntegerField(
        db_column="TOTAL_COUNTER", blank=True, null=True
    )
    shree_counter = models.BigIntegerField(
        db_column="SHREE_COUNTER", blank=True, null=True
    )
    revised_plan = models.BigIntegerField(
        db_column="REVISED_PLAN", blank=True, null=True
    )
    reason = models.CharField(db_column="REASON", max_length=540, blank=True, null=True)
    applicable_to = models.CharField(
        db_column="APPLICABLE_TO", max_length=360, blank=True, null=True
    )
    raised_by = models.CharField(
        db_column="RAISED_BY", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    revised_target_by_tsm = models.DecimalField(
        db_column="REVISED_TARGET_BY_TSM",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    revised_by_tsm = models.CharField(
        db_column="REVISED_BY_TSM", max_length=360, blank=True, null=True
    )
    comments_for_revision_tsm = models.CharField(
        db_column="COMMENTS_FOR_REVISION_TSM", max_length=540, blank=True, null=True
    )
    action_performed = models.CharField(
        db_column="ACTION_PERFORMED", max_length=540, blank=True, null=True
    )
    action_performed_date = models.CharField(
        db_column="ACTION_PERFORMED_DATE", max_length=540, blank=True, null=True
    )
    action_performed_by = models.CharField(
        db_column="ACTION_PERFORMED_BY", max_length=360, blank=True, null=True
    )
    target_sent_for_revision = models.DecimalField(
        db_column="TARGET_SENT_FOR_REVISION",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    is_target_approved = models.CharField(
        db_column="IS_TARGET_APPROVED", max_length=360, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    revised_by_rh = models.CharField(
        db_column="REVISED_BY_RH", max_length=360, blank=True, null=True
    )
    revised_target_by_rh = models.DecimalField(
        db_column="REVISED_TARGET_BY_RH",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    revision_reason_by_rh = models.CharField(
        db_column="REVISION_REASON_BY_RH", max_length=360, blank=True, null=True
    )
    comments_for_revision_by_rh = models.CharField(
        db_column="COMMENTS_FOR_REVISION_BY_RH", max_length=360, blank=True, null=True
    )
    revised_target_by_sh = models.DecimalField(
        db_column="REVISED_TARGET_BY_SH",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    revised_by_sh = models.CharField(
        db_column="REVISED_BY_SH", max_length=360, blank=True, null=True
    )
    revision_reason_by_sh = models.CharField(
        db_column="REVISION_REASON_BY_SH", max_length=360, blank=True, null=True
    )
    comments_for_revision_by_sh = models.CharField(
        db_column="COMMENTS_FOR_REVISION_BY_SH", max_length=540, blank=True, null=True
    )
    approved_by = models.CharField(
        db_column="APPROVED_BY", max_length=360, blank=True, null=True
    )
    approval_level = models.CharField(
        db_column="APPROVAL_LEVEL", max_length=360, blank=True, null=True
    )
    status = models.CharField(
        db_column="STATUS",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=100,
    )
    month = models.CharField(db_column="MONTH", max_length=100, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NETWORK_ADDITION_PLAN"


class NetworkAdditionPlanState(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_ts = models.DateTimeField(db_column="CREATED_TS", blank=True, null=True)
    modified_ts = models.DateTimeField(db_column="MODIFIED_TS", blank=True, null=True)
    type_pk_string = models.CharField(
        db_column="TYPE_PK_STRING", max_length=360, blank=True, null=True
    )
    owner_pk_string = models.CharField(
        db_column="OWNER_PK_STRING", max_length=360, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=540, blank=True, null=True)
    total_counter = models.BigIntegerField(
        db_column="TOTAL_COUNTER", blank=True, null=True
    )
    shree_counter = models.BigIntegerField(
        db_column="SHREE_COUNTER", blank=True, null=True
    )
    revised_plan = models.BigIntegerField(
        db_column="REVISED_PLAN", blank=True, null=True
    )
    revised_by_sh = models.CharField(
        db_column="REVISED_BY_SH", max_length=360, blank=True, null=True
    )
    comments_by_sh = models.CharField(
        db_column="COMMENTS_BY_SH", max_length=360, blank=True, null=True
    )
    revised_by_zh = models.CharField(
        db_column="REVISED_BY_ZH", max_length=360, blank=True, null=True
    )
    revised_target_by_zh = models.BigIntegerField(
        db_column="REVISED_TARGET_BY_ZH", blank=True, null=True
    )
    comments_by_zh = models.CharField(
        db_column="COMMENTS_BY_ZH", max_length=360, blank=True, null=True
    )
    revised_by_nsh = models.CharField(
        db_column="REVISED_BY_NSH", max_length=360, blank=True, null=True
    )
    revised_target_by_nsh = models.BigIntegerField(
        db_column="REVISED_TARGET_BY_NSH", blank=True, null=True
    )
    comments_by_nsh = models.CharField(
        db_column="COMMENTS_BY_NSH", max_length=360, blank=True, null=True
    )
    status = models.CharField(
        db_column="STATUS",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=100,
    )
    approval_level = models.CharField(
        db_column="APPROVAL_LEVEL", max_length=360, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=100, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NETWORK_ADDITION_PLAN_STATE"


class TradeOrderPlacementApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    user_uid = models.BigIntegerField(db_column="USER_UID", blank=True, null=True)
    user_customer_no = models.BigIntegerField(
        db_column="USER_CUSTOMER_NO", blank=True, null=True
    )
    user_name = models.CharField(
        db_column="USER_NAME", max_length=540, blank=True, null=True
    )
    retailer_uid = models.BigIntegerField(
        db_column="RETAILER_UID", blank=True, null=True
    )
    retailer_customer_no = models.BigIntegerField(
        db_column="RETAILER_CUSTOMER_NO", blank=True, null=True
    )
    retailer_name = models.CharField(
        db_column="RETAILER_NAME", max_length=540, blank=True, null=True
    )
    code_crm_order_no = models.CharField(
        db_column="CODE_CRM_ORDER_NO", max_length=360, blank=True, null=True
    )
    erp_order_number = models.CharField(
        db_column="ERP_ORDER_NUMBER", max_length=360, blank=True, null=True
    )
    date = models.DateTimeField(db_column="DATE", blank=True, null=True)
    delivery_address = models.CharField(
        db_column="DELIVERY_ADDRESS", max_length=540, blank=True, null=True
    )
    rejection_reasons = models.CharField(
        db_column="REJECTION_REASONS", max_length=360, blank=True, null=True
    )
    suggestions = models.CharField(
        db_column="SUGGESTIONS", max_length=540, blank=True, null=True
    )
    is_dealer_provide_own_transport = models.CharField(
        db_column="IS_DEALER_PROVIDE_OWN_TRANSPORT",
        max_length=360,
        blank=True,
        null=True,
    )
    spa_pproval_status = models.CharField(
        db_column="SPA_PPROVAL_STATUS", max_length=360, blank=True, null=True
    )
    sp_rejection_reason = models.CharField(
        db_column="SP_REJECTION_REASON", max_length=360, blank=True, null=True
    )
    entry_number = models.BigIntegerField(
        db_column="ENTRY_NUMBER", blank=True, null=True
    )
    erp_line_item_id = models.BigIntegerField(
        db_column="ERP_LINE_ITEM_ID", blank=True, null=True
    )
    product_code = models.BigIntegerField(
        db_column="PRODUCT_CODE", blank=True, null=True
    )
    invoice_creation_date_and_time = models.DateTimeField(
        db_column="INVOICE_CREATION_DATE_AND_TIME", blank=True, null=True
    )
    dicreation_date_and_time = models.DateTimeField(
        db_column="DICREATION_DATE_AND_TIME", blank=True, null=True
    )
    cancelled_date = models.DateTimeField(
        db_column="CANCELLED_DATE", blank=True, null=True
    )
    delivered_date = models.DateTimeField(
        db_column="DELIVERED_DATE", blank=True, null=True
    )
    status_code = models.CharField(
        db_column="STATUS_CODE", max_length=360, blank=True, null=True
    )
    quantity_in_mt = models.DecimalField(
        db_column="QUANTITY_IN_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    invoice_quantity = models.DecimalField(
        db_column="INVOICE_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    truck_allocated_qty = models.DecimalField(
        db_column="TRUCK_ALLOCATED_QTY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    delivery_qty = models.DecimalField(
        db_column="DELIVERY_QTY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    route_id = models.BigIntegerField(db_column="ROUTE_ID", blank=True, null=True)
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    freight_terms_code = models.CharField(
        db_column="FREIGHT_TERMS_CODE", max_length=360, blank=True, null=True
    )
    fob_code = models.CharField(
        db_column="FOB_CODE", max_length=360, blank=True, null=True
    )
    epod_completed = models.CharField(
        db_column="EPOD_COMPLETED", max_length=360, blank=True, null=True
    )
    truck_no = models.CharField(
        db_column="TRUCK_NO", max_length=360, blank=True, null=True
    )
    driver_contact_no = models.BigIntegerField(
        db_column="DRIVER_CONTACT_NO", blank=True, null=True
    )
    truck_allocated_date = models.DateTimeField(
        db_column="TRUCK_ALLOCATED_DATE", blank=True, null=True
    )
    truck_dispatched_date = models.DateTimeField(
        db_column="TRUCK_DISPATCHED_DATE", blank=True, null=True
    )
    invoice_number = models.BigIntegerField(
        db_column="INVOICE_NUMBER", blank=True, null=True
    )
    di_number = models.BigIntegerField(db_column="DI_NUMBER", blank=True, null=True)
    parent_id = models.DateTimeField(db_column="PARENT_ID", blank=True, null=True)
    transporter_name = models.CharField(
        db_column="TRANSPORTER_NAME", max_length=540, blank=True, null=True
    )
    transporter_phone_number = models.BigIntegerField(
        db_column="TRANSPORTER_PHONE_NUMBER", blank=True, null=True
    )
    erp_truck_number = models.CharField(
        db_column="ERP_TRUCK_NUMBER", max_length=360, blank=True, null=True
    )
    erp_driver_number = models.CharField(
        db_column="ERP_DRIVER_NUMBER", max_length=360, blank=True, null=True
    )
    consignee_id = models.CharField(
        db_column="CONSIGNEE_ID", max_length=360, blank=True, null=True
    )
    carrier_id = models.CharField(
        db_column="CARRIER_ID", max_length=360, blank=True, null=True
    )
    invoice_cancel_date = models.DateTimeField(
        db_column="INVOICE_CANCEL_DATE", blank=True, null=True
    )
    invoice_cancel_quantity = models.DecimalField(
        db_column="INVOICE_CANCEL_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    expected_delivery_slot = models.CharField(
        db_column="EXPECTED_DELIVERY_SLOT", max_length=360, blank=True, null=True
    )
    expected_delivery_date = models.DateTimeField(
        db_column="EXPECTED_DELIVERY_DATE", blank=True, null=True
    )
    sequence = models.BigIntegerField(db_column="SEQUENCE", blank=True, null=True)
    base_price = models.BigIntegerField(db_column="BASE_PRICE", blank=True, null=True)
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    token_number = models.BigIntegerField(
        db_column="TOKEN_NUMBER", blank=True, null=True
    )
    product_state = models.CharField(
        db_column="PRODUCT_STATE", max_length=360, blank=True, null=True
    )
    product_grade = models.CharField(
        db_column="PRODUCT_GRADE", max_length=360, blank=True, null=True
    )
    delivery_address_erp_address_id = models.CharField(
        db_column="DELIVERY_ADDRESS_ERP_ADDRESS_ID",
        max_length=360,
        blank=True,
        null=True,
    )
    delivery_address_erp_city = models.CharField(
        db_column="DELIVERY_ADDRESS_ERP_CITY", max_length=360, blank=True, null=True
    )
    source_code = models.CharField(
        db_column="SOURCE_CODE", max_length=360, blank=True, null=True
    )
    source_name = models.CharField(
        db_column="SOURCE_NAME", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    comments_by_so = models.CharField(
        db_column="COMMENTS_BY_SO", max_length=540, blank=True, null=True
    )
    comments_by_tsm = models.CharField(
        db_column="COMMENTS_BY_TSM", max_length=540, blank=True, null=True
    )
    comments_by_rh = models.CharField(
        db_column="COMMENTS_BY_RH", max_length=540, blank=True, null=True
    )
    reason_by_sh = models.TextField(db_column="REASON_BY_SH", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=540, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TRADE_ORDER_PLACEMENT_APPROVAL"


class AnnualStateLevelTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zh_id = models.BigIntegerField(db_column="ZH_ID", blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=360, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    sh_id = models.BigIntegerField(db_column="SH_ID", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    revised_target_by_zh = models.DecimalField(
        db_column="REVISED_TARGET_BY_ZH",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    comments_by_zh = models.TextField(db_column="COMMENTS_BY_ZH", blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    packaging_condition = models.CharField(
        db_column="PACKAGING_CONDITION", max_length=360, blank=True, null=True
    )
    bag_type = models.CharField(
        db_column="BAG_TYPE", max_length=360, blank=True, null=True
    )
    total = models.DecimalField(
        db_column="TOTAL", max_digits=22, decimal_places=2, blank=True, null=True
    )
    april = models.DecimalField(
        db_column="APRIL", max_digits=22, decimal_places=2, blank=True, null=True
    )
    may = models.DecimalField(
        db_column="MAY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    june = models.DecimalField(
        db_column="JUNE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    july = models.DecimalField(
        db_column="JULY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    august = models.DecimalField(
        db_column="AUGUST", max_digits=22, decimal_places=2, blank=True, null=True
    )
    september = models.DecimalField(
        db_column="SEPTEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    october = models.DecimalField(
        db_column="OCTOBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    november = models.DecimalField(
        db_column="NOVEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    december = models.DecimalField(
        db_column="DECEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    january = models.DecimalField(
        db_column="JANUARY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    february = models.DecimalField(
        db_column="FEBRUARY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    march = models.DecimalField(
        db_column="MARCH", max_digits=22, decimal_places=2, blank=True, null=True
    )
    is_target_sent_for_review = models.BooleanField(
        db_column="IS_TARGET_SENT_FOR_REVIEW", blank=True, null=True
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
        db_table = "ANNUAL_STATE_LEVEL_TARGET"


class AnnualDistrictLevelTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    rh_id = models.BigIntegerField(db_column="RH_ID", blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=360, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    revised_target_by_sh = models.DecimalField(
        db_column="REVISED_TARGET_BY_SH",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    comments_by_sh = models.TextField(db_column="COMMENTS_BY_SH", blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    packaging_condition = models.CharField(
        db_column="PACKAGING_CONDITION", max_length=360, blank=True, null=True
    )
    bag_type = models.CharField(
        db_column="BAG_TYPE", max_length=360, blank=True, null=True
    )
    total = models.DecimalField(
        db_column="TOTAL", max_digits=22, decimal_places=2, blank=True, null=True
    )
    april = models.DecimalField(
        db_column="APRIL", max_digits=22, decimal_places=2, blank=True, null=True
    )
    may = models.DecimalField(
        db_column="MAY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    june = models.DecimalField(
        db_column="JUNE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    july = models.DecimalField(
        db_column="JULY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    august = models.DecimalField(
        db_column="AUGUST", max_digits=22, decimal_places=2, blank=True, null=True
    )
    september = models.DecimalField(
        db_column="SEPTEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    october = models.DecimalField(
        db_column="OCTOBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    november = models.DecimalField(
        db_column="NOVEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    december = models.DecimalField(
        db_column="DECEMBER", max_digits=22, decimal_places=2, blank=True, null=True
    )
    january = models.DecimalField(
        db_column="JANUARY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    february = models.DecimalField(
        db_column="FEBRUARY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    march = models.DecimalField(
        db_column="MARCH", max_digits=22, decimal_places=2, blank=True, null=True
    )
    is_target_sent_for_review = models.BooleanField(
        db_column="IS_TARGET_SENT_FOR_REVIEW", blank=True, null=True
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
        db_table = "ANNUAL_DISTRICT_LEVEL_TARGET"


class RevisedBucketsApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    so_name = models.CharField(
        db_column="SO NAME", max_length=360, blank=True, null=True
    )
    so_code = models.CharField(db_column="SO CODE", max_length=1, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=100, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    packaging_condition = models.CharField(
        db_column="PACKAGING_CONDITION", max_length=360, blank=True, null=True
    )
    revised_target = models.DecimalField(
        db_column="REVISED_TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    new_revised_target = models.DecimalField(
        db_column="NEW_REVISED_TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    b1_field = models.DecimalField(
        db_column="B1 ", max_digits=22, decimal_places=2, blank=True, null=True
    )
    b2 = models.DecimalField(
        db_column="B2", max_digits=22, decimal_places=2, blank=True, null=True
    )
    b3 = models.DecimalField(
        db_column="B3", max_digits=22, decimal_places=2, blank=True, null=True
    )
    proposed_b3_target = models.DecimalField(
        db_column="PROPOSED_B3_TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    delta = models.DecimalField(
        db_column="DELTA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    deviation = models.DecimalField(
        db_column="DEVIATION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    reason = models.TextField(db_column="REASON", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "REVISED_BUCKETS_APPROVAL"


class CrmExceptionApprovalForReplacementOfProduct(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=360, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=360, blank=True, null=True
    )
    site_name = models.CharField(
        db_column="SITE_NAME", max_length=540, blank=True, null=True
    )
    site_code = models.CharField(
        db_column="SITE_CODE", max_length=360, blank=True, null=True
    )
    site_address = models.CharField(
        db_column="SITE_ADDRESS", max_length=360, blank=True, null=True
    )
    account_type = models.CharField(
        db_column="ACCOUNT_TYPE", max_length=360, blank=True, null=True
    )
    product_name = models.CharField(
        db_column="PRODUCT_NAME", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    quantity = models.BigIntegerField(db_column="QUANTITY", blank=True, null=True)
    quality = models.CharField(
        db_column="QUALITY", max_length=360, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=360, blank=True, null=True)
    so_name = models.CharField(
        db_column="SO_NAME", max_length=360, blank=True, null=True
    )
    so_emp_id = models.BigIntegerField(db_column="SO_EMP_ID", blank=True, null=True)
    so_phone_number = models.BigIntegerField(
        db_column="SO_PHONE_NUMBER", blank=True, null=True
    )
    so_email = models.CharField(
        db_column="SO_EMAIL", max_length=360, blank=True, null=True
    )
    tso_name = models.CharField(
        db_column="TSO_NAME", max_length=360, blank=True, null=True
    )
    tso_emp_id = models.BigIntegerField(db_column="TSO_EMP_ID", blank=True, null=True)
    tso_phone_number = models.BigIntegerField(
        db_column="TSO_PHONE_NUMBER", blank=True, null=True
    )
    tso_email = models.CharField(
        db_column="TSO_EMAIL", max_length=360, blank=True, null=True
    )
    reason_by_tso = models.TextField(db_column="REASON_BY_TSO", blank=True, null=True)
    datetime_of_escalation = models.DateTimeField(
        db_column="DATETIME_OF_ESCALATION", blank=True, null=True
    )
    date_of_invoice = models.DateTimeField(
        db_column="DATE_OF_INVOICE", blank=True, null=True
    )
    comment_by_sh = models.TextField(db_column="COMMENT_BY_SH", blank=True, null=True)
    status_by_sh = models.CharField(
        db_column="STATUS_BY_SH",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=360,
    )
    status_by_nsh = models.CharField(
        db_column="STATUS_BY_NSH",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=200,
    )
    comment_by_nsh = models.TextField(db_column="COMMENT_BY_NSH", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    approved_by = models.CharField(
        db_column="APPROVED_BY", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_EXCEPTION_APPROVAL_FOR_REPLACEMENT_OF_PRODUCT"


class CrmVerificationAndApprovalOfDealerSpForm(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    dealer_name = models.CharField(
        db_column="DEALER_NAME", max_length=360, blank=True, null=True
    )
    dealer_crm_code = models.CharField(
        db_column="DEALER_CRM_CODE", max_length=360, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=360, blank=True, null=True)
    potential = models.CharField(
        db_column="POTENTIAL", max_length=360, blank=True, null=True
    )
    approving_so = models.CharField(
        db_column="APPROVING_SO", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    account_number = models.BigIntegerField(
        db_column="ACCOUNT_NUMBER", blank=True, null=True
    )
    ifsc_code = models.CharField(
        db_column="IFSC_CODE", max_length=360, blank=True, null=True
    )
    doc = models.CharField(db_column="DOC", max_length=360, blank=True, null=True)
    account_name = models.CharField(
        db_column="ACCOUNT_NAME", max_length=360, blank=True, null=True
    )
    gst_number = models.CharField(
        db_column="GST_NUMBER", max_length=360, blank=True, null=True
    )
    state_registration = models.CharField(
        db_column="STATE_REGISTRATION", max_length=360, blank=True, null=True
    )
    registration_address = models.CharField(
        db_column="REGISTRATION_ADDRESS", max_length=540, blank=True, null=True
    )
    pin_code = models.BigIntegerField(db_column="PIN_CODE", blank=True, null=True)
    contact_number = models.BigIntegerField(
        db_column="CONTACT_NUMBER", blank=True, null=True
    )
    aadhaar_number = models.BigIntegerField(
        db_column="AADHAAR_NUMBER", blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    comment_by_rh = models.CharField(
        db_column="COMMENT_BY_RH", max_length=360, blank=True, null=True
    )
    status_by_sh = models.CharField(
        db_column="STATUS_BY_SH", max_length=360, blank=True, null=True
    )
    email_address = models.CharField(
        db_column="EMAIL_ADDRESS", max_length=200, blank=True, null=True
    )
    status_by_nsh = models.TextField(db_column="STATUS_BY_NSH", blank=True, null=True)
    comment_by_sh = models.TextField(db_column="COMMENT_BY_SH", blank=True, null=True)
    comment_by_nsh = models.TextField(db_column="COMMENT_BY_NSH", blank=True, null=True)
    approving_so_email = models.CharField(
        db_column="APPROVING_SO_EMAIL", max_length=360, blank=True, null=True
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
        db_table = "CRM_VERIFICATION_AND_APPROVAL_OF_DEALER_SP_FORM"


class CrmCompanyDetails(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    director_name = models.CharField(
        db_column="DIRECTOR_NAME", max_length=540, blank=True, null=True
    )
    director_father_name = models.CharField(
        db_column="DIRECTOR_FATHER_NAME", max_length=540, blank=True, null=True
    )
    address = models.TextField(db_column="ADDRESS", blank=True, null=True)
    pan = models.CharField(db_column="PAN", max_length=540, blank=True, null=True)
    din = models.BigIntegerField(db_column="DIN", blank=True, null=True)
    pan_link = models.TextField(db_column="PAN_LINK", blank=True, null=True)
    din_link = models.TextField(db_column="DIN_LINK", blank=True, null=True)
    verfication_dealer_sp_form = models.ForeignKey(
        "CrmVerificationAndApprovalOfDealerSpForm",
        models.DO_NOTHING,
        db_column="VERFICATION_DEALER_SP_FORM_ID",
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_COMPANY_DETAILS"


class CrmFinancialInfo(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    nominee_name = models.CharField(
        db_column="NOMINEE_NAME", max_length=540, blank=True, null=True
    )
    nominee_father_name = models.CharField(
        db_column="NOMINEE_FATHER_NAME", max_length=540, blank=True, null=True
    )
    address = models.TextField(db_column="ADDRESS", blank=True, null=True)
    crm_company_details = models.ForeignKey(
        "CrmCompanyDetails",
        models.DO_NOTHING,
        db_column="CRM_COMPANY_DETAILS_ID",
        blank=True,
        null=True,
    )
    pan = models.CharField(db_column="PAN", max_length=540, blank=True, null=True)
    pan_link = models.TextField(db_column="PAN_LINK", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_FINANCIAL_INFO"


class CrmPotential(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_uid = models.BigIntegerField(
        db_column="CUSTOMER_UID", blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    brand_name = models.CharField(
        db_column="BRAND_NAME", max_length=540, blank=True, null=True
    )
    brand_wise_sale_in_mt = models.DecimalField(
        db_column="BRAND_WISE_SALE_IN_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    warehouse_capacity = models.DecimalField(
        db_column="WAREHOUSE_CAPACITY",
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

    class Meta:
        managed = False
        db_table = "CRM_POTENTIAL"


class CrmDriverDetails(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_uid = models.BigIntegerField(
        db_column="CUSTOMER_UID", blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    driver_name = models.CharField(
        db_column="DRIVER_NAME", max_length=540, blank=True, null=True
    )
    driver_contact_number = models.BigIntegerField(
        db_column="DRIVER_CONTACT_NUMBER", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_DRIVER_DETAILS"


class CrmVehicleMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_uid = models.BigIntegerField(
        db_column="CUSTOMER_UID", blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    vehicle_make = models.CharField(
        db_column="VEHICLE_MAKE", max_length=540, blank=True, null=True
    )
    vehicle_model = models.CharField(
        db_column="VEHICLE_MODEL", max_length=540, blank=True, null=True
    )
    vehicle_number = models.CharField(
        db_column="VEHICLE_NUMBER", max_length=540, blank=True, null=True
    )
    vehicle_capacity = models.DecimalField(
        db_column="VEHICLE_CAPACITY",
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

    class Meta:
        managed = False
        db_table = "CRM_VEHICLE_MASTER"


class ExceptionDisbursementApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_id = models.BigIntegerField(db_column="REQUEST_ID", blank=True, null=True)
    customer_id = models.BigIntegerField(db_column="CUSTOMER_ID", blank=True, null=True)
    scheme_id = models.BigIntegerField(db_column="SCHEME_ID", blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    slab = models.CharField(db_column="SLAB", max_length=360, blank=True, null=True)
    slab_incentive = models.CharField(
        db_column="SLAB_INCENTIVE", max_length=360, blank=True, null=True
    )
    incentive_earned = models.CharField(
        db_column="INCENTIVE_EARNED", max_length=360, blank=True, null=True
    )
    missed_target = models.DecimalField(
        db_column="MISSED_TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    status_by_sh = models.CharField(
        db_column="STATUS_BY_SH",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=360,
    )
    reason = models.TextField(db_column="REASON", blank=True, null=True)
    channel_partner_name = models.CharField(
        db_column="CHANNEL_PARTNER_NAME", max_length=360, blank=True, null=True
    )
    so_name = models.CharField(
        db_column="SO_NAME", max_length=360, blank=True, null=True
    )
    disbursement_type = models.CharField(
        db_column="DISBURSEMENT_TYPE", max_length=360, blank=True, null=True
    )
    discount_or_scheme_name = models.CharField(
        db_column="DISCOUNT_OR_SCHEME_NAME", max_length=360, blank=True, null=True
    )
    dealer_achievement = models.CharField(
        db_column="DEALER_ACHIEVEMENT", max_length=360, blank=True, null=True
    )
    cp_category = models.CharField(
        db_column="CP_CATEGORY", max_length=360, blank=True, null=True
    )
    counter_share = models.DecimalField(
        db_column="COUNTER_SHARE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    counter_potential = models.DecimalField(
        db_column="COUNTER_POTENTIAL",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    scheme_name = models.CharField(
        db_column="SCHEME_NAME", max_length=360, blank=True, null=True
    )
    scheme_objective = models.TextField(
        db_column="SCHEME_OBJECTIVE", blank=True, null=True
    )
    comment_by_so = models.CharField(
        db_column="COMMENT_BY_SO", max_length=360, blank=True, null=True
    )
    comment_by_sh = models.CharField(
        db_column="COMMENT_BY_SH", max_length=360, blank=True, null=True
    )
    comment_by_nsh = models.CharField(
        db_column="COMMENT_BY_NSH", max_length=360, blank=True, null=True
    )
    status_by_nsh = models.CharField(
        db_column="STATUS_BY_NSH",
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
        max_length=540,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    approved_by = models.CharField(
        db_column="APPROVED_BY", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "EXCEPTION_DISBURSEMENT_APPROVAL"


class GiftRedeemRequestApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_id = models.BigIntegerField(db_column="REQUEST_ID", blank=True, null=True)
    entity_id = models.BigIntegerField(db_column="ENTITY_ID", blank=True, null=True)
    entity_type = models.CharField(
        db_column="ENTITY_TYPE", max_length=360, blank=True, null=True
    )
    redeeem_type = models.CharField(
        db_column="REDEEEM_TYPE", max_length=360, blank=True, null=True
    )
    gift_name = models.CharField(
        db_column="GIFT_NAME", max_length=360, blank=True, null=True
    )
    gift_id = models.CharField(
        db_column="GIFT_ID", max_length=360, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    redeem_request_raised_by_type = models.CharField(
        db_column="REDEEM_REQUEST_RAISED_BY_TYPE", max_length=360, blank=True, null=True
    )
    redeem_request_raised_by_entity_id = models.BigIntegerField(
        db_column="REDEEM_REQUEST_RAISED_BY_ENTITY_ID", blank=True, null=True
    )
    redeem_request_raised_by_name = models.CharField(
        db_column="REDEEM_REQUEST_RAISED_BY_NAME", max_length=540, blank=True, null=True
    )
    redeem_request_value = models.DecimalField(
        db_column="REDEEM_REQUEST_VALUE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    reason = models.TextField(db_column="REASON", blank=True, null=True)
    partner_name = models.CharField(
        db_column="PARTNER_NAME", max_length=360, blank=True, null=True
    )
    partner_type = models.CharField(
        db_column="PARTNER_TYPE", max_length=360, blank=True, null=True
    )
    partner_code = models.BigIntegerField(
        db_column="PARTNER_CODE", blank=True, null=True
    )
    partner_category = models.CharField(
        db_column="PARTNER_CATEGORY", max_length=360, blank=True, null=True
    )
    requested_date = models.DateTimeField(
        db_column="REQUESTED_DATE", blank=True, null=True
    )
    approved_by = models.CharField(
        db_column="APPROVED_BY", max_length=360, blank=True, null=True
    )
    approver_mail = models.CharField(
        db_column="APPROVER_MAIL", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    status_by_sh = models.CharField(
        db_column="STATUS_BY_SH",
        max_length=360,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
    )
    status_by_nsh = models.CharField(
        db_column="STATUS_BY_NSH",
        max_length=360,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING,
    )
    comment_by_sh = models.TextField(db_column="COMMENT_BY_SH", blank=True, null=True)
    comment_by_nsh = models.TextField(db_column="COMMENT_BY_NSH", blank=True, null=True)
    nsh_approved = models.CharField(
        db_column="NSH_APPROVED", max_length=360, blank=True, null=True
    )
    comment_by_do = models.TextField(db_column="COMMENT_BY_DO", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "GIFT_REDEEM_REQUEST_APPROVAL"


class GiftRedeemRequestApprovalRewards(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    gift_redeem_request_approval = models.ForeignKey(
        GiftRedeemRequestApproval,
        models.DO_NOTHING,
        db_column="GIFT_REDEEM_REQUEST_APPROVAL",
        blank=True,
        null=True,
    )
    reward_type = models.CharField(
        db_column="REWARD_TYPE", max_length=360, blank=True, null=True
    )
    reward_name = models.CharField(
        db_column="REWARD_NAME", max_length=360, blank=True, null=True
    )
    reward_value = models.DecimalField(
        db_column="REWARD_VALUE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "GIFT_REDEEM_REQUEST_APPROVAL_REWARDS"
