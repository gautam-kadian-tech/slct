"""Models module to manage users."""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

from accounts.user_role_choices import UserActionChoices, UserRoleChoice
from Master_Data_Sales.models import ZoneMappingNew


class UserManager(BaseUserManager):
    """User manager create to create superuser"""

    def create_superuser(self, email, name, password):
        """create method for super user"""
        user = self.model(email=UserManager.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# class CustomToken(Token):
#     """Custom token class to handle role based login."""

#     id = models.AutoField(primary_key=True)
#     role = models.CharField(max_length=20, choices=UserRoleChoice.choices)


class User(AbstractUser):
    """Main User Model for table users"""

    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=255, db_index=True)
    # last_login = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # role = models.CharField(
    #     max_length=20, choices=UserRoleChoice.choices, null=True, blank=True
    # )
    # user_role = models.ManyToManyField(UserRole)

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        db_table = "users"
        managed = True

    def __str__(self):
        return self.email

    def get_auth_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key


def set_password(sender, instance, **kwargs):
    random_pass = "Password@123456"
    if (
        not instance.password
        and not User.objects.filter(email=instance.email).exists()
        and not instance.password
    ):
        hashed_pwd = make_password(random_pass)
        instance.password = hashed_pwd


models.signals.pre_save.connect(set_password, sender=User)


class UserLoginDetail(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="USER", blank=True, null=True
    )
    activity_type = models.CharField(
        db_column="ACTIVITY_TYPE", max_length=150, choices=UserActionChoices.choices
    )
    date_time = models.DateTimeField(db_column="DATE_TIME", auto_now_add=True)

    class Meta:
        managed = False
        db_table = "USER_LOGIN_DETAIL"


