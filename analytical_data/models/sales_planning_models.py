"""Analytical data sales planning models module."""
from django.db import models


class DfKachaPakkaConversionRate(models.Model):
    """Kachcha pakka conversion rate model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    kacha_pakka_conversion_rate = models.DecimalField(
        db_column="KACHA_PAKKA_CONVERSION_RATE",
        max_digits=20,
        decimal_places=5,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_KACHA_PAKKA_CONVERSION_RATE"
        ordering = ["state", "district"]


class DfAnnualUrbanizationRate(models.Model):
    """Annual urbanization rate model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    annual_urbanization_rate = models.DecimalField(
        db_column="ANNUAL_URBANIZATION_RATE",
        max_digits=20,
        decimal_places=5,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_ANNUAL_URBANIZATION_RATE"
        ordering = ["state"]


class DfAverageFlatSize(models.Model):
    """Average flat size model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    household_size_rural = models.DecimalField(
        db_column="HOUSEHOLD_SIZE_RURAL",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    household_size_urban = models.DecimalField(
        db_column="HOUSEHOLD_SIZE_URBAN",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_AVERAGE_FLAT_SIZE"
        ordering = ["state", "district"]


class DfUrbanRuralHouseholdSize(models.Model):
    """Urban rural household size model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    urban_household_size = models.DecimalField(
        db_column="URBAN_HOUSEHOLD_SIZE",
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
    )
    rural_household_size = models.DecimalField(
        db_column="RURAL_HOUSEHOLD_SIZE",
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_URBAN_RURAL_HOUSEHOLD_SIZE"
        ordering = ["state", "district"]


class DfCementConsumptionPerSqFt(models.Model):
    """Cement consumption per square foot model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    low_rise_cement_consumption = models.DecimalField(
        db_column="LOW_RISE_CEMENT_CONSUMPTION",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    high_rise_cement_consumption = models.DecimalField(
        db_column="HIGH_RISE_CEMENT_CONSUMPTION",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_CEMENT_CONSUMPTION_PER_SQ_FT"
        ordering = ["state", "district"]


class DfProjectDatabase(models.Model):
    """Project db model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    project_name = models.CharField(
        db_column="PROJECT_NAME", max_length=100, blank=True, null=True
    )
    cost = models.DecimalField(
        db_column="COST", max_digits=20, decimal_places=2, blank=True, null=True
    )
    duration = models.DecimalField(
        db_column="DURATION", max_digits=10, decimal_places=5, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=100, blank=True, null=True)
    cement_value_as_percentage_of_cost = models.DecimalField(
        db_column="CEMENT_VALUE_AS_PERCENTAGE_OF_COST",
        max_digits=10,
        decimal_places=5,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_PROJECT_DATABASE"
        ordering = ["state"]


class DfDesiredMarketShare(models.Model):
    """Desired market share model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    desired_market_share = models.DecimalField(
        db_column="DESIRED_MARKET_SHARE",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_DESIRED_MARKET_SHARE"
        ordering = ["state"]


class DfGeographicalPresence(models.Model):
    """Geographical presence model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    geographical_presence = models.DecimalField(
        db_column="GEOGRAPHICAL_PRESENCE",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_GEOGRAPHICAL_PRESENCE"
        ordering = ["state"]


class DfSeasonality(models.Model):
    """Seasonality model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    invoice_date_month = models.IntegerField(
        db_column="INVOICE_DATE_MONTH", blank=True, null=True
    )
    quantity_invoiced = models.DecimalField(
        db_column="QUANTITY_INVOICED",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sum_all = models.DecimalField(
        db_column="SUM_ALL", max_digits=20, decimal_places=2, blank=True, null=True
    )
    total_sum = models.DecimalField(
        db_column="TOTAL_SUM", max_digits=20, decimal_places=2, blank=True, null=True
    )
    percentage = models.DecimalField(
        db_column="PERCENTAGE", max_digits=20, decimal_places=9, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DF_SEASONALITY"
        ordering = ["state"]


class DfHighRiseLowRiseSplit(models.Model):
    """High rise low rise split model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    number_1_floor = models.DecimalField(
        db_column="1_FLOOR", max_digits=10, decimal_places=2, blank=True, null=True
    )
    number_2_floor = models.DecimalField(
        db_column="2_FLOOR", max_digits=10, decimal_places=2, blank=True, null=True
    )
    number_3_to_5_floor = models.DecimalField(
        db_column="3_TO_5_FLOOR", max_digits=10, decimal_places=2, blank=True, null=True
    )
    number_5_to_10_floor = models.DecimalField(
        db_column="5_TO_10_FLOOR",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    number_10_floor = models.DecimalField(
        db_column="10_FLOOR", max_digits=10, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DF_HIGH_RISE_LOW_RISE_SPLIT"
        ordering = ["state"]


class DfTopDownTargets(models.Model):
    """Top down targets model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=100, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=100, blank=True, null=True
    )
    last_year_actual_sale = models.DecimalField(
        db_column="LAST_YEAR_ACTUAL_SALE",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    last_year_target = models.DecimalField(
        db_column="LAST_YEAR_TARGET",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    percent_achievement = models.DecimalField(
        db_column="PERCENT_ACHIEVEMENT",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    top_down_target = models.DecimalField(
        db_column="TOP_DOWN_TARGET",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DF_TOP_DOWN_TARGETS"
        ordering = ["state", "district"]


class DemandForecastRunDtl(models.Model):
    """Top down targets model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    run_id = models.BigIntegerField(db_column="RUN_ID", blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=100, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=100, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=100, blank=True, null=True)
    grade = models.CharField(db_column="GRADE", max_length=100, blank=True, null=True)
    forecast_month = models.DateField(db_column="FORECAST_MONTH", blank=True, null=True)
    forecast_bucket = models.CharField(
        db_column="FORECAST_BUCKET", max_length=50, blank=True, null=True
    )
    forecast = models.DecimalField(
        db_column="FORECAST",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "DEMAND_FORECAST_RUN_DTL"
        ordering = ["state", "district"]


class DfMacroOutputFinal(models.Model):
    """Macro output final model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=500, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=500, blank=True, null=True)
    invoice_month = models.CharField(
        db_column="INVOICE_MONTH", max_length=500, blank=True, null=True
    )
    state_target = models.CharField(
        db_column="STATE_TARGET", max_length=500, blank=True, null=True
    )
    individual_state_percentage = models.CharField(
        db_column="INDIVIDUAL_STATE_PERCENTAGE", max_length=500, blank=True, null=True
    )
    final_demand = models.DecimalField(
        db_column="FINAL_DEMAND", max_digits=10, decimal_places=2, blank=True, null=True
    )
    date = models.DateField(db_column="DATE", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "DF_MACRO_OUTPUT_FINAL"


class SalesTargetMonthly(models.Model):
    """Sales target monthly model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="District", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="Brand", max_length=50, blank=True, null=True)
    sales_x = models.DecimalField(
        db_column="Sales_x", max_digits=65535, decimal_places=2, blank=True, null=True
    )
    product = models.CharField(
        db_column="Product", max_length=50, blank=True, null=True
    )
    ncr = models.DecimalField(
        db_column="Ncr", max_digits=65535, decimal_places=2, blank=True, null=True
    )
    ncr_market_potential_rating = models.CharField(
        db_column="Ncr_market_potential_rating", max_length=50, blank=True, null=True
    )
    prev_month_share_delta = models.DecimalField(
        db_column="Prev_month_share_delta",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    prev_year_share_delta = models.DecimalField(
        db_column="Prev_year_share_delta",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_potential_rating = models.CharField(max_length=50, blank=True, null=True)
    month = models.DateField(db_column="Month", blank=True, null=True)
    leader_market_share = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_share_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_leader = models.CharField(
        db_column="Market Leader", max_length=10, blank=True, null=True
    )
    delta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delta_market_share_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_share_potential_rating = models.CharField(
        max_length=50, blank=True, null=True
    )
    delta_market_share_potential_rating = models.CharField(
        max_length=50, blank=True, null=True
    )
    plan_month = models.DateField(blank=True, null=True)
    zone = models.CharField(db_column="Zone", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    market_position = models.CharField(max_length=50, blank=True, null=True)
    market_lucrativeness = models.CharField(max_length=50, blank=True, null=True)
    market_growth_strategy = models.CharField(max_length=50, blank=True, null=True)
    sales = models.DecimalField(
        db_column="Sales", max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_potential = models.DecimalField(
        db_column="Market potential",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    market_share = models.DecimalField(
        db_column="Market share",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    prev_market_potential = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prev_market_share = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prev_market_share2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prev_market_share3 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    curr_prev = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prev_prev2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prev2_prev3 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    max_market_share = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    future_market_share_thres = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    future_market_share = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    future_market_potential = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    target_sales = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_potential_diff = models.DecimalField(
        max_digits=50, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "SALES_TARGET_MONTHLY"


class DfBottomUpTargetsMonthly2(models.Model):
    """Bottom up targets monthly 2 model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=200, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=200, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=200, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=200, blank=True, null=True)
    so_name = models.CharField(
        db_column="SO_NAME", max_length=200, blank=True, null=True
    )
    counter_name = models.CharField(
        db_column="COUNTER_NAME", max_length=200, blank=True, null=True
    )
    counter_type = models.CharField(
        db_column="COUNTER_TYPE", max_length=200, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=200, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=200, blank=True, null=True
    )
    year = models.DecimalField(
        db_column="YEAR", max_digits=20, decimal_places=2, blank=True, null=True
    )
    quarter = models.CharField(
        db_column="QUARTER", max_length=200, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=200, blank=True, null=True)
    bucket = models.CharField(db_column="BUCKET", max_length=200, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    bottom_up_retailer_targets = models.DecimalField(
        db_column="BOTTOM_UP_RETAILER_TARGETS",
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=20, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DF_BOTTOM_UP_TARGETS_MONTHLY2"


class ConsensusTarget(models.Model):
    """Consensus target model class."""

    id = models.AutoField(db_column="Id", primary_key=True)
    zone = models.CharField(db_column="Zone", max_length=20, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    month = models.CharField(db_column="Month", max_length=20, blank=True, null=True)
    date = models.DateField(db_column="Date", blank=True, null=True)
    consensus_target = models.DecimalField(
        db_column="Consensus target",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    brand = models.CharField(db_column="Brand", max_length=20, blank=True, null=True)
    premium_product_target = models.DecimalField(
        db_column="Premium_Product_Target",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    other_product_target = models.DecimalField(
        db_column="Other_Product_Target",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    nt_poduct_target = models.DecimalField(
        db_column="Nt_Poduct_Target",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    # Below line commented because it's not present anywhere at the time
    # of addition and might create some error in post APIs.
    # consensus_types = models.CharField(
    #     db_column="CONSENSUS_TYPES", max_length=20, blank=True, null=True
    # )

    class Meta:
        managed = False
        db_table = "CONSENSUS_TARGET"


class TdtMultiplier(models.Model):
    state = models.CharField(db_column="State", max_length=50, blank=True, null=True)
    multiplier = models.DecimalField(
        db_column="Multiplier", max_digits=10, decimal_places=2, blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)

    class Meta:
        managed = False
        db_table = "TDT_Multiplier"


class MarketMappingMarketPotential(models.Model):
    """Market mapping market potentials model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=300, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=300, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=300, blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_MARKET_POTENTIAL"


class MarketMappingGrowthPotential(models.Model):
    """Market mapping growth potential model class."""

    id = models.AutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=300, blank=True, null=True)
    month = models.DateField(db_column="MONTH", blank=True, null=True)
    target_type = models.CharField(
        db_column="TARGET_TYPE", max_length=300, blank=True, null=True
    )
    previous = models.DecimalField(
        db_column="PREVIOUS", max_digits=20, decimal_places=2, blank=True, null=True
    )
    current = models.DecimalField(
        db_column="CURRENT", max_digits=20, decimal_places=2, blank=True, null=True
    )
    next = models.DecimalField(
        db_column="NEXT", max_digits=20, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_GROWTH_POTENTIAL"


class MarketMappingRun(models.Model):
    run_id = models.AutoField(db_column="RUN_ID", primary_key=True)
    run_type = models.CharField(
        db_column="RUN_TYPE", max_length=50, blank=True, null=True
    )
    run_date = models.DateField(db_column="RUN_DATE", blank=True, null=True)
    plan_month = models.DateTimeField(
        db_column="PLAN_MONTH", max_length=50, blank=True, null=True
    )
    plan_quarter = models.CharField(
        db_column="PLAN_QUARTER", max_length=50, blank=True, null=True
    )
    plan_year = models.CharField(
        db_column="PLAN_YEAR", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_RUN"


class MarketMappingStateClassification(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    sales = models.FloatField(db_column="SALES", blank=True, null=True)
    avg_ncr = models.FloatField(db_column="AVG_NCR", blank=True, null=True)
    market_potential = models.FloatField(
        db_column="MARKET_POTENTIAL", blank=True, null=True
    )
    market_share = models.FloatField(db_column="MARKET_SHARE", blank=True, null=True)
    prev_year_share_delta = models.FloatField(
        db_column="PREV_YEAR_SHARE_DELTA", blank=True, null=True
    )
    prev_month_share_delta = models.FloatField(
        db_column="PREV_MONTH_SHARE_DELTA", blank=True, null=True
    )
    leader_market_share = models.FloatField(
        db_column="LEADER_MARKET_SHARE", blank=True, null=True
    )
    delta_market_share_max = models.FloatField(
        db_column="DELTA_MARKET_SHARE_MAX", blank=True, null=True
    )
    ncr_market_potential_rating = models.CharField(
        db_column="NCR_MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
    )
    market_potential_rating = models.CharField(
        db_column="MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
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
    market_lucrativeness = models.CharField(
        db_column="MARKET_LUCRATIVENESS", max_length=50, blank=True, null=True
    )
    market_position = models.CharField(
        db_column="MARKET_POSITION", max_length=50, blank=True, null=True
    )
    market_growth_strategy = models.CharField(
        db_column="MARKET_GROWTH_STRATEGY", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_STATE_CLASSIFICATION"


class MarketMappingDistrictClassification(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    sales = models.FloatField(db_column="SALES", blank=True, null=True)
    market_potential = models.FloatField(
        db_column="MARKET_POTENTIAL", blank=True, null=True
    )
    market_share = models.FloatField(db_column="MARKET_SHARE", blank=True, null=True)
    prev_year_share_delta = models.FloatField(
        db_column="PREV_YEAR_SHARE_DELTA", blank=True, null=True
    )
    prev_month_share_delta = models.FloatField(
        db_column="PREV_MONTH_SHARE_DELTA", blank=True, null=True
    )
    leader_market_share = models.FloatField(
        db_column="LEADER_MARKET_SHARE", blank=True, null=True
    )
    market_leader = models.CharField(
        db_column="MARKET_LEADER", max_length=50, blank=True, null=True
    )
    delta_market_share_max = models.FloatField(
        db_column="DELTA_MARKET_SHARE_MAX", blank=True, null=True
    )
    ncr_market_potential_rating = models.CharField(
        db_column="NCR_MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
    )
    market_potential_rating = models.CharField(
        db_column="MARKET_POTENTIAL_RATING", max_length=50, blank=True, null=True
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
    market_lucrativeness = models.CharField(
        db_column="MARKET_LUCRATIVENESS", max_length=50, blank=True, null=True
    )
    market_position = models.CharField(
        db_column="MARKET_POSITION", max_length=50, blank=True, null=True
    )
    market_growth_strategy = models.CharField(
        db_column="MARKET_GROWTH_STRATEGY", max_length=50, blank=True, null=True
    )
    avg_ncr = models.FloatField(db_column="AVG_NCR", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_DISTRICT_CLASSIFICATION"


class MarketMappingSalesTarget(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    zone = models.CharField(db_column="ZONE", max_length=50, blank=True, null=True)
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="REGION", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=50, blank=True, null=True
    )
    sales = models.FloatField(db_column="SALES", blank=True, null=True)
    target_sales = models.FloatField(db_column="TARGET_SALES", blank=True, null=True)
    future_market_potential = models.FloatField(
        db_column="FUTURE_MARKET_POTENTIAL", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_SALES_TARGET"


class MarketMappingChannelStrategy(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    total_retail_sales = models.FloatField(
        db_column="TOTAL_RETAIL_SALES", blank=True, null=True
    )
    counter_share = models.FloatField(db_column="COUNTER_SHARE", blank=True, null=True)
    total_sales = models.BigIntegerField(db_column="TOTAL_SALES", blank=True, null=True)
    acv = models.FloatField(db_column="ACV", blank=True, null=True)
    min_target_acv = models.FloatField(
        db_column="MIN_TARGET_ACV", blank=True, null=True
    )
    max_target_acv = models.FloatField(
        db_column="MAX_TARGET_ACV", blank=True, null=True
    )
    future_market_share = models.FloatField(
        db_column="FUTURE_MARKET_SHARE", blank=True, null=True
    )
    future_market_share_thres = models.FloatField(
        db_column="FUTURE_MARKET_SHARE_THRES", blank=True, null=True
    )
    counter_share_target = models.FloatField(
        db_column="COUNTER_SHARE_TARGET", blank=True, null=True
    )
    counter_share_strategy = models.CharField(
        db_column="COUNTER_SHARE_STRATEGY", max_length=50, blank=True, null=True
    )
    retail_sale = models.FloatField(db_column="RETAIL_SALE", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_CHANNEL_STRATEGY"


class MarketMappingCounterStrategy(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    counter_name = models.CharField(
        db_column="COUNTER_NAME", max_length=100, blank=True, null=True
    )
    address_block = models.TextField(db_column="ADDRESS_BLOCK", blank=True, null=True)
    collected_on = models.DateField(db_column="COLLECTED_ON", blank=True, null=True)
    counter_share_action = models.CharField(
        db_column="COUNTER_SHARE_ACTION", max_length=100, blank=True, null=True
    )
    total_retail_sales = models.FloatField(
        db_column="TOTAL_RETAIL_SALES", blank=True, null=True
    )
    counter_share = models.FloatField(db_column="COUNTER_SHARE", blank=True, null=True)
    total_market_sale = models.FloatField(
        db_column="TOTAL_MARKET_SALE", blank=True, null=True
    )
    contribution_to_market_sale = models.FloatField(
        db_column="CONTRIBUTION_TO_MARKET_SALE", blank=True, null=True
    )
    scl_retail_sale = models.BigIntegerField(
        db_column="SCL_RETAIL_SALE", blank=True, null=True
    )
    scl_counter_share = models.FloatField(
        db_column="SCL_COUNTER_SHARE", blank=True, null=True
    )
    retail_sale = models.BigIntegerField(db_column="RETAIL_SALE", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_COUNTER_STRATEGY"


class MarketMappingBrandingOuput(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey(MarketMappingRun, models.DO_NOTHING, db_column="RUN_ID")
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    tot_cost_rs_lac = models.FloatField(
        db_column="TOT_COST_RS_LAC", blank=True, null=True
    )
    quantity_invoiced = models.FloatField(
        db_column="QUANTITY_INVOICED", blank=True, null=True
    )
    target_sales = models.FloatField(db_column="TARGET_SALES", blank=True, null=True)
    per_mt_cost = models.FloatField(db_column="PER_MT_COST", blank=True, null=True)
    new_cost = models.FloatField(db_column="NEW_COST", blank=True, null=True)
    multiplier = models.FloatField(db_column="MULTIPLIER", blank=True, null=True)
    budget = models.FloatField(db_column="BUDGET", blank=True, null=True)
    pos_budget = models.FloatField(db_column="POS_BUDGET", blank=True, null=True)
    outdoor_budget = models.FloatField(
        db_column="OUTDOOR_BUDGET", blank=True, null=True
    )
    event_budget = models.FloatField(db_column="EVENT_BUDGET", blank=True, null=True)
    corporate_budget = models.FloatField(
        db_column="CORPORATE_BUDGET", blank=True, null=True
    )
    total_budget = models.FloatField(db_column="TOTAL_BUDGET", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_BRANDING_OUPUT"


class MarketMappingPricingOuput(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    run = models.ForeignKey("MarketMappingRun", models.DO_NOTHING, db_column="RUN_ID")
    state = models.CharField(db_column="STATE", max_length=50, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=50, blank=True, null=True
    )
    brand = models.CharField(db_column="BRAND", max_length=50, blank=True, null=True)
    wsp_price = models.FloatField(db_column="WSP_PRICE", blank=True, null=True)
    wsp_leader_price = models.FloatField(
        db_column="WSP_LEADER_PRICE", blank=True, null=True
    )
    wsp_leader_gap = models.FloatField(
        db_column="WSP_LEADER_GAP", blank=True, null=True
    )
    wsp_price_leader = models.CharField(
        db_column="WSP_PRICE_LEADER", max_length=50, blank=True, null=True
    )
    wsp_min_margin = models.FloatField(
        db_column="WSP_MIN_MARGIN", blank=True, null=True
    )
    wsp_max_margin = models.FloatField(
        db_column="WSP_MAX_MARGIN", blank=True, null=True
    )
    rsp_price = models.FloatField(db_column="RSP_PRICE", blank=True, null=True)
    rsp_leader_price = models.FloatField(
        db_column="RSP_LEADER_PRICE", blank=True, null=True
    )
    rsp_leader_gap = models.FloatField(
        db_column="RSP_LEADER_GAP", blank=True, null=True
    )
    rsp_price_leader = models.CharField(
        db_column="RSP_PRICE_LEADER", max_length=50, blank=True, null=True
    )
    rsp_min_margin = models.FloatField(
        db_column="RSP_MIN_MARGIN", blank=True, null=True
    )
    rsp_max_margin = models.FloatField(
        db_column="RSP_MAX_MARGIN", blank=True, null=True
    )
    pricing_strategy = models.CharField(
        db_column="PRICING_STRATEGY", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "MARKET_MAPPING_PRICING_OUPUT"


class DemandForMarketMapping(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    month = models.DateTimeField(db_column="MONTH", blank=True, null=True)
    destination = models.DecimalField(
        db_column="DESTINATION", max_digits=19, decimal_places=2, blank=True, null=True
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
    created_at = models.DateTimeField(db_column="CREATED_AT", blank=True, null=True)
    updated_at = models.DateTimeField(db_column="UPDATED_AT", blank=True, null=True)
    packaging = models.CharField(
        db_column="PACKAGING", max_length=50, blank=True, null=True
    )
    di_perc = models.DecimalField(
        db_column="DI_perc", max_digits=4, decimal_places=0, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "DEMAND"


class BottomUpNt(models.Model):
    state = models.CharField(db_column="STATE", max_length=20, blank=True, null=True)
    customer_name = models.CharField(
        db_column="CUSTOMER NAME", max_length=20, blank=True, null=True
    )
    customer_type = models.CharField(
        db_column="CUSTOMER TYPE", max_length=20, blank=True, null=True
    )
    year = models.DecimalField(
        db_column="YEAR", max_digits=22, decimal_places=0, blank=True, null=True
    )
    quarter = models.CharField(
        db_column="QUARTER", max_length=20, blank=True, null=True
    )
    month = models.CharField(db_column="MONTH", max_length=20, blank=True, null=True)
    date = models.DateField(db_column="DATE", blank=True, null=True)
    brand = models.CharField(db_column="BRAND", max_length=20, blank=True, null=True)
    product = models.CharField(
        db_column="PRODUCT", max_length=20, blank=True, null=True
    )
    pack_type = models.CharField(
        db_column="PACK_TYPE", max_length=20, blank=True, null=True
    )
    packaging = models.CharField(
        db_column="PACKAGING", max_length=20, blank=True, null=True
    )
    cust_category = models.CharField(
        db_column="CUST_CATEGORY", max_length=20, blank=True, null=True
    )
    demand_qty = models.DecimalField(
        db_column="DEMAND QTY", max_digits=22, decimal_places=2, blank=True, null=True
    )
    id = models.AutoField(db_column="ID", primary_key=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "BOTTOM_UP_NT"


class UrlMapping(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=255, blank=True, null=True)
    url = models.CharField(db_column="URL", max_length=3000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "URL_MAPPING"


class DepotAdditionMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=360, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=360, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=360, blank=True, null=True)
    secondary_ptpk = models.DecimalField(
        db_column="SECONDARY_PTPK",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    promised_market_sla = models.DecimalField(
        db_column="PROMISED_MARKET_SLA",
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
        db_table = "DEPOT_ADDITION_MASTER"
        unique_together = ("state", "district", "taluka")


class ExistingDepotLocations(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
    )
    taluka = models.CharField(db_column="TALUKA", max_length=540, blank=True, null=True)
    type = models.CharField(db_column="TYPE", max_length=540, blank=True, null=True)
    existing_depo_lead = models.DecimalField(
        db_column="EXISTING_DEPO_LEAD",
        max_digits=22,
        decimal_places=2,
        blank=True,
        null=True,
    )
    run_id = models.BigIntegerField(db_column="RUN_ID", blank=True, null=True)
    lat = models.DecimalField(
        db_column="LAT", max_digits=22, decimal_places=10, blank=True, null=True
    )
    long = models.DecimalField(
        db_column="LONG", max_digits=22, decimal_places=10, blank=True, null=True
    )
    potential = models.BigIntegerField(db_column="POTENTIAL", blank=True, null=True)
    depot_lat = models.DecimalField(
        db_column="DEPOT_LAT", max_digits=22, decimal_places=10, blank=True, null=True
    )
    depot_long = models.DecimalField(
        db_column="DEPOT_LONG", max_digits=22, decimal_places=10, blank=True, null=True
    )
    depot_name = models.CharField(
        db_column="DEPOT_NAME", max_length=200, blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "EXISTING_DEPOT_LOCATIONS"
