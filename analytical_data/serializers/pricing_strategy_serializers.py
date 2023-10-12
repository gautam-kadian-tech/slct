"""
This module contains implementation of bulk create and bulk update in
serializers.
"""
from datetime import datetime

from django.db import IntegrityError
from rest_framework import serializers

from analytical_data.models.marketing_branding_models import (
    NewMarketPricingApproval,
)
from analytical_data.models.pricing_strategy_models import *
from analytical_data.models.state_head_models import PricingProposalApproval
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateListSerializer,
    BulkUpdateOrCreateListSerializer,
    serializers,
)


class CompetitionPriceNewMarketsSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CompetitionPriceNewMarkets
        list_serializer_class = BulkUpdateListSerializer
        exclude = ("id",)
        editable_fields = {"zone", "state", "region", "district", "brand", "price"}


class CompetitionPriceNewMarketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionPriceNewMarkets
        fields = "__all__"


class CompetitionPriceNewMarketsDownloadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CompetitionPriceNewMarkets
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "zone",
            "state",
            "region",
            "district",
            "brand",
            "price",
            "date",
            "value",
            "business_segment",
            "grade",
        }


class PriceBenchmarksDownloadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = PriceBenchmarks
        list_serializer_class = BulkUpdateOrCreateListSerializer
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        editable_fields = {
            "zone",
            "state",
            "district",
            "month",
            "benchmark_name",
            "price_difference_to_be_maintained",
            "business_segment",
            "grade",
        }


class PriceBenchmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceBenchmarks
        fields = "__all__"


class NewPriceComputationSerializer(serializers.ModelSerializer):
    market_data = serializers.SerializerMethodField()
    market_pricing_approval = serializers.SerializerMethodField()

    class Meta:
        model = NewPriceComputation
        fields = "__all__"

    def get_market_pricing_approval(self, data):
        market_data = (
            NewMarketPricingApproval.objects.filter(price_computation_key__id=data.id)
            .values()
            .first()
        )

        return market_data

    def get_market_data(self, data):
        date = datetime.strftime(data.date, "%Y-%m-%d")
        data_date = datetime.strptime(date, "%Y-%m-%d")
        data_date = data_date.replace(day=1)

        market_obj = (
            NmMarket4X4Output.objects.filter(
                zone=data.zone,
                state=data.state,
                district=data.district,
                month=data_date,
                business_segment=data.business_segment,
            )
            .values("pricing_strategy", "wsp_price", "sales")
            .order_by("month")
            .first()
        )
        try:
            pricing_strategy = market_obj["pricing_strategy"]
        except:
            pricing_strategy = None
        try:
            sales = market_obj["sales"]
        except:
            sales = 0
        try:
            wsp_price = market_obj["wsp_price"]
        except:
            wsp_price = 0
        try:
            min_price = data.price_min
        except:
            min_price = 0
        try:
            max_price = data.price_max
        except:
            max_price = 0
        data = {
            "rev_min": min_price * sales,
            "rev_max": max_price * sales,
            "wsp_price_4*4": wsp_price,
            "pricing_strategy": pricing_strategy,
            "revenue": wsp_price * sales,
            "sales": sales,
        }
        return data


class NmMarketSharePotentialDownloadSerializer(BulkOperationsModelSerializer):
    class Meta:
        model = NmMarketSharePotential
        list_serializer_class = BulkUpdateOrCreateListSerializer
        exclude = ()
        editable_fields = {
            "zone",
            "state",
            "district",
            "brand",
            "month",
            "sales",
            "market_potential",
            "market_share",
            "delta_market_share",
            "business_segment",
            "grade",
        }


class NmMarket4X4OutputListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PpShiftDetails."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class NmMarket4X4OutputSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = NmMarket4X4Output
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = NmMarket4X4OutputListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )
        # validated_data.update({"created_by":self.context.get("request_user")})

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class NmMarket4X4OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = NmMarket4X4Output
        fields = "__all__"


class SoLeagueWeightageSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = SoLeagueWeightage
        fields = "__all__"
        list_serializer_class = BulkUpdateListSerializer
        read_only_fields = (
            "last_update_login",
            "last_update_date",
            "last_updated_by",
            "creation_date",
            "created_by",
            "kpi_name",
            "kpi",
        )
        editable_fields = {"weightage"}


# class PriceChangeRequestApprovalSerializer(serializers.ModelSerializer):
#     wsp_price = serializers.SerializerMethodField()
#     rsp_price = serializers.SerializerMethodField()
#     benchmark_name = serializers.SerializerMethodField()
#     price_difference = serializers.SerializerMethodField()

#     class Meta:
#         model = PriceChangeRequestApproval
#         fields = "__all__"

#     def get_wsp_price(self, data):
#         wsp_price = (
#             PricingProposalApproval.objects.filter(
#                 crm_pricing_key__brand__in=data.brand
#             )
#             .values("wsp_price")
#             .first()
#         )

#         return wsp_price

#     def get_rsp_price(self, data):
#         rsp_price = (
#             PricingProposalApproval.objects.filter(
#                 crm_pricing_key__brand__in=data.brand
#             )
#             .values("rsp_price")
#             .first()
#         )
#         return rsp_price

#     def get_benchmark_name(self, data):
#         benchmark_name = (
#             PriceBenchmarks.objects.filter(district=data.district)
#             .values("benchmark_name")
#             .distinct()
#         )
#         return benchmark_name

#     def get_price_difference(self, data):
#         price_difference = (
#             PriceBenchmarks.objects.filter(district=data.district)
#             .values("price_difference_to_be_maintained")
#             .distinct()
#         )
#         return price_difference


class PriceChangeRequestApprovalSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    wsp_price_and_rsp_price = serializers.SerializerMethodField()
    benchmark_name_and_price_difference = serializers.SerializerMethodField()

    class Meta:
        model = PriceChangeRequestApproval
        # fields = "__all__"
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "status",
            "comments_of_approval",
            "comments_of_raiser",
        }

    def get_wsp_price_and_rsp_price(self, data):
        wsp_price = (
            PricingProposalApproval.objects.filter(
                crm_pricing_key__brand__in=data.brand
            ).values("wsp_price", "rsp_price")
        ).first()

        return wsp_price

    def get_benchmark_name_and_price_difference(self, data):
        benchmark_name = (
            PriceBenchmarks.objects.filter(district=data.district).values(
                "benchmark_name", "price_difference_to_be_maintained"
            )
        ).first()
        return benchmark_name
