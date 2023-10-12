"""Analytical data decision on negative contribution models module."""
from django.db import models


class NshContributionScenario(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=360, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=360, blank=True, null=True
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    revenue = models.DecimalField(
        db_column="REVENUE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    price = models.DecimalField(
        db_column="PRICE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    price_delta = models.DecimalField(
        db_column="PRICE_DELTA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    freight = models.DecimalField(
        db_column="FREIGHT", max_digits=22, decimal_places=2, blank=True, null=True
    )
    freight_delta = models.DecimalField(
        db_column="FREIGHT_DELTA",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vpc = models.DecimalField(
        db_column="VPC", max_digits=22, decimal_places=2, blank=True, null=True
    )
    vpc_delta = models.DecimalField(
        db_column="VPC_DELTA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    other_tlc_components = models.DecimalField(
        db_column="OTHER_TLC_COMPONENTS",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    other_components_delta = models.DecimalField(
        db_column="OTHER_COMPONENTS_DELTA",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="BRAND", max_length=360, blank=True, null=True)
    created_by = models.IntegerField(db_column="CREATED_BY")
    creation_date = models.DateField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.IntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.IntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NSH_CONTRIBUTION_SCENARIO"
