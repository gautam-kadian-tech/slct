from django.db import models

# from auditlog.registry import auditlog

# Create your models here.


class EtaUpdatedNoEntry(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    route_id = models.DecimalField(
        db_column="Route_ID", max_digits=22, decimal_places=0, blank=True, null=True
    )
    source_city = models.CharField(
        db_column="Source_City", max_length=350, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="Destination_District", max_length=350, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="Destination_City", max_length=350, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="Pack_Type", max_length=350, blank=True, null=True
    )
    start_time = models.TimeField(db_column="START_TIME", blank=True, null=True)
    end_time = models.TimeField(db_column="END_TIME", blank=True, null=True)
    start_time_no_entry_2 = models.TimeField(
        db_column="START_TIME_NO_ENTRY_2", blank=True, null=True
    )
    end_time_no_entry_2 = models.TimeField(
        db_column="END_TIME_NO_ENTRY_2", blank=True, null=True
    )
    start_time_no_entry_3 = models.TimeField(
        db_column="START_TIME_NO_ENTRY_3", blank=True, null=True
    )
    end_time_no_entry_3 = models.TimeField(
        db_column="END_TIME_NO_ENTRY_3", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ETA_UPDATED_NO_ENTRY"
        verbose_name_plural = "Eta Updated No Entry"


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
        decimal_places=0,
        blank=True,
        null=True,
    )
    truck_loader = models.CharField(
        db_column="TRUCK_LOADER", max_length=20, blank=True, null=True
    )
    tl_rated_capacity_mt_hr = models.DecimalField(
        db_column="TL_RATED_CAPACITY_MT/HR",
        max_digits=20,
        decimal_places=0,
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
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
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
        verbose_name_plural = "Packer Rated Capacity"


class PlantwiseSwitchoverTime(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    plant = models.CharField(db_column="PLANT", max_length=20, blank=True, null=True)
    grade_switch_time_min = models.IntegerField(
        db_column="GRADE_SWITCH_TIME_MIN", blank=True, null=True
    )
    worker_switch_time_diff_packer_min = models.IntegerField(
        db_column="WORKER_SWITCH_TIME_DIFF_PACKER_MIN", blank=True, null=True
    )
    switch_time_bw_trucks_min = models.IntegerField(
        db_column="SWITCH_TIME_BW_TRUCKS_MIN", blank=True, null=True
    )
    brand_switch_time_min = models.IntegerField(
        db_column="BRAND_SWITCH_TIME_MIN", blank=True, null=True
    )
    tea_break_time_min = models.IntegerField(
        db_column="TEA_BREAK_TIME_MIN", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    effective_start_date = models.DateTimeField(
        db_column="EFFECTIVE_START_DATE", blank=True, null=True
    )
    effective_end_date = models.DateTimeField(
        db_column="EFFECTIVE_END_DATE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "PLANTWISE_SWITCHOVER_TIME"
        verbose_name_plural = "Plantwise Switchover Time"


class FreightMaster(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    link_id = models.IntegerField(db_column="LINK_ID")
    primary_frt = models.DecimalField(
        db_column="PRIMARY_FRT", max_digits=18, decimal_places=0, blank=True, null=True
    )
    secondary_frt = models.DecimalField(
        db_column="SECONDARY_FRT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    handling_charges = models.DecimalField(
        db_column="HANDLING_CHARGES",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    rake_charges = models.DecimalField(
        db_column="RAKE_CHARGES", max_digits=20, decimal_places=0, blank=True, null=True
    )
    demurrage = models.DecimalField(
        db_column="DEMURRAGE", max_digits=20, decimal_places=0, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=20, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=20, blank=True, null=True
    )
    damages = models.DecimalField(
        db_column="DAMAGES", max_digits=20, decimal_places=0, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="CREATED_AT", blank=True, null=True)
    updated_at = models.DateTimeField(db_column="UPDATED_AT", blank=True, null=True)
    notional_freight = models.IntegerField(
        db_column="NOTIONAL_FREIGHT", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "FREIGHT_MASTER"
        verbose_name_plural = "Freight Master"


class TgtPlantLookup(models.Model):
    commudity = models.CharField(
        db_column="Commudity", max_length=100, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=100, blank=True, null=True)
    org = models.CharField(db_column="ORG", max_length=100, blank=True, null=True)
    plant_name = models.CharField(
        db_column="Plant NAME", max_length=50, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "TGT_PLANT_LOOKUP"
        verbose_name_plural = "Tgt Plant Lookup"


class LpSourceMappingTlc(models.Model):
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=50, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=50, blank=True, null=True
    )
    source_id = models.CharField(
        db_column="SOURCE_ID", max_length=50, blank=True, null=True
    )
    from_city_id = models.DecimalField(
        db_column="FROM_CITY_ID",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    source_city = models.CharField(
        db_column="SOURCE_CITY", max_length=50, blank=True, null=True
    )
    source_district = models.CharField(
        db_column="SOURCE_DISTRICT", max_length=50, blank=True, null=True
    )
    source_taluka = models.CharField(
        db_column="SOURCE_TALUKA", max_length=50, blank=True, null=True
    )
    source_state = models.CharField(
        db_column="SOURCE_STATE", max_length=50, blank=True, null=True
    )
    source_type = models.CharField(
        db_column="SOURCE_TYPE", max_length=50, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=50, blank=True, null=True)
    to_city_id = models.DecimalField(
        db_column="TO_CITY_ID",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=50, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=50, blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=50, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    contribution_per_mt = models.DecimalField(
        db_column="CONTRIBUTION_PER_MT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    tlc_per_mt = models.DecimalField(
        db_column="TLC_PER_MT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    ncr_per_mt = models.DecimalField(
        db_column="NCR_PER_MT",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    distance = models.DecimalField(
        db_column="DISTANCE",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    sla = models.DecimalField(
        db_column="SLA", max_digits=10, decimal_places=0, blank=True, null=True
    )
    primary_secondary_route = models.CharField(
        db_column="PRIMARY_SECONDARY_ROUTE", max_length=50, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=50, blank=True, null=True)
    priority = models.DecimalField(
        max_digits=20, decimal_places=0, blank=True, null=True
    )
    destination_taluka = models.CharField(
        db_column="DESTINATION_TALUKA", max_length=50, blank=True, null=True
    )
    route_id_secondary = models.DecimalField(
        db_column="ROUTE_ID_SECONDARY",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )

    reasons = models.CharField(
        db_column="REASONS", max_length=50, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "LP_SOURCE_MAPPING_TLC"
        verbose_name_plural = "Lp Source Mapping Tlc"


class ReasonsForFreightChange(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    reasons = models.CharField(
        db_column="REASONS", max_length=540, blank=True, null=True
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
        db_table = "REASONS_FOR_FREIGHT_CHANGE"


class RakeTypes(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    rake_types = models.CharField(
        db_column="RAKE_TYPES", max_length=540, blank=True, null=True
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
        db_table = "RAKE_TYPES"


class SidingCodeMapping(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=540, blank=True, null=True
    )  # Field name made lowercase.
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )  # Field name made lowercase.
    rake_point_type = models.CharField(
        db_column="RAKE_POINT_TYPE", max_length=540, blank=True, null=True
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
        db_table = "SIDING_CODE_MAPPING"


class ReasonsForDispatchDelay(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    reasons = models.CharField(
        db_column="REASONS", max_length=540, blank=True, null=True
    )  # Field name made lowercase.
    no_trucks_available = models.CharField(
        db_column="NO_TRUCKS_AVAILABLE", max_length=540, blank=True, null=True
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
        db_table = "REASONS_FOR_DISPATCH_DELAY"


class SourceChangeFreightMaster(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    state = models.CharField(
        db_column="STATE", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    brand = models.BigIntegerField(db_column="BRAND", blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    org_type = models.CharField(
        db_column="ORG_TYPE", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    incoterm = models.CharField(
        db_column="INCOTERM", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    created_by = models.BigIntegerField(
        db_column="CREATED_BY", default=32
    )  # Field name made lowercase.
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", auto_now_add=True
    )  # Field name made lowercase.
    last_updated_by = models.BigIntegerField(
        db_column="LAST_UPDATED_BY", default=32
    )  # Field name made lowercase.
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )  # Field name made lowercase.
    last_update_login = models.BigIntegerField(
        db_column="LAST_UPDATE_LOGIN", default=32
    )  # Field name made lowercase.

    class Meta:
        unique_together = [
            ("state", "brand", "district", "org_type", "incoterm", "freight_term")
        ]
        managed = False
        db_table = "SOURCE_CHANGE_FREIGHT_MASTER"


class VpcHistorical(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    vpc = models.DecimalField(
        db_column="VPC", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "VPC_HISTORICAL"


# auditlog.register(EtaUpdatedNoEntry)
# auditlog.register(PackerRatedCapacity)
# auditlog.register(PlantwiseSwitchoverTime)
# auditlog.register(FreightMaster)
# auditlog.register(TgtPlantLookup)
# auditlog.register(LpSourceMappingTlc)
# auditlog.register(ReasonsForFreightChange)
# auditlog.register(RakeTypes)
# auditlog.register(SidingCodeMapping)
# auditlog.register(ReasonsForDispatchDelay)
# auditlog.register(SourceChangeFreightMaster)
