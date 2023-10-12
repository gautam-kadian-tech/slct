from django.db import models

from analytical_data.enum_classes import SlctApprovalStatusChoices


class CrmMabBrandingAppr(models.Model):
    """Crm Mab Branding Approval Model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    raised_by = models.CharField(
        db_column="RAISED_BY", max_length=150, blank=True, null=True
    )
    site_details = models.CharField(
        db_column="SITE_DETAILS", max_length=100, blank=True, null=True
    )
    activity_type = models.CharField(
        db_column="ACTIVITY_TYPE", max_length=100, blank=True, null=True
    )
    activity_type_cnt = models.DecimalField(
        db_column="ACTIVITY_TYPE_CNT",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    activity_type_size = models.DecimalField(
        db_column="ACTIVITY_TYPE_SIZE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    activity_type_amt = models.DecimalField(
        db_column="ACTIVITY_TYPE_AMT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    objective = models.CharField(
        db_column="OBJECTIVE", max_length=200, blank=True, null=True
    )
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    vendor_name = models.CharField(
        db_column="VENDOR_NAME", max_length=100, blank=True, null=True
    )
    budget = models.DecimalField(
        db_column="BUDGET", max_digits=20, decimal_places=2, blank=True, null=True
    )
    change_reason = models.CharField(
        db_column="CHANGE_REASON", max_length=200, blank=True, null=True
    )
    rejection_reason = models.CharField(
        db_column="REJECTION_REASON", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    brand_req_date = models.DateField(db_column="BRAND_REQ_DATE", blank=True, null=True)
    brand_activity_photo = models.CharField(
        db_column="BRAND_ACTIVITY_PHOTO", max_length=200, blank=True, null=True
    )
    validity_period_from = models.DateField(
        db_column="VALIDITY_PERIOD_FROM", blank=True, null=True
    )
    validity_period_to = models.DateField(
        db_column="VALIDITY_PERIOD_TO", blank=True, null=True
    )
    manual_cost = models.DecimalField(
        db_column="MANUAL_COST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    system_gen_cost = models.DecimalField(
        db_column="SYSTEM_GEN_COST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    upload_rev_report = models.FileField(
        db_column="UPLOAD_REV_REPORT", upload_to="static\media", blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "CRM_MAB_BRANDING_APPR"


class CrmMabBtlPlanning(models.Model):
    """Crm Mab Bt Planning model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    branding_activity = models.CharField(
        db_column="BRANDING_ACTIVITY", max_length=100, blank=True, null=True
    )
    branding_budget_last_year = models.DecimalField(
        db_column="BRANDING_BUDGET_LAST_YEAR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    branding_expense_last_year = models.DecimalField(
        db_column="BRANDING_EXPENSE_LAST_YEAR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    branding_budget_curr_year = models.DecimalField(
        db_column="BRANDING_BUDGET_CURR_YEAR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    recommend_matrix = models.CharField(
        db_column="RECOMMEND_MATRIX", max_length=200, blank=True, null=True
    )
    activities_count = models.DecimalField(
        db_column="ACTIVITIES_COUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="STATUS",
        max_length=360,
        default=SlctApprovalStatusChoices.PENDING.value,
        choices=SlctApprovalStatusChoices.choices,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_MAB_BTL_PLANNING"


class CrmMabPastRequisitions(models.Model):
    "Crm Mab Past Requisitions Model"
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    raised_by = models.CharField(
        db_column="RAISED_BY", max_length=100, blank=True, null=True
    )
    site_details = models.CharField(
        db_column="SITE_DETAILS", max_length=100, blank=True, null=True
    )
    activity_type = models.CharField(
        db_column="ACTIVITY_TYPE", max_length=100, blank=True, null=True
    )
    objective = models.CharField(
        db_column="OBJECTIVE", max_length=200, blank=True, null=True
    )
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    vendor_name = models.CharField(
        db_column="VENDOR_NAME", max_length=100, blank=True, null=True
    )
    po_number = models.CharField(
        db_column="PO_NUMBER", max_length=100, blank=True, null=True
    )
    req_number = models.CharField(
        db_column="REQ_NUMBER", max_length=100, blank=True, null=True
    )
    mat_qual_rating = models.DecimalField(
        db_column="MAT_QUAL_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    comp_time_rating = models.DecimalField(
        db_column="COMP_TIME_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    long_dist_visib = models.CharField(
        db_column="LONG_DIST_VISIB", max_length=100, blank=True, null=True
    )
    head_on = models.CharField(
        db_column="HEAD_ON", max_length=100, blank=True, null=True
    )
    format_size = models.CharField(
        db_column="FORMAT_SIZE", max_length=100, blank=True, null=True
    )
    landmark_value = models.CharField(
        db_column="LANDMARK_VALUE", max_length=100, blank=True, null=True
    )
    people_visib = models.CharField(
        db_column="PEOPLE_VISIB", max_length=100, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=100, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    vendor_contact_no = models.CharField(
        db_column="VENDOR_CONTACT_NO", max_length=50, blank=True, null=True
    )
    timely_comp_rating = models.DecimalField(
        db_column="TIMELY_COMP_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    quality_work_rating = models.DecimalField(
        db_column="QUALITY_WORK_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    overall_rating = models.DecimalField(
        db_column="OVERALL_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    experience_rating = models.DecimalField(
        db_column="EXPERIENCE_RATING",
        max_digits=4,
        decimal_places=0,
        blank=True,
        null=True,
    )
    start_date = models.DateField(db_column="START_DATE", blank=True, null=True)
    completion_date = models.DateField(
        db_column="COMPLETION_DATE", blank=True, null=True
    )
    add_comments = models.CharField(
        db_column="ADD_COMMENTS", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "CRM_MAB_PAST_REQUISITIONS"


class CrmMabInitReq(models.Model):
    """Crm Mab Init Req Model"""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    rasing_request_date = models.DateField(
        db_column="RASING_REQUEST_DATE", blank=True, null=True
    )
    photo_before_brand = models.FileField(
        db_column="PHOTO_BEFORE_BRAND", upload_to="static\media", blank=True, null=True
    )
    validity_period_from = models.DateField(
        db_column="VALIDITY_PERIOD_FROM", blank=True, null=True
    )
    validity_period_to = models.DateField(
        db_column="VALIDITY_PERIOD_TO", blank=True, null=True
    )
    vendor = models.CharField(db_column="VENDOR", max_length=200, blank=True, null=True)
    annual_budget_util = models.DecimalField(
        db_column="ANNUAL_BUDGET_UTIL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    balance_budget = models.DecimalField(
        db_column="BALANCE_BUDGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_cost = models.DecimalField(
        db_column="MANUAL_COST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    system_gen_cost = models.DecimalField(
        db_column="SYSTEM_GEN_COST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    upload_doc = models.FileField(
        db_column="UPLOAD_DOC", upload_to="static\media", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    branding_activity = models.ForeignKey(
        "BrandingActivity",
        models.DO_NOTHING,
        db_column="BRANDING_ACTIVITY",
        blank=True,
        null=True,
    )
    additional_comment = models.TextField(
        db_column="ADDITIONAL_COMMENT", blank=True, null=True
    )
    photo_after_brand = models.CharField(
        db_column="PHOTO_AFTER_BRAND", max_length=200, blank=True, null=True
    )
    objective_actual = models.CharField(
        db_column="OBJECTIVE_ACTUAL", max_length=200, blank=True, null=True
    )
    comment_by_lbt = models.CharField(
        db_column="COMMENT_BY_LBT", max_length=360, blank=True, null=True
    )
    comment_by_cbt = models.CharField(
        db_column="COMMENT_BY_CBT", max_length=360, blank=True, null=True
    )
    comment_by_nsh = models.CharField(
        db_column="COMMENT_BY_NSH", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_MAB_INIT_REQ"


class VendorDetailMaster(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    city_id = models.DecimalField(
        db_column="CITY_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    city = models.CharField(db_column="CITY", max_length=50, blank=True, null=True)
    vendor_name = models.CharField(
        db_column="VENDOR NAME", max_length=50, blank=True, null=True
    )
    vendor_code = models.DecimalField(
        db_column="VENDOR CODE",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    category = models.CharField(
        db_column="CATEGORY", max_length=50, blank=True, null=True
    )
    no_of_previous_engagements = models.DecimalField(
        db_column="NO. OF PREVIOUS ENGAGEMENTS",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    type_of_work = models.CharField(
        db_column="TYPE OF WORK", max_length=50, blank=True, null=True
    )
    email_id = models.CharField(
        db_column="EMAIL ID", max_length=50, blank=True, null=True
    )
    contact_number = models.DecimalField(
        db_column="CONTACT NUMBER",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    overall_rating = models.DecimalField(
        db_column="OVERALL RATING",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    quality_rating = models.DecimalField(
        db_column="QUALITY RATING",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "VENDOR_DETAIL_MASTER"


class TNmOmxMaterialTransactionsV(models.Model):
    transaction_id = models.CharField(
        db_column="TRANSACTION_ID", max_length=41, blank=True, null=True
    )
    from_party_id = models.DecimalField(
        db_column="FROM_PARTY_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    from_cust_acc_num = models.CharField(
        db_column="FROM_CUST_ACC_NUM", max_length=90, blank=True, null=True
    )
    from_party_name = models.CharField(
        db_column="FROM_PARTY_NAME", max_length=1080, blank=True, null=True
    )
    to_party_id = models.DecimalField(
        db_column="TO_PARTY_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    to_cust_acc_num = models.CharField(
        db_column="TO_CUST_ACC_NUM", max_length=90, blank=True, null=True
    )
    to_party_name = models.CharField(
        db_column="TO_PARTY_NAME", max_length=1080, blank=True, null=True
    )
    transaction_type = models.CharField(
        db_column="TRANSACTION_TYPE", max_length=2, blank=True, null=True
    )
    transaction_type_disp = models.CharField(
        db_column="TRANSACTION_TYPE_DISP", max_length=80, blank=True, null=True
    )
    transaction_date = models.DateTimeField(
        db_column="TRANSACTION_DATE", blank=True, null=True
    )
    transaction_quantity = models.DecimalField(
        db_column="TRANSACTION_QUANTITY",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    inventory_item_id = models.DecimalField(
        db_column="INVENTORY_ITEM_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    inventory_item_name = models.CharField(
        db_column="INVENTORY_ITEM_NAME", max_length=80, blank=True, null=True
    )
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=100, blank=True, null=True
    )
    org_id = models.DecimalField(
        db_column="ORG_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=15, decimal_places=0, blank=True, null=True
    )
    created_by_name = models.CharField(
        db_column="CREATED_BY_NAME", max_length=80, blank=True, null=True
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
    last_updated_by_name = models.CharField(
        db_column="LAST_UPDATED_BY_NAME", max_length=80, blank=True, null=True
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    approval_status = models.CharField(
        db_column="APPROVAL_STATUS", max_length=1, blank=True, null=True
    )
    approval_status_disp = models.CharField(
        db_column="APPROVAL_STATUS_DISP", max_length=80, blank=True, null=True
    )
    user_type = models.CharField(
        db_column="USER_TYPE", max_length=1, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=150, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    city_id = models.DecimalField(
        db_column="CITY_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    architect_involved_flag = models.CharField(
        db_column="ARCHITECT_INVOLVED_FLAG", max_length=1, blank=True, null=True
    )
    architect_id = models.DecimalField(
        db_column="ARCHITECT_ID",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    architect_name = models.CharField(
        db_column="ARCHITECT_NAME", max_length=240, blank=True, null=True
    )
    rollback_quantity = models.DecimalField(
        db_column="ROLLBACK_QUANTITY",
        max_digits=65535,
        decimal_places=65535,
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
        db_table = "T_NM_OMX_MATERIAL_TRANSACTIONS_V"


class MarketMappingBrandingBudget(models.Model):
    state = models.CharField(db_column="STATE", max_length=500, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=500, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=500, blank=True, null=True)
    tot_cost_rs_lac = models.DecimalField(
        db_column="TOT_COST_RS_LAC",
        max_digits=22,
        decimal_places=4,
        blank=True,
        null=True,
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    change_tot_cost_rs_lac = models.DecimalField(
        db_column="CHANGE_TOT_COST_RS_LAC",
        max_digits=22,
        decimal_places=4,
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_BRANDING_BUDGET"


class SponsorshipBudget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    market_mapping_branding_budget_key = models.OneToOneField(
        MarketMappingBrandingBudget,
        models.DO_NOTHING,
        db_column="MARKET_MAPPING_BRANDING_BUDGET_KEY",
        blank=True,
        null=True,
        related_name="sponsor_budget",
    )
    budget = models.DecimalField(
        db_column="BUDGET", max_digits=22, decimal_places=2, blank=True, null=True
    )
    comment_raised_by = models.TextField(
        db_column="COMMENT_RAISED_BY", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    raised_by = models.CharField(
        db_column="RAISED_BY", max_length=50, blank=True, null=True
    )
    comment_approved_by = models.TextField(
        db_column="COMMENT_APPROVED_BY", blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SPONSORSHIP_BUDGET"


class NewMarketPricingApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    price_computation_key = models.OneToOneField(
        MarketMappingBrandingBudget,
        models.DO_NOTHING,
        db_column="PRICE_COMPUTATION_KEY",
        unique=True,
        blank=True,
        null=True,
        related_name="market_pricing_approval",
    )
    price = models.IntegerField(db_column="PRICE", blank=True, null=True)
    revenue = models.DecimalField(
        db_column="REVENUE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    ebitda = models.DecimalField(
        db_column="EBITDA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NEW_MARKET_PRICING_APPROVAL"
