from django.db import models


class BackhaulingInboundTruck(models.Model):
    plant_id = models.CharField(
        db_column="PLANT_ID", max_length=360, blank=True, null=True
    )
    truck_number = models.CharField(
        db_column="TRUCK_NUMBER", max_length=360, blank=True, null=True
    )
    arrival_date = models.DateTimeField(db_column="ARRIVAL_DATE", blank=True, null=True)
    departure_date = models.DateTimeField(
        db_column="DEPARTURE_DATE", blank=True, null=True
    )
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=360, blank=True, null=True
    )
    vehicle_size = models.BigIntegerField(
        db_column="VEHICLE_SIZE", blank=True, null=True
    )
    destination_state = models.CharField(
        db_column="DESTINATION_STATE", max_length=540, blank=True, null=True
    )
    destination_district = models.CharField(
        db_column="DESTINATION_DISTRICT", max_length=540, blank=True, null=True
    )
    destination_city = models.CharField(
        db_column="DESTINATION_CITY", max_length=540, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "BACKHAULING_INBOUND_TRUCK"


class BackhaulingOpportunities(models.Model):
    inbound = models.ForeignKey(
        "BackhaulingInboundTruck",
        models.DO_NOTHING,
        db_column="INBOUND_ID",
        blank=True,
        null=True,
    )
    order_master = models.ForeignKey(
        "LpSchedulingOrderMaster",
        models.DO_NOTHING,
        db_column="ORDER_MASTER_ID",
        blank=True,
        null=True,
    )
    total_score = models.BigIntegerField(db_column="TOTAL_SCORE", blank=True, null=True)
    order_clubbed = models.BooleanField(
        db_column="ORDER_CLUBBED", blank=True, null=True
    )
    club_id = models.BigIntegerField(db_column="CLUB_ID", blank=True, null=True)
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    status = models.BooleanField(db_column="STATUS", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "BACKHAULING_OPPORTUNITIES"
