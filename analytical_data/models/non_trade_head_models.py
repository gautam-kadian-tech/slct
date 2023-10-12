"""Analytical data non-trade head models module."""
from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import User


class TOebsXxsclMktLink(models.Model):
    """Market link model class."""

    rec_link_id = models.DecimalField(
        db_column="REC_LINK_ID",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        unique=True,
    )
    org_id = models.DecimalField(
        db_column="ORG_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    field_officer = models.CharField(
        db_column="FIELD_OFFICER", max_length=320, blank=True, null=True
    )
    regional_manager = models.CharField(
        db_column="REGIONAL_MANAGER", max_length=320, blank=True, null=True
    )
    state_head = models.CharField(
        db_column="STATE_HEAD", max_length=320, blank=True, null=True
    )
    marketing_head = models.CharField(
        db_column="MARKETING_HEAD", max_length=320, blank=True, null=True
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    created_by = models.DecimalField(
        db_column="CREATED_BY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    field_officer_name = models.CharField(
        db_column="FIELD_OFFICER_NAME", max_length=100, blank=True, null=True
    )
    regional_manager_name = models.CharField(
        db_column="REGIONAL_MANAGER_NAME", max_length=100, blank=True, null=True
    )
    state_head_name = models.CharField(
        db_column="STATE_HEAD_NAME", max_length=100, blank=True, null=True
    )
    marketing_head_name = models.CharField(
        db_column="MARKETING_HEAD_NAME", max_length=100, blank=True, null=True
    )
    mh_code = models.CharField(
        db_column="MH_CODE", max_length=100, blank=True, null=True
    )
    mh_name = models.CharField(
        db_column="MH_NAME", max_length=100, blank=True, null=True
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
        db_table = "T_OEBS_XXSCL_MKT_LINK"


class TOebsHzCustAccounts(models.Model):
    """Customer accounts model class."""

    cust_account_id = models.DecimalField(
        db_column="CUST_ACCOUNT_ID",
        unique=True,
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    account_number = models.CharField(
        db_column="ACCOUNT_NUMBER", max_length=30, blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
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
    wh_update_date = models.DateTimeField(
        db_column="WH_UPDATE_DATE", blank=True, null=True
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
    # attribute3 = models.CharField(
    #     db_column="ATTRIBUTE3", max_length=150, blank=True, null=True
    # )
    attribute3 = models.ForeignKey(
        TOebsXxsclMktLink,
        to_field="rec_link_id",
        db_column="ATTRIBUTE3",
        on_delete=models.CASCADE,
        related_name="customer_accounts",
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
    attribute16 = models.CharField(
        db_column="ATTRIBUTE16", max_length=150, blank=True, null=True
    )
    attribute17 = models.CharField(
        db_column="ATTRIBUTE17", max_length=150, blank=True, null=True
    )
    attribute18 = models.CharField(
        db_column="ATTRIBUTE18", max_length=150, blank=True, null=True
    )
    attribute19 = models.CharField(
        db_column="ATTRIBUTE19", max_length=150, blank=True, null=True
    )
    attribute20 = models.CharField(
        db_column="ATTRIBUTE20", max_length=150, blank=True, null=True
    )
    global_attribute_category = models.CharField(
        db_column="GLOBAL_ATTRIBUTE_CATEGORY", max_length=30, blank=True, null=True
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
    orig_system_reference = models.CharField(
        db_column="ORIG_SYSTEM_REFERENCE",
        unique=True,
        max_length=240,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=1, blank=True, null=True)
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=30, blank=True, null=True
    )
    customer_class_code = models.CharField(
        db_column="CUSTOMER_CLASS_CODE", max_length=30, blank=True, null=True
    )
    primary_salesrep_id = models.DecimalField(
        db_column="PRIMARY_SALESREP_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    sales_channel_code = models.CharField(
        db_column="SALES_CHANNEL_CODE", max_length=30, blank=True, null=True
    )
    order_type_id = models.DecimalField(
        db_column="ORDER_TYPE_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    price_list_id = models.DecimalField(
        db_column="PRICE_LIST_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    subcategory_code = models.CharField(
        db_column="SUBCATEGORY_CODE", max_length=30, blank=True, null=True
    )
    tax_code = models.CharField(
        db_column="TAX_CODE", max_length=50, blank=True, null=True
    )
    fob_point = models.CharField(
        db_column="FOB_POINT", max_length=30, blank=True, null=True
    )
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=30, blank=True, null=True
    )
    ship_partial = models.CharField(
        db_column="SHIP_PARTIAL", max_length=1, blank=True, null=True
    )
    ship_via = models.CharField(
        db_column="SHIP_VIA", max_length=30, blank=True, null=True
    )
    warehouse_id = models.DecimalField(
        db_column="WAREHOUSE_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    payment_term_id = models.DecimalField(
        db_column="PAYMENT_TERM_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    tax_header_level_flag = models.CharField(
        db_column="TAX_HEADER_LEVEL_FLAG", max_length=1, blank=True, null=True
    )
    tax_rounding_rule = models.CharField(
        db_column="TAX_ROUNDING_RULE", max_length=30, blank=True, null=True
    )
    coterminate_day_month = models.CharField(
        db_column="COTERMINATE_DAY_MONTH", max_length=6, blank=True, null=True
    )
    primary_specialist_id = models.DecimalField(
        db_column="PRIMARY_SPECIALIST_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    secondary_specialist_id = models.DecimalField(
        db_column="SECONDARY_SPECIALIST_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    account_liable_flag = models.CharField(
        db_column="ACCOUNT_LIABLE_FLAG", max_length=1, blank=True, null=True
    )
    restriction_limit_amount = models.DecimalField(
        db_column="RESTRICTION_LIMIT_AMOUNT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_balance = models.DecimalField(
        db_column="CURRENT_BALANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    password_text = models.CharField(
        db_column="PASSWORD_TEXT", max_length=60, blank=True, null=True
    )
    high_priority_indicator = models.CharField(
        db_column="HIGH_PRIORITY_INDICATOR", max_length=1, blank=True, null=True
    )
    account_established_date = models.DateTimeField(
        db_column="ACCOUNT_ESTABLISHED_DATE", blank=True, null=True
    )
    account_termination_date = models.DateTimeField(
        db_column="ACCOUNT_TERMINATION_DATE", blank=True, null=True
    )
    account_activation_date = models.DateTimeField(
        db_column="ACCOUNT_ACTIVATION_DATE", blank=True, null=True
    )
    credit_classification_code = models.CharField(
        db_column="CREDIT_CLASSIFICATION_CODE", max_length=30, blank=True, null=True
    )
    department = models.CharField(
        db_column="DEPARTMENT", max_length=30, blank=True, null=True
    )
    major_account_number = models.CharField(
        db_column="MAJOR_ACCOUNT_NUMBER", max_length=30, blank=True, null=True
    )
    hotwatch_service_flag = models.CharField(
        db_column="HOTWATCH_SERVICE_FLAG", max_length=1, blank=True, null=True
    )
    hotwatch_svc_bal_ind = models.CharField(
        db_column="HOTWATCH_SVC_BAL_IND", max_length=30, blank=True, null=True
    )
    held_bill_expiration_date = models.DateTimeField(
        db_column="HELD_BILL_EXPIRATION_DATE", blank=True, null=True
    )
    hold_bill_flag = models.CharField(
        db_column="HOLD_BILL_FLAG", max_length=1, blank=True, null=True
    )
    high_priority_remarks = models.CharField(
        db_column="HIGH_PRIORITY_REMARKS", max_length=80, blank=True, null=True
    )
    po_effective_date = models.DateTimeField(
        db_column="PO_EFFECTIVE_DATE", blank=True, null=True
    )
    po_expiration_date = models.DateTimeField(
        db_column="PO_EXPIRATION_DATE", blank=True, null=True
    )
    realtime_rate_flag = models.CharField(
        db_column="REALTIME_RATE_FLAG", max_length=1, blank=True, null=True
    )
    single_user_flag = models.CharField(
        db_column="SINGLE_USER_FLAG", max_length=1, blank=True, null=True
    )
    watch_account_flag = models.CharField(
        db_column="WATCH_ACCOUNT_FLAG", max_length=1, blank=True, null=True
    )
    watch_balance_indicator = models.CharField(
        db_column="WATCH_BALANCE_INDICATOR", max_length=1, blank=True, null=True
    )
    geo_code = models.CharField(
        db_column="GEO_CODE", max_length=30, blank=True, null=True
    )
    acct_life_cycle_status = models.CharField(
        db_column="ACCT_LIFE_CYCLE_STATUS", max_length=30, blank=True, null=True
    )
    account_name = models.CharField(
        db_column="ACCOUNT_NAME", max_length=240, blank=True, null=True
    )
    deposit_refund_method = models.CharField(
        db_column="DEPOSIT_REFUND_METHOD", max_length=20, blank=True, null=True
    )
    dormant_account_flag = models.CharField(
        db_column="DORMANT_ACCOUNT_FLAG", max_length=1, blank=True, null=True
    )
    npa_number = models.CharField(
        db_column="NPA_NUMBER", max_length=60, blank=True, null=True
    )
    pin_number = models.DecimalField(
        db_column="PIN_NUMBER", max_digits=16, decimal_places=0, blank=True, null=True
    )
    suspension_date = models.DateTimeField(
        db_column="SUSPENSION_DATE", blank=True, null=True
    )
    write_off_adjustment_amount = models.DecimalField(
        db_column="WRITE_OFF_ADJUSTMENT_AMOUNT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    write_off_payment_amount = models.DecimalField(
        db_column="WRITE_OFF_PAYMENT_AMOUNT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    write_off_amount = models.DecimalField(
        db_column="WRITE_OFF_AMOUNT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    source_code = models.CharField(
        db_column="SOURCE_CODE", max_length=150, blank=True, null=True
    )
    competitor_type = models.CharField(
        db_column="COMPETITOR_TYPE", max_length=150, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=240, blank=True, null=True
    )
    dates_negative_tolerance = models.DecimalField(
        db_column="DATES_NEGATIVE_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dates_positive_tolerance = models.DecimalField(
        db_column="DATES_POSITIVE_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date_type_preference = models.CharField(
        db_column="DATE_TYPE_PREFERENCE", max_length=20, blank=True, null=True
    )
    over_shipment_tolerance = models.DecimalField(
        db_column="OVER_SHIPMENT_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    under_shipment_tolerance = models.DecimalField(
        db_column="UNDER_SHIPMENT_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    over_return_tolerance = models.DecimalField(
        db_column="OVER_RETURN_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    under_return_tolerance = models.DecimalField(
        db_column="UNDER_RETURN_TOLERANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    item_cross_ref_pref = models.CharField(
        db_column="ITEM_CROSS_REF_PREF", max_length=30, blank=True, null=True
    )
    ship_sets_include_lines_flag = models.CharField(
        db_column="SHIP_SETS_INCLUDE_LINES_FLAG", max_length=1, blank=True, null=True
    )
    arrivalsets_include_lines_flag = models.CharField(
        db_column="ARRIVALSETS_INCLUDE_LINES_FLAG", max_length=1, blank=True, null=True
    )
    sched_date_push_flag = models.CharField(
        db_column="SCHED_DATE_PUSH_FLAG", max_length=1, blank=True, null=True
    )
    invoice_quantity_rule = models.CharField(
        db_column="INVOICE_QUANTITY_RULE", max_length=30, blank=True, null=True
    )
    pricing_event = models.CharField(
        db_column="PRICING_EVENT", max_length=30, blank=True, null=True
    )
    account_replication_key = models.DecimalField(
        db_column="ACCOUNT_REPLICATION_KEY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    status_update_date = models.DateTimeField(
        db_column="STATUS_UPDATE_DATE", blank=True, null=True
    )
    autopay_flag = models.CharField(
        db_column="AUTOPAY_FLAG", max_length=1, blank=True, null=True
    )
    notify_flag = models.CharField(
        db_column="NOTIFY_FLAG", max_length=1, blank=True, null=True
    )
    last_batch_id = models.DecimalField(
        db_column="LAST_BATCH_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    org_id = models.DecimalField(
        db_column="ORG_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    object_version_number = models.DecimalField(
        db_column="OBJECT_VERSION_NUMBER",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by_module = models.CharField(
        db_column="CREATED_BY_MODULE", max_length=150, blank=True, null=True
    )
    application_id = models.DecimalField(
        db_column="APPLICATION_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    selling_party_id = models.DecimalField(
        db_column="SELLING_PARTY_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    federal_entity_type = models.CharField(
        db_column="FEDERAL_ENTITY_TYPE", max_length=30, blank=True, null=True
    )
    trading_partner_agency_id = models.CharField(
        db_column="TRADING_PARTNER_AGENCY_ID", max_length=3, blank=True, null=True
    )
    duns_extension = models.CharField(
        db_column="DUNS_EXTENSION", max_length=4, blank=True, null=True
    )
    advance_payment_indicator = models.CharField(
        db_column="ADVANCE_PAYMENT_INDICATOR", max_length=30, blank=True, null=True
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
        db_table = "T_OEBS_HZ_CUST_ACCOUNTS"


class NtNotesComms(models.Model):
    """Non-trade notes and communication model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    type = models.CharField(db_column="TYPE", max_length=100, blank=True, null=True)
    subject = models.CharField(db_column="SUBJECT", max_length=100)
    remark = models.CharField(db_column="REMARK", max_length=255)
    attachment = models.CharField(
        db_column="ATTACHMENT", max_length=250, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NT_NOTES_COMMS"


class DimResources(models.Model):
    """Resources data (NTSOs) model class."""

    id = models.BigIntegerField(db_column="ID", primary_key=True)
    resource_name = models.CharField(db_column="RESOURCE_NAME", max_length=360)
    resource_id = models.TextField(db_column="RESOURCE_ID", blank=True, null=True)
    designation = models.CharField(db_column="DESIGNATION", max_length=360)
    segment = models.CharField(db_column="SEGMENT", max_length=5, blank=True, null=True)
    eff_start_date = models.DateTimeField(db_column="EFF_START_DATE")
    eff_end_date = models.DateTimeField(db_column="EFF_END_DATE")
    resource_city_id = models.BigIntegerField(db_column="RESOURCE_CITY_ID")
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "DIM_RESOURCES"


class NtCommsNotified(models.Model):
    """Nt communication notified to model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    nnc_id = models.ForeignKey(
        NtNotesComms,
        db_column="NNC_ID",
        on_delete=models.CASCADE,
        related_name="communication_notifies",
    )
    notified_to = models.ForeignKey(
        DimResources, db_column="NOTIFIED_TO", on_delete=models.CASCADE
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NT_COMMS_NOTIFIED"


class NtNcrThreshold(models.Model):
    """Non-trade ncr threshold model class."""

    ACCOUNT_TYPE_CHOICES = [("Key", "Key"), ("General", "General")]

    id = models.BigAutoField(db_column="ID", primary_key=True)
    threshold_id = models.CharField(
        db_column="THRESHOLD_ID", max_length=20, blank=True, null=True
    )
    account_type = models.CharField(
        db_column="ACCOUNT_TYPE",
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    ncr_thresholds = models.DecimalField(
        db_column="NCR_THRESHOLDS",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    valid_till = models.DateField(db_column="VALID_TILL", blank=True, null=True)
    product_string = models.CharField(
        db_column="PRODUCT_STRING", max_length=30, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=50, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=50, blank=True, null=True)
    comments = models.CharField(
        db_column="COMMENTS", max_length=255, blank=True, null=True
    )
    status = models.BooleanField(db_column="STATUS", default=True)
    type = models.CharField(db_column="TYPE", max_length=50, blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "NT_NCR_THRESHOLD"


class TOebsSclArNcrAdvanceCalcTab(models.Model):
    """Non-trade ncr advance calc tab model class."""

    quantity_invoiced = models.DecimalField(
        db_column="QUANTITY_INVOICED",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    customer_number = models.DecimalField(
        db_column="CUSTOMER_NUMBER",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=240, blank=True, null=True
    )
    order_classification = models.CharField(
        db_column="ORDER_CLASSIFICATION", max_length=50, blank=True, null=True
    )
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=50, blank=True, null=True
    )
    delivery_id = models.DecimalField(
        db_column="DELIVERY_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    misc_charges = models.DecimalField(
        db_column="MISC_CHARGES", max_digits=20, decimal_places=0, blank=True, null=True
    )
    misc_charges_dummy = models.DecimalField(
        db_column="MISC_CHARGES_DUMMY",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    customer_trx_line_id = models.DecimalField(
        db_column="CUSTOMER_TRX_LINE_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    unit_standard_price = models.DecimalField(
        db_column="UNIT_STANDARD_PRICE",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    org_id = models.DecimalField(
        db_column="ORG_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    city = models.CharField(db_column="CITY", max_length=60, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=60, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=60, blank=True, null=True)
    warehouse = models.CharField(
        db_column="WAREHOUSE", max_length=50, blank=True, null=True
    )
    invoice_number = models.DecimalField(
        db_column="INVOICE_NUMBER",
        max_digits=50,
        decimal_places=0,
        primary_key=True,
    )
    invoice_date = models.DateTimeField(db_column="INVOICE_DATE", blank=True, null=True)
    sales_order_date = models.DateTimeField(
        db_column="SALES_ORDER_DATE", blank=True, null=True
    )
    customer_id = models.DecimalField(
        db_column="CUSTOMER_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    customer_depot = models.CharField(
        db_column="CUSTOMER_DEPOT", max_length=50, blank=True, null=True
    )
    sales_order_number = models.DecimalField(
        db_column="SALES_ORDER_NUMBER",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    unit_selling_price = models.DecimalField(
        db_column="UNIT_SELLING_PRICE",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    customer_trx_id = models.DecimalField(
        db_column="CUSTOMER_TRX_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    uom_code = models.CharField(
        db_column="UOM_CODE", max_length=50, blank=True, null=True
    )
    sales_tax_pmt = models.DecimalField(
        db_column="SALES_TAX_PMT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    excise_tax_pmt = models.DecimalField(
        db_column="EXCISE_TAX_PMT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    rebate_and_discount = models.DecimalField(
        db_column="REBATE_AND_DISCOUNT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ha_commission = models.DecimalField(
        db_column="HA_COMMISSION",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    shortage = models.DecimalField(
        db_column="SHORTAGE", max_digits=20, decimal_places=0, blank=True, null=True
    )
    demurrages_and_warfages = models.DecimalField(
        db_column="DEMURRAGES_AND_WARFAGES",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    rake_charges = models.DecimalField(
        db_column="RAKE_CHARGES", max_digits=20, decimal_places=0, blank=True, null=True
    )
    unloading_charges = models.DecimalField(
        db_column="UNLOADING_CHARGES",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    packing_charges = models.DecimalField(
        db_column="PACKING_CHARGES",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    primary_freight = models.DecimalField(
        db_column="PRIMARY_FREIGHT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    secondary_freight = models.DecimalField(
        db_column="SECONDARY_FREIGHT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    sp_commission = models.DecimalField(
        db_column="SP_COMMISSION",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    isp_commission = models.DecimalField(
        db_column="ISP_COMMISSION",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    new_misc_charges = models.DecimalField(
        db_column="NEW_MISC_CHARGES",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ncr = models.DecimalField(
        db_column="NCR", max_digits=20, decimal_places=0, blank=True, null=True
    )
    credit_memo_number = models.DecimalField(
        db_column="CREDIT_MEMO_NUMBER",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    credit_memo_date = models.DateTimeField(
        db_column="CREDIT_MEMO_DATE", blank=True, null=True
    )
    manual_invoice_flag = models.CharField(
        db_column="MANUAL_INVOICE_FLAG", max_length=10, blank=True, null=True
    )
    manual_invoice_number = models.DecimalField(
        db_column="MANUAL_INVOICE_NUMBER",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_invoice_date = models.DateTimeField(
        db_column="MANUAL_INVOICE_DATE", blank=True, null=True
    )
    new_mm_commission = models.DecimalField(
        db_column="NEW_MM_COMMISSION",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    mm_comm_dummy = models.DecimalField(
        db_column="MM_COMM_DUMMY",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    new_selling_price = models.DecimalField(
        db_column="NEW_SELLING_PRICE",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    selling_price_dummy = models.DecimalField(
        db_column="SELLING_PRICE_DUMMY",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    new_ncr = models.DecimalField(
        db_column="NEW_NCR", max_digits=20, decimal_places=0, blank=True, null=True
    )
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
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
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=30, blank=True, null=True
    )
    kkg_pri_freight_rate = models.DecimalField(
        db_column="KKG_PRI_FREIGHT_RATE",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    city_id = models.DecimalField(
        db_column="CITY_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sch1 = models.DecimalField(
        db_column="SCH1", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch2 = models.DecimalField(
        db_column="SCH2", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch3 = models.DecimalField(
        db_column="SCH3", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch4 = models.DecimalField(
        db_column="SCH4", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch5 = models.DecimalField(
        db_column="SCH5", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch6 = models.DecimalField(
        db_column="SCH6", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch7 = models.DecimalField(
        db_column="SCH7", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch8 = models.DecimalField(
        db_column="SCH8", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch9 = models.DecimalField(
        db_column="SCH9", max_digits=50, decimal_places=2, blank=True, null=True
    )
    pl_id = models.DecimalField(
        db_column="PL_ID", max_digits=50, decimal_places=2, blank=True, null=True
    )
    line_id = models.DecimalField(
        db_column="LINE_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fob_code = models.CharField(
        db_column="FOB_CODE", max_length=32, blank=True, null=True
    )
    primary_frt_term = models.CharField(
        db_column="PRIMARY_FRT_TERM", max_length=32, blank=True, null=True
    )
    secondary_frt_term = models.CharField(
        db_column="SECONDARY_FRT_TERM", max_length=32, blank=True, null=True
    )
    secondary_frt_all = models.DecimalField(
        db_column="SECONDARY_FRT_ALL",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sales_type = models.CharField(
        db_column="SALES_TYPE", max_length=32, blank=True, null=True
    )
    vat_invoice_no = models.CharField(
        db_column="VAT_INVOICE_NO", max_length=32, blank=True, null=True
    )
    tax_category_id = models.DecimalField(
        db_column="TAX_CATEGORY_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    mm_name = models.CharField(
        db_column="MM_NAME", max_length=240, blank=True, null=True
    )
    org_type = models.CharField(
        db_column="ORG_TYPE", max_length=50, blank=True, null=True
    )
    inventory_item_id = models.DecimalField(
        db_column="INVENTORY_ITEM_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sch0 = models.DecimalField(
        db_column="SCH0", max_digits=50, decimal_places=2, blank=True, null=True
    )
    tax_rate = models.DecimalField(
        db_column="TAX_RATE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vatcredit = models.CharField(
        db_column="VATCREDIT", max_length=10, blank=True, null=True
    )
    unloading_by = models.CharField(
        db_column="UNLOADING_BY", max_length=50, blank=True, null=True
    )
    whse_state = models.CharField(
        db_column="WHSE_STATE", max_length=30, blank=True, null=True
    )
    vat_cst = models.CharField(
        db_column="VAT_CST", max_length=30, blank=True, null=True
    )
    cust_categ = models.CharField(
        db_column="CUST_CATEG", max_length=30, blank=True, null=True
    )
    cust_subcateg = models.CharField(
        db_column="CUST_SUBCATEG", max_length=30, blank=True, null=True
    )
    hid0 = models.DecimalField(
        db_column="HID0", max_digits=50, decimal_places=2, blank=True, null=True
    )
    exp0 = models.DecimalField(
        db_column="EXP0", max_digits=50, decimal_places=2, blank=True, null=True
    )
    exp1 = models.DecimalField(
        db_column="EXP1", max_digits=50, decimal_places=2, blank=True, null=True
    )
    exp2 = models.DecimalField(
        db_column="EXP2", max_digits=50, decimal_places=2, blank=True, null=True
    )
    exp3 = models.DecimalField(
        db_column="EXP3", max_digits=50, decimal_places=2, blank=True, null=True
    )
    exp4 = models.DecimalField(
        db_column="EXP4", max_digits=50, decimal_places=2, blank=True, null=True
    )
    ncr_exp = models.DecimalField(
        db_column="NCR_EXP",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    subsidy = models.DecimalField(
        db_column="SUBSIDY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ncr_subsidy = models.DecimalField(
        db_column="NCR_SUBSIDY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    subsidy_lot = models.CharField(
        db_column="SUBSIDY_LOT", max_length=32, blank=True, null=True
    )
    frt_st_exp = models.DecimalField(
        db_column="FRT_ST_EXP",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=32, blank=True, null=True
    )
    packing_bag = models.CharField(
        db_column="PACKING_BAG", max_length=32, blank=True, null=True
    )
    rd_frt_amt = models.DecimalField(
        db_column="RD_FRT_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sch11 = models.DecimalField(
        db_column="SCH11", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch12 = models.DecimalField(
        db_column="SCH12", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch13 = models.DecimalField(
        db_column="SCH13", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch14 = models.DecimalField(
        db_column="SCH14", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch15 = models.DecimalField(
        db_column="SCH15", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch16 = models.DecimalField(
        db_column="SCH16", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch17 = models.DecimalField(
        db_column="SCH17", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch18 = models.DecimalField(
        db_column="SCH18", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch19 = models.DecimalField(
        db_column="SCH19", max_digits=50, decimal_places=2, blank=True, null=True
    )
    sch20 = models.DecimalField(
        db_column="SCH20", max_digits=50, decimal_places=2, blank=True, null=True
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
    # id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB"
        unique_together = (("org_id", "customer_trx_id", "customer_trx_line_id"),)


class SclHierarchyMaster(models.Model):
    """Scl hierarchy master model class."""

    zone_scl = models.CharField(
        db_column="ZONE_SCL", max_length=100, blank=True, null=True
    )
    state_scl = models.CharField(
        db_column="STATE_SCL", max_length=100, blank=True, null=True
    )
    region_scl = models.CharField(
        db_column="REGION_SCL", max_length=100, blank=True, null=True
    )
    district_scl = models.CharField(
        db_column="DISTRICT_SCL", max_length=100, blank=True, null=True
    )
    taluka_scl = models.CharField(
        db_column="TALUKA_SCL", max_length=100, blank=True, null=True
    )
    erp_city_scl = models.CharField(
        db_column="ERP_CITY_SCL", max_length=100, blank=True, null=True
    )
    city_id_erp = models.BigIntegerField(db_column="CITY_ID_ERP", blank=True, null=True)
    city_erp = models.CharField(
        db_column="CITY_ERP", max_length=100, blank=True, null=True
    )
    state_erp = models.CharField(
        db_column="STATE_ERP", max_length=100, blank=True, null=True
    )
    district_erp = models.CharField(
        db_column="DISTRICT_ERP", max_length=100, blank=True, null=True
    )
    taluka_erp = models.CharField(
        db_column="TALUKA_ERP", max_length=100, blank=True, null=True
    )
    id = models.BigIntegerField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "SCL_HIERARCHY_MASTER"


class NshNonTradeSales(models.Model):
    id = models.BigIntegerField(db_column="ID", blank=True, primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    cp_account_id = models.DecimalField(
        db_column="CP_ACCOUNT_ID",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
    )
    cp_account_number = models.CharField(
        db_column="CP_ACCOUNT_NUMBER", max_length=30, blank=True, null=True
    )
    p_account_key = models.TextField(db_column="P_ACCOUNT_KEY", blank=True, null=True)
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    channel_partner_name = models.CharField(
        db_column="CHANNEL_PARTNER_NAME", max_length=240, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    order_classification = models.CharField(
        db_column="ORDER_CLASSIFICATION", max_length=50, blank=True, null=True
    )
    party_type = models.CharField(
        db_column="PARTY_TYPE", max_length=240, blank=True, null=True
    )
    field_officer_name = models.CharField(
        db_column="FIELD_OFFICER_NAME", max_length=10, blank=True, null=True
    )
    status = models.TextField(db_column="STATUS", blank=True, null=True)
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    product_category = models.TextField(
        db_column="PRODUCT_CATEGORY", blank=True, null=True
    )
    volume_sales_mt = models.DecimalField(
        db_column="VOLUME_SALES_MT",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
    )
    invoice_date = models.DateTimeField(db_column="INVOICE_DATE", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "NSH_NON_TRADE_SALES"


class DimPeriod(models.Model):
    """Dim period model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    month = models.DecimalField(
        db_column="MONTH", max_digits=20, decimal_places=2, blank=True, null=True
    )
    month_name = models.TextField(db_column="MONTH_NAME", blank=True, null=True)
    quarter = models.DecimalField(
        db_column="QUARTER", max_digits=20, decimal_places=2, blank=True, null=True
    )
    year = models.DecimalField(
        db_column="YEAR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_update_login = models.IntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DIM_PERIOD"


class DimAccountType(models.Model):
    id = models.BigIntegerField(db_column="ID", primary_key=True)
    acct_type_code = models.CharField(
        db_column="ACCT_TYPE_CODE", max_length=10, blank=True, null=True
    )
    account_name = models.CharField(
        db_column="ACCOUNT_NAME", max_length=100, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "DIM_ACCOUNT_TYPE"


class FactNtSalesPlanning(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=250, blank=True, null=True)
    monthly_qty = models.DecimalField(
        db_column="MONTHLY_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    monthly_ncr_target = models.DecimalField(
        db_column="MONTHLY_NCR_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=240)
    packaging = models.CharField(db_column="PACKAGING", max_length=240)
    account_key = models.BigIntegerField(db_column="ACCOUNT_KEY", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=250, blank=True, null=True
    )
    new_customer_no_target = models.DecimalField(
        db_column="NEW_CUSTOMER_NO_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    new_customer_volume_target = models.DecimalField(
        db_column="NEW_CUSTOMER_VOLUME_TARGET",
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
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    month = models.TextField(db_column="MONTH", blank=True, null=True)
    quarterly_sales_plan_month1 = models.TextField(
        db_column="QUARTERLY_SALES_PLAN_MONTH1", blank=True, null=True
    )
    quarterly_sales_plan_month2 = models.TextField(
        db_column="QUARTERLY_SALES_PLAN_MONTH2", blank=True, null=True
    )
    quarterly_sales_plan_month3 = models.TextField(
        db_column="QUARTERLY_SALES_PLAN_MONTH3", blank=True, null=True
    )
    monthly_contri_target = models.TextField(
        db_column="MONTHLY_CONTRI_TARGET", blank=True, null=True
    )
    resource = models.BigIntegerField(db_column="RESOURCE", blank=True, null=True)
    yearly_sales_plan = models.DecimalField(
        db_column="YEARLY_SALES_PLAN",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    period_key = models.ForeignKey(
        DimPeriod, on_delete=models.CASCADE, db_column="PERIOD_KEY"
    )
    so_key = models.BigIntegerField(db_column="SO_KEY", blank=True, null=True)
    quarterly_sales_plan = models.DecimalField(
        db_column="QUARTERLY_SALES_PLAN",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    monthly_sales_target = models.DecimalField(
        db_column="MONTHLY_SALES_TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    kam_key = models.CharField(
        db_column="KAM_KEY", max_length=100, blank=True, null=True
    )
    new_customer_target = models.CharField(
        db_column="NEW_CUSTOMER_TARGET", max_length=100, blank=True, null=True
    )
    new_customer_sale_percent = models.CharField(
        db_column="NEW_CUSTOMER_SALE_PERCENT", max_length=100, blank=True, null=True
    )
    action_field = models.CharField(
        db_column="ACTION_BY", max_length=100, blank=True, null=True
    )

    action_date = models.DateField(db_column="ACTION_DATE", blank=True, null=True)
    action_remark = models.CharField(
        db_column="ACTION_REMARK", max_length=100, blank=True, null=True
    )
    action_status = models.CharField(
        db_column="ACTION_STATUS", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "FACT_NT_SALES_PLANNING"


class DimCustomersTest(models.Model):
    """Customers details model class."""

    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=15, decimal_places=0, blank=True, null=True
    )
    party_name = models.CharField(
        db_column="PARTY_NAME", max_length=360, blank=True, null=True
    )
    category_code = models.CharField(
        db_column="CATEGORY_CODE", max_length=300, blank=True, null=True
    )
    cust_account_id = models.DecimalField(
        db_column="CUST_ACCOUNT_ID", max_digits=15, decimal_places=0
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
    id = models.AutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "DIM_CUSTOMERS_TEST"


class NtCreditLimit(models.Model):
    """Credit limit non-trade model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    credit_limit_id = models.BigIntegerField(db_column="CREDIT_LIMIT_ID")
    cust = models.OneToOneField(
        DimCustomersTest,
        models.DO_NOTHING,
        related_name="credit_limits",
        db_column="CUST_ID",
    )
    account_number = models.CharField(db_column="ACCOUNT_NUMBER", max_length=50)
    comment = models.CharField(db_column="COMMENT", max_length=250)
    credit_limit = models.DecimalField(
        db_column="CREDIT_LIMIT", max_digits=20, decimal_places=2
    )
    status = models.BooleanField(db_column="STATUS", default=True)
    reason_for_escalation = models.CharField(
        db_column="REASON_FOR_ESCALATION", max_length=255, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NT_CREDIT_LIMIT"


class DimProjectDetails(models.Model):
    """Project details model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    project_name = models.CharField(db_column="PROJECT_NAME", max_length=360)
    project_description = models.CharField(
        db_column="PROJECT_DESCRIPTION", max_length=4000
    )
    approving_authority = models.CharField(
        db_column="APPROVING_AUTHORITY", max_length=360
    )
    project_location = models.CharField(
        db_column="PROJECT_LOCATION", max_length=100, blank=True, null=True
    )
    concerned_officer = models.CharField(db_column="CONCERNED_OFFICER", max_length=50)
    officer_designation = models.CharField(
        db_column="OFFICER_DESIGNATION", max_length=50
    )
    officer_contact_no = models.CharField(db_column="OFFICER_CONTACT_NO", max_length=20)
    officer_email = models.CharField(db_column="OFFICER_EMAIL", max_length=50)
    officer_address = models.CharField(
        db_column="OFFICER_ADDRESS", max_length=1000, blank=True, null=True
    )
    approval_required_by_date = models.DateField(db_column="APPROVAL_REQUIRED_BY_DATE")
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "DIM_PROJECT_DETAILS"


class FactBrandApproval(models.Model):
    """Brand approval model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    # customer_id = models.BigIntegerField(db_column="CUSTOMER_ID")
    customer_id = models.ForeignKey(
        DimCustomersTest, db_column="CUSTOMER_ID", on_delete=models.DO_NOTHING
    )
    # project_key = models.CharField(db_column="PROJECT_KEY", max_length=30)
    project_key = models.ForeignKey(
        DimProjectDetails, db_column="PROJECT_KEY", on_delete=models.DO_NOTHING
    )
    tpc_name = models.CharField(db_column="TPC_NAME", max_length=30)
    brand = models.CharField(db_column="BRAND", max_length=20)
    product = models.CharField(db_column="PRODUCT", max_length=20)
    document = models.CharField(
        db_column="DOCUMENT", max_length=250, blank=True, null=True
    )
    document_remark = models.TextField(
        db_column="DOCUMENT_REMARK", blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=1000, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=20, default="Not Assigned")
    # assignee_key = models.CharField(db_column="ASSIGNEE_KEY", max_length=20)
    assignee_key = models.ForeignKey(
        DimResources,
        db_column="ASSIGNEE_KEY",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FACT_BRAND_APPROVAL"


class NtAccRelation(models.Model):
    """NT_ACC_RELATION model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    resource = models.ForeignKey(
        DimResources, models.DO_NOTHING, db_column="RESOURCE_ID"
    )
    cust = models.ForeignKey(
        DimCustomersTest,
        models.DO_NOTHING,
        related_name="acc_relations",
        db_column="CUST_ID",
    )
    account_type = models.ForeignKey(
        DimAccountType,
        models.DO_NOTHING,
        db_column="ACCOUNT_TYPE_ID",
        blank=True,
        null=True,
    )
    effective_from = models.DateField(db_column="EFFECTIVE_FROM", auto_now_add=True)
    effective_till = models.DateField(db_column="EFFECTIVE_TILL", blank=True, null=True)
    # parent_id = models.BigIntegerField(db_column='PARENT_ID')
    # parent_id = models.ForeignKey(
    #     "self", db_column="PARENT_ID", null=True, on_delete=models.SET_NULL
    # )
    parent_id = models.CharField(
        db_column="PARENT_ID", max_length=250, null=True, blank=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=250, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NT_ACC_RELATION"


class CrmNthQuotNcrExcpAppr(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=150, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=100, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=100, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=100, blank=True, null=True
    )
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    ncr = models.CharField(db_column="NCR", max_length=100, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=150, blank=True, null=True)
    approval = models.CharField(
        db_column="APPROVAL", max_length=100, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_QUOT_NCR_EXCP_APPR"


class CrmNthSoNcrExcpAppr(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=100, blank=True, null=True
    )
    qnty_unit = models.DecimalField(
        db_column="QNTY_UNIT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    sales = models.DecimalField(
        db_column="SALES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=200, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=100, blank=True, null=True
    )
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    qtn_ncr = models.CharField(
        db_column="QTN_NCR", max_length=100, blank=True, null=True
    )
    price = models.DecimalField(
        db_column="PRICE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    what_changed = models.CharField(
        db_column="WHAT_CHANGED", max_length=150, blank=True, null=True
    )
    prev_price_freight = models.DecimalField(
        db_column="PREV_PRICE_FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    curr_price_freight = models.DecimalField(
        db_column="CURR_PRICE_FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    diff = models.DecimalField(
        db_column="DIFF", max_digits=20, decimal_places=2, blank=True, null=True
    )
    approval = models.CharField(
        db_column="APPROVAL", max_length=50, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_SO_NCR_EXCP_APPR"


class CrmNthSourceChgReq(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=100, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    order_qnty = models.DecimalField(
        db_column="ORDER_QNTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    l1_source = models.CharField(
        db_column="L1_SOURCE", max_length=200, blank=True, null=True
    )
    req_source = models.CharField(
        db_column="REQ_SOURCE", max_length=200, blank=True, null=True
    )
    fin_impl = models.CharField(
        db_column="FIN_IMPL", max_length=200, blank=True, null=True
    )
    ntso_region = models.CharField(
        db_column="NTSO_REGION", max_length=200, blank=True, null=True
    )
    approval = models.CharField(
        db_column="APPROVAL", max_length=50, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_SOURCE_CHG_REQ"


class CrmNthExtendValidity(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=50, blank=True, null=True
    )
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    tpc_name = models.CharField(
        db_column="TPC_NAME", max_length=200, blank=True, null=True
    )
    tpc_code = models.CharField(
        db_column="TPC_CODE", max_length=100, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    packing = models.CharField(
        db_column="PACKING", max_length=100, blank=True, null=True
    )
    valid_till_date = models.DateField(
        db_column="VALID_TILL_DATE", blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    location = models.CharField(
        db_column="LOCATION", max_length=100, blank=True, null=True
    )
    details = models.CharField(
        db_column="DETAILS", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_EXTEND_VALIDITY"


class CrmNthOrderCancAppr(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=100, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    order_date = models.DateField(db_column="ORDER_DATE", blank=True, null=True)
    order_number = models.CharField(
        db_column="ORDER_NUMBER", max_length=100, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=0, blank=True, null=True
    )
    unit = models.CharField(db_column="UNIT", max_length=50, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=50, blank=True, null=True
    )
    ncr = models.CharField(db_column="NCR", max_length=50, blank=True, null=True)
    delv_loct = models.CharField(
        db_column="DELV_LOCT", max_length=50, blank=True, null=True
    )
    order_status = models.CharField(
        db_column="ORDER_STATUS", max_length=50, blank=True, null=True
    )
    canc_reason = models.CharField(
        db_column="CANC_REASON", max_length=200, blank=True, null=True
    )
    approval = models.CharField(
        db_column="APPROVAL", max_length=20, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_ORDER_CANC_APPR"


class CrmNthBankGuartAppr(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=100, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=100, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    bg_amount = models.DecimalField(
        db_column="BG_AMOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    iss_bank_details = models.CharField(
        db_column="ISS_BANK_DETAILS", max_length=200, blank=True, null=True
    )
    validity = models.CharField(
        db_column="VALIDITY", max_length=100, blank=True, null=True
    )
    bg_status = models.CharField(
        db_column="BG_STATUS", max_length=50, blank=True, null=True
    )
    remark = models.CharField(db_column="REMARK", max_length=200, blank=True, null=True)
    approval = models.CharField(
        db_column="APPROVAL", max_length=20, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_BANK_GUART_APPR"


class CrmNthLeadForm(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    lead_no = models.CharField(
        db_column="LEAD_NO", max_length=50, blank=True, null=True
    )
    lead_by = models.CharField(
        db_column="LEAD_BY", max_length=50, blank=True, null=True
    )
    course_code = models.CharField(
        db_column="COURSE_CODE", max_length=50, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    business_address = models.CharField(
        db_column="BUSINESS_ADDRESS", max_length=200, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    pin_code = models.BigIntegerField(db_column="PIN_CODE", blank=True, null=True)
    project_details = models.CharField(
        db_column="PROJECT_DETAILS", max_length=200, blank=True, null=True
    )
    email = models.CharField(db_column="EMAIL", max_length=100, blank=True, null=True)
    contact_number = models.DecimalField(
        db_column="CONTACT_NUMBER",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    delv_address = models.CharField(
        db_column="DELV_ADDRESS", max_length=200, blank=True, null=True
    )
    delv_window = models.CharField(
        db_column="DELV_WINDOW", max_length=200, blank=True, null=True
    )
    assigned_to_ntso_kam = models.CharField(
        db_column="ASSIGNED_TO_NTSO_KAM", max_length=200, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=200, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_LEAD_FORM"


class CrmNthRefuReq(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=50, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=50, blank=True, null=True
    )
    last_order_details = models.CharField(
        db_column="LAST_ORDER_DETAILS", max_length=200, blank=True, null=True
    )
    view_details = models.CharField(
        db_column="VIEW_DETAILS", max_length=200, blank=True, null=True
    )
    tpc_name = models.CharField(
        db_column="TPC_NAME", max_length=200, blank=True, null=True
    )
    tpc_code = models.CharField(
        db_column="TPC_CODE", max_length=50, blank=True, null=True
    )
    location = models.CharField(
        db_column="LOCATION", max_length=50, blank=True, null=True
    )
    credit_balance = models.DecimalField(
        db_column="CREDIT_BALANCE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=200, blank=True, null=True
    )
    approval = models.CharField(
        db_column="APPROVAL", max_length=20, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_REFU_REQ"


class CrmNthCustCodeCre(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    ntso_name = models.CharField(
        db_column="NTSO_NAME", max_length=200, blank=True, null=True
    )
    ntso_code = models.CharField(
        db_column="NTSO_CODE", max_length=50, blank=True, null=True
    )
    req_date = models.DateTimeField(db_column="REQ_DATE", blank=True, null=True)
    view_details = models.CharField(
        db_column="VIEW_DETAILS", max_length=200, blank=True, null=True
    )
    tpc_name = models.CharField(
        db_column="TPC_NAME", max_length=200, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    location = models.CharField(
        db_column="LOCATION", max_length=100, blank=True, null=True
    )
    urgency = models.CharField(
        db_column="URGENCY", max_length=100, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    field_officer_name = models.CharField(
        db_column="FIELD_OFFICER_NAME", max_length=200, blank=True, null=True
    )
    gst_reg_avl = models.CharField(
        db_column="GST_REG_AVL", max_length=20, blank=True, null=True
    )
    customer_catg = models.CharField(
        db_column="CUSTOMER_CATG", max_length=50, blank=True, null=True
    )
    gst_no = models.CharField(db_column="GST_NO", max_length=50, blank=True, null=True)
    nt_category = models.CharField(
        db_column="NT_CATEGORY", max_length=20, blank=True, null=True
    )
    decl_doc = models.CharField(
        db_column="DECL_DOC", max_length=200, blank=True, null=True
    )
    pan = models.CharField(db_column="PAN", max_length=50, blank=True, null=True)
    sub_catg = models.CharField(
        db_column="SUB_CATG", max_length=50, blank=True, null=True
    )
    customer_class = models.CharField(
        db_column="CUSTOMER_CLASS", max_length=50, blank=True, null=True
    )
    month_potential = models.CharField(
        db_column="MONTH_POTENTIAL", max_length=50, blank=True, null=True
    )
    parent_child_conn = models.CharField(
        db_column="PARENT_CHILD_CONN", max_length=50, blank=True, null=True
    )
    parent_account_name = models.CharField(
        db_column="PARENT_ACCOUNT_NAME", max_length=200, blank=True, null=True
    )
    parent_account_code = models.CharField(
        db_column="PARENT_ACCOUNT_CODE", max_length=50, blank=True, null=True
    )
    credit_worthness = models.CharField(
        db_column="CREDIT_WORTHNESS", max_length=50, blank=True, null=True
    )
    order_product_req = models.CharField(
        db_column="ORDER_PRODUCT_REQ", max_length=200, blank=True, null=True
    )
    order_quantity = models.DecimalField(
        db_column="ORDER_QUANTITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_packing_type = models.CharField(
        db_column="ORDER_PACKING_TYPE", max_length=50, blank=True, null=True
    )
    order_hist_product = models.CharField(
        db_column="ORDER_HIST_PRODUCT", max_length=200, blank=True, null=True
    )
    order_hist_quantity = models.DecimalField(
        db_column="ORDER_HIST_QUANTITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_hist_rate = models.DecimalField(
        db_column="ORDER_HIST_RATE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_hist_inv_date = models.DateField(
        db_column="ORDER_HIST_INV_DATE", blank=True, null=True
    )
    order_hist_mode_paym = models.CharField(
        db_column="ORDER_HIST_MODE_PAYM", max_length=50, blank=True, null=True
    )
    billing_addr = models.CharField(
        db_column="BILLING_ADDR", max_length=200, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    pin_code = models.CharField(
        db_column="PIN_CODE", max_length=50, blank=True, null=True
    )
    payment_terms = models.CharField(
        db_column="PAYMENT_TERMS", max_length=50, blank=True, null=True
    )
    tan_number = models.CharField(
        db_column="TAN_NUMBER", max_length=50, blank=True, null=True
    )
    canc_cheque = models.CharField(
        db_column="CANC_CHEQUE", max_length=100, blank=True, null=True
    )
    shopping_poc = models.CharField(
        db_column="SHOPPING_POC", max_length=50, blank=True, null=True
    )
    contact_number = models.CharField(
        db_column="CONTACT_NUMBER", max_length=50, blank=True, null=True
    )
    email = models.CharField(db_column="EMAIL", max_length=50, blank=True, null=True)
    business_addr = models.CharField(
        db_column="BUSINESS_ADDR", max_length=200, blank=True, null=True
    )
    project_details = models.CharField(
        db_column="PROJECT_DETAILS", max_length=200, blank=True, null=True
    )
    tpc_agent_name = models.CharField(
        db_column="TPC_AGENT_NAME", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_CUST_CODE_CRE"


class FactNtSalesPlanAnnual(models.Model):
    year = models.IntegerField(db_column="YEAR")
    fact_nt_jan = models.IntegerField(db_column="FACT_NT_JAN")
    fact_nt_feb = models.IntegerField(db_column="FACT_NT_FEB")
    fact_nt_mar = models.IntegerField(db_column="FACT_NT_MAR")
    fact_nt_apr = models.IntegerField(db_column="FACT_NT_APR")
    fact_nt_may = models.IntegerField(db_column="FACT_NT_MAY")
    fact_nt_jun = models.IntegerField(db_column="FACT_NT_JUN")
    fact_nt_jul = models.IntegerField(db_column="FACT_NT_JUL")
    fact_nt_aug = models.IntegerField(db_column="FACT_NT_AUG")
    fact_nt_sep = models.IntegerField(db_column="FACT_NT_SEP")
    fact_nt_oct = models.IntegerField(db_column="FACT_NT_OCT")
    fact_nt_nov = models.IntegerField(db_column="FACT_NT_NOV")
    fact_nt_dec = models.IntegerField(db_column="FACT_NT_DEC")
    brand = models.CharField(db_column="BRAND", max_length=30)
    product = models.CharField(db_column="PRODUCT", max_length=30)
    packaging = models.CharField(db_column="PACKAGING", max_length=30)
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    resource = models.ForeignKey(
        "DimResources", models.DO_NOTHING, db_column="RESOURCE", blank=True, null=True
    )
    account_type = models.ForeignKey(
        "DimAccountType",
        models.DO_NOTHING,
        db_column="ACCOUNT_TYPE",
        blank=True,
        null=True,
    )
    plan_type = models.CharField(
        db_column="PLAN_TYPE", max_length=20, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now_add=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")
    id = models.BigAutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "FACT_NT_SALES_PLAN_ANNUAL"


class DimProductTest(models.Model):
    product_id = models.AutoField(db_column="PRODUCT_ID", primary_key=True)
    product_key = models.DecimalField(
        db_column="PRODUCT_KEY",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    description = models.CharField(
        db_column="DESCRIPTION", max_length=240, blank=True, null=True
    )
    org_id = models.DecimalField(
        db_column="ORG_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    product_category = models.TextField(
        db_column="PRODUCT_CATEGORY", blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=32, blank=True, null=True
    )
    packing_bag = models.CharField(
        db_column="PACKING_BAG", max_length=32, blank=True, null=True
    )
    sku = models.TextField(db_column="SKU", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    last_updated_by = models.IntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_update_login = models.IntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )
    product_type = models.CharField(
        db_column="PRODUCT_TYPE", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DIM_PRODUCT_TEST"


class FactNtSalesPlanningMonth(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    monthly_qty = models.DecimalField(
        db_column="MONTHLY_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    monthly_ncr_target = models.DecimalField(
        db_column="MONTHLY_NCR_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    account_key = models.BigIntegerField(db_column="ACCOUNT_KEY", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=100, blank=True, null=True
    )
    new_customer_no_target = models.DecimalField(
        db_column="NEW_CUSTOMER_NO_TARGET",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    new_customer_volume_target = models.DecimalField(
        db_column="NEW_CUSTOMER_VOLUME_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    year = models.DecimalField(
        db_column="YEAR", max_digits=4, decimal_places=0, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=50, blank=True, null=True)
    quarterly_sales_plan_month1 = models.DecimalField(
        db_column="QUARTERLY_SALES_PLAN_MONTH1",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quarterly_sales_plan_month2 = models.DecimalField(
        db_column="QUARTERLY_SALES_PLAN_MONTH2",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quarterly_sales_plan_month3 = models.DecimalField(
        db_column="QUARTERLY_SALES_PLAN_MONTH3",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    monthly_contri_target = models.DecimalField(
        db_column="MONTHLY_CONTRI_TARGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    resource = models.BigIntegerField(db_column="RESOURCE", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FACT_NT_SALES_PLANNING_MONTH"


class FactNtSalesPlanningNcr(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    year = models.IntegerField(db_column="YEAR")
    month = models.CharField(db_column="MONTH", max_length=3, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=30)
    product = models.CharField(db_column="PRODUCT", max_length=30)
    packaging = models.CharField(db_column="PACKAGING", max_length=30)
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    account_key = models.IntegerField(db_column="ACCOUNT_KEY", blank=True, null=True)
    monthly_ncr_target = models.IntegerField(db_column="MONTHLY_NCR_TARGET")
    monthly_contri_target = models.IntegerField(db_column="MONTHLY_CONTRI_TARGET")
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FACT_NT_SALES_PLANNING_NCR"


class PremiumProductsMasterTmp(models.Model):
    org_id = models.BigIntegerField(db_column="ORG_ID", blank=True, null=True)
    code = models.BigIntegerField(db_column="CODE", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    cust_cat = models.CharField(
        db_column="CUST_CAT", max_length=30, blank=True, null=True
    )
    inventory_id = models.BigIntegerField(
        db_column="INVENTORY_ID", blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    packaging_condition = models.CharField(
        db_column="PACKAGING_CONDITION", max_length=100, blank=True, null=True
    )
    bag_type = models.CharField(
        db_column="BAG_TYPE", max_length=100, blank=True, null=True
    )
    revised_name = models.CharField(
        db_column="REVISED_NAME", max_length=360, blank=True, null=True
    )
    premium = models.CharField(db_column="PREMIUM", max_length=1, blank=True, null=True)
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PREMIUM_PRODUCTS_MASTER_TMP"


class NtResourceTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    resource_name = models.CharField(
        db_column="RESOURCE NAME", max_length=540, blank=True, null=True
    )
    resource_type = models.CharField(
        db_column="RESOURCE TYPE", max_length=360, blank=True, null=True
    )
    resource_id = models.BigIntegerField(db_column="RESOURCE ID", blank=True, null=True)
    business_segment = models.CharField(
        db_column="BUSINESS SEGMENT", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    pack = models.CharField(db_column="PACK", max_length=360, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=360, blank=True, null=True
    )
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    quarter = models.CharField(
        db_column="QUARTER", max_length=360, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    non_trade_target = models.DecimalField(
        db_column="NON TRADE TARGET",
        max_digits=22,
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
        db_table = "NT_RESOURCE_TARGET"


class NtMarketTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    business_segment = models.CharField(
        db_column="BUSINESS SEGMENT", max_length=360, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    pack = models.CharField(db_column="PACK", max_length=360, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=360, blank=True, null=True
    )
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    quarter = models.CharField(
        db_column="QUARTER", max_length=360, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    non_trade_target = models.DecimalField(
        db_column="NON TRADE TARGET",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NT_MARKET_TARGET"


class MonthlyTargetSetting(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    packing = models.CharField(
        db_column="PACKING", max_length=360, blank=True, null=True
    )
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    target_type = models.CharField(
        db_column="TARGET_TYPE", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "MONTHLY_TARGET_SETTING"


class NonTradeSalesPlanningState(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_STATE"


class NonTradeSalesPlanningAccount(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    account_key = models.ForeignKey(
        DimAccountType, on_delete=models.CASCADE, db_column="ACCOUNT_KEY"
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_ACCOUNT"


class NonTradeSalesPlanningProduct(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_PRODUCT"


class NonTradeSalesPlanningDesignation(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    so_key = models.BigIntegerField(db_column="SO_KEY", blank=True, null=True)
    kam_key = models.BigIntegerField(db_column="KAM_KEY", blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_DESIGNATION"


class NonTradeSalesPlanningStateMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_STATE_MONTHLY"


class NonTradeSalesPlanningAccountMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    account_key = models.ForeignKey(
        DimAccountType, on_delete=models.CASCADE, db_column="ACCOUNT_KEY"
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_ACCOUNT_MONTHLY"


class NonTradeSalesPlanningProductMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_PRODUCT_MONTHLY"


class NonTradeSalesPlanningDesignationMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    so_key = models.BigIntegerField(db_column="SO_KEY", blank=True, null=True)
    kam_key = models.BigIntegerField(db_column="KAM_KEY", blank=True, null=True)
    month = models.IntegerField(db_column="MONTH", blank=True, null=True)
    year = models.IntegerField(db_column="YEAR", blank=True, null=True)
    target = models.BigIntegerField(db_column="TARGET", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    type = models.CharField(db_column="TYPE", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_DESIGNATION_MONTHLY"


class NonTradeTopDownMonthlyTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    ntso_or_kam = models.BigIntegerField(db_column="NTSO_OR_KAM", blank=True, null=True)
    ntso_or_kam_type = models.CharField(
        db_column="NTSO_OR_KAM_TYPE", max_length=360, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    account_type = models.ForeignKey(
        DimAccountType,
        on_delete=models.CASCADE,
        db_column="ACCOUNT_TYPE",
        blank=True,
        null=True,
    )
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    target = models.DecimalField(
        db_column="TARGET", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NON_TRADE_TOP_DOWN_MONTHLY_TARGET"


class NonTradeSalesPlanningMonthlyNcrTarget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=360, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    target = models.DecimalField(
        db_column="TARGET", max_digits=22, decimal_places=2, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=200, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NON_TRADE_SALES_PLANNING_MONTHLY_NCR_TARGET"


class TpcCustomerMapping(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    tpc_code = models.BigIntegerField(db_column="TPC_CODE", blank=True, null=True)
    tpc_name = models.CharField(
        db_column="TPC_NAME", max_length=540, blank=True, null=True
    )
    customer_code = models.BigIntegerField(
        db_column="CUSTOMER_CODE", blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "TPC_CUSTOMER_MAPPING"


class TgtOrderDataAp(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=360, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=540, blank=True, null=True
    )
    cust_categ = models.CharField(
        db_column="CUST_CATEG", max_length=360, blank=True, null=True
    )
    cust_sub_categ = models.CharField(
        db_column="CUST_SUB_CATEG", max_length=360, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=360, blank=True, null=True
    )
    so_name = models.CharField(
        db_column="SO_NAME", max_length=540, blank=True, null=True
    )
    order_number = models.BigIntegerField(
        db_column="ORDER_NUMBER", blank=True, null=True
    )
    header_id = models.BigIntegerField(db_column="HEADER_ID", blank=True, null=True)
    line_id = models.BigIntegerField(db_column="LINE_ID", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    context = models.CharField(
        db_column="CONTEXT", max_length=360, blank=True, null=True
    )
    organization_id = models.BigIntegerField(
        db_column="ORGANIZATION_ID", blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=360, blank=True, null=True)
    shipped_quantity = models.DecimalField(
        db_column="SHIPPED_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ordered_quantity = models.DecimalField(
        db_column="ORDERED_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_quantity_uom = models.CharField(
        db_column="ORDER_QUANTITY_UOM", max_length=360, blank=True, null=True
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=540, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=540, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=540, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    unit_selling_price = models.DecimalField(
        db_column="UNIT_SELLING_PRICE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    flow_status_code = models.CharField(
        db_column="FLOW_STATUS_CODE", max_length=540, blank=True, null=True
    )
    ordered_date = models.DateTimeField(db_column="ORDERED_DATE", blank=True, null=True)
    dispatched_date = models.DateTimeField(
        db_column="DISPATCHED_DATE", blank=True, null=True
    )
    expiry_date = models.DateTimeField(db_column="EXPIRY_DATE", blank=True, null=True)
    promise_date = models.DateTimeField(db_column="PROMISE_DATE", blank=True, null=True)
    schedule_ship_date = models.DateTimeField(
        db_column="SCHEDULE_SHIP_DATE", blank=True, null=True
    )
    actual_shipment_date = models.DateTimeField(
        db_column="ACTUAL_SHIPMENT_DATE", blank=True, null=True
    )
    fulfillment_date = models.DateTimeField(
        db_column="FULFILLMENT_DATE", blank=True, null=True
    )
    actual_fulfillment_date = models.DateTimeField(
        db_column="ACTUAL_FULFILLMENT_DATE", blank=True, null=True
    )
    di_so = models.CharField(db_column="DI_SO", max_length=360, blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=360, blank=True, null=True)
    whse_code = models.CharField(
        db_column="WHSE_CODE", max_length=360, blank=True, null=True
    )
    order_status = models.CharField(
        db_column="ORDER_STATUS", max_length=360, blank=True, null=True
    )
    org_id = models.IntegerField(db_column="ORG_ID", blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=360, blank=True, null=True
    )
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    booked_date = models.DateTimeField(db_column="BOOKED_DATE", blank=True, null=True)
    invoiced_quantity = models.DecimalField(
        db_column="INVOICED_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    mm_name = models.CharField(
        db_column="MM_NAME", max_length=540, blank=True, null=True
    )
    mm_comm = models.BigIntegerField(db_column="MM_COMM", blank=True, null=True)
    delivery_id = models.BigIntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    mm_code = models.BigIntegerField(db_column="MM_CODE", blank=True, null=True)
    city_id = models.BigIntegerField(db_column="CITY_ID", blank=True, null=True)
    cancelled_quantity = models.DecimalField(
        db_column="CANCELLED_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "TGT_ORDER_DATA_AP"
