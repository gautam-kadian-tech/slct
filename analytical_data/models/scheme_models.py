"""Scheme influncer  models module."""
from django.db import models


class Schemes(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True, unique=True)
    scheme_name = models.CharField(
        db_column="SCHEME_NAME", max_length=200, blank=True, null=True
    )
    eff_start_date = models.DateTimeField(
        db_column="EFF_START_DATE", blank=True, null=True
    )
    eff_end_date = models.DateTimeField(db_column="EFF_END_DATE", blank=True, null=True)
    objectives = models.CharField(
        db_column="OBJECTIVES", max_length=2000, blank=True, null=True
    )
    eligibility_for_carry_forward = models.BooleanField(
        db_column="ELIGIBILITY_FOR_CARRY_FORWARD", blank=True, null=True
    )
    tentative_outflow_per_bag = models.CharField(
        db_column="TENTATIVE_OUTFLOW_PER_BAG", max_length=200, blank=True, null=True
    )
    document = models.FileField(
        db_column="DOCUMENT", upload_to="static\media", blank=True, null=True
    )
    scheme_budget = models.DecimalField(
        db_column="SCHEME_BUDGET",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
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
    redemption_start_date = models.DateField(
        db_column="REDEMPTION_START_DATE", blank=True, null=True
    )
    redemption_end_date = models.DateField(
        db_column="REDEMPTION_END_DATE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SCHEMES"


class SchemeLocation(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True, unique=True)
    scheme = models.ForeignKey(
        "Schemes",
        models.DO_NOTHING,
        db_column="SCHEME_ID",
        blank=True,
        null=True,
        related_name="locations",
    )
    state = models.CharField(db_column="STATE", max_length=200, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=200, blank=True, null=True
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
        db_table = "SCHEME_LOCATION"


class SchemeFor(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True, unique=True)
    scheme = models.ForeignKey(
        "Schemes", models.DO_NOTHING, db_column="SCHEME_ID", blank=True, null=True
    )
    scheme_for_code = models.CharField(
        db_column="SCHEME_FOR_CODE", max_length=200, blank=True, null=True
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
        db_table = "SCHEME_FOR"


class SchemeProducts(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    scheme = models.ForeignKey(
        "Schemes", models.DO_NOTHING, db_column="SCHEME_ID", blank=True, null=True
    )
    no_of_bags = models.BigIntegerField(db_column="NO_OF_BAGS", blank=True, null=True)
    # org_id = models.BigIntegerField(db_column="ORG_ID", blank=True, null=True)
    # grade = models.CharField(db_column="GRADE", max_length=240, blank=True, null=True)
    # packaging = models.CharField(
    #     db_column="PACKAGING", max_length=240, blank=True, null=True
    # )
    # bag_type = models.CharField(
    #     db_column="BAG_TYPE", max_length=360, blank=True, null=True
    # )
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
        db_table = "SCHEME_PRODUCTS"


class SchemeRewards(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True, unique=True)
    scheme = models.ForeignKey(
        "Schemes", models.DO_NOTHING, db_column="SCHEME_ID", blank=True, null=True
    )
    rewards_points = models.BigIntegerField(
        db_column="REWARDS_POINTS", blank=True, null=True
    )
    rewards = models.CharField(
        db_column="REWARDS", max_length=500, blank=True, null=True
    )
    gift = models.CharField(db_column="GIFT", max_length=50, blank=True, null=True)
    cash = models.DecimalField(
        db_column="CASH", max_digits=20, decimal_places=2, blank=True, null=True
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
        db_table = "SCHEME_REWARDS"


# National Technical Head Work
class CrmComplaints(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=150, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=150, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=240, blank=True, null=True
    )
    customer_contact = models.DecimalField(
        db_column="CUSTOMER_CONTACT",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    registered_by = models.CharField(
        db_column="REGISTERED_BY", max_length=150, blank=True, null=True
    )
    so_name = models.CharField(
        db_column="SO_NAME", max_length=150, blank=True, null=True
    )
    details = models.CharField(
        db_column="DETAILS", max_length=200, blank=True, null=True
    )
    related_doc = models.CharField(
        db_column="RELATED_DOC", max_length=200, blank=True, null=True
    )
    assign_tso = models.CharField(
        db_column="ASSIGN_TSO", max_length=100, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    taluka = models.CharField(db_column="TALUKA", max_length=500, blank=True, null=True)
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        max_length=360,
        upload_to=r"static\media\influencer_manager\scheme",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "CRM_COMPLAINTS"


class GiftMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    item_code = models.CharField(
        db_column="ITEM_CODE", max_length=240, blank=True, null=True
    )
    item_name = models.CharField(
        db_column="ITEM_NAME", max_length=360, blank=True, null=True
    )
    item_name_code_comb = models.TextField(
        db_column="ITEM_NAME_CODE_COMB", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "GIFT_MASTER"
