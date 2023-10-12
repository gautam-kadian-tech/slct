"""Analytical data monthly scheduling models module"""
# pylint: disable=too-few-public-methods
from compositefk.fields import CompositeForeignKey
from django.db import models

from analytical_data.enum_classes import LpModelDfFnlBrandChoices


class TOebsSclAddressLink(models.Model):
    """City id and city name mapping."""

    city = models.CharField(db_column="CITY", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    city_id = models.DecimalField(
        db_column="CITY_ID",
        max_digits=10,
        primary_key=True,
        decimal_places=0,
    )
    country = models.CharField(
        db_column="COUNTRY", max_length=500, blank=True, null=True
    )
    pincode = models.CharField(
        db_column="PINCODE", max_length=500, blank=True, null=True
    )
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=150,
        decimal_places=0,
        blank=True,
        null=True,
    )
    taluka = models.CharField(db_column="TALUKA", max_length=500, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=500, blank=True, null=True)
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=150, decimal_places=0, blank=True, null=True
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=150,
        decimal_places=0,
        blank=True,
        null=True,
    )
    bangur_pl = models.CharField(
        db_column="BANGUR_PL", max_length=500, blank=True, null=True
    )
    cemento_pl = models.CharField(
        db_column="CEMENTO_PL", max_length=500, blank=True, null=True
    )
    shree_pl = models.CharField(
        db_column="SHREE_PL", max_length=500, blank=True, null=True
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=500, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=500, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=500, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=500, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=500, blank=True, null=True
    )
    attribute_category = models.CharField(
        db_column="ATTRIBUTE_CATEGORY", max_length=500, blank=True, null=True
    )
    attribute6 = models.CharField(
        db_column="ATTRIBUTE6", max_length=500, blank=True, null=True
    )
    attribute7 = models.CharField(
        db_column="ATTRIBUTE7", max_length=500, blank=True, null=True
    )
    attribute8 = models.CharField(
        db_column="ATTRIBUTE8", max_length=500, blank=True, null=True
    )
    attribute9 = models.CharField(
        db_column="ATTRIBUTE9", max_length=500, blank=True, null=True
    )
    attribute10 = models.CharField(
        db_column="ATTRIBUTE10", max_length=500, blank=True, null=True
    )
    rename_type = models.CharField(
        db_column="RENAME_TYPE", max_length=500, blank=True, null=True
    )
    active = models.CharField(db_column="ACTIVE", max_length=500, blank=True, null=True)
    old_city_id = models.DecimalField(
        db_column="OLD_CITY_ID", max_digits=100, decimal_places=0, blank=True, null=True
    )
    key = models.BigIntegerField(db_column="Key", blank=True, null=True)
    active_0 = models.IntegerField(db_column="Active", blank=True, null=True)
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
        db_table = "T_OEBS_SCL_ADDRESS_LINK"
        # ordering = ["id"]


