from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from accounts.models import TgtRlsRoleData, User, UserRole

# class UserRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRole
#         fields = ("role_name", )


class LoginSerializer(serializers.ModelSerializer):
    """Login serializer."""

    # user_role = UserRoleSerializer(many=True)
    email = serializers.EmailField()
    token = serializers.SerializerMethodField()
    session_key = serializers.SerializerMethodField()
    # user_role = UserRoleSerializer(many=True)
    user_role = serializers.SerializerMethodField()
    user_state = serializers.SerializerMethodField()
    user_zone = serializers.SerializerMethodField()
    user_district = serializers.SerializerMethodField()
    user_regions = serializers.SerializerMethodField()
    user_plant_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "token",
            "session_key",
            "user_role",
            "user_state",
            "user_zone",
            "user_district",
            "user_regions",
            "user_plant_name",
        )
        # read_only_fields = ("user_role'",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if user:
            return user
        raise serializers.ValidationError("Incorrect credentials.")

    def get_token(self, user):
        return "Token " + user.get_auth_token()

    def get_session_key(self, user):
        session = self.context.get("session")
        session.save()
        return session.session_key

    def get_user_role(self, value):
        user_roles = UserRole.objects.filter(user__email=value).values("role_name")
        return user_roles

    def get_user_state(Self, value):
        if TgtRlsRoleData.objects.filter(email=value).values("state"):
            return TgtRlsRoleData.objects.filter(email=value).values("state")
        else:
            return None

    def get_user_zone(Self, value):
        if TgtRlsRoleData.objects.filter(email=value).values("zone"):
            return TgtRlsRoleData.objects.filter(email=value).values("zone")
        else:
            return None

    def get_user_district(Self, value):
        if TgtRlsRoleData.objects.filter(email=value).values("district"):
            return TgtRlsRoleData.objects.filter(email=value).values("district")
        else:
            return None

    def get_user_regions(Self, value):
        if TgtRlsRoleData.objects.filter(email=value).values("regions"):
            return TgtRlsRoleData.objects.filter(email=value).values("regions")
        else:
            return None

    def get_user_plant_name(Self, value):
        if TgtRlsRoleData.objects.filter(email=value).values("plant_name"):
            return TgtRlsRoleData.objects.filter(email=value).values("plant_name")
        else:
            return None
