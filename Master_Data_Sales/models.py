import datetime

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.user_role_choices import UserRoleChoice

# from auditlog.registry import auditlog

# Create your models here.


class ZoneMappingNew(models.Model):
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
        db_column="CITY_ID", max_digits=100, decimal_places=0, blank=True, null=True
    )
    pincode = models.CharField(
        db_column="PINCODE", max_length=100, blank=True, null=True
    )
    active = models.CharField(db_column="ACTIVE", max_length=100, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    id = models.BigAutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "ZONE_MAPPING_NEW"
        verbose_name_plural = "Zone Mapping New"


class SoTalukaMappingDelhiHyd(models.Model):
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    org_id = models.IntegerField(db_column="ORG_ID", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    emp_code = models.BigIntegerField(db_column="EMP_CODE", blank=True, null=True)
    emp_name = models.CharField(
        db_column="EMP_NAME", max_length=360, blank=True, null=True
    )
    email_id = models.CharField(
        db_column="EMAIL_ID_SHREE", max_length=100, blank=True, null=True
    )
    mobile_number = models.DecimalField(
        db_column="MOBILE_NUMBER",
        max_digits=11,
        decimal_places=0,
        blank=True,
        null=True,
    )
    playstore_id = models.CharField(
        db_column="PLAYSTORE_ID", max_length=100, blank=True, null=True
    )
    ios_or_android = models.CharField(
        db_column="IOS_OR_ANDROID", max_length=100, blank=True, null=True
    )
    active = models.CharField(db_column="ACTIVE", max_length=1, blank=True, null=True)
    crm_updated = models.CharField(
        db_column="CRM_UPDATED", max_length=1, blank=True, null=True, default="N"
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", default=32)
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY", default=32)
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", default=32
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "SO_TALUKA_MAPPING_DELHI_HYD"
        verbose_name_plural = "So Taluka Mapping Delhi Hyd"


@receiver(pre_save, sender=SoTalukaMappingDelhiHyd)
def signal_so_taluka_mapping_update(sender, instance, **kwargs):
    instance.crm_updated = "N"


class ObjectiveWeightage(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    objective = models.CharField(
        db_column="OBJECTIVE", max_length=100, blank=True, null=True
    )
    parameter = models.CharField(
        db_column="PARAMETER", max_length=100, blank=True, null=True
    )
    weightage = models.DecimalField(
        db_column="WEIGHTAGE", max_digits=18, decimal_places=0, blank=True, null=True
    )
    inverse_score = models.BigIntegerField(
        db_column="INVERSE_SCORE", blank=True, null=True
    )
    created_at = models.DateField(db_column="CREATED_AT", blank=True, null=True)
    updated_at = models.DateField(db_column="UPDATED_AT", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "OBJECTIVE_WEIGHTAGE"
        verbose_name_plural = "Objective Weightage"


class PricingInputTemplateAllIndia(models.Model):
    state = models.CharField(db_column="STATE", max_length=500, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=500, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=500, blank=True, null=True)
    price_type = models.CharField(
        db_column="PRICE_TYPE", max_length=500, blank=True, null=True
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)
    price = models.DecimalField(
        db_column="PRICE", max_digits=10, decimal_places=0, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PRICING_INPUT_TEMPLATE_ALL_INDIA"
        verbose_name_plural = "Pricing Input Template All India"


class DoMasterAllIndiaData(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    email = models.CharField(db_column="EMAIL", max_length=360, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    do_emp_code = models.BigIntegerField(db_column="DO_EMP_CODE", blank=True, null=True)
    name = models.CharField(db_column="NAME", max_length=540, blank=True, null=True)
    mobile_number = models.DecimalField(
        db_column="MOBILE_NUMBER",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    active = models.CharField(db_column="ACTIVE", max_length=1, blank=True, null=True)
    crm_updated = models.CharField(
        db_column="CRM_UPDATED", max_length=1, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY", default=32)
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", default=datetime.datetime.now
    )
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY", default=32)
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", default=datetime.datetime.now
    )
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", default=32
    )

    class Meta:
        managed = False
        db_table = "DO_MASTER_ALL_INDIA_DATA"
        verbose_name_plural = "Do Master All India Data"


@receiver(pre_save, sender=DoMasterAllIndiaData)
def signal_do_master_update(sender, instance, **kwargs):
    instance.crm_updated = "N"


class TgtRlsRoleData(models.Model):
    emp_id = models.DecimalField(
        db_column="Emp_Id",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(db_column="Name", max_length=100, blank=True, null=True)
    email = models.CharField(
        db_column="Email", max_length=100, blank=True, null=True, unique=True
    )
    role = models.CharField(
        db_column="Role",
        max_length=100,
        blank=True,
        null=True,
        choices=UserRoleChoice.choices,
    )
    zone = models.CharField(db_column="Zone", max_length=100, blank=True, null=True)
    state = models.CharField(db_column="State", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    regions = models.CharField(
        db_column="REGIONS", max_length=100, blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=100, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "TGT_RLS_ROLE_DATA"
        verbose_name_plural = "Tgt Rls Role Data"


class NcrThreshold(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=540, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=540, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=540, blank=True, null=True)
    pack = models.CharField(db_column="PACK", max_length=540, blank=True, null=True)
    red_ncr_threshold = models.DecimalField(
        db_column="RED_NCR_THRESHOLD",
        max_digits=22,
        decimal_places=0,
        blank=True,
        null=True,
    )
    green_ncr_threshold = models.DecimalField(
        db_column="GREEN_NCR _THRESHOLD",
        max_digits=22,
        decimal_places=0,
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
        db_table = "NCR_THRESHOLD"


class RouteWeightage(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    parameter = models.CharField(
        db_column="PARAMETER", max_length=255, blank=True, null=True
    )
    weightage = models.IntegerField(db_column="WEIGHTAGE", blank=True, null=True)
    inverse_score = models.IntegerField(
        db_column="INVERSE_SCORE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ROUTE_WEIGHTAGE"
        verbose_name_plural = "Route Weightage"


class L1SourceMapping(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
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
        decimal_places=0,
        blank=True,
        null=True,
    )
    tlc_per_mt = models.DecimalField(
        db_column="TLC_PER_MT", max_digits=20, decimal_places=0, blank=True, null=True
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=20, decimal_places=0, blank=True, null=True
    )
    sla = models.DecimalField(
        db_column="SLA", max_digits=20, decimal_places=0, blank=True, null=True
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


class PremiumProductsMasterTmp(models.Model):
    org_id = models.BigIntegerField(
        db_column="ORG_ID", blank=True, null=True
    )  # Field name made lowercase.
    code = models.BigIntegerField(
        db_column="CODE", blank=True, null=True
    )  # Field name made lowercase.
    state = models.CharField(
        db_column="STATE", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    cust_cat = models.CharField(
        db_column="CUST_CAT", max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    inventory_id = models.BigIntegerField(
        db_column="INVENTORY_ID", blank=True, null=True
    )  # Field name made lowercase.
    grade = models.CharField(
        db_column="GRADE", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    packaging_condition = models.CharField(
        db_column="PACKAGING_CONDITION", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    bag_type = models.CharField(
        db_column="BAG_TYPE", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    revised_name = models.CharField(
        db_column="REVISED_NAME", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    premium = models.CharField(
        db_column="PREMIUM", max_length=1, blank=True, null=True
    )  # Field name made lowercase.
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    created_by = models.BigIntegerField(
        db_column="CREATED_BY"
    )  # Field name made lowercase.
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE"
    )  # Field name made lowercase.
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY"
    )  # Field name made lowercase.
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE"
    )  # Field name made lowercase.
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "PREMIUM_PRODUCTS_MASTER_TMP"


# auditlog.register(ZoneMappingNew)
# auditlog.register(SoTalukaMappingDelhiHyd)
# auditlog.register(ObjectiveWeightage)
# auditlog.register(PricingInputTemplateAllIndia)
# auditlog.register(DoMasterAllIndiaData)
# auditlog.register(TgtRlsRoleData)
# auditlog.register(NcrThreshold)
# auditlog.register(RouteWeightage)
# auditlog.register(L1SourceMapping)
# auditlog.register(PremiumProductsMasterTmp)