class LinksMaster(models.Model):
    """Model class for links master data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    from_city_id = models.DecimalField(
        db_column="FROM_CITY_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    to_city_id = models.DecimalField(
        db_column="TO_CITY_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=20, blank=True, null=True)
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=20, decimal_places=5, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=20, blank=True, null=True)
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=100, blank=True, null=True
    )
    source_name = models.CharField(
        db_column="SOURCE_NAME", max_length=500, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=100, blank=True, null=True
    )
    source_city = models.CharField(
        db_column="SOURCE_CITY", max_length=100, blank=True, null=True
    )
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=100, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=100, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=100, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=100, blank=True, null=True
    )
    avg_time = models.CharField(
        db_column="AVG_TIME", max_length=50, blank=True, null=True
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID", max_digits=10, decimal_places=0, blank=True, null=True
    )
    is_active = models.BooleanField(db_column="IS_ACTIVE", blank=True, null=True)
    plant = models.CharField(db_column="PLANT", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    node_city_id = models.IntegerField(db_column="NODE_CITY_ID", blank=True, null=True)
    warehouse = models.CharField(
        db_column="WAREHOUSE", max_length=200, blank=True, null=True
    )
    route_id_secondary = models.DecimalField(
        db_column="ROUTE_ID_SECONDARY",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=50, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=50, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LINKS_MASTER"
        ordering = ["id"]


class GodownMaster(models.Model):
    """Model class for godown master data."""

    id = models.IntegerField(primary_key=True, db_column="ID")
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    capacity = models.CharField(
        db_column="CAPACITY", max_length=20, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=20, blank=True, null=True)
    start_time = models.CharField(
        db_column="START_TIME", max_length=20, blank=True, null=True
    )
    end_time = models.CharField(
        db_column="END_TIME", max_length=20, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "GODOWN_MASTER"
        ordering = ["id"]


class PackagingMaster(models.Model):
    """Model class for packaging master data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant_id = models.DecimalField(
        db_column="PLANT_ID", max_digits=4, decimal_places=2, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    cost = models.DecimalField(
        db_column="COST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKAGING_MASTER"
        ordering = ["id"]


class PlantProductsMaster(models.Model):
    """Model class for plant products master data."""

    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant_id = models.CharField(db_column="PLANT_ID", max_length=50)
    grade = models.CharField(db_column="GRADE", max_length=50)
    quantity = models.DecimalField(
        db_column="QUANTITY", max_digits=20, decimal_places=2
    )
    variable_production_cost = models.IntegerField(
        db_column="VARIABLE_PRODUCTION_COST", blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    clinker_cf = models.DecimalField(
        db_column="CLINKER_CF", max_digits=20, decimal_places=2, blank=True, null=True
    )
    min_inventory = models.DecimalField(
        db_column="MIN_INVENTORY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    silo_capacity = models.DecimalField(
        db_column="SILO_CAPACITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "PLANT_PRODUCTS_MASTER"
        ordering = ["id"]


class PlantConstraintsMaster(models.Model):
    """Model class for plant constraints master data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=4, blank=True, null=True
    )
    railway_bridging_cost = models.IntegerField(
        db_column="RAILWAY_BRIDGING_COST", blank=True, null=True
    )
    sididng_inside = models.CharField(
        db_column="SIDIDNG_INSIDE", max_length=100, blank=True, null=True
    )
    fiscal_benefit = models.CharField(
        db_column="FISCAL_BENEFIT", max_length=100, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PLANT_CONSTRAINTS_MASTER"
        ordering = ["id"]


class ClinkerLinksMaster(models.Model):
    """Clinker links master model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    fg_whse = models.CharField(db_column="FG_WHSE", max_length=200)
    fc_whse = models.CharField(db_column="FC_WHSE", max_length=200)
    mode_of_transport = models.CharField(db_column="MODE_OF_TRANSPORT", max_length=200)
    clinker_freight = models.IntegerField(db_column="CLINKER_FREIGHT")
    is_active = models.BooleanField(db_column="IS_ACTIVE", blank=True, null=True)
    route_id = models.IntegerField(db_column="ROUTE_ID", blank=True, null=True)
    clinker_bridging_loading = models.IntegerField(
        db_column="CLINKER_BRIDGING_LOADING", blank=True, null=True
    )
    clinker_bridging_unloading = models.IntegerField(
        db_column="CLINKER_BRIDGING_UNLOADING", blank=True, null=True
    )
    clinker_notional_freight = models.IntegerField(
        db_column="CLINKER_NOTIONAL_FREIGHT", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "CLINKER_LINKS_MASTER"
        ordering = ["id"]


class RailHandling(models.Model):
    """Rail handling model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=100, blank=True, null=True)
    depot = models.CharField(db_column="DEPOT", max_length=100, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    ha_commission = models.IntegerField(
        db_column="HA_COMMISSION", blank=True, null=True
    )
    packing = models.CharField(
        db_column="PACKING", max_length=100, blank=True, null=True
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=100, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "RAIL_HANDLING"


class Demand(models.Model):
    """Demand data model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    month = models.DateTimeField(db_column="MONTH", blank=True, null=True)
    destination = models.ForeignKey(
        TOebsSclAddressLink,
        to_field="city_id",
        on_delete=models.DO_NOTHING,
        db_column="DESTINATION",
    )
    brand = models.CharField(db_column="BRAND", max_length=20, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=20, blank=True, null=True)
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=20, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=10, blank=True, null=True
    )
    demand_qty = models.DecimalField(
        db_column="DEMAND_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    di_perc = models.DecimalField(
        db_column="DI_perc", max_digits=4, decimal_places=0, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DEMAND"
        ordering = ["id"]


class PriceMaster(models.Model):
    """Model class for price master data."""

    id = models.IntegerField(primary_key=True, db_column="ID")
    destination = models.ForeignKey(
        TOebsSclAddressLink,
        to_field="city_id",
        on_delete=models.DO_NOTHING,
        db_column="DESTINATION",
    )
    cust_category = models.CharField(db_column="CUST_CATEGORY", max_length=50)
    brand = models.CharField(db_column="BRAND", max_length=50)
    grade = models.CharField(db_column="GRADE", max_length=50)
    packaging = models.CharField(db_column="PACKAGING", max_length=50)
    price = models.DecimalField(db_column="PRICE", max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=50, blank=True, null=True
    )
    ha_commission = models.DecimalField(
        db_column="HA_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    discount = models.DecimalField(
        db_column="DISCOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    taxes = models.DecimalField(
        db_column="TAXES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    sp_commission = models.DecimalField(
        db_column="SP_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    isp_commission = models.DecimalField(
        db_column="ISP_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    misc_charges = models.DecimalField(
        db_column="MISC_CHARGES", max_digits=20, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PRICE_MASTER"
        ordering = ["id"]


class PackerConstraintsMaster(models.Model):
    """Model class for packer constraints master data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=4, blank=True, null=True
    )
    packer_no = models.CharField(
        db_column="PACKER_NO", max_length=4, blank=True, null=True
    )
    packer_capacity = models.DecimalField(
        db_column="PACKER_CAPACITY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    truck_loader_no = models.CharField(
        db_column="TRUCK_LOADER_NO", max_length=4, blank=True, null=True
    )
    tl_rated_output = models.CharField(
        db_column="TL_RATED_OUTPUT", max_length=4, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PACKER_CONSTRAINTS_MASTER"
        ordering = ["id"]


class VehicleAvailability(models.Model):
    """Vehicle availability model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=4, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)
    mode = models.CharField(db_column="MODE", max_length=50, blank=True, null=True)
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=50, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    cust_category = models.TextField(db_column="CUST_CATEGORY", blank=True, null=True)
    pack_type = models.TextField(db_column="PACK_TYPE", blank=True, null=True)
    quantity = models.IntegerField(db_column="QUANTITY", blank=True, null=True)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "VEHICLE_AVAILABILITY"
        ordering = ["id"]


class ServiceLevelSla(models.Model):
    """Model class for service level sla data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    destination = models.ForeignKey(
        TOebsSclAddressLink,
        to_field="city_id",
        on_delete=models.DO_NOTHING,
        db_column="DESTINATION",
    )
    sla = models.CharField(db_column="SLA", max_length=100)
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SERVICE_LEVEL_SLA"
        ordering = ["id"]


class LpTargetSetting(models.Model):
    """Lp target settings model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=100, blank=True, null=True
    )
    target = models.DecimalField(
        db_column="TARGET",
        max_digits=1000,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LP_TARGET_SETTING"
        ordering = ["id"]


class LpModelRun(models.Model):
    """Lp model run model class."""

    run_id = models.AutoField(db_column="RUN_ID", primary_key=True)
    run_date = models.DateField(db_column="RUN_DATE")
    user = models.CharField(db_column="USER", max_length=100, blank=True, null=True)
    run_status = models.CharField(
        db_column="RUN_STATUS", max_length=100, blank=True, null=True
    )
    contribution = models.IntegerField(db_column="CONTRIBUTION")
    tlc = models.DecimalField(
        db_column="TLC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    dmnd_fulfiled = models.DecimalField(
        db_column="DMND_FULFILED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    direct_dispatch = models.DecimalField(
        db_column="DIRECT_DISPATCH",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    plan_date = models.DateField(db_column="PLAN_DATE", blank=True, null=True)
    run_type = models.CharField(
        db_column="RUN_TYPE", max_length=255, blank=True, null=True
    )
    approve_status = models.IntegerField(
        db_column="APPROVE_STATUS", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_MODEL_RUN"
        ordering = ["-run_id"]


class FreightMaster(models.Model):
    """Model class for freight master data."""

    id = models.AutoField(db_column="ID", primary_key=True)
    link_id = models.OneToOneField(
        LinksMaster,
        db_column="LINK_ID",
        on_delete=models.CASCADE,
        related_name="freight_master",
    )
    # link_id = models.IntegerField(db_column="LINK_ID")
    primary_frt = models.DecimalField(
        db_column="PRIMARY_FRT", max_digits=18, decimal_places=0, blank=True, null=True
    )
    secondary_frt = models.DecimalField(
        db_column="SECONDARY_FRT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    handling_charges = models.DecimalField(
        db_column="HANDLING_CHARGES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rake_charges = models.DecimalField(
        db_column="RAKE_CHARGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    demurrage = models.DecimalField(
        db_column="DEMURRAGE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=20, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=20, blank=True, null=True
    )
    damages = models.DecimalField(
        db_column="DAMAGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", auto_now_add=True)
    updated_at = models.DateTimeField(
        db_column="UPDATED_AT", auto_now=True, blank=True, null=True
    )
    notional_freight = models.IntegerField(
        db_column="NOTIONAL_FREIGHT", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "FREIGHT_MASTER"
        ordering = ["id"]


class LpModelDfFnl(models.Model):
    """Lp model df fnl model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    scenario = models.CharField(
        db_column="SCENARIO", max_length=100, blank=True, null=True
    )
    run_id = models.DecimalField(
        db_column="RUN_ID", max_digits=20, decimal_places=2, blank=True, null=True
    )
    route_id = models.IntegerField(db_column="ROUTE_ID", blank=True, null=True)
    route_id_secondary = models.IntegerField(
        db_column="ROUTE_ID_SECONDARY", blank=True, null=True
    )
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=100, blank=True, null=True
    )
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    plant_products_master = CompositeForeignKey(
        PlantProductsMaster,
        on_delete=models.DO_NOTHING,
        related_name="lp_model_df_fnl",
        to_fields={"plant_id": "plant_id", "grade": "grade"},
    )
    node_city = models.CharField(
        db_column="NODE_CITY", max_length=100, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=100, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=100, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=100, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=100, blank=True, null=True)
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=100, blank=True, null=True
    )
    brand = models.IntegerField(
        db_column="BRAND",
        choices=LpModelDfFnlBrandChoices.choices,
        blank=True,
        null=True,
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=100, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=100, blank=True, null=True
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=100, blank=True, null=True
    )
    price = models.IntegerField(db_column="PRICE", blank=True, null=True)
    primary_frt = models.DecimalField(
        db_column="PRIMARY_FRT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    secondary_frt = models.DecimalField(
        db_column="SECONDARY_FRT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    discount = models.DecimalField(
        db_column="DISCOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    taxes = models.DecimalField(
        db_column="TAXES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    misc_charges = models.DecimalField(
        db_column="MISC_CHARGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    ha_commission = models.DecimalField(
        db_column="HA_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    demurrage = models.DecimalField(
        db_column="DEMURRAGE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    damages = models.DecimalField(
        db_column="DAMAGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rake_charges = models.DecimalField(
        db_column="RAKE_CHARGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    sp_commission = models.DecimalField(
        db_column="SP_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    isp_commission = models.DecimalField(
        db_column="ISP_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    variable_production_cost = models.DecimalField(
        db_column="VARIABLE_PRODUCTION_COST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    clinker_plant = models.CharField(
        db_column="CLINKER_PLANT", max_length=100, blank=True, null=True
    )
    clinker_mode = models.CharField(
        db_column="CLINKER_MODE", max_length=100, blank=True, null=True
    )
    clinker_freight = models.DecimalField(
        db_column="CLINKER_FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    route_changed = models.CharField(
        db_column="ROUTE_CHANGED", max_length=100, blank=True, null=True
    )
    clinker_cf = models.DecimalField(
        db_column="CLINKER_CF", max_digits=20, decimal_places=2, blank=True, null=True
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=20, decimal_places=2, blank=True, null=True
    )
    qty = models.DecimalField(
        db_column="QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    tlc = models.DecimalField(
        db_column="TLC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    direct_plant_discount = models.IntegerField(blank=True, null=True)
    jhju_rail_discount = models.IntegerField(blank=True, null=True)
    avg_time = models.FloatField(blank=True, null=True)
    notional_freight = models.IntegerField(
        db_column="NOTIONAL_FREIGHT", blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    warehouse = models.CharField(
        db_column="WAREHOUSE", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LP_MODEL_DF_FNL"
        ordering = ["id"]


class LpModelDfRank(models.Model):
    """LP model df rank table model class."""

    run_id = models.BigIntegerField(db_column="RUN_ID", blank=True, null=True)
    route_id = models.BigIntegerField(db_column="ROUTE_ID", blank=True, null=True)
    route_id_secondary = models.BigIntegerField(
        db_column="ROUTE_ID_SECONDARY", blank=True, null=True
    )
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=100, blank=True, null=True
    )
    warehouse = models.CharField(
        db_column="WAREHOUSE", max_length=100, blank=True, null=True
    )
    from_city_id = models.BigIntegerField(
        db_column="FROM_CITY_ID", blank=True, null=True
    )
    node_city_id = models.BigIntegerField(
        db_column="NODE_CITY_ID", blank=True, null=True
    )
    node_city = models.CharField(
        db_column="NODE_CITY", max_length=100, blank=True, null=True
    )
    node_state = models.CharField(
        db_column="NODE_STATE", max_length=100, blank=True, null=True
    )
    node_district = models.CharField(
        db_column="NODE_DISTRICT", max_length=100, blank=True, null=True
    )
    node_taluka = models.CharField(
        db_column="NODE_TALUKA", max_length=100, blank=True, null=True
    )
    to_city_id = models.BigIntegerField(db_column="TO_CITY_ID", blank=True, null=True)
    mode = models.CharField(db_column="MODE", max_length=100, blank=True, null=True)
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=100, blank=True, null=True)
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=100, blank=True, null=True
    )
    source_city = models.CharField(
        db_column="SOURCE_CITY", max_length=100, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=100, blank=True, null=True
    )
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=100, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=100, blank=True, null=True
    )
    destination_taluka = models.CharField(
        db_column="DESTINATION_TALUKA", max_length=100, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=100, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=100, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=100, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=100, blank=True, null=True
    )
    freight_type = models.CharField(
        db_column="FREIGHT_TYPE", max_length=100, blank=True, null=True
    )
    primary_frt = models.DecimalField(
        db_column="PRIMARY_FRT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    secondary_frt = models.DecimalField(
        db_column="SECONDARY_FRT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    handling_charges = models.DecimalField(
        db_column="HANDLING_CHARGES",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    demurrage = models.DecimalField(
        db_column="DEMURRAGE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    damages = models.DecimalField(
        db_column="DAMAGES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    notional_freight = models.DecimalField(
        db_column="NOTIONAL_FREIGHT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.BigIntegerField(db_column="BRAND", blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=100, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    fiscal_benefit_amt = models.DecimalField(
        db_column="FISCAL_BENEFIT_AMT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    variable_production_cost = models.DecimalField(
        db_column="VARIABLE_PRODUCTION_COST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    packing = models.CharField(
        db_column="PACKING", max_length=100, blank=True, null=True
    )
    ha_commission = models.DecimalField(
        db_column="HA_COMMISSION",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    direct_plant_discount = models.DecimalField(
        db_column="DIRECT_PLANT_DISCOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=20, decimal_places=2, blank=True, null=True
    )
    depot_id = models.CharField(
        db_column="DEPOT_ID", max_length=100, blank=True, null=True
    )
    qty = models.DecimalField(
        db_column="QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    rank = models.BigIntegerField(db_column="RANK", blank=True, null=True)
    id = models.AutoField(db_column="ID", primary_key=True)
    rake_charges = models.IntegerField(db_column="RAKE_CHARGES", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "LP_MODEL_DF_RANK"


class DjpRun(models.Model):
    """DJP Run model class."""

    run_id = models.AutoField(db_column="RUN_ID", primary_key=True)
    emp_code = models.BigIntegerField(db_column="EMP_CODE", blank=True, null=True)
    recommended_route_1 = models.CharField(
        db_column="RECOMMENDED_ROUTE_1", max_length=100, blank=True, null=True
    )
    recommended_route_2 = models.CharField(
        db_column="RECOMMENDED_ROUTE_2", max_length=100, blank=True, null=True
    )
    plan_date = models.DateField(db_column="PLAN_DATE", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "DJP_RUN"
        ordering = ["run_id"]


class TOebsHrAllOrganizationUnits(models.Model):
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    business_group_id = models.DecimalField(
        db_column="BUSINESS_GROUP_ID",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    cost_allocation_keyflex_id = models.DecimalField(
        db_column="COST_ALLOCATION_KEYFLEX_ID",
        max_digits=900,
        decimal_places=0,
        blank=True,
        null=True,
    )
    location_id = models.DecimalField(
        db_column="LOCATION_ID", max_digits=500, decimal_places=0, blank=True, null=True
    )
    soft_coding_keyflex_id = models.DecimalField(
        db_column="SOFT_CODING_KEYFLEX_ID",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    date_from = models.DateTimeField(db_column="DATE_FROM", blank=True, null=True)
    name = models.CharField(db_column="NAME", max_length=2400, blank=True, null=True)
    date_to = models.DateTimeField(db_column="DATE_TO", blank=True, null=True)
    internal_external_flag = models.CharField(
        db_column="INTERNAL_EXTERNAL_FLAG", max_length=300, blank=True, null=True
    )

    internal_address_line = models.CharField(
        db_column="INTERNAL_ADDRESS_LINE", max_length=800, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=3000, blank=True, null=True)
    request_id = models.DecimalField(
        db_column="REQUEST_ID", max_digits=500, decimal_places=0, blank=True, null=True
    )
    program_application_id = models.DecimalField(
        db_column="PROGRAM_APPLICATION_ID",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    program_id = models.DecimalField(
        db_column="PROGRAM_ID", max_digits=500, decimal_places=0, blank=True, null=True
    )
    program_update_date = models.DateTimeField(
        db_column="PROGRAM_UPDATE_DATE", blank=True, null=True
    )
    attribute_category = models.CharField(
        db_column="ATTRIBUTE_CATEGORY", max_length=3000, blank=True, null=True
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=1500, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=1500, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=1500, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=1500, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=1500, blank=True, null=True
    )
    attribute6 = models.CharField(
        db_column="ATTRIBUTE6", max_length=1500, blank=True, null=True
    )
    attribute7 = models.CharField(
        db_column="ATTRIBUTE7", max_length=1500, blank=True, null=True
    )
    attribute8 = models.CharField(
        db_column="ATTRIBUTE8", max_length=1500, blank=True, null=True
    )
    attribute9 = models.CharField(
        db_column="ATTRIBUTE9", max_length=1500, blank=True, null=True
    )
    attribute10 = models.CharField(
        db_column="ATTRIBUTE10", max_length=1000, blank=True, null=True
    )
    attribute11 = models.CharField(
        db_column="ATTRIBUTE11", max_length=1000, blank=True, null=True
    )
    attribute12 = models.CharField(
        db_column="ATTRIBUTE12", max_length=1000, blank=True, null=True
    )
    attribute13 = models.CharField(
        db_column="ATTRIBUTE13", max_length=1000, blank=True, null=True
    )
    attribute14 = models.CharField(
        db_column="ATTRIBUTE14", max_length=1000, blank=True, null=True
    )
    attribute15 = models.CharField(
        db_column="ATTRIBUTE15", max_length=1000, blank=True, null=True
    )
    attribute16 = models.CharField(
        db_column="ATTRIBUTE16", max_length=1000, blank=True, null=True
    )
    attribute17 = models.CharField(
        db_column="ATTRIBUTE17", max_length=1000, blank=True, null=True
    )
    attribute18 = models.CharField(
        db_column="ATTRIBUTE18", max_length=1000, blank=True, null=True
    )
    attribute19 = models.CharField(
        db_column="ATTRIBUTE19", max_length=1000, blank=True, null=True
    )
    attribute20 = models.CharField(
        db_column="ATTRIBUTE20", max_length=1000, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=500, decimal_places=0, blank=True, null=True
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    object_version_number = models.DecimalField(
        db_column="OBJECT_VERSION_NUMBER",
        max_digits=900,
        decimal_places=0,
        blank=True,
        null=True,
    )
    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=500, decimal_places=0, blank=True, null=True
    )
    comments = models.CharField(
        db_column="COMMENTS", max_length=1000, blank=True, null=True
    )
    attribute21 = models.CharField(
        db_column="ATTRIBUTE21", max_length=1500, blank=True, null=True
    )
    attribute22 = models.CharField(
        db_column="ATTRIBUTE22", max_length=1500, blank=True, null=True
    )
    attribute23 = models.CharField(
        db_column="ATTRIBUTE23", max_length=1500, blank=True, null=True
    )
    attribute24 = models.CharField(
        db_column="ATTRIBUTE24", max_length=1500, blank=True, null=True
    )
    attribute25 = models.CharField(
        db_column="ATTRIBUTE25", max_length=1500, blank=True, null=True
    )
    attribute26 = models.CharField(
        db_column="ATTRIBUTE26", max_length=1500, blank=True, null=True
    )
    attribute27 = models.CharField(
        db_column="ATTRIBUTE27", max_length=1500, blank=True, null=True
    )
    attribute28 = models.CharField(
        db_column="ATTRIBUTE28", max_length=1500, blank=True, null=True
    )
    attribute29 = models.CharField(
        db_column="ATTRIBUTE29", max_length=1500, blank=True, null=True
    )
    attribute30 = models.CharField(
        db_column="ATTRIBUTE30", max_length=1500, blank=True, null=True
    )
    cost_allocation_keyflex_id_1 = models.DecimalField(
        db_column="COST_ALLOCATION_KEYFLEX_ID#1",
        max_digits=500,
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
    id = models.AutoField(primary_key=True, db_column="ID")

    class Meta:
        managed = False
        db_table = "T_OEBS_HR_ALL_ORGANIZATION_UNITS"


class DjpRouteScore(models.Model):
    """Djp route score model class."""

    route_score_id = models.AutoField(db_column="ROUTE_SCORE_ID", primary_key=True)
    run = models.ForeignKey(
        DjpRun,
        models.DO_NOTHING,
        related_name="djp_route_score",
        db_column="RUN_ID",
        blank=True,
        null=True,
    )
    route = models.CharField(db_column="ROUTE", max_length=100, blank=True, null=True)
    route_score = models.IntegerField(db_column="ROUTE_SCORE", blank=True, null=True)
    recommended_objective_1 = models.IntegerField(
        db_column="RECOMMENDED_OBJECTIVE_1", blank=True, null=True
    )
    recommended_objective_2 = models.IntegerField(
        db_column="RECOMMENDED_OBJECTIVE_2", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DJP_ROUTE_SCORE"
        ordering = ["route_score_id"]


class DjpCounterScore(models.Model):
    """Djp counter score model class."""

    counter_score_id = models.AutoField(db_column="COUNTER_SCORE_ID", primary_key=True)
    run = models.ForeignKey(
        DjpRun,
        models.DO_NOTHING,
        related_name="djp_counter_score",
        db_column="RUN_ID",
        blank=True,
        null=True,
    )
    route_score = models.ForeignKey(
        DjpRouteScore,
        models.DO_NOTHING,
        related_name="related_route_score",
        db_column="ROUTE_SCORE_ID",
        blank=True,
        null=True,
    )
    objective_id = models.IntegerField(db_column="OBJECTIVE_ID", blank=True, null=True)
    customer_code = models.BigIntegerField(
        db_column="CUSTOMER_CODE", blank=True, null=True
    )
    counter_id = models.BigIntegerField(db_column="COUNTER_ID", blank=True, null=True)
    counter_name = models.CharField(
        db_column="COUNTER_NAME", max_length=100, blank=True, null=True
    )
    counter_score = models.IntegerField(
        db_column="COUNTER_SCORE", blank=True, null=True
    )
    visit_sequence = models.IntegerField(
        db_column="VISIT_SEQUENCE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DJP_COUNTER_SCORE"
        ordering = ["counter_score_id"]


class ClinkerDemandRun(models.Model):
    """Clinker demand run model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey(
        LpModelRun, models.DO_NOTHING, db_column="RUN_ID", blank=True, null=True
    )
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=100, blank=True, null=True
    )
    fc_whse = models.CharField(
        db_column="FC_WHSE", max_length=100, blank=True, null=True
    )
    cement_demand = models.IntegerField(
        db_column="CEMENT_DEMAND", blank=True, null=True
    )
    clinker_demand = models.IntegerField(
        db_column="CLINKER_DEMAND", blank=True, null=True
    )
    clinker_freight = models.IntegerField(
        db_column="CLINKER_FREIGHT", blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=100, blank=True, null=True)
    route_id = models.IntegerField(db_column="ROUTE_ID", blank=True, null=True)
    clinker_notional_freight = models.IntegerField(
        db_column="CLINKER_NOTIONAL_FREIGHT", blank=True, null=True
    )
    clinker_bridging_loading = models.IntegerField(
        db_column="CLINKER_BRIDGING_LOADING", blank=True, null=True
    )
    clinker_bridging_unloading = models.IntegerField(
        db_column="CLINKER_BRIDGING_UNLOADING", blank=True, null=True
    )
    railway_bridging_cost = models.IntegerField(
        db_column="RAILWAY_BRIDGING_COST", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CLINKER_DEMAND_RUN"
        ordering = ["id"]


class LpMinCapacity(models.Model):
    """Minimum and maximum capacity model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=255, blank=True, null=True)
    max_capacity_perc = models.DecimalField(
        db_column="MAX_CAPACITY_PERC",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    min_capacity_perc = models.DecimalField(
        db_column="MIN_CAPACITY_PERC",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LP_MIN_CAPACTIY"


class SidingCodeMapping(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=540, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )
    rake_point_type = models.CharField(
        db_column="RAKE_POINT_TYPE", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SIDING_CODE_MAPPING"


class ReasonsForDispatchDelay(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    reasons = models.CharField(
        db_column="REASONS", max_length=540, blank=True, null=True
    )
    no_trucks_available = models.CharField(
        db_column="NO_TRUCKS_AVAILABLE", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "REASONS_FOR_DISPATCH_DELAY"


class RakeTypes(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_types = models.CharField(
        db_column="RAKE_TYPES", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "RAKE_TYPES"


class ReasonsForFreightChange(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    reasons = models.CharField(
        db_column="REASONS", max_length=540, blank=True, null=True
    )
    diesel_prices_gone_up = models.CharField(
        db_column="DIESEL_PRICES_GONE_UP", max_length=540, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "REASONS_FOR_FREIGHT_CHANGE"
