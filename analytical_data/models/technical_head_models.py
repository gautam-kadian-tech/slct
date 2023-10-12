from django.db import models


class CrmMaterialtestCertificate(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant_name = models.CharField(db_column="PLANT_NAME", max_length=200)
    from_date = models.DateField(db_column="FROM_DATE")
    end_date = models.DateField(db_column="END_DATE")
    grade = models.CharField(db_column="GRADE", max_length=200)
    upload_doc = models.FileField(
        db_column="UPLOAD_DOC", upload_to="static\media", blank=True, null=True
    )
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    brand = models.CharField(db_column="BRAND", max_length=200, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_MATERIAL_TEST_CERTIFICATE"


class CrmAnnualSiteConvPlan(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=150, blank=True, null=True)
    plan = models.CharField(db_column="PLAN", max_length=5, blank=True, null=True)
    plan_year = models.IntegerField(db_column="PLAN_YEAR", blank=True, null=True)
    target_jan = models.DecimalField(
        db_column="TARGET_JAN_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_feb = models.DecimalField(
        db_column="TARGET_FEB_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_mar = models.DecimalField(
        db_column="TARGET_MAR_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_apr = models.DecimalField(
        db_column="TARGET_APR_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_may = models.DecimalField(
        db_column="TARGET_MAY_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_jun = models.DecimalField(
        db_column="TARGET_JUN_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_jul = models.DecimalField(
        db_column="TARGET_JUL_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_aug = models.DecimalField(
        db_column="TARGET_AUG_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_sep = models.DecimalField(
        db_column="TARGET_SEP_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_oct = models.DecimalField(
        db_column="TARGET_OCT_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_nov = models.DecimalField(
        db_column="TARGET_NOV_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    target_dec = models.DecimalField(
        db_column="TARGET_DEC_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )

    volume_gen_jan = models.DecimalField(
        db_column="VOLUME_GEN_JAN_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_feb = models.DecimalField(
        db_column="VOLUME_GEN_FEB_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_mar = models.DecimalField(
        db_column="VOLUME_GEN_MAR_NXT_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_apr = models.DecimalField(
        db_column="VOLUME_GEN_APR_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_may = models.DecimalField(
        db_column="VOLUME_GEN_MAY_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_jun = models.DecimalField(
        db_column="VOLUME_GEN_JUN_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_jul = models.DecimalField(
        db_column="VOLUME_GEN_JULY_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_aug = models.DecimalField(
        db_column="VOLUME_GEN_AUG_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_sep = models.DecimalField(
        db_column="VOLUME_GEN_SEP_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_oct = models.DecimalField(
        db_column="VOLUME_GEN_OCT_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_nov = models.DecimalField(
        db_column="VOLUME_GEN_NOV_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    volume_gen_dec = models.DecimalField(
        db_column="VOLUME_GEN_DEC_CUR_YR",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_ANNUAL_SITE_CONV_PLAN"


class CrmNthProductApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    so_name = models.CharField(
        db_column="SO_NAME", max_length=150, blank=True, null=True
    )
    project_code = models.CharField(
        db_column="PROJECT_CODE", max_length=50, blank=True, null=True
    )
    project_name = models.CharField(
        db_column="PROJECT_NAME", max_length=150, blank=True, null=True
    )
    approval_date = models.DateField(db_column="APPROVAL_DATE", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=100, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    approval_auth = models.CharField(
        db_column="APPROVAL_AUTH", max_length=100, blank=True, null=True
    )
    designation = models.CharField(
        db_column="DESIGNATION", max_length=100, blank=True, null=True
    )
    phone_no = models.CharField(
        db_column="PHONE_NO", max_length=30, blank=True, null=True
    )
    email = models.CharField(db_column="EMAIL", max_length=100, blank=True, null=True)
    approval_status = models.CharField(
        db_column="APPROVAL_STATUS", max_length=30, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_NTH_PRODUCT_APPROVAL"


class CrmNthActivityPlan(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    service = models.CharField(
        db_column="SERVICE", max_length=50, blank=True, null=True
    )
    service_test = models.CharField(
        db_column="SERVICE_TEST", max_length=50, blank=True, null=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    service_sub_test = models.CharField(
        db_column="SERVICE_SUB_TEST", max_length=50, blank=True, null=True
    )
    plan = models.CharField(db_column="PLAN", max_length=1, blank=True, null=True)
    plan_year = models.IntegerField(db_column="PLAN_YEAR", blank=True, null=True)
    manual_chg_jan = models.DecimalField(
        db_column="MANUAL_CHG_JAN",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_feb = models.DecimalField(
        db_column="MANUAL_CHG_FEB",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_mar = models.DecimalField(
        db_column="MANUAL_CHG_MAR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_apr = models.DecimalField(
        db_column="MANUAL_CHG_APR",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_may = models.DecimalField(
        db_column="MANUAL_CHG_MAY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_jun = models.DecimalField(
        db_column="MANUAL_CHG_JUN",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_jul = models.DecimalField(
        db_column="MANUAL_CHG_JUL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_aug = models.DecimalField(
        db_column="MANUAL_CHG_AUG",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_sep = models.DecimalField(
        db_column="MANUAL_CHG_SEP",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_oct = models.DecimalField(
        db_column="MANUAL_CHG_OCT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_nov = models.DecimalField(
        db_column="MANUAL_CHG_NOV",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    manual_chg_dec = models.DecimalField(
        db_column="MANUAL_CHG_DEC",
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
        db_table = "CRM_NTH_ACTIVITY_PLAN"


class CrmMabRateList(models.Model):
    """Rate list model class."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    media = models.CharField(db_column="MEDIA", max_length=100, blank=True, null=True)
    wall_shop_paint = models.DecimalField(
        db_column="WALL_SHOP_PAINT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    impact_paint = models.DecimalField(
        db_column="IMPACT_PAINT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    glow_sign_board = models.DecimalField(
        db_column="GLOW_SIGN_BOARD",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    in_shop_brd_one_way = models.DecimalField(
        db_column="IN_SHOP_BRD_ONE_WAY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    in_shop_brd_snb_vinyl = models.DecimalField(
        db_column="IN_SHOP_BRD_SNB_VINYL",
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
        db_table = "CRM_MAB_RATE_LIST"


class NthBudgetPlan(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
    )
    service = models.CharField(
        db_column="SERVICE", max_length=540, blank=True, null=True
    )
    sub_service = models.CharField(
        db_column="SUB_SERVICE", max_length=540, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=540, blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    activity_plan = models.BigIntegerField(
        db_column="ACTIVITY_PLAN", blank=True, null=True
    )
    budget = models.DecimalField(
        db_column="BUDGET", max_digits=22, decimal_places=0, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NTH_BUDGET_PLAN"


class CrmAnnualSiteConvPlanMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    site_conversion = models.BigIntegerField(
        db_column="SITE_CONVERSION", blank=True, null=True
    )
    volume_generated = models.BigIntegerField(
        db_column="VOLUME_GENERATED", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CRM_ANNUAL_SITE_CONV_PLAN_MONTHLY"


class NthBudgetPlanMonthly(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    service = models.CharField(
        db_column="SERVICE", max_length=360, blank=True, null=True
    )
    sub_service = models.CharField(
        db_column="SUB_SERVICE", max_length=360, blank=True, null=True
    )
    activity_plan = models.BigIntegerField(
        db_column="ACTIVITY_PLAN", blank=True, null=True
    )
    budget = models.BigIntegerField(db_column="BUDGET", blank=True, null=True)
    year = models.BigIntegerField(db_column="YEAR", blank=True, null=True)
    month = models.CharField(db_column="MONTH", max_length=360, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NTH_BUDGET_PLAN_MONTHLY"
