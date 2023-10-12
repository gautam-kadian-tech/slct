from django.db import models


class SclCaseStudy(models.Model):
    "Scl CaseStudy data."

    id = models.BigAutoField(db_column="ID", primary_key=True)
    case_subject = models.CharField(
        db_column="CASE_SUBJECT", max_length=500, blank=True, null=True
    )
    origin_state = models.CharField(
        db_column="ORIGIN_STATE", max_length=200, blank=True, null=True
    )
    case_date = models.DateTimeField(db_column="CASE_DATE", blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=4000, blank=True, null=True
    )
    external_persons = models.CharField(
        db_column="EXTERNAL_PERSONS", max_length=500, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )
    related_doc = models.FileField(
        db_column="RELATED_DOC", upload_to="static\media", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SCL_CASE_STUDY"


class SclCaseObjects(models.Model):
    "Scl Case Objects data."

    id = models.BigAutoField(db_column="ID", primary_key=True)
    case = models.ForeignKey(
        "SclCaseStudy", models.DO_NOTHING, db_column="CASE_ID", blank=True, null=True
    )
    object_type = models.CharField(
        db_column="OBJECT_TYPE", max_length=25, blank=True, null=True
    )
    object_details = models.BinaryField(
        db_column="OBJECT_DETAILS", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SCL_CASE_OBJECTS"


class InternalCaseResources(models.Model):
    "Internal Case Resources data."

    id = models.BigAutoField(db_column="ID", primary_key=True)
    case = models.ForeignKey(
        "SclCaseStudy", models.DO_NOTHING, db_column="CASE_ID", blank=True, null=True
    )
    resource_id = models.BigIntegerField(db_column="RESOURCE_ID", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "INTERNAL_CASE_RESOURCES"


class IntendedAudienceStates(models.Model):
    "Intended Audience States Model"

    id = models.BigAutoField(db_column="ID", primary_key=True)
    case = models.ForeignKey(
        "SclCaseStudy", models.DO_NOTHING, db_column="CASE_ID", blank=True, null=True
    )
    state_code = models.CharField(
        db_column="STATE_CODE", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", blank=True, null=True)
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", blank=True, null=True
    )
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "INTENDED_AUDIENCE_STATES"


class CrmInflAssistReq(models.Model):
    "Crm Infl AssitReq Model"

    id = models.BigAutoField(db_column="ID", primary_key=True)
    ticket_id = models.BigIntegerField(db_column="TICKET_ID", blank=True, null=True)
    influencer_code = models.CharField(
        db_column="INFLUENCER_CODE", max_length=30, blank=True, null=True
    )
    influencer_name = models.CharField(
        db_column="INFLUENCER_NAME", max_length=250, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=150, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=150, blank=True, null=True
    )
    subject = models.CharField(
        db_column="SUBJECT", max_length=150, blank=True, null=True
    )
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    taluka = models.CharField(db_column="TALUKA", max_length=150, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        max_length=360,
        upload_to=r"static\media\influencer_manager\assist_request",
        blank=True,
        null=True,
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_INFL_ASSIST_REQ"


class CrmInflChgReq(models.Model):
    "Crm Infl change req model"

    id = models.BigAutoField(db_column="ID", primary_key=True)
    ticket_id = models.BigIntegerField(db_column="TICKET_ID")
    influencer_code = models.CharField(
        db_column="INFLUENCER_CODE", max_length=30, blank=True, null=True
    )
    influencer_name = models.CharField(
        db_column="INFLUENCER_NAME", max_length=250, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=150, blank=True, null=True
    )
    type_of_change = models.CharField(
        db_column="TYPE_OF_CHANGE", max_length=100, blank=True, null=True
    )
    request_date = models.DateField(db_column="REQUEST_DATE", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    sales_officer_name = models.CharField(
        db_column="SALES_OFFICER_NAME", max_length=100, blank=True, null=True
    )
    previous_details = models.CharField(
        db_column="PREVIOUS_DETAILS", max_length=100, blank=True, null=True
    )
    new_details = models.CharField(
        db_column="NEW_DETAILS", max_length=100, blank=True, null=True
    )
    reason_for_change = models.CharField(
        db_column="REASON_FOR_CHANGE", max_length=100, blank=True, null=True
    )
    sales_officer_mno = models.CharField(
        db_column="SALES_OFFICER_MNO", max_length=100, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=100, blank=True, null=True
    )
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        max_length=360,
        upload_to=r"static\media\influencer_manager\change_requset",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "CRM_INFL_CHG_REQ"


class CrmInflMgrMeetPlan(models.Model):
    "Crm Infl Mgr Meet Plan Model"

    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=100, blank=True, null=True
    )
    plan = models.CharField(db_column="PLAN", max_length=100, blank=True, null=True)
    plan_year = models.DecimalField(
        db_column="PLAN_YEAR", max_digits=4, decimal_places=0, blank=True, null=True
    )
    budget_jan = models.DecimalField(
        db_column="BUDGET_JAN", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_feb = models.DecimalField(
        db_column="BUDGET_FEB", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_mar = models.DecimalField(
        db_column="BUDGET_MAR", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_apr = models.DecimalField(
        db_column="BUDGET_APR", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_may = models.DecimalField(
        db_column="BUDGET_MAY", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_jun = models.DecimalField(
        db_column="BUDGET_JUN", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_jul = models.DecimalField(
        db_column="BUDGET_JUL", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_aug = models.DecimalField(
        db_column="BUDGET_AUG", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_sep = models.DecimalField(
        db_column="BUDGET_SEP", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_oct = models.DecimalField(
        db_column="BUDGET_OCT", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_nov = models.DecimalField(
        db_column="BUDGET_NOV", max_digits=20, decimal_places=0, blank=True, null=True
    )
    budget_dec = models.DecimalField(
        db_column="BUDGET_DEC", max_digits=20, decimal_places=0, blank=True, null=True
    )
    no_of_meets_jan = models.DecimalField(
        db_column="NO_OF_MEETS_JAN",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_feb = models.DecimalField(
        db_column="NO_OF_MEETS_FEB",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_mar = models.DecimalField(
        db_column="NO_OF_MEETS_MAR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_apr = models.DecimalField(
        db_column="NO_OF_MEETS_APR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_may = models.DecimalField(
        db_column="NO_OF_MEETS_MAY",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_jun = models.DecimalField(
        db_column="NO_OF_MEETS_JUN",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_jul = models.DecimalField(
        db_column="NO_OF_MEETS_JUL",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_aug = models.DecimalField(
        db_column="NO_OF_MEETS_AUG",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_sep = models.DecimalField(
        db_column="NO_OF_MEETS_SEP",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_oct = models.DecimalField(
        db_column="NO_OF_MEETS_OCT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_nov = models.DecimalField(
        db_column="NO_OF_MEETS_NOV",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    no_of_meets_dec = models.DecimalField(
        db_column="NO_OF_MEETS_DEC",
        max_digits=20,
        decimal_places=0,
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
        db_table = "CRM_INFL_MGR_MEET_PLAN"


class CrmInflMgrAnnualPlan(models.Model):
    "Crm Infl Mgr Annual Plan Model"

    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=150, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=150, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=50, blank=True, null=True
    )
    plan = models.CharField(db_column="PLAN", max_length=10, blank=True, null=True)
    plan_year = models.DecimalField(
        db_column="PLAN_YEAR", max_digits=5, decimal_places=0, blank=True, null=True
    )
    regt_plan_jan = models.DecimalField(
        db_column="REGT_PLAN_JAN",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_feb = models.DecimalField(
        db_column="REGT_PLAN_FEB",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_mar = models.DecimalField(
        db_column="REGT_PLAN_MAR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_apr = models.DecimalField(
        db_column="REGT_PLAN_APR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_may = models.DecimalField(
        db_column="REGT_PLAN_MAY",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_jun = models.DecimalField(
        db_column="REGT_PLAN_JUN",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_jul = models.DecimalField(
        db_column="REGT_PLAN_JUL",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_aug = models.DecimalField(
        db_column="REGT_PLAN_AUG",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_sep = models.DecimalField(
        db_column="REGT_PLAN_SEP",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_oct = models.DecimalField(
        db_column="REGT_PLAN_OCT",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_nov = models.DecimalField(
        db_column="REGT_PLAN_NOV",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    regt_plan_dec = models.DecimalField(
        db_column="REGT_PLAN_DEC",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_jan = models.DecimalField(
        db_column="CONT_PLAN_JAN",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_feb = models.DecimalField(
        db_column="CONT_PLAN_FEB",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_mar = models.DecimalField(
        db_column="CONT_PLAN_MAR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_apr = models.DecimalField(
        db_column="CONT_PLAN_APR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_may = models.DecimalField(
        db_column="CONT_PLAN_MAY",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_jun = models.DecimalField(
        db_column="CONT_PLAN_JUN",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_jul = models.DecimalField(
        db_column="CONT_PLAN_JUL",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_aug = models.DecimalField(
        db_column="CONT_PLAN_AUG",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_sep = models.DecimalField(
        db_column="CONT_PLAN_SEP",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_oct = models.DecimalField(
        db_column="CONT_PLAN_OCT",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_nov = models.DecimalField(
        db_column="CONT_PLAN_NOV",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cont_plan_dec = models.DecimalField(
        db_column="CONT_PLAN_DEC",
        max_digits=10,
        decimal_places=0,
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
        db_table = "CRM_INFL_MGR_ANNUAL_PLAN"


class CrmInflMgrSchemeBudget(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plan_year = models.DecimalField(
        db_column="PLAN_YEAR", max_digits=4, decimal_places=0, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=20, blank=True, null=True
    )
    budget_apr_cur_yr = models.DecimalField(
        db_column="BUDGET_APR_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_may_cur_yr = models.DecimalField(
        db_column="BUDGET_MAY_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_jun_cur_yr = models.DecimalField(
        db_column="BUDGET_JUN_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_jul_cur_yr = models.DecimalField(
        db_column="BUDGET_JUL_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_aug_cur_yr = models.DecimalField(
        db_column="BUDGET_AUG_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_sep_cur_yr = models.DecimalField(
        db_column="BUDGET_SEP_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_oct_cur_yr = models.DecimalField(
        db_column="BUDGET_OCT_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_nov_cur_yr = models.DecimalField(
        db_column="BUDGET_NOV_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_dec_cur_yr = models.DecimalField(
        db_column="BUDGET_DEC_CUR_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_jan_nxt_yr = models.DecimalField(
        db_column="BUDGET_JAN_NXT_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_feb_nxt_yr = models.DecimalField(
        db_column="BUDGET_FEB_NXT_YR",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    budget_mar_nxt_yr = models.DecimalField(
        db_column="BUDGET_MAR_NXT_YR",
        max_digits=20,
        decimal_places=0,
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
        db_table = "CRM_INFL_MGR_SCHEME_BUDGET"


class CrmInflMgrSchmBdgtActlExp(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plan_year = models.DecimalField(
        db_column="PLAN_YEAR", max_digits=4, decimal_places=0, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=3, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    actual_exp = models.DecimalField(
        db_column="ACTUAL_EXP", max_digits=20, decimal_places=0, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_MGR_SCHM_BDGT_ACTL_EXP"


class InfluencerMeetConstrainedRun(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    technical_activity_type = models.CharField(
        db_column="TECHNICAL_ACTIVITY_TYPE", max_length=360, blank=True, null=True
    )
    monthly_budget = models.DecimalField(
        db_column="MONTHLY_BUDGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    avg_attendees_per_meeting = models.DecimalField(
        db_column="AVG_ATTENDEES_PER_MEETING",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    budeget_per_head = models.DecimalField(
        db_column="BUDEGET_PER_HEAD",
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
        db_table = "INFLUENCER_MEET_CONSTRAINED_RUN"


class InfluencerOutput(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey(
        "InfluencerMeetConstrainedRun",
        models.DO_NOTHING,
        db_column="RUN_ID",
        blank=True,
        null=True,
    )
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    influencer_code = models.CharField(
        db_column="INFLUENCER_CODE", max_length=360, blank=True, null=True
    )
    influencer_name = models.CharField(
        db_column="INFLUENCER_NAME", max_length=360, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=360, blank=True, null=True
    )
    total_score = models.DecimalField(
        db_column="TOTAL_SCORE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    score_category = models.CharField(
        db_column="SCORE_CATEGORY", max_length=360, blank=True, null=True
    )
    invited = models.DecimalField(
        db_column="INVITED", max_digits=22, decimal_places=2, blank=True, null=True
    )
    meetings_invited = models.DecimalField(
        db_column="MEETINGS_INVITED",
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

    class Meta:
        managed = False
        db_table = "INFLUENCER_OUTPUT"


class InfluencerTechActivityMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    technical_activity_type = models.CharField(
        db_column="TECHNICAL_ACTIVITY_TYPE", max_length=360, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=360, blank=True, null=True
    )
    composition = models.DecimalField(
        db_column="COMPOSITION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "INFLUENCER_TECH_ACTIVITY_MASTER"


class InfluencerMeetBudgetOutput(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    technical_activity_type = models.CharField(
        db_column="TECHNICAL_ACTIVITY_TYPE", max_length=360, blank=True, null=True
    )
    total_influencers = models.BigIntegerField(
        db_column="TOTAL_INFLUENCERS", blank=True, null=True
    )
    avg_attendees_per_meeting = models.BigIntegerField(
        db_column="AVG_ATTENDEES_PER_MEETING", blank=True, null=True
    )
    min_a = models.BigIntegerField(db_column="MIN_A", blank=True, null=True)
    min_b = models.BigIntegerField(db_column="MIN_B", blank=True, null=True)
    min_c = models.BigIntegerField(db_column="MIN_C", blank=True, null=True)
    budeget_per_head = models.DecimalField(
        db_column="BUDEGET_PER_HEAD",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    concat = models.CharField(db_column="CONCAT", max_length=360, blank=True, null=True)
    a = models.BigIntegerField(db_column="A", blank=True, null=True)
    b = models.BigIntegerField(db_column="B", blank=True, null=True)
    c = models.BigIntegerField(db_column="C", blank=True, null=True)
    meetings_a = models.BigIntegerField(db_column="meetings_A", blank=True, null=True)
    meetings_b = models.BigIntegerField(db_column="meetings_B", blank=True, null=True)
    meetings_c = models.BigIntegerField(db_column="meetings_C", blank=True, null=True)
    total_meeting = models.BigIntegerField(
        db_column="TOTAL_MEETING", blank=True, null=True
    )
    no_meetings = models.BigIntegerField(db_column="NO_MEETINGS", blank=True, null=True)
    total_budget = models.DecimalField(
        db_column="TOTAL_BUDGET", max_digits=22, decimal_places=2, blank=True, null=True
    )
    attendees_per_meeting = models.BigIntegerField(
        db_column="ATTENDEES_PER_MEETING", blank=True, null=True
    )
    inactive_attendee = models.BigIntegerField(
        db_column="INACTIVE_ATTENDEE", blank=True, null=True
    )
    cat_a_attendee = models.BigIntegerField(
        db_column="CAT_A_ATTENDEE", blank=True, null=True
    )
    cat_b_attendee = models.BigIntegerField(
        db_column="CAT_B_ATTENDEE", blank=True, null=True
    )
    cat_c_attendee = models.BigIntegerField(
        db_column="CAT_C_ATTENDEE", blank=True, null=True
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
        db_table = "INFLUENCER_MEET_BUDGET_OUTPUT"


class InfluencerMeetingOutput(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    influencer_code = models.CharField(
        db_column="INFLUENCER_CODE", max_length=360, blank=True, null=True
    )
    influencer_name = models.CharField(
        db_column="INFLUENCER_NAME", max_length=360, blank=True, null=True
    )
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=360, blank=True, null=True
    )
    score_category = models.CharField(
        db_column="SCORE_CATEGORY", max_length=360, blank=True, null=True
    )
    lifting_previous_month_mt = models.DecimalField(
        db_column="LIFTING_PREVIOUS_MONTH_MT",
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
    meeting_invited = models.CharField(
        db_column="MEETING_INVITED", max_length=360, blank=True, null=True
    )
    invited = models.IntegerField(db_column="INVITED", blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    technical_activity_type = models.CharField(
        db_column="TECHNICAL_ACTIVITY_TYPE", max_length=360, blank=True, null=True
    )
    free_run = models.BooleanField(db_column="FREE_RUN", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "INFLUENCER_MEETING_OUTPUT"


class AugmentationOutputTable(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    so_code = models.DecimalField(
        db_column="SO_CODE", max_digits=50, decimal_places=10, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    geo_spread = models.DecimalField(
        db_column="GEO_SPREAD", max_digits=50, decimal_places=10, blank=True, null=True
    )
    geo_per_so = models.DecimalField(
        db_column="GEO_PER_SO", max_digits=50, decimal_places=10, blank=True, null=True
    )
    avg_geo = models.DecimalField(
        db_column="AVG_GEO", max_digits=50, decimal_places=10, blank=True, null=True
    )
    geo_rating = models.CharField(
        db_column="GEO_ RATING", max_length=50, blank=True, null=True
    )
    counter_potential = models.DecimalField(
        db_column="COUNTER_POTENTIAL",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    so_count = models.DecimalField(
        db_column="SO_COUNT", max_digits=50, decimal_places=10, blank=True, null=True
    )
    mp_per_so = models.DecimalField(
        db_column="MP_PER_SO", max_digits=50, decimal_places=10, blank=True, null=True
    )
    avg_mp = models.DecimalField(
        db_column="AVG_MP", max_digits=50, decimal_places=10, blank=True, null=True
    )
    mp_rating = models.CharField(
        db_column="MP_RATING", max_length=50, blank=True, null=True
    )
    counter_code_count = models.DecimalField(
        db_column="COUNTER_CODE_COUNT",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    counter_per_so = models.DecimalField(
        db_column="COUNTER_PER_SO",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    avg_c = models.DecimalField(
        db_column="AVG_C", max_digits=50, decimal_places=10, blank=True, null=True
    )
    counter_rating = models.CharField(
        db_column="COUNTER_RATING", max_length=50, blank=True, null=True
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)
    geo_rating_score = models.DecimalField(
        db_column="GEO_RATING_SCORE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    geo_rating_score_weightage = models.DecimalField(
        db_column="GEO_RATING_SCORE_WEIGHTAGE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    mp_rating_score = models.DecimalField(
        db_column="MP_RATING_SCORE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    mp_rating_score_weightage = models.DecimalField(
        db_column="MP_RATING_SCORE_WEIGHTAGE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    counter_rating_score = models.DecimalField(
        db_column="COUNTER_RATING_SCORE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    counter_rating_score_weightage = models.DecimalField(
        db_column="COUNTER_RATING_SCORE_WEIGHTAGE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    sum_all_rating_weightage = models.DecimalField(
        db_column="SUM_ALL_RATING_WEIGHTAGE",
        max_digits=50,
        decimal_places=10,
        blank=True,
        null=True,
    )
    remarks = models.CharField(
        db_column="REMARKS", max_length=250, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "AUGMENTATION_OUTPUT_TABLE"


class CrmInflScheme(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=540, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    start_date = models.DateField(db_column="START_DATE", blank=True, null=True)
    end_date = models.DateField(db_column="END_DATE", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_SCHEME"


class CrmInflSchemeProductPoint(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=540, blank=True, null=True
    )
    points_per_bag = models.BigIntegerField(
        db_column="POINTS_PER_BAG", blank=True, null=True
    )
    scheme = models.ForeignKey(
        "CrmInflScheme", models.DO_NOTHING, db_column="SCHEME", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_SCHEME_PRODUCT_POINT"


class CrmInflGiftMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    gift_name = models.CharField(
        db_column="GIFT_NAME", max_length=540, blank=True, null=True
    )
    amount = models.BigIntegerField(db_column="AMOUNT", blank=True, null=True)
    is_active = models.BooleanField(db_column="IS_ACTIVE", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_GIFT_MASTER"


class CrmInflGiftScheme(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=540, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    start_date = models.DateField(db_column="START_DATE", blank=True, null=True)
    end_date = models.DateField(db_column="END_DATE", blank=True, null=True)
    document = models.FileField(
        db_column="DOCUMENT",
        max_length=360,
        upload_to=r"static\media\influencer_manager\gift_scheme",
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_GIFT_SCHEME"


class CrmInflGiftSchemeItemList(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    item_id = models.BigIntegerField(db_column="ITEM_ID", blank=True, null=True)
    item_name = models.CharField(
        db_column="ITEM_NAME", max_length=540, blank=True, null=True
    )
    points_per_item = models.BigIntegerField(
        db_column="POINTS_PER_ITEM", blank=True, null=True
    )
    gift_scheme = models.ForeignKey(
        "CrmInflGiftScheme",
        models.DO_NOTHING,
        db_column="GIFT_SCHEME",
        blank=True,
        null=True,
    )
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_GIFT_SCHEME_ITEM_LIST"


class CrmInflMgrMeetPlanMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=360, blank=True, null=True
    )
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=100, blank=True, null=True)
    meet_budget = models.BigIntegerField(db_column="MEET_BUDGET", blank=True, null=True)
    no_of_meets = models.BigIntegerField(db_column="NO_OF_MEETS", blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_MGR_MEET_PLAN_MONTHLY"


class CrmInflMgrAnnualPlanMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    influencer_type = models.CharField(
        db_column="INFLUENCER_TYPE", max_length=360, blank=True, null=True
    )
    registration_plan = models.BigIntegerField(
        db_column="REGISTRATION_PLAN", blank=True, null=True
    )
    contribution_plan = models.BigIntegerField(
        db_column="CONTRIBUTION_PLAN", blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_INFL_MGR_ANNUAL_PLAN_MONTHLY"
