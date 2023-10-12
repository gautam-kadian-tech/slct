"""Handling agent models module."""
from django.db import models

from analytical_data.enum_classes import (
    ApprovalStatusChoices,
    BrandChoices,
    InventoryItemIdChoices,
    LpModelDfFnlBrandChoices,
)


class TgtDepoInventoryStk(models.Model):
    whse_code = models.CharField(
        db_column="WHSE_CODE", max_length=50, blank=True, null=True
    )
    location = models.CharField(
        db_column="LOCATION", max_length=50, blank=True, null=True
    )
    item = models.CharField(db_column="ITEM", max_length=50, blank=True, null=True)
    opening_stock = models.DecimalField(
        db_column="OPENING_STOCK",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    trans_qty = models.DecimalField(
        db_column="TRANS_QTY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    closing_stock = models.DecimalField(
        db_column="CLOSING_STOCK",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    trans_date = models.DateField(db_column="TRANS_DATE", blank=True, null=True)
    d_trans_date = models.DateField(db_column="d_TRANS_DATE", blank=True, null=True)
    frt_leg1 = models.DecimalField(
        db_column="FRT_LEG1", max_digits=20, decimal_places=2, blank=True, null=True
    )
    clk_frt = models.DecimalField(
        db_column="CLK_FRT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    handling = models.DecimalField(
        db_column="HANDLING", max_digits=20, decimal_places=2, blank=True, null=True
    )
    frt_leg2 = models.DecimalField(
        db_column="FRT_LEG2", max_digits=20, decimal_places=2, blank=True, null=True
    )
    frt_leg3 = models.DecimalField(
        db_column="FRT_LEG3", max_digits=20, decimal_places=2, blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TGT_DEPO_INVENTORY_STK"


class TgtDepoDispatchData(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    tax_invoice_no = models.CharField(
        db_column="TAX_INVOICE_NO", max_length=250, blank=True, null=True
    )
    # excise_invoice_no = models.CharField(
    #     db_column="EXCISE_INVOICE_NO", max_length=250, blank=True, null=True
    # )
    excise_invoice_no = models.OneToOneField(
        "TgtSlhServiceLevelDepo",
        to_field="excise_invoice_no",
        on_delete=models.DO_NOTHING,
        related_name="tgt_slh_service_level_depo",
        db_column="EXCISE_INVOICE_NO",
        max_length=250,
    )
    ordered_quantity = models.DecimalField(
        db_column="ORDERED_QUANTITY",
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
    )
    shipped_qty = models.DecimalField(
        db_column="SHIPPED_QTY", max_digits=20, decimal_places=3, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=200, blank=True, null=True
    )
    vehicle_no = models.CharField(
        db_column="VEHICLE_NO", max_length=250, blank=True, null=True
    )
    lr_gr_no = models.CharField(
        db_column="LR_GR_NO", max_length=250, blank=True, null=True
    )
    lr_gr_dt = models.DateTimeField(db_column="LR_GR_DT", blank=True, null=True)
    transporter = models.CharField(
        db_column="TRANSPORTER", max_length=500, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=200, blank=True, null=True
    )
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=200, blank=True, null=True
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=200, blank=True, null=True
    )
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=200, blank=True, null=True
    )
    sec_freight_term = models.CharField(
        db_column="SEC_FREIGHT_TERM", max_length=200, blank=True, null=True
    )
    inco_term = models.CharField(
        db_column="INCO_TERM", max_length=200, blank=True, null=True
    )
    d1 = models.CharField(db_column="D1", max_length=250, blank=True, null=True)
    d2 = models.CharField(db_column="D2", max_length=300, blank=True, null=True)
    d3 = models.CharField(db_column="D3", max_length=250, blank=True, null=True)
    primary_distance = models.DecimalField(
        db_column="PRIMARY_DISTANCE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    secondary_distance = models.CharField(
        db_column="SECONDARY_DISTANCE", max_length=200, blank=True, null=True
    )
    first_leg_distance = models.CharField(
        db_column="FIRST_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    second_leg_distance = models.CharField(
        db_column="SECOND_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    second_route_id = models.CharField(
        db_column="SECOND_ROUTE_ID", max_length=250, blank=True, null=True
    )
    third_leg_distance = models.CharField(
        db_column="THIRD_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=50, decimal_places=2, blank=True, null=True
    )
    frt_amt = models.CharField(
        db_column="FRT_AMT", max_length=250, blank=True, null=True
    )
    primary_frt = models.CharField(
        db_column="PRIMARY_FRT", max_length=250, blank=True, null=True
    )
    rail_frt_secondary = models.CharField(
        db_column="RAIL_FRT_SECONDARY", max_length=250, blank=True, null=True
    )
    di_so = models.CharField(db_column="DI_SO", max_length=200, blank=True, null=True)
    delivery_id = models.DecimalField(
        db_column="DELIVERY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    token_no = models.CharField(
        db_column="TOKEN_NO", max_length=200, blank=True, null=True
    )
    chute_name = models.CharField(
        db_column="CHUTE_NAME", max_length=250, blank=True, null=True
    )
    di_date = models.DateTimeField(db_column="DI_DATE", blank=True, null=True)
    silo_no = models.CharField(
        db_column="SILO_NO", max_length=250, blank=True, null=True
    )
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    diesel_qty = models.CharField(
        db_column="DIESEL_QTY", max_length=20, blank=True, null=True
    )
    diesel_slip_no = models.DecimalField(
        db_column="DIESEL_SLIP_NO",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=200, blank=True, null=True
    )
    unloading_amt = models.DecimalField(
        db_column="UNLOADING_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    mm_comm = models.CharField(
        db_column="MM_COMM", max_length=200, blank=True, null=True
    )
    unloading = models.CharField(
        db_column="UNLOADING", max_length=200, blank=True, null=True
    )
    commission = models.DecimalField(
        db_column="COMMISSION", max_digits=50, decimal_places=2, blank=True, null=True
    )
    diesel_per_litre = models.DecimalField(
        db_column="DIESEL_PER_LITRE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=200, blank=True, null=True
    )
    cust_sub_category = models.CharField(
        db_column="CUST_SUB_CATEGORY", max_length=200, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    consignee = models.CharField(
        db_column="CONSIGNEE", max_length=500, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=250, blank=True, null=True
    )
    ship_taluka = models.CharField(
        db_column="SHIP_TALUKA", max_length=250, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=250, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=250, blank=True, null=True
    )
    bill_city = models.CharField(
        db_column="BILL_CITY", max_length=250, blank=True, null=True
    )
    bill_district = models.CharField(
        db_column="BILL_DISTRICT", max_length=250, blank=True, null=True
    )
    bill_state = models.CharField(
        db_column="BILL_STATE", max_length=250, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=250, blank=True, null=True)
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=250, blank=True, null=True
    )
    order_number = models.DecimalField(
        db_column="ORDER_NUMBER", max_digits=25, decimal_places=0, blank=True, null=True
    )
    oe_creation_dt = models.DateTimeField(
        db_column="OE_CREATION_DT", blank=True, null=True
    )
    oe_punch_dt = models.DateTimeField(db_column="OE_PUNCH_DT", blank=True, null=True)
    oe_book_dt = models.DateTimeField(db_column="OE_BOOK_DT", blank=True, null=True)
    so_validity_dt = models.CharField(
        db_column="SO_VALIDITY_DT", max_length=300, blank=True, null=True
    )
    sgst_amt = models.DecimalField(
        db_column="SGST_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sgst_rate = models.DecimalField(
        db_column="SGST_RATE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cgst_amt = models.DecimalField(
        db_column="CGST_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cgst_rate = models.DecimalField(
        db_column="CGST_RATE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    igst_amt = models.DecimalField(
        db_column="IGST_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    igst_rate = models.DecimalField(
        db_column="IGST_RATE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    utgst_amt = models.DecimalField(
        db_column="UTGST_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    utgst_rate = models.DecimalField(
        db_column="UTGST_RATE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    line_amt = models.DecimalField(
        db_column="LINE_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    tax_amt = models.DecimalField(
        db_column="TAX_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_amt = models.DecimalField(
        db_column="TOTAL_AMT",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    mrp = models.DecimalField(
        db_column="MRP", max_digits=50, decimal_places=2, blank=True, null=True
    )
    unit_price = models.DecimalField(
        db_column="UNIT_PRICE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ncr = models.DecimalField(
        db_column="NCR", max_digits=25, decimal_places=3, blank=True, null=True
    )
    dis = models.DecimalField(
        db_column="DIS", max_digits=50, decimal_places=2, blank=True, null=True
    )
    ship_price = models.DecimalField(
        db_column="SHIP_PRICE",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_list = models.CharField(
        db_column="PRICE_LIST", max_length=250, blank=True, null=True
    )
    header_id = models.DecimalField(
        db_column="HEADER_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    dealer_flag = models.CharField(
        db_column="DEALER_FLAG", max_length=250, blank=True, null=True
    )
    sale_type = models.CharField(
        db_column="SALE_TYPE", max_length=250, blank=True, null=True
    )
    plant_depo = models.CharField(
        db_column="PLANT_DEPO", max_length=250, blank=True, null=True
    )
    customer_id = models.DecimalField(
        db_column="CUSTOMER_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    customer_number = models.CharField(
        db_column="CUSTOMER_NUMBER", max_length=20, blank=True, null=True
    )
    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_DEPO_DISPATCH_DATA"


class TgtPlantDispatchData(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    tax_invoice_no = models.CharField(
        db_column="TAX_INVOICE_NO", max_length=250, blank=True, null=True
    )
    excise_invoice_no = models.CharField(
        db_column="EXCISE_INVOICE_NO", max_length=250, blank=True, null=True
    )
    ordered_qty = models.DecimalField(
        db_column="ORDERED_QTY", max_digits=20, decimal_places=3, blank=True, null=True
    )
    shipped_qty = models.DecimalField(
        db_column="SHIPPED_QTY", max_digits=20, decimal_places=3, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=200, blank=True, null=True
    )
    vehicle_no = models.CharField(
        db_column="VEHICLE_NO", max_length=250, blank=True, null=True
    )
    lr_gr_no = models.CharField(
        db_column="LR_GR_NO", max_length=250, blank=True, null=True
    )
    lr_gr_dt = models.DateTimeField(db_column="LR_GR_DT", blank=True, null=True)
    transporter = models.CharField(
        db_column="TRANSPORTER", max_length=500, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=200, blank=True, null=True
    )
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=200, blank=True, null=True
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=200, blank=True, null=True
    )
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=200, blank=True, null=True
    )
    sec_freight_term = models.CharField(
        db_column="SEC_FREIGHT_TERM", max_length=200, blank=True, null=True
    )
    inco_term = models.CharField(
        db_column="INCO_TERM", max_length=200, blank=True, null=True
    )
    d1 = models.CharField(db_column="D1", max_length=250, blank=True, null=True)
    d2 = models.CharField(db_column="D2", max_length=300, blank=True, null=True)
    d3 = models.CharField(db_column="D3", max_length=250, blank=True, null=True)
    primary_distance = models.DecimalField(
        db_column="PRIMARY_DISTANCE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    secondary_distance = models.CharField(
        db_column="SECONDARY_DISTANCE", max_length=200, blank=True, null=True
    )
    first_leg_distance = models.CharField(
        db_column="FIRST_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    second_leg_distance = models.CharField(
        db_column="SECOND_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    second_route_id = models.CharField(
        db_column="SECOND_ROUTE_ID", max_length=250, blank=True, null=True
    )
    third_leg_distance = models.CharField(
        db_column="THIRD_LEG_DISTANCE", max_length=200, blank=True, null=True
    )
    distance = models.DecimalField(
        db_column="DISTANCE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    frt_amt = models.CharField(
        db_column="FRT_AMT", max_length=250, blank=True, null=True
    )
    primary_frt = models.CharField(
        db_column="PRIMARY_FRT", max_length=250, blank=True, null=True
    )
    rail_frt_secondary = models.CharField(
        db_column="RAIL_FRT_SECONDARY", max_length=250, blank=True, null=True
    )
    di_so = models.CharField(db_column="DI_SO", max_length=200, blank=True, null=True)
    # delivery_id = models.DecimalField(
    #     db_column="DELIVERY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    # )
    delivery_id = models.ForeignKey(
        "TOebsWshNewDeliveries",
        on_delete=models.DO_NOTHING,
        to_field="delivery_id",
        db_column="DELIVERY_ID",
        blank=True,
        null=True,
        db_constraint=False,
    )
    token_no = models.CharField(
        db_column="TOKEN_NO", max_length=200, blank=True, null=True
    )
    chute_name = models.CharField(
        db_column="CHUTE_NAME", max_length=250, blank=True, null=True
    )
    di_date = models.DateTimeField(db_column="DI_DATE", blank=True, null=True)
    silo_no = models.CharField(
        db_column="SILO_NO", max_length=250, blank=True, null=True
    )
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    diesel_qty = models.CharField(
        db_column="DIESEL_QTY", max_length=20, blank=True, null=True
    )
    diesel_slip_no = models.DecimalField(
        db_column="DIESEL_SLIP_NO",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=200, blank=True, null=True
    )
    unloading_amt = models.DecimalField(
        db_column="UNLOADING_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    mm_comm = models.CharField(
        db_column="MM_COMM", max_length=200, blank=True, null=True
    )
    unloading = models.CharField(
        db_column="UNLOADING", max_length=200, blank=True, null=True
    )
    commission = models.DecimalField(
        db_column="COMMISSION",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    diesel_per_litre = models.DecimalField(
        db_column="DIESEL_PER_LITRE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=200, blank=True, null=True
    )
    cust_sub_category = models.CharField(
        db_column="CUST_SUB_CATEGORY", max_length=200, blank=True, null=True
    )
    customer_name = models.CharField(
        db_column="CUSTOMER_NAME", max_length=200, blank=True, null=True
    )
    consignee = models.CharField(
        db_column="CONSIGNEE", max_length=500, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=250, blank=True, null=True
    )
    ship_taluka = models.CharField(
        db_column="SHIP_TALUKA", max_length=250, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=250, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=250, blank=True, null=True
    )
    bill_city = models.CharField(
        db_column="BILL_CITY", max_length=250, blank=True, null=True
    )
    bill_district = models.CharField(
        db_column="BILL_DISTRICT", max_length=250, blank=True, null=True
    )
    bill_state = models.CharField(
        db_column="BILL_STATE", max_length=250, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=250, blank=True, null=True)
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=250, blank=True, null=True
    )
    order_number = models.DecimalField(
        db_column="ORDER_NUMBER", max_digits=25, decimal_places=0, blank=True, null=True
    )
    oe_creation_dt = models.DateTimeField(
        db_column="OE_CREATION_DT", blank=True, null=True
    )
    oe_punch_dt = models.DateTimeField(db_column="OE_PUNCH_DT", blank=True, null=True)
    oe_book_dt = models.DateTimeField(db_column="OE_BOOK_DT", blank=True, null=True)
    so_validity_dt = models.CharField(
        db_column="SO_VALIDITY_DT", max_length=300, blank=True, null=True
    )
    sgst_amt = models.DecimalField(
        db_column="SGST_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    sgst_rate = models.DecimalField(
        db_column="SGST_RATE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    cgst_amt = models.DecimalField(
        db_column="CGST_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    cgst_rate = models.DecimalField(
        db_column="CGST_RATE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    igst_amt = models.DecimalField(
        db_column="IGST_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    igst_rate = models.DecimalField(
        db_column="IGST_RATE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    utgst_amt = models.DecimalField(
        db_column="UTGST_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    utgst_rate = models.DecimalField(
        db_column="UTGST_RATE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    line_amt = models.DecimalField(
        db_column="LINE_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    tax_amt = models.DecimalField(
        db_column="TAX_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    total_amt = models.DecimalField(
        db_column="TOTAL_AMT",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    mrp = models.DecimalField(
        db_column="MRP", max_digits=22, decimal_places=3, blank=True, null=True
    )
    unit_price = models.DecimalField(
        db_column="UNIT_PRICE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    ncr = models.DecimalField(
        db_column="NCR", max_digits=25, decimal_places=3, blank=True, null=True
    )
    dis = models.DecimalField(
        db_column="DIS", max_digits=22, decimal_places=3, blank=True, null=True
    )
    ship_price = models.DecimalField(
        db_column="SHIP_PRICE",
        max_digits=22,
        decimal_places=3,
        blank=True,
        null=True,
    )
    price_list = models.CharField(
        db_column="PRICE_LIST", max_length=250, blank=True, null=True
    )
    header_id = models.DecimalField(
        db_column="HEADER_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    route_id = models.DecimalField(
        db_column="ROUTE_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    dealer_flag = models.CharField(
        db_column="DEALER_FLAG", max_length=250, blank=True, null=True
    )
    sale_type = models.CharField(
        db_column="SALE_TYPE", max_length=250, blank=True, null=True
    )
    plant_depo = models.CharField(
        db_column="PLANT_DEPO", max_length=250, blank=True, null=True
    )
    customer_id = models.DecimalField(
        db_column="CUSTOMER_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    customer_number = models.CharField(
        db_column="CUSTOMER_NUMBER", max_length=20, blank=True, null=True
    )
    party_id = models.DecimalField(
        db_column="PARTY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_PLANT_DISPATCH_DATA"


class TgtPlantDepoMaster(models.Model):
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
        db_column="CUST_ACCOUNT_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
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
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
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
    active = models.IntegerField(db_column="Active", blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=3000, blank=True, null=True)
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=500,
        decimal_places=0,
        blank=True,
        null=True,
    )
    region = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_PLANT_DEPO_MASTER"


class TgtPlantSiloCapacity(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    site = models.CharField(db_column="SITE", max_length=50, blank=True, null=True)
    code = models.CharField(db_column="CODE", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    capacity = models.DecimalField(
        db_column="CAPACITY", max_digits=20, decimal_places=2, blank=True, null=True
    )
    min_inventory = models.DecimalField(
        db_column="MIN_INVENTORY",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "TGT_PLANT_SILO_CAPACITY"


class TgtSlhServiceLevelDepo(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    header_id = models.DecimalField(
        db_column="HEADER_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    dispatched_qty = models.DecimalField(
        db_column="DISPATCHED_QTY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    di_so = models.CharField(db_column="DI_SO", max_length=200, blank=True, null=True)
    di_date = models.DateTimeField(db_column="DI_DATE", blank=True, null=True)
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    tax_inovice_date_d = models.DateField(blank=True, null=True)
    mode = models.CharField(max_length=200, blank=True, null=True)
    distance = models.DecimalField(
        db_column="DISTANCE", max_digits=50, decimal_places=2, blank=True, null=True
    )
    segment = models.CharField(
        db_column="SEGMENT", max_length=200, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=250, blank=True, null=True)
    taluka = models.CharField(db_column="TALUKA", max_length=250, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=250, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=250, blank=True, null=True)
    sale_type = models.CharField(
        db_column="SALE_TYPE", max_length=250, blank=True, null=True
    )
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    order_type = models.TextField(db_column="ORDER_TYPE", blank=True, null=True)
    excise_invoice_no = models.CharField(
        db_column="EXCISE_INVOICE_NO",
        max_length=250,
        blank=True,
        null=True,
        unique=True,
    )
    tax_invoice_no = models.CharField(
        db_column="TAX_INVOICE_NO", max_length=250, blank=True, null=True
    )
    delivery_id = models.DecimalField(
        db_column="DELIVERY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    oe_creation_date = models.DateTimeField(
        db_column="OE_CREATION_DATE", blank=True, null=True
    )
    order_number = models.DecimalField(
        max_digits=50, decimal_places=2, blank=True, null=True
    )
    di_date_0 = models.DateTimeField(db_column="di_date", blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=3000, blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    depo_name = models.TextField(blank=True, null=True)
    depo = models.TextField(blank=True, null=True)
    transit_time = models.DurationField(db_column="TRANSIT_TIME", blank=True, null=True)
    epod1_time = models.DateTimeField(db_column="EPOD1_TIME", blank=True, null=True)
    epod2_time = models.DateTimeField(db_column="EPOD2_TIME", blank=True, null=True)
    order_executable_time = models.DateTimeField(
        db_column="ORDER_EXECUTABLE_TIME", blank=True, null=True
    )
    delivery_delay = models.DurationField(
        db_column="DELIVERY_DELAY", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_SLH_SERVICE_LEVEL_DEPO"


class TgtSlhOrderPendency(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    delivery_id = models.IntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    delivery_detail_id = models.IntegerField(
        db_column="DELIVERY_DETAIL_ID", blank=True, null=True
    )
    order_type = models.TextField(db_column="ORDER_TYPE", blank=True, null=True)
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=300, blank=True, null=True
    )
    order_id = models.CharField(
        db_column="ORDER_ID", max_length=10050, blank=True, null=True
    )
    order_header_id = models.DecimalField(
        db_column="ORDER_HEADER_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_line_id = models.DecimalField(
        db_column="ORDER_LINE_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.TextField(db_column="BRAND", blank=True, null=True)
    org_id = models.DecimalField(
        db_column="ORG_ID", max_digits=50, decimal_places=2, blank=True, null=True
    )
    organization_id = models.DecimalField(
        db_column="ORGANIZATION_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    inventory_item_id = models.DecimalField(
        db_column="INVENTORY_ITEM_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dispatched_quantity = models.DecimalField(
        db_column="Dispatched Quantity",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order_quantity = models.DecimalField(
        db_column="ORDER_QUANTITY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    auto_tagged_mode = models.CharField(
        db_column="AUTO_TAGGED_MODE", max_length=240, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=240, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=240, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=2000, blank=True, null=True)
    order_date = models.DateTimeField(db_column="ORDER_DATE", blank=True, null=True)
    request_date = models.DateTimeField(db_column="REQUEST_DATE", blank=True, null=True)
    di_generated = models.DateTimeField(db_column="DI_GENERATED", blank=True, null=True)
    dilink_creation_dt = models.DateTimeField(
        db_column="DILINK_CREATION_DT", blank=True, null=True
    )
    tax_invoice_date = models.DateTimeField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    order_status = models.TextField(db_column="ORDER_STATUS", blank=True, null=True)
    cust_name = models.CharField(
        db_column="CUST_NAME", max_length=360, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER_TYPE", max_length=150, blank=True, null=True
    )
    cust_sub_cat = models.CharField(
        db_column="CUST_SUB_CAT", max_length=150, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=60, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=60, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=60, blank=True, null=True
    )
    full_address = models.TextField(db_column="Full Address", blank=True, null=True)
    vehicle_type = models.CharField(
        db_column="VEHICLE_TYPE", max_length=150, blank=True, null=True
    )
    vehicle_number = models.CharField(
        db_column="VEHICLE_NUMBER", max_length=150, blank=True, null=True
    )
    auto_tagged_source = models.TextField(
        db_column="AUTO_TAGGED_SOURCE", blank=True, null=True
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME", max_length=360, blank=True, null=True
    )
    ship_from_zone = models.CharField(
        db_column="Ship_from_zone", max_length=100, blank=True, null=True
    )
    warehouse = models.DecimalField(
        db_column="WAREHOUSE", max_digits=50, decimal_places=2, blank=True, null=True
    )
    ship_to_org_id = models.DecimalField(
        db_column="SHIP_TO_ORG_ID",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    freightterms = models.CharField(
        db_column="FREIGHTTERMS", max_length=3000, blank=True, null=True
    )
    fob = models.CharField(db_column="FOB", max_length=3000, blank=True, null=True)
    token_id = models.DecimalField(
        db_column="TOKEN_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    route = models.CharField(db_column="ROUTE", max_length=100, blank=True, null=True)
    source_location_id = models.DecimalField(
        db_column="SOURCE_LOCATION_ID",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    shipinglocation = models.BigIntegerField(
        db_column="SHIPINGLOCATION", blank=True, null=True
    )
    sales_order_type = models.CharField(
        db_column="SALES_ORDER_TYPE", max_length=240, blank=True, null=True
    )
    released_date = models.DateTimeField(
        db_column="RELEASED_DATE", blank=True, null=True
    )
    delivery_due_date = models.DateTimeField(
        db_column="DELIVERY_DUE_DATE", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_SLH_ORDER_PENDENCY"


class TgtMrnData(models.Model):
    """tgt mrn data model"""

    order_number = models.DecimalField(
        db_column="ORDER_NUMBER", max_digits=40, decimal_places=0, blank=True, null=True
    )  # order number
    header_id = models.DecimalField(
        db_column="HEADER_ID", max_digits=40, decimal_places=0, blank=True, null=True
    )
    line_id = models.DecimalField(
        db_column="LINE_ID", max_digits=40, decimal_places=0, blank=True, null=True
    )
    incoterm = models.CharField(
        db_column="INCOTERM", max_length=200, blank=True, null=True
    )
    freight_term = models.CharField(
        db_column="FREIGHT_TERM", max_length=200, blank=True, null=True
    )
    customer_code = models.CharField(
        db_column="CUSTOMER_CODE", max_length=200, blank=True, null=True
    )
    customer = models.CharField(
        db_column="CUSTOMER", max_length=200, blank=True, null=True
    )
    category_code = models.CharField(
        db_column="CATEGORY_CODE", max_length=200, blank=True, null=True
    )
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=200, blank=True, null=True
    )
    ship_tehsil = models.CharField(
        db_column="SHIP_TEHSIL", max_length=200, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=200, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=200, blank=True, null=True
    )
    mrp = models.CharField(db_column="MRP", max_length=200, blank=True, null=True)
    pack_typ = models.CharField(
        db_column="PACK_TYP", max_length=200, blank=True, null=True
    )  # packagingcocatinationpack_mat+pack_typ
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=200, blank=True, null=True
    )
    c = models.CharField(db_column="C", max_length=200, blank=True, null=True)
    org_id = models.DecimalField(
        db_column="ORG_ID", max_digits=40, decimal_places=0, blank=True, null=True
    )
    delivery_id = models.DecimalField(
        db_column="DELIVERY_ID", max_digits=40, decimal_places=0, blank=True, null=True
    )  # di number
    delivery_detail_id = models.DecimalField(
        db_column="DELIVERY_DETAIL_ID",
        max_digits=40,
        decimal_places=0,
        blank=True,
        null=True,
    )
    trnsp_code = models.DecimalField(
        db_column="TRNSP_CODE", max_digits=40, decimal_places=0, blank=True, null=True
    )
    trnsp_name = models.CharField(
        db_column="TRNSP_NAME", max_length=200, blank=True, null=True
    )  # transport name
    token_no = models.DecimalField(
        db_column="TOKEN_NO", max_digits=40, decimal_places=0, blank=True, null=True
    )
    tr_number = models.CharField(
        db_column="TR_NUMBER", max_length=200, blank=True, null=True
    )
    tr_rr_no = models.CharField(
        db_column="TR_RR_NO", max_length=200, blank=True, null=True
    )
    challan_no = models.CharField(
        db_column="CHALLAN_NO", max_length=200, blank=True, null=True
    )
    dispmode = models.CharField(
        db_column="DISPMODE", max_length=200, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=200, blank=True, null=True
    )
    truck_number = models.CharField(
        db_column="TRUCK_NUMBER", max_length=200, blank=True, null=True
    )  # tkruck number
    pri_frt = models.DecimalField(
        db_column="PRI_FRT", max_digits=50, decimal_places=2, blank=True, null=True
    )
    pri_frt_rail = models.CharField(
        db_column="PRI_FRT_RAIL", max_length=200, blank=True, null=True
    )
    ordered_item = models.CharField(
        db_column="ORDERED_ITEM", max_length=200, blank=True, null=True
    )
    order_quantity_uom = models.CharField(
        db_column="ORDER_QUANTITY_UOM", max_length=200, blank=True, null=True
    )
    ordered_date = models.DateTimeField(db_column="ORDERED_DATE", blank=True, null=True)
    excise_invoice_no = models.CharField(
        db_column="EXCISE_INVOICE_NO", max_length=200, blank=True, null=True
    )
    excise_invoice_date = models.DateTimeField(
        db_column="EXCISE_INVOICE_DATE", blank=True, null=True
    )
    actual_departure_date = models.DateTimeField(
        db_column="ACTUAL_DEPARTURE_DATE", blank=True, null=True
    )  # exp deleviry date
    attribute14 = models.CharField(
        db_column="ATTRIBUTE14", max_length=200, blank=True, null=True
    )
    attribute16 = models.CharField(
        db_column="ATTRIBUTE16", max_length=200, blank=True, null=True
    )
    shipment_num = models.CharField(
        db_column="SHIPMENT_NUM", max_length=200, blank=True, null=True
    )
    receipt_number = models.CharField(
        db_column="RECEIPT_NUMBER", max_length=100, blank=True, null=True
    )
    from_org_name = models.CharField(
        db_column="FROM_ORG_NAME", max_length=200, blank=True, null=True
    )  # source
    route_id = models.CharField(
        db_column="ROUTE_ID", max_length=200, blank=True, null=True
    )
    sale_type = models.CharField(
        db_column="SALE_TYPE", max_length=200, blank=True, null=True
    )
    ordered_quantity = models.DecimalField(
        db_column="ORDERED_QUANTITY",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )  # orderqua
    quantity_shipped = models.DecimalField(
        db_column="QUANTITY_SHIPPED",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    quantity_received = models.DecimalField(
        db_column="QUANTITY_RECEIVED",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    # receipt_date = models.DateTimeField(
    #     db_column="RECEIPT_DATE", blank=True, null=True
    # )  # mrn punch date
    receipt_date = models.DateTimeField(db_column="RECEIPT_DATE", blank=True, null=True)
    id = models.BigAutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TGT_MRN_DATA"


class TgtRakeLoading(models.Model):
    WAIVER_DEPOSITED_STATUS_CHOICES = (
        ("Before", "BEFORE"),
        ("After", "AFTER"),
    )

    rake_id = models.BigAutoField(db_column="RAKE_ID", primary_key=True)
    dispatch_from_plant = models.CharField(
        db_column="DISPATCH_FROM_PLANT", max_length=250
    )
    rake_type = models.CharField(db_column="RAKE_TYPE", max_length=100)
    placement_date = models.DateTimeField(db_column="PLACEMENT_DATE")
    actual_release_date = models.DateTimeField(
        db_column="ACTUAL_RELEASE_DATE", blank=True, null=True
    )
    total_time = models.DecimalField(
        db_column="TOTAL_TIME", max_digits=20, decimal_places=2, default=0
    )
    free_hours = models.DecimalField(
        db_column="FREE_HOURS", max_digits=20, decimal_places=2, default=0
    )
    material_cleaning_date = models.DateField(
        db_column="MATERIAL_CLEANING_DATE", blank=True, null=True
    )
    total_demm_hours = models.DecimalField(
        db_column="TOTAL_DEMM_HOURS",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_demm_amount = models.DecimalField(
        db_column="TOTAL_DEMM_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    waiver_percent = models.DecimalField(
        db_column="WAIVER_PERCENT", max_digits=20, decimal_places=2, default=0
    )
    waiver_amount = models.DecimalField(
        db_column="WAIVER_AMOUNT", max_digits=20, decimal_places=2, default=0
    )
    sgst = models.DecimalField(
        db_column="SGST", max_digits=20, decimal_places=2, default=0
    )
    cgst = models.DecimalField(
        db_column="CGST", max_digits=20, decimal_places=2, default=0
    )
    igst = models.DecimalField(
        db_column="IGST", max_digits=20, decimal_places=2, default=0
    )
    sgst_amt = models.DecimalField(
        db_column="SGST_AMT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    cgst_amt = models.DecimalField(
        db_column="CGST_AMT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    igst_amt = models.DecimalField(
        db_column="IGST_AMT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    total_gst_amt = models.DecimalField(
        db_column="TOTAL_GST_AMT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_amount = models.DecimalField(
        db_column="TOTAL_AMOUNT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    dispatch_date = models.DateTimeField(
        db_column="DISPATCH_DATE", blank=True, null=True
    )
    rr_no = models.CharField(db_column="RR_NO", max_length=50, blank=True, null=True)
    demm_rate_per_wagon = models.IntegerField(
        db_column="DEMM_RATE_PER_WAGON", default=0
    )
    no_of_wagons = models.IntegerField(db_column="NO_OF_WAGONS", default=0)
    attachment = models.TextField(db_column="ATTACHMENT", blank=True, null=True)
    rake_capacity = models.IntegerField(
        db_column="RAKE_CAPACITY", blank=True, null=True
    )
    free_time = models.DateTimeField(db_column="FREE_TIME", blank=True, null=True)
    reason_for_demm = models.CharField(
        db_column="REASON_FOR_DEMM", max_length=200, blank=True, null=True
    )
    siding_name = models.CharField(
        db_column="SIDING_NAME", max_length=360, blank=True, null=True
    )
    siding_code = models.CharField(
        db_column="SIDING_CODE", max_length=360, blank=True, null=True
    )
    wv_case_no = models.CharField(
        db_column="WV_CASE_NO", max_length=360, blank=True, null=True
    )
    wv_deposited_status = models.CharField(
        db_column="WV_DEPOSITED_STATUS",
        max_length=360,
        choices=WAIVER_DEPOSITED_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    wv_deposited_amount = models.DecimalField(
        db_column="WV_DEPOSITED_AMOUNT", max_digits=20, decimal_places=2, default=0
    )
    dm_final_amt_after_wv = models.DecimalField(
        db_column="DM_FINAL_AMT_AFTER_WV", max_digits=20, decimal_places=2, default=0
    )
    waiver_status = models.CharField(
        db_column="WAIVER_STATUS", max_length=360, blank=True, null=True
    )
    other_charges = models.DecimalField(
        db_column="OTHER_CHARGES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "TGT_RAKE_LOADING"


class TgtRakeLoadingDetails(models.Model):
    rld_id = models.BigAutoField(db_column="RLD_ID", primary_key=True)
    rake = models.ForeignKey(
        TgtRakeLoading,
        models.DO_NOTHING,
        db_column="RAKE_ID",
        related_name="loading_details",
    )
    segment = models.CharField(db_column="SEGMENT", max_length=250)
    org_id = models.BigIntegerField(db_column="ORG_ID", choices=BrandChoices.choices)
    inventory_item_id = models.BigIntegerField(
        db_column="INVENTORY_ITEM_ID", choices=InventoryItemIdChoices.choices
    )
    no_of_wagons = models.BigIntegerField(db_column="NO_OF_WAGONS", default=0)
    qty_dispatch_frm_plant = models.DecimalField(
        db_column="QTY_DISPATCH_FRM_PLANT", max_digits=20, decimal_places=2
    )
    qty_net_received = models.DecimalField(
        db_column="QTY_NET_RECEIVED", max_digits=20, decimal_places=2
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    packing_type = models.CharField(
        db_column="PACKING_TYPE", max_length=360, blank=True, null=True
    )
    rr_no = models.IntegerField(db_column="RR_NO", blank=True, null=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=50, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=25, blank=True, null=True
    )
    ship_to_depot = models.CharField(
        db_column="SHIP_TO_DEPOT", max_length=40, blank=True, null=True
    )
    excise_invoice_no = models.CharField(
        db_column="EXCISE_INVOICE_NO", max_length=250, blank=True, null=True
    )
    siding_name = models.CharField(
        db_column="SIDING_NAME", max_length=360, blank=True, null=True
    )
    siding_code = models.CharField(
        db_column="SIDING_CODE", max_length=240, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_RAKE_LOADING_DETAILS"


class TgtRakeCharges(models.Model):
    rc_id = models.BigAutoField(db_column="RC_ID", primary_key=True)
    rld = models.OneToOneField(
        TgtRakeLoadingDetails,
        models.DO_NOTHING,
        db_column="RLD_ID",
        related_name="rake_charges",
    )
    dm_hours = models.DecimalField(
        db_column="DM_HOURS", max_digits=20, decimal_places=2, default=0
    )
    dm_total_wgn_placed = models.DecimalField(
        db_column="DM_TOTAL_WGN_PLACED",
        max_digits=10,
        decimal_places=0,
        default=0,
    )
    dm_rate_per_wagon = models.DecimalField(
        db_column="DM_RATE_PER_WAGON", max_digits=22, decimal_places=2, default=0
    )
    dm_cgst_percent = models.DecimalField(
        db_column="DM_CGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    dm_sgst_percent = models.DecimalField(
        db_column="DM_SGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    dm_igst_percent = models.DecimalField(
        db_column="DM_IGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    dm_cgst_amt = models.DecimalField(
        db_column="DM_CGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    dm_sgst_amt = models.DecimalField(
        db_column="DM_SGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    dm_igst_amt = models.DecimalField(
        db_column="DM_IGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    dm_total_gst = models.DecimalField(
        db_column="DM_TOTAL_GST", max_digits=22, decimal_places=2, default=0
    )
    total_demurrage_amount = models.DecimalField(
        db_column="TOTAL_DEMURRAGE_AMOUNT", max_digits=22, decimal_places=2, default=0
    )
    dm_reason = models.CharField(
        db_column="DM_REASON", max_length=360, blank=True, null=True
    )
    wf_hours = models.DecimalField(
        db_column="WF_HOURS", max_digits=20, decimal_places=2, default=0
    )
    wf_total_wgn_placed = models.DecimalField(
        db_column="WF_TOTAL_WGN_PLACED", max_digits=10, decimal_places=0, default=0
    )
    wf_rate_per_wagon = models.DecimalField(
        db_column="WF_RATE_PER_WAGON", max_digits=22, decimal_places=2, default=0
    )
    wf_cgst_percent = models.DecimalField(
        db_column="WF_CGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    wf_sgst_percent = models.DecimalField(
        db_column="WF_SGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    wf_igst_percent = models.DecimalField(
        db_column="WF_IGST_PERCENT", max_digits=22, decimal_places=2, default=0
    )
    wf_cgst_amt = models.DecimalField(
        db_column="WF_CGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    wf_sgst_amt = models.DecimalField(
        db_column="WF_SGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    wf_igst_amt = models.DecimalField(
        db_column="WF_IGST_AMT", max_digits=22, decimal_places=2, default=0
    )
    wf_total_gst = models.DecimalField(
        db_column="WF_TOTAL_GST", max_digits=22, decimal_places=2, default=0
    )
    total_wharfage_amount = models.DecimalField(
        db_column="TOTAL_WHARFAGE_AMOUNT", max_digits=22, decimal_places=2, default=0
    )
    wf_reason = models.CharField(
        db_column="WF_REASON", max_length=360, blank=True, null=True
    )
    crwc_wharehouse_charges = models.DecimalField(
        db_column="CRWC_WHAREHOUSE_CHARGES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    storage_charges_reason = models.CharField(
        db_column="STORAGE_CHARGES_REASON", max_length=360, blank=True, null=True
    )
    rake_shunting_remark = models.CharField(
        db_column="RAKE_SHUNTING_REMARK", max_length=360, blank=True, null=True
    )
    wheather_conditions = models.CharField(
        db_column="WHEATHER_CONDITIONS", max_length=360, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    placement_time_at_depot_siding = models.DateTimeField(
        db_column="PLACEMENT_TIME_AT_DEPOT_SIDING", blank=True, null=True
    )
    free_hours = models.BigIntegerField(db_column="FREE_HOURS", default=0)
    free_time = models.DateTimeField(db_column="FREE_TIME", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TGT_RAKE_CHARGES"


class TgtRakeUnloadingDetails(models.Model):
    DM_DEPOSITED_STATUS_CHOICES = (
        ("Before", "BEFORE"),
        ("After", "AFTER"),
    )

    rk_unload_id = models.BigAutoField(db_column="RK_UNLOAD_ID", primary_key=True)
    rld = models.OneToOneField(
        TgtRakeLoadingDetails,
        models.CASCADE,
        db_column="RLD_ID",
        related_name="unloading_details",
    )
    depo_org_id = models.CharField(
        db_column="DEPO_ORG_ID", max_length=100, blank=True, null=True
    )
    transit_qty = models.DecimalField(
        db_column="TRANSIT_QTY", max_digits=22, decimal_places=2, default=0
    )
    shortage_qty = models.DecimalField(
        db_column="SHORTAGE_QTY", max_digits=22, decimal_places=2, default=0
    )
    excess_qty = models.DecimalField(
        db_column="EXCESS_QTY", max_digits=22, decimal_places=2, default=0
    )
    cut_torn_qty = models.DecimalField(
        db_column="CUT_TORN_QTY", max_digits=22, decimal_places=2, default=0
    )
    set_damage_qty = models.DecimalField(
        db_column="SET_DAMAGE_QTY",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    st_ct_disp_qty_rly_yard = models.DecimalField(
        db_column="ST_CT_DISP_QTY_RLY_YARD",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    fresh_qty_from_rly_yard = models.DecimalField(
        db_column="FRESH_QTY_FROM_RLY_YARD",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    fresh_qty_rec_frm_oth_depo = models.DecimalField(
        db_column="FRESH_QTY_REC_FRM_OTH_DEPO",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    fresh_qty_dis_to_oth_depo = models.DecimalField(
        db_column="FRESH_QTY_DIS_TO_OTH_DEPO",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    damage_qty_shifted_to_godown = models.DecimalField(
        db_column="DAMAGE_QTY_SHIFTED_TO_GODOWN",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    unloading_remarks = models.CharField(
        db_column="UNLOADING_REMARKS", max_length=520, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    free_time = models.DecimalField(
        db_column="FREE_TIME", max_digits=20, decimal_places=2, blank=True, null=True
    )
    material_cleaning_date = models.DateField(
        db_column="MATERIAL_CLEANING_DATE", blank=True, null=True
    )
    placement_date = models.DateTimeField(
        db_column="PLACEMENT_DATE", blank=True, null=True
    )
    fresh_qty_shifted_to_godown = models.DecimalField(
        db_column="FRESH_QTY_SHIFTED_TO_GODOWN",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    actual_release = models.DateTimeField(
        db_column="ACTUAL_RELEASE", blank=True, null=True
    )
    material_clearing_from_siding = models.DateTimeField(
        db_column="MATERIAL_CLEARING_FROM_SIDING", blank=True, null=True
    )
    qty_placed = models.DecimalField(
        db_column="QTY_PLACED", max_digits=22, decimal_places=2, blank=True, null=True
    )
    free_time_for_rake_release = models.DateTimeField(
        db_column="FREE_TIME_FOR_RAKE_RELEASE", blank=True, null=True
    )
    free_time_for_material_clearance = models.DateTimeField(
        db_column="FREE_TIME_FOR_MATERIAL_CLEARANCE", blank=True, null=True
    )
    actual_time_for_rake_release = models.DateTimeField(
        db_column="ACTUAL_TIME_FOR_RAKE_RELEASE", blank=True, null=True
    )
    dm_case_no = models.CharField(
        db_column="DM_CASE_NO", max_length=200, blank=True, null=True
    )
    dm_deposited_status = models.CharField(
        db_column="DM_DEPOSITED_STATUS",
        max_length=360,
        blank=True,
        null=True,
        choices=DM_DEPOSITED_STATUS_CHOICES,
    )
    dm_deposited_amount = models.DecimalField(
        db_column="DM_DEPOSITED_AMOUNT",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    dm_waiver_percentage = models.BigIntegerField(
        db_column="DM_WAIVER_PERCENTAGE", default=0
    )
    dm_waiver_amount = models.DecimalField(
        db_column="DM_WAIVER_AMOUNT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dm_final_amount = models.DecimalField(
        db_column="DM_FINAL_AMOUNT",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    wf_case_no = models.CharField(
        db_column="WF_CASE_NO", max_length=360, blank=True, null=True
    )
    wf_deposited_status = models.CharField(
        db_column="WF_DEPOSITED_STATUS",
        max_length=360,
        blank=True,
        null=True,
        choices=DM_DEPOSITED_STATUS_CHOICES,
    )
    wf_deposited_amount = models.DecimalField(
        db_column="WF_DEPOSITED_AMOUNT",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    wf_waiver_percentage = models.BigIntegerField(
        db_column="WF_WAIVER_PERCENTAGE", default=0
    )
    wf_waiver_amount = models.DecimalField(
        db_column="WF_WAIVER_AMOUNT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_final_amount = models.DecimalField(
        db_column="WF_FINAL_AMOUNT",
        max_digits=22,
        decimal_places=2,
        default=0,
    )
    dm_waiver_status = models.CharField(
        db_column="DM_WAIVER_STATUS", max_length=100, blank=True, null=True
    )
    wf_waiver_status = models.CharField(
        db_column="WF_WAIVER_STATUS", max_length=100, blank=True, null=True
    )
    rake = models.ForeignKey(
        "TgtRakeLoading", models.DO_NOTHING, db_column="RAKE_ID", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TGT_RAKE_UNLOADING_DETAILS"


class TgtRakeDisposals(models.Model):
    rd_rk_unload_id = models.BigAutoField(db_column="RD_RK_UNLOAD_ID", primary_key=True)
    rk_unload = models.ForeignKey(
        "TgtRakeUnloadingDetails", models.DO_NOTHING, db_column="RK_UNLOAD_ID"
    )
    qty_unloaded_at_platform = models.DecimalField(
        db_column="QTY_UNLOADED_AT_PLATFORM",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    qty_unloaded_dir_to_truck = models.DecimalField(
        db_column="QTY_UNLOADED_DIR_TO_TRUCK",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    qty_shifted_to_crwc = models.DecimalField(
        db_column="QTY_SHIFTED_TO_CRWC",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    qty_sold_dir_to_parties = models.DecimalField(
        db_column="QTY_SOLD_DIR_TO_PARTIES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    qty_shifted_to_godown = models.DecimalField(
        db_column="QTY_SHIFTED_TO_GODOWN",
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
        db_table = "TGT_RAKE_DISPOSALS"


class TgtDayWiseLifting(models.Model):
    daywise_lifting_id = models.BigAutoField(
        db_column="DAYWISE_LIFTING_ID", primary_key=True
    )
    rk_unload = models.ForeignKey(
        TgtRakeUnloadingDetails,
        models.DO_NOTHING,
        db_column="RK_UNLOAD_ID",
        related_name="daywise_liftings",
        blank=True,
        null=True,
    )
    lifting_date = models.DateField(db_column="LIFTING_DATE", blank=True, null=True)
    lifting_day_number = models.DecimalField(
        db_column="LIFTING_DAY_NUMBER",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    lifting_qty = models.DecimalField(
        db_column="LIFTING_QTY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    lifting_uom = models.CharField(
        db_column="LIFTING_UOM", max_length=50, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    opening_quantity = models.DecimalField(
        db_column="OPENING_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    closing_quantity = models.DecimalField(
        db_column="CLOSING_QUANTITY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "TGT_DAYWISE_LIFTING"


class NewFreightInitiation(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    near_by_route_code = models.CharField(
        db_column="NEAR_BY_ROUTE_CODE", max_length=360, blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=360, blank=True, null=True)
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=360, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=360, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=360, blank=True, null=True
    )
    ship_taluka = models.CharField(
        db_column="SHIP_TALUKA", max_length=360, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=360, blank=True, null=True)
    segment = models.CharField(
        db_column="SEGMENT", max_length=360, blank=True, null=True
    )
    dispatch_type = models.CharField(
        db_column="DISPATCH_TYPE", max_length=360, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=360, blank=True, null=True
    )
    current_freight = models.DecimalField(
        db_column="CURRENT_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_distance = models.DecimalField(
        db_column="CURRENT_DISTANCE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    new_distance = models.DecimalField(
        db_column="NEW_DISTANCE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    additional_distance = models.DecimalField(
        db_column="ADDITIONAL_DISTANCE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    terrain_suggestion = models.CharField(
        db_column="TERRAIN_SUGGESTION", max_length=360, blank=True, null=True
    )
    to_be_freight = models.DecimalField(
        db_column="TO_BE_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ptpk_for_add_kms = models.DecimalField(
        db_column="PTPK_FOR_ADD_KMS",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    applicability_date = models.DateTimeField(
        db_column="APPLICABILITY_DATE", blank=True, null=True
    )
    description = models.CharField(
        db_column="DESCRIPTION", max_length=360, blank=True, null=True
    )
    reason = models.CharField(db_column="REASON", max_length=360, blank=True, null=True)
    next_approver = models.CharField(
        db_column="NEXT_APPROVER", max_length=360, blank=True, null=True
    )
    related_doc = models.FileField(
        db_column="RELATED_DOC",
        max_length=360,
        upload_to=r"static\media\handling_agent\new_freight_initiation",
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="STATUS",
        max_length=360,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING.value,
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    approval_type = models.CharField(
        db_column="APPROVAL_TYPE", max_length=360, blank=True, null=True
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    persona = models.CharField(
        db_column="PERSONA", max_length=540, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NEW_FREIGHT_INITIATION"


class FreightChangeInitiation(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    route_code = models.CharField(
        db_column="ROUTE_CODE", max_length=360, blank=True, null=True
    )
    plant = models.CharField(db_column="PLANT", max_length=360, blank=True, null=True)
    ship_city = models.CharField(
        db_column="SHIP_CITY", max_length=360, blank=True, null=True
    )
    ship_state = models.CharField(
        db_column="SHIP_STATE", max_length=360, blank=True, null=True
    )
    ship_district = models.CharField(
        db_column="SHIP_DISTRICT", max_length=360, blank=True, null=True
    )
    ship_taluka = models.CharField(
        db_column="SHIP_TALUKA", max_length=360, blank=True, null=True
    )
    mode = models.CharField(db_column="MODE", max_length=360, blank=True, null=True)
    segment = models.CharField(
        db_column="SEGMENT", max_length=360, blank=True, null=True
    )
    dispatch_type = models.CharField(
        db_column="DISPATCH_TYPE", max_length=360, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=360, blank=True, null=True
    )
    current_freight = models.DecimalField(
        db_column="CURRENT_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    to_be_freight = models.DecimalField(
        db_column="TO_BE_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    applicability_date = models.DateTimeField(
        db_column="APPLICABILITY_DATE", blank=True, null=True
    )
    description = models.CharField(
        db_column="DESCRIPTION", max_length=360, blank=True, null=True
    )
    reason = models.CharField(db_column="REASON", max_length=360, blank=True, null=True)
    current_distance = models.IntegerField(
        db_column="CURRENT_DISTANCE", blank=True, null=True
    )
    to_be_distance = models.IntegerField(
        db_column="TO_BE_DISTANCE", blank=True, null=True
    )
    status = models.CharField(
        db_column="STATUS",
        max_length=360,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.PENDING.value,
    )
    approved_by = models.CharField(
        db_column="APPROVED_BY", max_length=540, blank=True, null=True
    )
    persona = models.CharField(
        db_column="PERSONA", max_length=360, blank=True, null=True
    )
    approval_type = models.CharField(
        db_column="APPROVAL_TYPE", max_length=360, blank=True, null=True
    )
    contribution = models.DecimalField(
        db_column="CONTRIBUTION", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FREIGHT_CHANGE_INITIATION"


class TOebsFndLookupValues(models.Model):
    lookup_type = models.CharField(
        db_column="LOOKUP_TYPE", max_length=300, blank=True, null=True
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=300, blank=True, null=True
    )
    lookup_code = models.CharField(
        db_column="LOOKUP_CODE", max_length=300, blank=True, null=True
    )
    meaning = models.CharField(
        db_column="MEANING", max_length=800, blank=True, null=True
    )
    description = models.CharField(
        db_column="DESCRIPTION", max_length=240, blank=True, null=True
    )
    enabled_flag = models.CharField(
        db_column="ENABLED_FLAG", max_length=240, blank=True, null=True
    )
    start_date_active = models.DateTimeField(
        db_column="START_DATE_ACTIVE", blank=True, null=True
    )
    end_date_active = models.DateTimeField(
        db_column="END_DATE_ACTIVE", blank=True, null=True
    )
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=15, decimal_places=0, blank=True, null=True
    )
    creation_date = models.DateTimeField(
        db_column="CREATION_DATE", blank=True, null=True
    )
    last_updated_by = models.DecimalField(
        db_column="LAST_UPDATED_BY",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    last_update_login = models.DecimalField(
        db_column="LAST_UPDATE_LOGIN",
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
    )
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", blank=True, null=True
    )
    source_lang = models.CharField(
        db_column="SOURCE_LANG", max_length=400, blank=True, null=True
    )
    security_group_id = models.BigIntegerField(
        db_column="SECURITY_GROUP_ID", blank=True, null=True
    )
    view_application_id = models.BigIntegerField(
        db_column="VIEW_APPLICATION_ID", blank=True, null=True
    )
    territory_code = models.CharField(
        db_column="TERRITORY_CODE", max_length=200, blank=True, null=True
    )
    attribute_category = models.CharField(
        db_column="ATTRIBUTE_CATEGORY", max_length=300, blank=True, null=True
    )
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=150, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=150, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=150, blank=True, null=True
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
    tag = models.CharField(db_column="TAG", max_length=150, blank=True, null=True)
    leaf_node = models.CharField(
        db_column="LEAF_NODE", max_length=100, blank=True, null=True
    )
    zd_edition_name = models.CharField(
        db_column="ZD_EDITION_NAME", max_length=300, blank=True, null=True
    )
    zd_sync = models.CharField(
        db_column="ZD_SYNC", max_length=300, blank=True, null=True
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
        db_table = "T_OEBS_FND_LOOKUP_VALUES"
        unique_together = (
            (
                "lookup_type",
                "view_application_id",
                "lookup_code",
                "security_group_id",
                "security_group_id",
                "language",
                "zd_edition_name",
            ),
        )


class FdAnnualCharges(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    road_permit_pa = models.BigIntegerField(
        db_column="ROAD_PERMIT_PA", blank=True, null=True
    )
    road_tax_pa = models.BigIntegerField(db_column="ROAD_TAX_PA", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_ANNUAL_CHARGES"


class FdCapexComputations(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    capacity = models.FloatField(db_column="CAPACITY", blank=True, null=True)
    cost_of_truck = models.BigIntegerField(
        db_column="COST_OF_TRUCK", blank=True, null=True
    )
    residual_value_of_truck = models.FloatField(
        db_column="RESIDUAL_VALUE_OF_TRUCK", blank=True, null=True
    )
    loan_amount = models.FloatField(db_column="LOAN_AMOUNT", blank=True, null=True)
    amount_paid_by_self = models.FloatField(
        db_column="AMOUNT_PAID_BY_SELF", blank=True, null=True
    )
    current_value_of_truck = models.FloatField(
        db_column="CURRENT_VALUE_OF_TRUCK", blank=True, null=True
    )
    depreciation_per_month = models.FloatField(
        db_column="DEPRECIATION_PER_MONTH", blank=True, null=True
    )
    interest_cost_per_month = models.FloatField(
        db_column="INTEREST_COST_PER_MONTH", blank=True, null=True
    )
    created_by = models.FloatField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_CAPEX_COMPUTATIONS"


class FdCostProfile(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    direct_ptpk = models.FloatField(db_column="DIRECT_PTPK", blank=True, null=True)
    semi_variable_ptpk = models.FloatField(
        db_column="SEMI_VARIABLE_PTPK", blank=True, null=True
    )
    fixed_ptpk = models.FloatField(db_column="FIXED_PTPK", blank=True, null=True)
    profit_ptpk = models.FloatField(db_column="PROFIT_PTPK", blank=True, null=True)
    total_ptpk = models.FloatField(db_column="TOTAL_PTPK", blank=True, null=True)
    freight_per_tonne = models.BigIntegerField(
        db_column="FREIGHT_PER_TONNE", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_COST_PROFILE"


class FdDirectCostComputations(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    tyre_cost_per_km = models.FloatField(
        db_column="TYRE_COST_PER_KM", blank=True, null=True
    )
    net_mileage = models.FloatField(db_column="NET_MILEAGE", blank=True, null=True)
    diesel_cost_per_km = models.FloatField(
        db_column="DIESEL_COST_PER_KM", blank=True, null=True
    )
    fuel_tyre_cost = models.FloatField(
        db_column="FUEL_TYRE_COST", blank=True, null=True
    )
    running_cost_per_month = models.FloatField(
        db_column="RUNNING_COST_PER_MONTH", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_DIRECT_COST_COMPUTATIONS"


class FdFinancialFeasibilityCheck(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    emi = models.FloatField(db_column="EMI", blank=True, null=True)
    cash_inflow = models.FloatField(db_column="CASH_INFLOW", blank=True, null=True)
    cash_flow_per_month = models.FloatField(
        db_column="CASH_FLOW_PER_MONTH", blank=True, null=True
    )
    irr = models.FloatField(db_column="IRR", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_FINANCIAL_FEASIBILITY_CHECK"


class FdFixedCostComputations(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    road_permit_per_month = models.BigIntegerField(
        db_column="ROAD_PERMIT_PER_MONTH", blank=True, null=True
    )
    road_tax_per_month = models.FloatField(
        db_column="ROAD_TAX_PER_MONTH", blank=True, null=True
    )
    insurance_per_month = models.FloatField(
        db_column="INSURANCE_PER_MONTH", blank=True, null=True
    )
    working_capital_interest_cost_per_month = models.BigIntegerField(
        db_column="WORKING_CAPITAL_INTEREST_COST_PER_MONTH", blank=True, null=True
    )
    other_fixed_costs = models.BigIntegerField(
        db_column="OTHER_FIXED_COSTS", blank=True, null=True
    )
    total_fixed_cost_per_month = models.FloatField(
        db_column="TOTAL_FIXED_COST_PER_MONTH", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    depreciation_per_month = models.FloatField(
        db_column="DEPRECIATION_PER_MONTH", blank=True, null=True
    )
    interest_cost_per_month = models.FloatField(
        db_column="INTEREST_COST_PER_MONTH", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "FD_FIXED_COST_COMPUTATIONS"


class FdFuelCharges(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    mileage_with_load = models.FloatField(
        db_column="MILEAGE_WITH_LOAD", blank=True, null=True
    )
    mileage_without_load = models.FloatField(
        db_column="MILEAGE_WITHOUT_LOAD", blank=True, null=True
    )
    diesel_cost = models.FloatField(db_column="DIESEL_COST", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_FUEL_CHARGES"


class FdLocationOverview(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
    )
    city = models.CharField(db_column="CITY", max_length=540, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_LOCATION_OVERVIEW"


class FdMonthlyCharges(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    driver_cleaner_monthly_salary = models.BigIntegerField(
        db_column="DRIVER_CLEANER_MONTHLY_SALARY", blank=True, null=True
    )
    driver_cleaner_monthly_bhatta = models.BigIntegerField(
        db_column="DRIVER_CLEANER_MONTHLY_BHATTA", blank=True, null=True
    )
    maintenance_per_month = models.BigIntegerField(
        db_column="MAINTENANCE_PER_MONTH", blank=True, null=True
    )
    gps_per_month = models.BigIntegerField(
        db_column="GPS_PER_MONTH", blank=True, null=True
    )
    other_overhead_expenses = models.BigIntegerField(
        db_column="OTHER_OVERHEAD_EXPENSES", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_MONTHLY_CHARGES"


class FdOtherVariableCharges(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    route_expenses = models.BigIntegerField(
        db_column="ROUTE_EXPENSES", blank=True, null=True
    )
    toll = models.BigIntegerField(db_column="TOLL", blank=True, null=True)
    loading_charges_per_mt = models.BigIntegerField(
        db_column="LOADING_CHARGES_PER_MT", blank=True, null=True
    )
    unloading_charges_per_mt = models.BigIntegerField(
        db_column="UNLOADING_CHARGES_PER_MT", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_OTHER_VARIABLE_CHARGES"


class FdPrimaryAssumptions(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    capacity = models.FloatField(db_column="CAPACITY", blank=True, null=True)
    no_of_tyres = models.BigIntegerField(db_column="NO_OF_TYRES", blank=True, null=True)
    age_of_truck = models.BigIntegerField(
        db_column="AGE_OF_TRUCK", blank=True, null=True
    )
    round_trip_distance = models.BigIntegerField(
        db_column="ROUND_TRIP_DISTANCE", blank=True, null=True
    )
    no_of_trips_per_month = models.BigIntegerField(
        db_column="NO_OF_TRIPS_PER_MONTH", blank=True, null=True
    )
    backhauling_percentage = models.FloatField(
        db_column="BACKHAULING_PERCENTAGE", blank=True, null=True
    )
    loaded_km_run_per_trip = models.BigIntegerField(
        db_column="LOADED_KM_RUN_PER_TRIP", blank=True, null=True
    )
    loaded_km_run_per_month = models.BigIntegerField(
        db_column="LOADED_KM_RUN_PER_MONTH", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_PRIMARY_ASSUMPTIONS"


class FdProfitabilitySettings(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    monthly_operating_cost = models.FloatField(
        db_column="MONTHLY_OPERATING_COST", blank=True, null=True
    )
    profit_margin = models.BigIntegerField(
        db_column="PROFIT_MARGIN", blank=True, null=True
    )
    profit_margin_percentage = models.FloatField(
        db_column="PROFIT_MARGIN_PERCENTAGE", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_PROFITABILITY_SETTINGS"


class FdPurchaseInputs(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    cost_of_truck = models.BigIntegerField(
        db_column="COST_OF_TRUCK", blank=True, null=True
    )
    loan_amoount_percentage = models.FloatField(
        db_column="LOAN_AMOOUNT_PERCENTAGE", blank=True, null=True
    )
    residual_value_of_truck_at_end_of_emi = models.FloatField(
        db_column="RESIDUAL_VALUE_OF_TRUCK_AT_END_OF_EMI", blank=True, null=True
    )
    no_of_years_emi = models.BigIntegerField(
        db_column="NO_OF_YEARS_EMI", blank=True, null=True
    )
    emi_rate_of_interest_percentage = models.FloatField(
        db_column="EMI_RATE_OF_INTEREST_PERCENTAGE", blank=True, null=True
    )
    flat_rate_of_interest_percentage = models.FloatField(
        db_column="FLAT_RATE_OF_INTEREST_PERCENTAGE", blank=True, null=True
    )
    insurance_as_percentage_of_vehicle_cost = models.FloatField(
        db_column="INSURANCE_AS_PERCENTAGE_OF_VEHICLE_COST", blank=True, null=True
    )
    interest_rate_on_working_capital = models.FloatField(
        db_column="INTEREST_RATE_ON_WORKING_CAPITAL", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_PURCHASE_INPUTS"


class FdSemiVariableCostComputations(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    loading_unloading_per_trip = models.BigIntegerField(
        db_column="LOADING_UNLOADING_PER_TRIP", blank=True, null=True
    )
    loading_unloading_per_month = models.BigIntegerField(
        db_column="LOADING_UNLOADING_PER_MONTH", blank=True, null=True
    )
    tarpaulin_charges_per_trip = models.BigIntegerField(
        db_column="TARPAULIN_CHARGES_PER_TRIP", blank=True, null=True
    )
    handling_cost_per_trip = models.BigIntegerField(
        db_column="HANDLING_COST_PER_TRIP", blank=True, null=True
    )
    handling_cost_per_month = models.BigIntegerField(
        db_column="HANDLING_COST_PER_MONTH", blank=True, null=True
    )
    other_variable_cost_per_km = models.FloatField(
        db_column="OTHER_VARIABLE_COST_PER_KM", blank=True, null=True
    )
    other_variable_cost_per_month = models.BigIntegerField(
        db_column="OTHER_VARIABLE_COST_PER_MONTH", blank=True, null=True
    )
    semi_variable_cost_per_month = models.BigIntegerField(
        db_column="SEMI_VARIABLE_COST_PER_MONTH", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    toll = models.TextField(db_column="TOLL", blank=True, null=True)
    route_expenses = models.TextField(db_column="ROUTE_EXPENSES", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "FD_SEMI_VARIABLE_COST_COMPUTATIONS"


class FdTyreCharges(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    tyre_life = models.BigIntegerField(db_column="TYRE_LIFE", blank=True, null=True)
    tyre_life_retredded = models.BigIntegerField(
        db_column="TYRE_LIFE_RETREDDED", blank=True, null=True
    )
    tyre_cost = models.BigIntegerField(db_column="TYRE_COST", blank=True, null=True)
    tyre_cost_retredded = models.BigIntegerField(
        db_column="TYRE_COST_RETREDDED", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "FD_TYRE_CHARGES"


class FreightDiscoveryProfiles(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    origin = models.ForeignKey(
        "FdLocationOverview",
        models.DO_NOTHING,
        related_name="origin_freigth_discovery",
        db_column="ORIGIN",
        blank=True,
        null=True,
    )
    cost_profile = models.ForeignKey(
        "FdCostProfile",
        models.DO_NOTHING,
        db_column="COST_PROFILE",
        blank=True,
        null=True,
    )
    primary_assumptions = models.ForeignKey(
        "FdPrimaryAssumptions",
        models.DO_NOTHING,
        db_column="PRIMARY_ASSUMPTIONS",
        blank=True,
        null=True,
    )
    purchase_inputs = models.ForeignKey(
        "FdPurchaseInputs",
        models.DO_NOTHING,
        db_column="PURCHASE_INPUTS",
        blank=True,
        null=True,
    )
    capex_computations = models.ForeignKey(
        "FdCapexComputations",
        models.DO_NOTHING,
        db_column="CAPEX_COMPUTATIONS",
        blank=True,
        null=True,
    )
    profitability_settings = models.ForeignKey(
        "FdProfitabilitySettings",
        models.DO_NOTHING,
        db_column="PROFITABILITY_SETTINGS",
        blank=True,
        null=True,
    )
    financial_feasibility_check = models.ForeignKey(
        "FdFinancialFeasibilityCheck",
        models.DO_NOTHING,
        db_column="FINANCIAL_FEASIBILITY_CHECK",
        blank=True,
        null=True,
    )
    tyre_charges = models.ForeignKey(
        "FdTyreCharges",
        models.DO_NOTHING,
        db_column="TYRE_CHARGES",
        blank=True,
        null=True,
    )
    fuel_charges = models.ForeignKey(
        "FdFuelCharges",
        models.DO_NOTHING,
        db_column="FUEL_CHARGES",
        blank=True,
        null=True,
    )
    direct_cost_computations = models.ForeignKey(
        "FdDirectCostComputations",
        models.DO_NOTHING,
        db_column="DIRECT_COST_COMPUTATIONS",
        blank=True,
        null=True,
    )
    other_variable_charges = models.ForeignKey(
        "FdOtherVariableCharges",
        models.DO_NOTHING,
        db_column="OTHER_VARIABLE_CHARGES",
        blank=True,
        null=True,
    )
    semi_variable_cost_computations = models.ForeignKey(
        "FdSemiVariableCostComputations",
        models.DO_NOTHING,
        db_column="SEMI_VARIABLE_COST_COMPUTATIONS",
        blank=True,
        null=True,
    )
    annual_charges = models.ForeignKey(
        "FdAnnualCharges",
        models.DO_NOTHING,
        db_column="ANNUAL_CHARGES",
        blank=True,
        null=True,
    )
    monthly_charges = models.ForeignKey(
        "FdMonthlyCharges",
        models.DO_NOTHING,
        db_column="MONTHLY_CHARGES",
        blank=True,
        null=True,
    )
    fixed_cost_computations = models.ForeignKey(
        "FdFixedCostComputations",
        models.DO_NOTHING,
        db_column="FIXED_COST_COMPUTATIONS",
        blank=True,
        null=True,
    )
    destination = models.ForeignKey(
        "FdLocationOverview",
        models.DO_NOTHING,
        related_name="destination_freight_discovery",
        db_column="DESTINATION",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "FREIGHT_DISCOVERY_PROFILES"


class EpodData(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    order_header_id = models.BigIntegerField(
        db_column="ORDER_HEADER_ID", blank=True, null=True
    )
    order_line_id = models.BigIntegerField(
        db_column="ORDER_LINE_ID", blank=True, null=True
    )
    excise_invoice_no = models.CharField(
        db_column="EXCISE_INVOICE_NO", max_length=150, blank=True, null=True
    )
    delivery_id = models.BigIntegerField(db_column="DELIVERY_ID", blank=True, null=True)
    truck_reach_time = models.DateTimeField(
        db_column="TRUCK_REACH_TIME", blank=True, null=True
    )
    truck_reach_time_confirm = models.DateTimeField(
        db_column="TRUCK_REACH_TIME_CONFIRM", blank=True, null=True
    )
    epod_completion_time = models.DateTimeField(
        db_column="EPOD_COMPLETION_TIME", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    customer_rating = models.BigIntegerField(
        db_column="CUSTOMER_RATING", blank=True, null=True
    )
    crm_update_status = models.CharField(
        db_column="CRM_UPDATE_STATUS", max_length=1, blank=True, null=True
    )
    crm_order_number = models.CharField(
        db_column="CRM_ORDER_NUMBER", max_length=360, blank=True, null=True
    )
    erp_order_number = models.CharField(
        db_column="ERP_ORDER_NUMBER", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "EPOD_DATA"
        unique_together = (
            ("order_header_id", "order_line_id", "excise_invoice_no", "delivery_id"),
        )


class TOebsWshNewDeliveries(models.Model):
    delivery_id = models.BigIntegerField(db_column="DELIVERY_ID", primary_key=True)
    attribute1 = models.CharField(
        db_column="ATTRIBUTE1", max_length=150, blank=True, null=True
    )
    attribute2 = models.CharField(
        db_column="ATTRIBUTE2", max_length=150, blank=True, null=True
    )
    attribute3 = models.CharField(
        db_column="ATTRIBUTE3", max_length=150, blank=True, null=True
    )
    attribute4 = models.CharField(
        db_column="ATTRIBUTE4", max_length=150, blank=True, null=True
    )
    attribute5 = models.CharField(
        db_column="ATTRIBUTE5", max_length=150, blank=True, null=True
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    created_by = models.DecimalField(
        db_column="CREATED_BY", max_digits=50, decimal_places=2, blank=True, null=True
    )
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
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

    class Meta:
        managed = False
        db_table = "T_OEBS_WSH_NEW_DELIVERIES"


class TgtPlantLookup(models.Model):
    commudity = models.CharField(
        db_column="Commudity", max_length=100, blank=True, null=True
    )
    zone = models.CharField(db_column="Zone", max_length=100, blank=True, null=True)
    org = models.CharField(db_column="ORG", max_length=100, blank=True, null=True)
    plant_name = models.CharField(
        db_column="Plant NAME", max_length=50, blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TGT_PLANT_LOOKUP"


PlantNameChoices = models.TextChoices(
    "PlantNameChoices", TgtPlantLookup.objects.values_list("plant_name", "org")
)


class ReasonsForDemurrageWharfage(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    reasons_for_demurrage_wharfage = models.CharField(
        db_column="REASONS_FOR_DEMURRAGE_WHARFAGE",
        max_length=540,
        blank=True,
        null=True,
    )
    category = models.CharField(
        db_column="CATEGORY", max_length=360, blank=True, null=True
    )
    rake_point_type = models.CharField(
        db_column="RAKE_POINT_TYPE", max_length=360, blank=True, null=True
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
        db_table = "REASONS_FOR_DEMURRAGE_WHARFAGE"


class WharfageSlabs(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    wharfage_hours_min = models.DecimalField(
        db_column="WHARFAGE_HOURS_MIN",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wharfage_hours_max = models.DecimalField(
        db_column="WHARFAGE_HOURS_MAX",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wharfage_rate_per_wagon_per_hour = models.DecimalField(
        db_column="WHARFAGE_RATE_PER_WAGON_PER_HOUR",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wagon_capacity_mt = models.DecimalField(
        db_column="WAGON_CAPACITY_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wharfage_rate_per_mt_per_hour = models.DecimalField(
        db_column="WHARFAGE_RATE_PER_MT_PER_HOUR",
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
        db_table = "WHARFAGE_SLABS"


class DemurrageSlabs(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    demurrage_hours_min = models.DecimalField(
        db_column="DEMURRAGE_HOURS_MIN",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    demurrage_hours_max = models.DecimalField(
        db_column="DEMURRAGE_HOURS_MAX",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    demurrage_rate_per_wagon_per_hour = models.DecimalField(
        db_column="DEMURRAGE_RATE_PER_WAGON_PER_HOUR",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wagon_capacity_mt = models.DecimalField(
        db_column="WAGON_CAPACITY_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    demurrage_rate_per_mt_per_hour = models.DecimalField(
        db_column="DEMURRAGE_RATE_PER_MT_PER_HOUR",
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
        db_table = "DEMURRAGE_SLABS"


class CrwcChargesMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )  # Field name made lowercase.
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )  # Field name made lowercase.
    min_days = models.BigIntegerField(db_column="MIN_DAYS", blank=True, null=True)
    max_days = models.BigIntegerField(db_column="MAX_DAYS", blank=True, null=True)
    rate_per_day_per_mt = models.DecimalField(
        db_column="RATE_PER_DAY_PER_MT",
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
        db_table = "CRWC_CHARGES_MASTER"


class WaiverCommissionMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    min_waiver = models.DecimalField(
        db_column="MIN_WAIVER", max_digits=22, decimal_places=3, blank=True, null=True
    )
    max_waiver = models.DecimalField(
        db_column="MAX_WAIVER", max_digits=22, decimal_places=3, blank=True, null=True
    )
    commission = models.DecimalField(
        db_column="COMMISSION", max_digits=22, decimal_places=3, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    agent = models.CharField(db_column="AGENT", max_length=540, blank=True, null=True)
    amount_deposited = models.CharField(
        db_column="AMOUNT_DEPOSITED", max_length=540, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "WAIVER_COMMISSION_MASTER"


class RailExpensesDetails(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    dm_hours = models.DecimalField(
        db_column="DM_HOURS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    wagon_under_dm = models.BigIntegerField(
        db_column="WAGON_UNDER_DM", blank=True, null=True
    )
    rate_per_wagon = models.DecimalField(
        db_column="RATE_PER_WAGON",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dm_amount_wth_gst = models.DecimalField(
        db_column="DM_AMOUNT_WTH_GST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dm_cgst_percent = models.DecimalField(
        db_column="DM_CGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dm_igst_percent = models.DecimalField(
        db_column="DM_IGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dm_sgst_percent = models.DecimalField(
        db_column="DM_SGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_gst_amount = models.DecimalField(
        db_column="TOTAL_GST_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_dm_amount = models.DecimalField(
        db_column="TOTAL_DM_AMOUNT",
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
    wf_hours = models.DecimalField(
        db_column="WF_HOURS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    wagon_under_wf = models.BigIntegerField(
        db_column="WAGON_UNDER_WF", blank=True, null=True
    )
    wf_rate_per_wagon = models.DecimalField(
        db_column="WF_RATE_PER_WAGON",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_amount_wth_gst = models.DecimalField(
        db_column="WF_AMOUNT_WTH_GST",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_cgst_percent = models.DecimalField(
        db_column="WF_CGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_igst_percent = models.DecimalField(
        db_column="WF_IGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_sgst_percent = models.DecimalField(
        db_column="WF_SGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_wf_gst_amount = models.DecimalField(
        db_column="TOTAL_WF_GST_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_wf_amount = models.DecimalField(
        db_column="TOTAL_WF_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    other_charges = models.DecimalField(
        db_column="OTHER_CHARGES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ship_to_depot = models.CharField(
        db_column="SHIP_TO_DEPOT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "RAIL_EXPENSES_DETAILS"


class HourlyLiftingEfficiencyMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=360, blank=True, null=True
    )
    min_time = models.DurationField(db_column="MIN_TIME", blank=True, null=True)
    max_time = models.DurationField(db_column="MAX_TIME", blank=True, null=True)
    time_range = models.CharField(
        db_column="TIME_RANGE", max_length=540, blank=True, null=True
    )
    lifting_efficiency = models.DecimalField(
        db_column="LIFTING_EFFICIENCY",
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
        db_table = "HOURLY_LIFTING_EFFICIENCY_MASTER"


class HourlyLiftingEfficiency(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run_id = models.BigIntegerField(db_column="RUN_ ID", blank=True, null=True)
    min_time = models.DurationField(db_column="MIN_TIME", blank=True, null=True)
    max_time = models.DurationField(db_column="MAX_TIME", blank=True, null=True)
    time_range = models.CharField(
        db_column="TIME_RANGE", max_length=540, blank=True, null=True
    )
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=540, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)
    lifting_efficiency_per = models.DecimalField(
        db_column="LIFTING_EFFICIENCY_PER",
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
        db_table = "HOURLY_LIFTING_EFFICIENCY"


class RailHeadToGodownShiftingCartageCosts(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=360, blank=True, null=True
    )
    godown = models.CharField(db_column="GODOWN", max_length=360, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    transferring_cost = models.BigIntegerField(
        db_column="TRANSFERRING_COST", blank=True, null=True
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
        db_table = "RAIL_HEAD_TO_GODOWN_SHIFTING_CARTAGE_COSTS"


class RoadHandlingMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    godown = models.CharField(db_column="GODOWN", max_length=360, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=360, blank=True, null=True
    )
    road_handling_per_mt = models.DecimalField(
        db_column="ROAD_HANDLING_PER_MT",
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
        db_table = "ROAD_HANDLING_MASTER"


class DepoWiseFreightMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    month_year = models.DateField(db_column="MONTH_YEAR", blank=True, null=True)
    depo_code = models.CharField(
        db_column="DEPO_CODE", max_length=360, blank=True, null=True
    )
    sale_type = models.CharField(
        db_column="SALE_TYPE", max_length=360, blank=True, null=True
    )
    average_freight = models.DecimalField(
        db_column="AVERAGE_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=360, blank=True, null=True
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
        db_table = "DEPO_WISE_FREIGHT_MASTER"


class SidingConstraints(models.Model):
    run_id = models.BigAutoField(db_column="RUN_ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=360, blank=True, null=True
    )
    rake_id = models.CharField(
        db_column="RAKE_ID", max_length=360, blank=True, null=True
    )
    expected_demurrage_waiver = models.DecimalField(
        db_column="EXPECTED_DEMURRAGE_WAIVER",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    expected_wharfage_waiver = models.DecimalField(
        db_column="EXPECTED_WHARFAGE_WAIVER",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date_of_next_expected_rake = models.DateTimeField(
        db_column="DATE_OF_NEXT_EXPECTED_RAKE", blank=True, null=True
    )
    unloading_at_siding = models.BooleanField(
        db_column="UNLOADING_AT SIDING", default=True
    )
    transfer_at_crwc = models.BooleanField(db_column="TRANSFER_AT_CRWC", default=True)
    transfer_to_godown = models.BooleanField(
        db_column="TRANSFER_TO_GODOWN", default=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    operation_start_time = models.TimeField(
        db_column="OPERATION_START_TIME", blank=True, null=True
    )
    operation_end_time = models.TimeField(
        db_column="OPERATION_END_TIME", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SIDING_CONSTRAINTS"


class LiftingPattern(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run_id = models.BigIntegerField(db_column="RUN_ID", blank=True, null=True)
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=360, blank=True, null=True
    )
    min_time = models.DateTimeField(db_column="MIN_TIME", blank=True, null=True)
    max_time = models.DateTimeField(db_column="MAX_TIME", blank=True, null=True)
    time_range = models.CharField(
        db_column="TIME_RANGE", max_length=540, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=540, blank=True, null=True
    )
    lifting_qty = models.DecimalField(
        db_column="LIFTING_QTY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    grade = models.CharField(db_column="GRADE", max_length=360, blank=True, null=True)
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=360, blank=True, null=True
    )
    slab_id = models.BigIntegerField(db_column="SLAB_ID", blank=True, null=True)
    expected_lifting_time = models.DateTimeField(
        db_column="EXPECTED_LIFTING_TIME", blank=True, null=True
    )
    time_slab = models.CharField(
        db_column="TIME_SLAB", max_length=350, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LIFTING_PATTERN"


class RakeHandlingMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=360, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=360, blank=True, null=True
    )
    packing = models.CharField(
        db_column="PACKING", max_length=360, blank=True, null=True
    )
    total_cost_per_mt = models.BigIntegerField(
        db_column="TOTAL_COST_PER_MT", blank=True, null=True
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
        db_table = "RAKE_HANDLING_MASTER"


class SidingWiseLiasioningAgent(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    siding_code = models.CharField(
        db_column="SIDING_CODE", max_length=540, blank=True, null=True
    )
    siding_name = models.CharField(
        db_column="SIDING_NAME", max_length=540, blank=True, null=True
    )
    dc_wf_in_ac_of = models.CharField(
        db_column="DC_WF_IN_AC_OF", max_length=540, blank=True, null=True
    )
    liasioning_agent = models.CharField(
        db_column="LIASIONING_AGENT", max_length=540, blank=True, null=True
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
        db_table = "SIDING_WISE_LIASIONING_AGENT"


class HandlingMasters(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=540, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )
    depot_name = models.CharField(
        db_column="DEPOT_NAME", max_length=540, blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=540, blank=True, null=True
    )
    rake_handling = models.DecimalField(
        db_column="RAKE_HANDLING",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cartage_cost = models.DecimalField(
        db_column="CARTAGE_COST", max_digits=22, decimal_places=2, blank=True, null=True
    )
    road_handling_from_godown = models.DecimalField(
        db_column="ROAD_HANDLING_FROM_GODOWN",
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
        db_table = "HANDLING_MASTERS"


class RailExpensesDetailsWarfage(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    wf_hours = models.DecimalField(
        db_column="WF_HOURS", max_digits=22, decimal_places=2, blank=True, null=True
    )
    wagon_under_wf = models.BigIntegerField(
        db_column="WAGON_UNDER_WF", blank=True, null=True
    )
    wf_rate_per_wagon = models.DecimalField(
        db_column="WF_RATE_PER_WAGON",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_amount_wth_gst = models.DecimalField(
        db_column="WF_AMOUNT_WTH_GST",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_cgst_percent = models.DecimalField(
        db_column="WF_CGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_igst_percent = models.DecimalField(
        db_column="WF_IGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wf_sgst_percent = models.DecimalField(
        db_column="WF_SGST_PERCENT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_wf_gst_amount = models.DecimalField(
        db_column="TOTAL_WF_GST_AMOUNT",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total_wf_amount = models.DecimalField(
        db_column="TOTAL_WF_AMOUNT",
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
    other_charges = models.DecimalField(
        db_column="OTHER_CHARGES",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ship_to_depot = models.CharField(
        db_column="SHIP_TO_DEPOT", max_length=360, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "RAIL_EXPENSES_DETAILS_WARFAGE"


class GdWharfageRunInput(models.Model):
    run_id = models.BigAutoField(db_column="RUN_ID", primary_key=True)
    run_date = models.DateField(db_column="RUN_DATE", blank=True, null=True)
    run_status = models.CharField(
        db_column="RUN_STATUS", max_length=540, blank=True, null=True
    )
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    rake_point = models.CharField(
        db_column="RAKE_POINT", max_length=540, blank=True, null=True
    )
    rake_point_code = models.CharField(
        db_column="RAKE_POINT_CODE", max_length=540, blank=True, null=True
    )
    next_rake_arrival_datetime = models.DateTimeField(
        db_column="NEXT_RAKE_ARRIVAL_DATETIME", blank=True, null=True
    )
    wagon_quantity = models.BigIntegerField(
        db_column="WAGON_QUANTITY", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "GD_WHARFAGE_RUN_INPUT"


class GdWharfageOutput(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run_id = models.BigIntegerField(db_column="RUN_ID", blank=True, null=True)
    rake_id = models.BigIntegerField(db_column="RAKE_ID", blank=True, null=True)
    start_time = models.DateTimeField(db_column="START_TIME", blank=True, null=True)
    end_time = models.DateTimeField(db_column="END_TIME", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=540, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=540, blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=540, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=540, blank=True, null=True
    )
    depot_code = models.CharField(
        db_column="DEPOT_CODE", max_length=540, blank=True, null=True
    )
    hourly_slab_id = models.BigIntegerField(
        db_column="HOURLY_SLAB_ID", blank=True, null=True
    )
    demurrage_hours = models.FloatField(
        db_column="DEMURRAGE_HOURS", blank=True, null=True
    )
    wharfage_hours = models.FloatField(
        db_column="WHARFAGE_HOURS", blank=True, null=True
    )
    demurrage_rate = models.FloatField(
        db_column="DEMURRAGE_RATE", blank=True, null=True
    )
    crwc_days = models.BigIntegerField(db_column="CRWC_DAYS", blank=True, null=True)
    crwc_rate = models.DecimalField(
        db_column="CRWC_RATE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    rake_handling_cost_per_mt = models.DecimalField(
        db_column="RAKE_HANDLING_COST_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    crwc_handling_charges_per_mt = models.DecimalField(
        db_column="CRWC_HANDLING_CHARGES_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    crwc_freight_per_mt = models.DecimalField(
        db_column="CRWC_FREIGHT_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    transfer_cost_per_mt = models.DecimalField(
        db_column="TRANSFER_COST_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    gd_freight_per_mt = models.DecimalField(
        db_column="GD_FREIGHT_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    gd_handling_charges_per_mt = models.DecimalField(
        db_column="GD_HANDLING_CHARGES_PER_MT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cmplsry_alloc = models.BooleanField(
        db_column="CMPLSRY_ALLOC", blank=True, null=True
    )
    qty = models.DecimalField(
        db_column="QTY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    rake_qty_id = models.DecimalField(
        db_column="RAKE_QTY_ID", max_digits=22, decimal_places=2, blank=True, null=True
    )
    no_of_wagons = models.DecimalField(
        db_column="NO_OF_WAGONS", max_digits=22, decimal_places=2, blank=True, null=True
    )
    lifting_effeciency_id = models.DecimalField(
        db_column="LIFTING_EFFECIENCY_ID",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    slab_id = models.DecimalField(
        db_column="SLAB_ID", max_digits=22, decimal_places=2, blank=True, null=True
    )
    max_lifting_qty = models.DecimalField(
        db_column="MAX_LIFTING_QTY",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wharfage_id = models.DecimalField(
        db_column="WHARFAGE_ID", max_digits=22, decimal_places=2, blank=True, null=True
    )
    wharfage_rate = models.DecimalField(
        db_column="WHARFAGE_RATE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    index = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    var_demurrage = models.CharField(max_length=540, blank=True, null=True)
    var_wharfage = models.CharField(max_length=540, blank=True, null=True)
    var_crwc = models.CharField(max_length=540, blank=True, null=True)
    var_gd = models.CharField(max_length=540, blank=True, null=True)
    var_wharfage_wagon = models.CharField(max_length=540, blank=True, null=True)
    var_wharfage_alloc = models.CharField(max_length=540, blank=True, null=True)
    qty_demurrage = models.DecimalField(
        max_digits=22, decimal_places=2, blank=True, null=True
    )
    qty_wharfage = models.DecimalField(
        max_digits=22, decimal_places=2, blank=True, null=True
    )
    qty_crwc = models.DecimalField(
        max_digits=22, decimal_places=2, blank=True, null=True
    )
    qty_gd = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    wharfage_wagon_no = models.DecimalField(
        max_digits=22, decimal_places=2, blank=True, null=True
    )
    wharfage_wagon_alloc = models.DecimalField(
        max_digits=22, decimal_places=2, blank=True, null=True
    )
    start_date = models.DateTimeField(db_column="START_DATE", blank=True, null=True)
    end_date = models.DateTimeField(db_column="END_DATE", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    total_demurrage = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_demurrage_rake_handling = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_demurrage_freight_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_wharfage = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_wharfage_rake_handling = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_wharfage_freight_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_crwc_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_crwc_rake_handling_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_crwc_freight_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_crwc_handling_charges_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_gd_rake_handling_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_gd_transfer_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_gd_freight_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_gd_handling_charges = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    cost_demurrage = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    cost_wharfage = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    cost_crwc = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    cost_gd = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )
    total_cost = models.DecimalField(
        max_digits=22, decimal_places=3, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "GD_WHARFAGE_OUTPUT"


class RrcIsoStockTransfer(models.Model):
    shipped_qty = models.DecimalField(
        db_column="SHIPPED_QTY", max_digits=20, decimal_places=3, blank=True, null=True
    )
    truck_type = models.CharField(
        db_column="TRUCK_TYPE", max_length=200, blank=True, null=True
    )
    vehicle_no = models.CharField(
        db_column="VEHICLE_NO", max_length=250, blank=True, null=True
    )
    transporter = models.CharField(
        db_column="TRANSPORTER", max_length=500, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=200, blank=True, null=True
    )
    pack_mat = models.CharField(
        db_column="PACK_MAT", max_length=200, blank=True, null=True
    )
    mode_of_transport = models.CharField(
        db_column="MODE_OF_TRANSPORT", max_length=200, blank=True, null=True
    )
    di_so = models.CharField(db_column="DI_SO", max_length=200, blank=True, null=True)
    tax_invoice_date = models.DateField(
        db_column="TAX_INVOICE_DATE", blank=True, null=True
    )
    tax_invoice_date1 = models.DateTimeField(
        db_column="TAX_INVOICE_DATE1", blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=350, blank=True, null=True)
    order_type = models.CharField(
        db_column="ORDER_TYPE", max_length=250, blank=True, null=True
    )
    final_to_taluka = models.CharField(max_length=350, blank=True, null=True)
    final_to_district = models.CharField(max_length=350, blank=True, null=True)
    final_to_state = models.CharField(max_length=350, blank=True, null=True)
    final_to_city = models.CharField(max_length=350, blank=True, null=True)
    consignee = models.TextField(db_column="CONSIGNEE", blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    plant = models.CharField(db_column="PLANT", max_length=350, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    source_plant = models.TextField(db_column="SOURCE_PLANT", blank=True, null=True)
    order_type_btst_final = models.CharField(
        db_column="ORDER_TYPE_BTST_FINAL", max_length=350, blank=True, null=True
    )
    delivery_id = models.DecimalField(
        db_column="DELIVERY_ID", max_digits=20, decimal_places=0, blank=True, null=True
    )
    order_number = models.DecimalField(
        db_column="ORDER_NUMBER", max_digits=25, decimal_places=0, blank=True, null=True
    )
    quantity_received = models.DecimalField(
        db_column="QUANTITY_RECEIVED",
        max_digits=65535,
        decimal_places=65535,
        blank=True,
        null=True,
    )
    receipt_number = models.CharField(
        db_column="RECEIPT_NUMBER", max_length=350, blank=True, null=True
    )
    receipt_date = models.DateTimeField(db_column="RECEIPT_DATE", blank=True, null=True)
    id = models.DecimalField(
        db_column="ID", primary_key=True, max_digits=60, decimal_places=0
    )

    class Meta:
        managed = False
        db_table = "RRC_ISO_STOCK_TRANSFER"
