from rest_framework import serializers

from analytical_data.models import (
    SchemeFor,
    SchemeLocation,
    SchemeProducts,
    SchemeRewards,
    Schemes,
)
from analytical_data.models.scheme_models import CrmComplaints


class SchemesSerializer(serializers.ModelSerializer):
    scheme_products_rel = serializers.SerializerMethodField()
    scheme_location_rel = serializers.SerializerMethodField()
    scheme_for_rel = serializers.SerializerMethodField()

    schemerewards_rel = serializers.SerializerMethodField()

    class Meta:
        model = Schemes
        fields = "__all__"

    def get_schemerewards_rel(self, data):
        schemewardsobj = SchemeRewards.objects.filter(scheme=data.id).values(
            "rewards_points", "rewards", "gift", "cash"
        )
        return schemewardsobj

    def get_scheme_for_rel(self, data):
        schemeforobj = SchemeFor.objects.filter(scheme=data.id).values(
            "scheme_for_code"
        )
        return schemeforobj

    def get_scheme_products_rel(self, data):
        schmeProductsObj = SchemeProducts.objects.filter(scheme=data.id).values(
            # "org_id", "grade", "packaging", "bag_type",
            "no_of_bags"
        )
        return schmeProductsObj

    def get_scheme_location_rel(self, data):
        schmelocationObj = SchemeLocation.objects.filter(scheme=data.id).values(
            "state", "district"
        )
        # for keys in schmelocationObj:
        #     SchemeProductsDict = {"state": keys["state"], "district": keys["district"]}
        #     return SchemeProductsDict
        return schmelocationObj


class SchemeProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeProducts
        fields = "__all__"


class SchemeForSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeFor
        fields = "__all__"


class SchemeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeLocation
        fields = "__all__"


class SchemeRewardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeRewards
        fields = "__all__"


# National Technical Head Work
class CrmComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmComplaints
        fields = "__all__"