class UserRole(models.Model):
    role_name = models.CharField(max_length=50, choices=UserRoleChoice.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roles")

    def __str__(self):
        return self.role_name

    class Meta:
        unique_together = (
            "role_name",
            "user",
        )


class TgtRlsRoleData(models.Model):
    emp_id = models.DecimalField(
        db_column="Emp_Id",
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
    )
    name = models.CharField(db_column="Name", max_length=100)
    email = models.CharField(db_column="Email", max_length=100)
    role = models.CharField(
        db_column="Role",
        max_length=100,
        choices=UserRoleChoice.choices,
        null=True,
        blank=True,
    )
    ZONE_CHOICES = (
        ("East", "East"),
        ("North 1", "North 1"),
        ("North 2", "North 2"),
        ("South West", "South West"),
        ("Central", "Central"),
        ("North", "North"),
    )
    zone = models.CharField(
        db_column="Zone", max_length=100, choices=ZONE_CHOICES, null=True, blank=True
    )
    STATE_CHOICES = (
        ("Jharkhand", "Jharkhand"),
        ("Gujarat", "Gujarat"),
        ("Rajasthan-A", "Rajasthan-A"),
        ("Punjab-S", "Punjab-S"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Outside India", "Outside India"),
        ("Bihar-S", "Bihar-S"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Delhi", "Delhi"),
        ("Haryana-1", "Haryana-1"),
        ("Assam", "Assam"),
        ("Rajasthan-B", "Rajasthan-B"),
        ("Punjab-N", "Punjab-N"),
        ("West Bengal", "West Bengal"),
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Bihar-N", "Bihar-N"),
        ("Telangana", "Telangana"),
        ("Haryana-2", "Haryana-2"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Rajasthan-C", "Rajasthan-C"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("MH-1", "MH-1"),
        ("TEST STATE 2", "TEST STATE 2"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("WEST UP", "WEST UP"),
        ("MH-2", "MH-2"),
        ("EAST UP", "EAST UP"),
        ("Goa", "Goa"),
        ("Odisha", "Odisha"),
        ("C-UP", "C-UP"),
        ("Uttranchal", "Uttranchal"),
        ("Jammu & Kashmir", "Jammu & Kashmir"),
    )
    STATE_CHOICES = sorted(STATE_CHOICES, key=lambda x: x[0])
    state = models.CharField(
        db_column="State", max_length=100, choices=STATE_CHOICES, null=True, blank=True
    )
    district = models.CharField(
        db_column="DISTRICT", max_length=100, null=True, blank=True
    )
    REGION_CHOICES = (
        ("Meerut", "Meerut"),
        ("TEST REGION 2", "TEST REGION 2"),
        ("Jaipur", "Jaipur"),
        ("Purnea", "Purnea"),
        ("Bhilwara", "Bhilwara"),
        ("Sambalpur", "Sambalpur"),
        ("Gwalior", "Gwalior"),
        ("Kashipur", "Kashipur"),
        ("Bhagalpur", "Bhagalpur"),
        ("Pali", "Pali"),
        ("Hissar", "Hissar"),
        ("Vidarbha", "Vidarbha"),
        ("Dhanbad", "Dhanbad"),
        ("Karimnagar", "Karimnagar"),
        ("Aligarh", "Aligarh"),
        ("Vikarabad", "Vikarabad"),
        ("Bilaspur", "Bilaspur"),
        ("Mahabub Nagar", "Mahabub Nagar"),
        ("Kalaburagi", "Kalaburagi"),
        ("Ahmednagar", "Ahmednagar"),
        ("Ajmer", "Ajmer"),
        ("Gurgaon", "Gurgaon"),
        ("Solan", "Solan"),
        ("Kurnool", "Kurnool"),
        ("Karnal-1", "Karnal-1"),
        ("Ludhiana", "Ludhiana"),
        ("Durgapur", "Durgapur"),
        ("Marathawada", "Marathawada"),
        ("Belgaum", "Belgaum"),
        ("Jabalpur", "Jabalpur"),
        ("Agra", "Agra"),
        ("Bareilly", "Bareilly"),
        ("Satara", "Satara"),
        ("Kolhapur", "Kolhapur"),
        ("Daltonganj", "Daltonganj"),
        ("Surat", "Surat"),
        ("Baleshwar", "Baleshwar"),
        ("Kanpur", "Kanpur"),
        ("Cuttack", "Cuttack"),
        ("Ranchi", "Ranchi"),
        ("Rajkot", "Rajkot"),
        ("Bikaner", "Bikaner"),
        ("Varanasi", "Varanasi"),
        ("Dehradoon", "Dehradoon"),
        ("Faridabad", "Faridabad"),
        ("Muzaffarpur", "Muzaffarpur"),
        ("Bhatinda", "Bhatinda"),
        ("Kota", "Kota"),
        ("OTHERS", "OTHERS"),
        ("Patna", "Patna"),
        ("Siwan", "Siwan"),
        ("Hyderabad", "Hyderabad"),
        ("Bharatpur", "Bharatpur"),
        ("Khandesh", "Khandesh"),
        ("Udaipur", "Udaipur"),
        ("Indore", "Indore"),
        ("Jammu", "Jammu"),
        ("Gaya", "Gaya"),
        ("Mumbai", "Mumbai"),
        ("Outside India", "Outside India"),
        ("Aurangabad", "Aurangabad"),
        ("Rudrapur", "Rudrapur"),
        ("Rangareddy", "Rangareddy"),
        ("Amritsar", "Amritsar"),
        ("Pune", "Pune"),
        ("Motihari", "Motihari"),
        ("Raipur", "Raipur"),
        ("Lucknow", "Lucknow"),
        ("Ghaziabad", "Ghaziabad"),
        ("Patiala", "Patiala"),
        ("Kolkata", "Kolkata"),
        ("Karnal-2", "Karnal-2"),
        ("Durg", "Durg"),
        ("Ahmedabad", "Ahmedabad"),
        ("Chandigarh", "Chandigarh"),
        ("Gorakhpur", "Gorakhpur"),
        ("Malda", "Malda"),
        ("Vadodara", "Vadodara"),
        ("Jhunjhunu", "Jhunjhunu"),
        ("Region Not Mapped", "Region Not Mapped"),
    )

    REGION_CHOICES = sorted(REGION_CHOICES, key=lambda x: x[0])

    regions = models.CharField(
        db_column="REGIONS",
        max_length=100,
        choices=REGION_CHOICES,
        null=True,
        blank=True,
    )
    PLANT_CHOICES = (
        ("Kodla", "Kodla"),
        ("JGU Clk", "JGU Clk"),
        ("Patas", "Patas"),
        ("UPGU Clk", "UPGU Clk"),
        ("AACB", "AACB"),
        ("SGU-2", "SGU-2"),
        ("RAS", "RAS"),
        ("Purulia Clk", "Purulia Clk"),
        ("RNCU", "RNCU"),
        ("BWR", "BWR"),
        ("PATAS Clk", "PATAS Clk"),
        ("RGU", "RGU"),
        ("RGU Clk", "RGU Clk"),
        ("KKG", "KKG"),
        ("Ras Clk", "Ras Cl"),
        ("Kodla Clk", "Kodla Clk"),
        ("JHGU Clk", "JHGU Clk"),
        ("BGU-1", "BGU-1"),
        ("KKG Clk", "KKG Clk"),
        ("JHGU", "JHGU"),
        ("ODGU", "ODGU"),
        ("BGU-2", "BGU-2"),
        ("PGU", "PGU"),
        ("JGU", "JGU"),
        ("UPGU", "UPGU"),
        ("Purulia", "Purulia"),
        ("PGU Clk", "PGU Clk"),
        ("SGU-1 Clk", "SGU-1 Clk"),
        ("SRCP Clk", "SRCP Clk"),
        ("ODGU Clk", "ODGU Clk"),
        ("SGU-2 Clk", "SGU-2 Clk"),
        ("BWR Clk", "BWR Clk"),
        ("SRCP", "SRCP"),
        ("BGU-2 Clk", "BGU-2 Clk"),
        ("BGU-1 Clk", "BGU-1 Clk"),
    )
    plant_name = models.CharField(
        db_column="PLANT_NAME",
        max_length=100,
        choices=PLANT_CHOICES,
        null=True,
        blank=True,
    )
    id = models.BigAutoField(db_column="ID", primary_key=True)
    transporter_company_name = models.TextField(
        db_column="TRANSPORTER_COMPANY_NAME", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE", auto_now=True)
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "TGT_RLS_ROLE_DATA"
        verbose_name_plural = "Tgt Rls Role Data"


class TrackingVisitor(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    ip_address = models.CharField(max_length=39)
    user_agent = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    expiry_age = models.IntegerField(blank=True, null=True)
    expiry_time = models.DateTimeField(blank=True, null=True)
    time_on_site = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("User", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tracking_visitor"


class TrackingPageview(models.Model):
    url = models.TextField()
    referer = models.TextField(blank=True, null=True)
    query_string = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=20, blank=True, null=True)
    view_time = models.DateTimeField()
    visitor = models.ForeignKey("TrackingVisitor", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tracking_pageview"


class UserUrlScreenNameMapping(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    url = models.TextField(db_column="URL", blank=True, null=True)
    screen_name = models.TextField(db_column="SCREEN_NAME", blank=True, null=True)
    persona = models.TextField(db_column="PERSONA", blank=True, null=True)
    page_action = models.TextField(db_column="PAGE_ACTION", blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "USER_URL_SCREEN_NAME_MAPPING"


class RoleNameFunctionType(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    role_name = models.CharField(
        db_column="ROLE NAME", max_length=540, blank=True, null=True
    )
    function = models.CharField(
        db_column="FUNCTION", max_length=540, blank=True, null=True
    )
    type = models.CharField(db_column="TYPE", max_length=540, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "ROLE_NAME_FUNCTION_TYPE"


class ZoneMappingNeww(models.Model):
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
        db_column="CITY_ID", max_digits=50, decimal_places=2, blank=True, null=True
    )
    pincode = models.CharField(
        db_column="PINCODE", max_length=100, blank=True, null=True
    )
    active = models.CharField(db_column="ACTIVE", max_length=100, blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ZONE_MAPPING_NEW"


class Zone(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.CharField(db_column="ZONE", max_length=540, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "ZONE"


class State(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    zone = models.ForeignKey(
        "Zone", models.DO_NOTHING, db_column="ZONE_ID", blank=True, null=True
    )
    state = models.CharField(db_column="STATE", max_length=540, blank=True, null=True)
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")

    class Meta:
        managed = False
        db_table = "STATE"


class District(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    state = models.ForeignKey(
        "State", models.DO_NOTHING, db_column="STATE_ID", blank=True, null=True
    )  # Field name made lowercase.
    district = models.CharField(
        db_column="DISTRICT", max_length=540, blank=True, null=True
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
        db_table = "DISTRICT"


class Region(models.Model):
    id = models.BigAutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    district = models.ForeignKey(
        "District", models.DO_NOTHING, db_column="DISTRICT_ID", blank=True, null=True
    )  # Field name made lowercase.
    region = models.CharField(
        db_column="REGION", max_length=540, blank=True, null=True
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
        db_table = "REGION"
