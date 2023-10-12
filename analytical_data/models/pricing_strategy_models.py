"""Pricing strategy models module."""
from django.db import models


class CompetitionPriceNewMarkets(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    price = models.CharField(db_column="PRICE", max_length=50, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    value = models.DecimalField(
        db_column="VALUE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    business_segment = models.CharField(
        db_column="BUSINESS_SEGMENT", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "COMPETITION_PRICE_NEW_MARKETS"


class NewPriceComputation(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    active = models.CharField(db_column="ACTIVE", max_length=50, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    zone = models.CharField(db_column="ZONE", max_length=240, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=240, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=240, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=240, blank=True, null=True
    )
    price_min = models.DecimalField(
        db_column="PRICE_MIN", max_digits=22, decimal_places=2, blank=True, null=True
    )
    price_max = models.DecimalField(
        db_column="PRICE_MAX", max_digits=22, decimal_places=2, blank=True, null=True
    )
    ebitda_min = models.DecimalField(
        db_column="EBITDA_MIN", max_digits=22, decimal_places=2, blank=True, null=True
    )
    ebitda_max = models.DecimalField(
        db_column="EBITDA_MAX", max_digits=22, decimal_places=2, blank=True, null=True
    )
    computed_wsp = models.DecimalField(
        db_column="COMPUTED_WSP", max_digits=22, decimal_places=2, blank=True, null=True
    )
    dealer_margin = models.DecimalField(
        db_column="DEALER_MARGIN",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    computed_nod = models.DecimalField(
        db_column="COMPUTED_NOD", max_digits=22, decimal_places=2, blank=True, null=True
    )
    tlc = models.DecimalField(
        db_column="TLC", max_digits=22, decimal_places=2, blank=True, null=True
    )
    primary_freight = models.DecimalField(
        db_column="PRIMARY_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    secondary_freight = models.DecimalField(
        db_column="SECONDARY_FREIGHT",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    commissions = models.DecimalField(
        db_column="COMMISSIONS", max_digits=22, decimal_places=2, blank=True, null=True
    )
    packaging_cost = models.DecimalField(
        db_column="PACKAGING_COST",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    misc_charges = models.DecimalField(
        db_column="MISC_CHARGES", max_digits=22, decimal_places=2, blank=True, null=True
    )
    vpc = models.DecimalField(
        db_column="VPC", max_digits=22, decimal_places=2, blank=True, null=True
    )
    fixed_cost_per = models.DecimalField(
        db_column="FIXED_COST_PER",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fixed_cost = models.DecimalField(
        db_column="FIXED_COST", max_digits=22, decimal_places=2, blank=True, null=True
    )
    ebitda_margin = models.DecimalField(
        db_column="EBITDA MARGIN",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ebitda = models.DecimalField(
        db_column="EBITDA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    business_segment = models.CharField(
        db_column="BUSINESS_SEGMENT", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "NEW_PRICE_COMPUTATION"


class PriceBenchmarks(models.Model):
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    benchmark_name = models.CharField(
        db_column="BENCHMARK NAME", max_length=50, blank=True, null=True
    )
    price_difference_to_be_maintained = models.DecimalField(
        db_column="PRICE DIFFERENCE TO BE MAINTAINED",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    business_segment = models.CharField(
        db_column="BUSINESS_SEGMENT", max_length=100, blank=True, null=True
    )
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PRICE_BENCHMARKS"


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


class NmMarketSharePotential(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    sales = models.DecimalField(
        db_column="SALES", max_digits=20, decimal_places=2, blank=True, null=True
    )
    market_potential = models.DecimalField(
        db_column="MARKET_POTENTIAL",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share = models.DecimalField(
        db_column="MARKET_SHARE", max_digits=20, decimal_places=2, blank=True, null=True
    )
    delta_market_share = models.DecimalField(
        db_column="DELTA_MARKET_SHARE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    business_segment = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "NM_MARKET_SHARE_POTENTIAL"


class NmMarket4X4Output(models.Model):
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    sales = models.DecimalField(
        db_column="SALES", max_digits=22, decimal_places=2, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    ncr = models.DecimalField(
        db_column="NCR", max_digits=22, decimal_places=2, blank=True, null=True
    )
    ncr_market_potential_rating = models.CharField(
        db_column="NCR_MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
    )
    prev_month_share_delta = models.DecimalField(
        db_column="PREV_MONTH_SHARE_DELTA",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    prev_year_share_delta = models.DecimalField(
        db_column="PREV_YEAR_SHARE_DELTA",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_potential_rating = models.CharField(
        db_column="MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    market_potential = models.DecimalField(
        db_column="MARKET_POTENTIAL",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share = models.DecimalField(
        db_column="MARKET_SHARE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    leader_market_share = models.DecimalField(
        db_column="LEADER_MARKET_SHARE",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share_max = models.DecimalField(
        db_column="MARKET_SHARE_MAX",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_leader = models.CharField(
        db_column="MARKET LEADER", max_length=50, blank=True, null=True
    )
    delta = models.DecimalField(
        db_column="DELTA", max_digits=22, decimal_places=2, blank=True, null=True
    )
    delta_market_share_max = models.DecimalField(
        db_column="DELTA_MARKET_SHARE_MAX",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share_potential_rating = models.CharField(
        db_column="MARKET_SHARE_POTENTIAL_RATING", max_length=50, blank=True, null=True
    )
    delta_market_share_potential_rating = models.CharField(
        db_column="DELTA_MARKET_SHARE_POTENTIAL_RATING",
        max_length=50,
        blank=True,
        null=True,
    )
    plan_month = models.DateField(db_column="PLAN_MONTH", blank=True, null=True)
    market_position = models.CharField(
        db_column="MARKET_POSITION", max_length=50, blank=True, null=True
    )
    market_lucrativeness = models.CharField(
        db_column="MARKET_LUCRATIVENESS", max_length=50, blank=True, null=True
    )
    market_growth_strategy = models.CharField(
        db_column="MARKET_GROWTH_STRATEGY", max_length=50, blank=True, null=True
    )
    pricing_strategy_driver = models.CharField(max_length=50, blank=True, null=True)
    pricing_strategy = models.CharField(max_length=50, blank=True, null=True)
    wsp_price = models.DecimalField(
        db_column="WSP_PRICE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    rsp_price = models.DecimalField(
        db_column="RSP_PRICE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    business_segment = models.CharField(
        db_column="BUSINESS_SEGMENT", max_length=100, blank=True, null=True
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
        db_table = "NM_MARKET_4x4_OUTPUT"


class SoLeagueWeightage(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    kpi = models.CharField(db_column="KPI", max_length=100, blank=True, null=True)
    kpi_name = models.CharField(
        db_column="KPI_NAME", max_length=500, blank=True, null=True
    )
    weightage = models.DecimalField(
        db_column="WEIGHTAGE", max_digits=22, decimal_places=2, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "SO_LEAGUE_WEIGHTAGE"


class PriceChangeRequestApproval(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=200, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=200, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=200, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=200, blank=True, null=True
    )
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=200, blank=True, null=True)
    wsp_change = models.DecimalField(
        db_column="WSP_CHANGE", max_digits=22, decimal_places=3, blank=True, null=True
    )
    wsp_effective_date = models.DateField(
        db_column="WSP_EFFECTIVE_DATE", blank=True, null=True
    )
    rsp_change = models.DecimalField(
        db_column="RSP_CHANGE", max_digits=22, decimal_places=3, blank=True, null=True
    )
    rsp_effective_date = models.DateField(
        db_column="RSP_EFFECTIVE_DATE", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=200, blank=True, null=True)
    comments_of_approval = models.CharField(
        db_column="COMMENTS_OF_APPROVAL", max_length=200, blank=True, null=True
    )
    comments_of_raiser = models.CharField(
        db_column="COMMENTS_OF_RAISER", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "PRICE_CHANGE_REQUEST_APPROVAL"
