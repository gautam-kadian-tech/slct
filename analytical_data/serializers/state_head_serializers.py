from calendar import monthrange
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter

import pandas as pd
from django.db import IntegrityError
from django.db.models import Sum
from rest_framework import serializers

from accounts.models import User
from analytical_data.models.non_trade_head_models import *
from analytical_data.models.state_head_models import *
from analytical_data.serializers.custom_serializers import (
    BulkOperationsAutoGenerateFieldsModelSerializer,
    BulkOperationsModelSerializer,
    BulkUpdateOrCreateListSerializer,
)


class SlctCashDiscPropsSerializer(serializers.ModelSerializer):
    cash_disc = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctCashDiscProps
        fields = "__all__"

    def get_cash_disc(self, data):
        case_discount_object = SlctCashDiscDaysIncentive.objects.filter(
            cash_disc=data.id
        ).values("no_of_days_upper", "no_of_days_lower", "incentive")
        return case_discount_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctCashDiscDaysIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctCashDiscDaysIncentive
        fields = "__all__"


class TNmOmxSchemesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TNmOmxSchemes
        fields = [
            "scheme_id",
            "scheme_type",
            "states",
            "districts",
            "scheme_status",
            "mitra_types",
            "org_id",
            "inventory_item_ids",
            "packing_types",
            "start_date",
            "end_date",
        ]


class SlctPartyWiseSchemePropsSerializer(serializers.ModelSerializer):
    party_wise_scheme = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctPartyWiseSchemeProps
        fields = "__all__"

    def get_party_wise_scheme(self, data):
        party_wise_scheme_object = SlctPartyWiseSchemePropsIncentive.objects.filter(
            party_wise_scheme=data.id
        ).values()
        return party_wise_scheme_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctPartyWiseSchemePropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctPartyWiseSchemePropsIncentive
        fields = "__all__"


class SlctQuantitySlabPropsSerializer(serializers.ModelSerializer):
    quantity_slab = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctQuantitySlabProps
        fields = "__all__"

    def get_quantity_slab(self, data):
        quantity_slab_object = SlctQuantitySlabPropsIncentive.objects.filter(
            quantity_slab=data.id
        ).values(
            "quantity_slab_lower",
            "quantity_slab_upper",
            "incentive",
            "incentive_kind",
        )
        return quantity_slab_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctQuantitySlabPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctQuantitySlabPropsIncentive
        fields = "__all__"


class SlctDirPltBilngDiscPropsSerializer(serializers.ModelSerializer):
    dir_plt_bilng = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctDirPltBilngDiscProps
        fields = "__all__"

    def get_dir_plt_bilng(self, data):
        dir_plt_bilng_object = SlctDirPltBilngDiscPropsIncentives.objects.filter(
            dir_plt_bilng=data.id
        ).values(
            "inc_district",
            "plant",
            "incentive",
        )
        return dir_plt_bilng_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctDirPltBilngDiscPropsIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctDirPltBilngDiscPropsIncentives
        fields = "__all__"


class SlctPrmPrdComboScmPropsSerializer(serializers.ModelSerializer):
    prm_prdt_combo = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctPrmPrdComboScmProps
        fields = "__all__"

    def get_prm_prdt_combo(self, data):
        prm_prdt_combo_object = SlctPrmPrdComboScmPropsIncentives.objects.filter(
            prm_prdt_combo=data.id
        ).values(
            "quantity_slab_lower",
            "quantity_slab_upper",
            "incentive",
            "inkind_incentive",
        )
        return prm_prdt_combo_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctPrmPrdComboScmPropsIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctPrmPrdComboScmPropsIncentives
        fields = "__all__"


class SlctVehicleSchPropsSerializer(serializers.ModelSerializer):
    vechicle_scheme_propsal_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctVehicleSchProps
        fields = "__all__"

    def get_vechicle_scheme_propsal_data(self, data):
        vechicle_scheme_propsal_data_obj = SlctVehicleSchPropsIncentives.objects.filter(
            vechicle_sch_props=data.id
        ).values()
        return vechicle_scheme_propsal_data_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctVehicleSchPropsIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctVehicleSchPropsIncentives
        fields = "__all__"


class SlctBorderDiscPropsSerializer(serializers.ModelSerializer):
    border_disc = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctBorderDiscProps
        fields = "__all__"

    def get_border_disc(self, data):
        border_discount_prop = SlctBorderDiscPropsIncentives.objects.filter(
            border_disc=data.id
        ).values("plant", "inc_district", "incentive", "border_disc")
        return border_discount_prop

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctBorderDiscPropsIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBorderDiscPropsIncentives
        fields = "__all__"


class SlctActivityPropsSerializer(serializers.ModelSerializer):
    activity_props = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctActivityProps
        fields = "__all__"

    def get_activity_props(self, data):
        activity_props_data = SlctActivityPropsIncentive.objects.filter(
            activity_props=data.id
        ).values("cost_head", "no_of_pax", "cost_per_head", "total_expense")
        return activity_props_data

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctActivityPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctActivityPropsIncentive
        fields = "__all__"


class SlctMasonKindSchPropsSerializer(serializers.ModelSerializer):
    bag_point_conv_data = serializers.SerializerMethodField()
    incentives_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_bag_point_conv_data(self, data):
        bag_point_conv = SlctMasonKindSchBagPointConv.objects.filter(
            mason_kind_sch=data.id
        ).values("brand", "product", "packaging", "bags_point_conv_rto")
        return bag_point_conv

    def get_incentives_data(self, data):
        incentive = SlctMasonKindSchPropsIncentive.objects.filter(
            mason_kind_sch=data.id
        ).values(
            "point_slab_lower", "point_slab_upper", "inkind_incentive", "cash_incentive"
        )
        return incentive

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object

    class Meta:
        model = SlctMasonKindSchProps
        fields = "__all__"


class SlctMasonKindSchBagPointConvSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctMasonKindSchBagPointConv
        fields = "__all__"


class SlctMasonKindSchPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctMasonKindSchPropsIncentive
        fields = "__all__"


class SlctRailBasedSchPropsSerializer(serializers.ModelSerializer):
    incentive_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_incentive_data(self, data):
        incentive = SlctRailBasedSchPropsIncentive.objects.filter(
            rail_based_sch=data.id
        ).values(
            "point_slab_lower",
            "point_slab_upper",
            "incentive_total_sales",
            "in_kind_incentive",
        )
        return incentive

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object

    class Meta:
        model = SlctRailBasedSchProps
        fields = "__all__"


class SlctRailBasedSchPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctRailBasedSchPropsIncentive
        fields = "__all__"


class SlctDealerOutsBasedPropsSerializer(serializers.ModelSerializer):
    dealer_outs_incentive_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctDealerOutsBasedProps
        fields = "__all__"

    def get_dealer_outs_incentive_data(self, data):
        dealer_outs_incentive = SlctDealerOutsBasedPropsIncentive.objects.filter(
            dealer_outs=data.id
        ).values(
            "outstanding_threshold",
            "target_incentive",
            "in_kind_incentive",
        )
        return dealer_outs_incentive

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctDealerOutsBasedPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctDealerOutsBasedPropsIncentive
        fields = "__all__"


class SlctEngCashSchPtPropsSerializer(serializers.ModelSerializer):
    eng_cash_sch_pts_conv = serializers.SerializerMethodField()
    eng_cash_sch_pt_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_eng_cash_sch_pts_conv(self, data):
        eng_cash_sch_pts_conv_obj = SlctEngCashSchPtBagPointConv.objects.filter(
            eng_cash_sch_pt=data.id
        ).values("brand", "product", "packaging", "bags_point_conv_rto")
        return eng_cash_sch_pts_conv_obj

    def get_eng_cash_sch_pt_incentive(self, data):
        eng_cash_sch_pt_incentive_obj = SlctEngCashSchPtPropsIncentive.objects.filter(
            eng_cash_sch_pt=data.id
        ).values(
            "point_slab_lower",
            "point_slab_upper",
            "in_kind_incentive",
            "cash_incentive",
        )
        return eng_cash_sch_pt_incentive_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object

    class Meta:
        model = SlctEngCashSchPtProps
        fields = "__all__"


class SlctEngCashSchPtBagPointConvSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctEngCashSchPtBagPointConv
        fields = "__all__"


class SlctEngCashSchPtPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctEngCashSchPtPropsIncentive
        fields = "__all__"


class SlctDealerLinkedSchPropsSerializer(serializers.ModelSerializer):
    dealer_linked_sch = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_dealer_linked_sch(self, data):
        dealer_linked_sch_obj = SlctDealerLinkedSchPropsIncentive.objects.filter(
            dealer_linked_sch=data.id
        ).values(
            "quantity_slab_lower",
            "quantity_slab_upper",
            "incentive_on_t_sale",
            "inkind_incentive",
            "points",
            "add_incentive_thres",
            "add_incentive",
            "add_inkind_incentive",
            "add_points",
        )
        return dealer_linked_sch_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object

    class Meta:
        model = SlctDealerLinkedSchProps
        fields = "__all__"


class SlctDealerLinkedSchPropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctDealerLinkedSchPropsIncentive
        fields = "__all__"


class SlctCombSlabGrowthPropsIncentiveSerializer(serializers.ModelSerializer):
    """Target incentive serializer class."""

    class Meta:
        model = SlctCombSlabGrowthPropsIncentive
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "comb_slab_props",
        )


class UpdateSlctCombSlabGrowthPropsIncentiveSerializer(serializers.ModelSerializer):
    """Target incentive serializer class."""

    class Meta:
        model = SlctCombSlabGrowthPropsIncentive
        fields = "__all__"


class UpdateSlctCombSlabGrowthPropsSerializer(serializers.ModelSerializer):
    """Slab growth props combination serializer class."""

    slct_comb_slab_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctCombSlabGrowthProps
        fields = "__all__"

    def get_slct_comb_slab_incentive(self, data):
        slct_comb_slab_incentive_object = (
            SlctCombSlabGrowthPropsIncentive.objects.filter(
                comb_slab_props=data.id
            ).values()
        )
        return slct_comb_slab_incentive_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctCombSlabGrowthPropsSerializer(serializers.ModelSerializer):
    """Slab growth props combination serializer class."""

    slct_combslab_growth_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctCombSlabGrowthProps
        fields = "__all__"

    def get_slct_combslab_growth_incentive(self, data):
        combo_slab_growth_obj = SlctCombSlabGrowthPropsIncentive.objects.filter(
            comb_slab_props=data.id
        ).values()
        return combo_slab_growth_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctCombSlabGrowthPropsIncentiveSerializer(serializers.ModelSerializer):
    """Slab growth props combination serializer class."""

    class Meta:
        model = SlctCombSlabGrowthPropsIncentive
        fields = "__all__"

    #     exclude = (
    #         "created_by",
    #         "creation_date",
    #         "last_updated_by",
    #         "last_update_date",
    #         "last_update_login",
    #     )

    # def create(self, validated_data):
    #     print("ppppppppppppppp",self.context.get("request").data)
    #     print("popopo",self.context.get("request").FILES.get())
    #     user = self.context.get("request").user.id
    #     default_fields = {
    #         "created_by": user,
    #         "last_updated_by": user,
    #         "last_update_login": user,
    #         # "related_doc":self.context.get("request").FILES.get("related_doc")
    #     }
    #     incentives = validated_data.pop("incentives", [])

    #     validated_data.update(default_fields)
    #     instance = super().create(validated_data)
    #     print("instance",instance)
    #     incentive_objs = []
    #     for incentive in incentives:
    #         incentive_objs.append(
    #             SlctCombSlabGrowthPropsIncentive(
    #                 **incentive, **default_fields, comb_slab_props=instance
    #             )
    #         )
    #         print(incentive_objs,"incentive_objs")
    #     SlctCombSlabGrowthPropsIncentive.objects.bulk_create(incentive_objs)
    #     print(instance,"instance")
    #     return instance


class SlctVolCutterTargetBasedIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctVolCutterTargetBasedIncentive
        fields = "__all__"


class SlctVolCutterTargetBasedSerializer(serializers.ModelSerializer):
    slct_vol_cutter_target_based = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctVolCutterTargetBased
        fields = "__all__"

    def get_slct_vol_cutter_target_based(self, data):
        slct_vol_cutter_target_based_object = (
            SlctVolCutterTargetBasedIncentive.objects.filter(
                vol_cutter_slab_basd=data.id
            ).values()
        )
        return slct_vol_cutter_target_based_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctVolCutterSlabBasedProposalSerializer(serializers.ModelSerializer):
    slct_vol_cutter_slab_based = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctVolCutterSlabBasedProposal
        fields = "__all__"

    def get_slct_vol_cutter_slab_based(self, data):
        slct_vol_cutter_slab_based_object = (
            SlctVolCutterSlabBasedProposalIncentives.objects.filter(
                vol_cutter_slab_bsd=data.id
            ).values()
        )
        return slct_vol_cutter_slab_based_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctVolCutterSlabBasedProposalIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctVolCutterSlabBasedProposalIncentives
        fields = "__all__"


class SlctBoosterPerDayTargetSchemeSerializer(serializers.ModelSerializer):
    slct_booster_per_day_target_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctBoosterPerDayTargetScheme
        fields = "__all__"

    def get_slct_booster_per_day_target_incentive(self, data):
        slct_booster_per_day_target_incentive_object = (
            SlctBoosterPerDayTargetSchemeIncentive.objects.filter(
                booster_per_day_target=data.id
            ).values()
        )
        return slct_booster_per_day_target_incentive_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctBoosterPerDayTargetSchemeIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBoosterPerDayTargetSchemeIncentive
        fields = "__all__"


class SlctBoosterPerDayGrowthSchemeSerializer(serializers.ModelSerializer):
    slct_booster_per_day_growth_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctBoosterPerDayGrowthScheme
        fields = "__all__"

    def get_slct_booster_per_day_growth_incentive(self, data):
        slct_booster_per_day_growth_incentive_object = (
            SlctBoosterPerDayGrowthSchemeIncentive.objects.filter(
                booster_per_growth_target=data.id
            ).values()
        )
        return slct_booster_per_day_growth_incentive_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctBoosterPerDayGrowthSchemeIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBoosterPerDayGrowthSchemeIncentive
        fields = "__all__"


class SlctBenchmarkChangeRequestSerializer(serializers.ModelSerializer):
    billing_gap_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctBenchmarkChangeRequest
        fields = "__all__"

    def get_billing_gap_data(self, data):
        bench_mark_chq_req_data = SlctBenchmarkChangeRequestBillingGap.objects.filter(
            bench_mark_chq_req=data.id
        ).values()
        return bench_mark_chq_req_data

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctBenchmarkChangeRequestBillingGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBenchmarkChangeRequestBillingGap
        fields = "__all__"


class SlctPriceChangeRequestExistingMarktSerializer(serializers.ModelSerializer):
    brand_vs_competitors = serializers.SerializerMethodField()
    bench_mark_price_working = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctPriceChangeRequestExistingMarkt
        fields = "__all__"

    def get_brand_vs_competitors(self, data):
        brand_vs_competitors_object = (
            SlctPriceChangeRequestBrandVsCompetitors.objects.filter(
                slct_price_change_request_existing_markt=data.id
            ).values()
        )
        return brand_vs_competitors_object

    def get_bench_mark_price_working(self, data):
        bench_mark_price_working_object = SlctBenchmarkPriceWorking.objects.filter(
            slct_benchmark_price=data.id
        ).values()
        return bench_mark_price_working_object

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctPriceChangeRequestBrandVsCompetitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctPriceChangeRequestBrandVsCompetitors
        fields = "__all__"


class SlctBenchmarkPriceWorkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBenchmarkPriceWorking
        fields = "__all__"


class SlctInKindQuantitySlabTourDestinationSerializer(serializers.ModelSerializer):
    """Slct inkind/tour quantity slab tour destinations serializer
    class."""

    class Meta:
        model = SlctInKindQuantitySlabTourDestination
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "in_kind_tour_prop",
        )


class SlctInKindTourProposalSerializer(serializers.ModelSerializer):
    """Slct inkind/tour proposal serializer class."""

    inkind_tour_destinations = SlctInKindQuantitySlabTourDestinationSerializer(
        many=True
    )

    class Meta:
        model = SlctInKindTourProposal
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )

    def create(self, validated_data):
        user_id = self.context.get("request").user.id
        default_fields = {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
        validated_data.update(default_fields)
        inkind_tour_destinations = validated_data.pop("inkind_tour_destinations", [])

        instance = super().create(validated_data)

        quantity_slab_objects = []
        for obj in inkind_tour_destinations:
            quantity_slab_objects.append(
                SlctInKindQuantitySlabTourDestination(
                    **obj, **default_fields, in_kind_tour_prop=instance
                )
            )
        SlctInKindQuantitySlabTourDestination.objects.bulk_create(quantity_slab_objects)

        return instance


class SlctMarketInformationSerializer(serializers.ModelSerializer):
    """Scheme discount proposal serializer class."""

    class Meta:
        model = SlctMarketInformation
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "scheme_discount_proposal",
        )


class SlctSchemeProposalGapSerializer(serializers.ModelSerializer):
    """Scheme discount proposal serializer class."""

    class Meta:
        model = SlctSchemeProposalGap
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "scheme_discount_proposal",
        )


class UpdateSlctSchemeDiscountProposalSerializer(serializers.ModelSerializer):
    Slct_Scheme_Proposal_Gap = serializers.SerializerMethodField()
    Slct_Market_Information = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctSchemeDiscountProposal
        fields = "__all__"

    def get_Slct_Scheme_Proposal_Gap(self, data):
        get_Slct_Scheme_Proposal_Gap_obj = SlctSchemeProposalGap.objects.filter(
            scheme_discount_proposal=data.id
        ).values()
        return get_Slct_Scheme_Proposal_Gap_obj

    def get_Slct_Market_Information(self, data):
        get_Slct_Market_Information_obj = SlctMarketInformation.objects.filter(
            scheme_discount_proposal=data.id
        ).values()
        return get_Slct_Market_Information_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class UpdateSlctSchemeProposalGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctSchemeProposalGap
        fields = "__all__"


class UpdateSlctMarketInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctMarketInformation
        fields = "__all__"


class SlctSchemeDiscountProposalSerializer(serializers.ModelSerializer):
    """Scheme discount proposal serializer class."""

    scheme_proposal_gap = SlctSchemeProposalGapSerializer(many=True)
    market_information = SlctMarketInformationSerializer(many=True)

    class Meta:
        model = SlctSchemeDiscountProposal
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )

    def create(self, validated_data):
        user_id = self.context.get("request").user.id
        scheme_proposal_gap = validated_data.pop("scheme_proposal_gap", [])
        market_information = validated_data.pop("market_information", [])
        default_fields = {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
        instance = super().create(validated_data)

        scheme_prop_list = []
        for obj in scheme_proposal_gap:
            scheme_prop_list.append(
                SlctSchemeProposalGap(
                    **default_fields, **obj, scheme_discount_proposal=instance
                )
            )
        SlctSchemeProposalGap.objects.bulk_create(scheme_prop_list)

        market_info_list = []
        for obj in market_information:
            market_info_list.append(
                SlctMarketInformation(
                    **default_fields, **obj, scheme_discount_proposal=instance
                )
            )
        SlctMarketInformation.objects.bulk_create(market_info_list)

        return instance


class SlctNewMarketPricingRequestSerializer(serializers.ModelSerializer):
    slct_gap_with_other_products = serializers.SerializerMethodField()
    slct_price_packing_inf = serializers.SerializerMethodField()
    slct_markting_information = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctNewMarketPricingRequest
        fields = "__all__"

    def get_slct_gap_with_other_products(self, data):
        slct_gap_with_other_products_object = SlctGapWithOtherProduct.objects.filter(
            new_market_pricing_request=data.id
        ).values()
        return slct_gap_with_other_products_object

    def get_slct_price_packing_inf(self, data):
        slct_price_packing_inf_object = SlctPricePackingInformation.objects.filter(
            pricing_packing_request=data.id
        ).values()
        return slct_price_packing_inf_object

    def get_slct_markting_information(sefl, data):
        slct_markting_information_obj = SlctMarktingInformation.objects.filter(
            marketing_information=data.id
        ).values()
        return slct_markting_information_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctGapWithOtherProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctGapWithOtherProduct
        fields = "__all__"


class SlctPricePackingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctPricePackingInformation
        fields = "__all__"


class SlctMarketingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctMarktingInformation
        fields = "__all__"


class SlctBrandingRequestsSerializer(serializers.ModelSerializer):
    slct_branding_activity = serializers.SerializerMethodField()
    slct_branding_address = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctBrandingRequests
        fields = "__all__"

    def get_slct_branding_activity(self, data):
        slct_branding_activity_obj = SlctBrandingActivity.objects.filter(
            branding_request_activity=data.id
        ).values()
        return slct_branding_activity_obj

    def get_slct_branding_address(self, data):
        slct_branding_address_obj = SlctBrandingAddress.objects.filter(
            branding_request=data.id
        ).values()
        return slct_branding_address_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctBrandingActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBrandingActivity
        fields = "__all__"


class SlctBrandingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctBrandingAddress
        fields = "__all__"


class SlctAnnualDiscTargetBasedSerializer(serializers.ModelSerializer):
    annual_target_based_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctAnnualDiscTargetBased
        fields = "__all__"

    def get_annual_target_based_incentive(self, data):
        annual_target_based_incentive_obj = (
            SlctAnnualDiscTargetBasedIncentives.objects.filter(
                annual_disc_props_slab=data.id
            ).values()
        )
        return annual_target_based_incentive_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctAnnualDiscTargetBasedIncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctAnnualDiscTargetBasedIncentives
        fields = "__all__"


class SlctAnnualDiscSlabBasedSerializer(serializers.ModelSerializer):
    annual_slab_based_incentive = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctAnnualDiscSlabBased
        fields = "__all__"

    def get_annual_slab_based_incentive(self, data):
        annual_slab_based_incentive_obj = (
            SlctAnnualDiscSlabBasedIncentive.objects.filter(
                disc_props_tgt=data.id
            ).values()
        )
        return annual_slab_based_incentive_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctAnnualDiscSlabBasedIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctAnnualDiscSlabBasedIncentive
        fields = "__all__"


class SlctInKindBoosterSchemePropsSerializer(serializers.ModelSerializer):
    inkind_booster_scheme_props_data = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SlctInKindBoosterSchemeProps
        fields = "__all__"

    def get_inkind_booster_scheme_props_data(self, data):
        inkind_booster_scheme_props_data_obj = (
            SlctInKindBoosterSchemePropsIncentive.objects.filter(
                in_kind_booster_scheme=data.id
            ).values()
        )
        return inkind_booster_scheme_props_data_obj

    def get_user_name(self, data):
        try:
            user_object = User.objects.get(id=data.created_by).name
        except:
            user_object = None
        return user_object


class SlctInKindBoosterSchemePropsIncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctInKindBoosterSchemePropsIncentive
        fields = "__all__"


class SlctAnnualSalesPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctAnnualSalesPlan
        fields = "__all__"


class SlctAnnualSalesPlandownloadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = SlctAnnualSalesPlan
        # fields = "__all__"
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "cur_yr_apr",
            "cur_yr_may",
            "cur_yr_jun",
            "cur_yr_jul",
            "cur_yr_aug",
            "cur_yr_sep",
            "cur_yr_oct",
            "cur_yr_nov",
            "cur_yr_dec",
            "nxt_yr_jan",
            "nxt_yr_feb",
            "nxt_yr_mar",
        }


class SlctMonthlySalesPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctMonthlySalesPlan
        fields = "__all__"


class SlctMonthlySalesPlandownloadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = SlctMonthlySalesPlan
        list_serializer_class = BulkUpdateOrCreateListSerializer
        # fields = "__all__"
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        editable_fields = {
            "next_month_bucket1",
            "next_month_bucket2",
            "next_month_bucket3",
            "next_month_total_target",
        }


class UpdateSlctInKindTourProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlctInKindTourProposal
        fields = "__all__"


class UpdateSlctInKindQuantitySlabTourDestinationSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SlctInKindQuantitySlabTourDestination
        fields = "__all__"


class TOebsXxsclVehicleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOebsXxsclVehicleMaster
        fields = "__all__"


class CrmMarketMappingPricingDownloadSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    counter_visit_start_time = serializers.SerializerMethodField()

    def get_counter_visit_start_time(self, obj):
        utc_to_ist_offset = timedelta(hours=5, minutes=30)
        obj.counter_visit_start_time = obj.counter_visit_start_time + utc_to_ist_offset
        return obj.counter_visit_start_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = CrmMarketMappingPricing
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "billing",
            "brand",
            "counter_visit_id",
            "counter_visit_start_time",
            "discount",
            "district",
            "employee_code_so",
            "product",
            "retail_sales",
            "retail_sale_price",
            "stock",
            "taluka",
            "whole_sales",
            "whole_sale_price",
            "so_name",
            "customer_name",
        }
        read_only_fields = ("id",)


class CrmPricingDownloadSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = CrmPricing
        exclude = (
            "taluka",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "district",
            "date",
            "brand",
            "product",
            "wsp_price",
            "rsp_price",
        }
        read_only_fields = ("id",)


class AutomatedModelsRunStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomatedModelsRunStatus
        fields = "__all__"


class TOebsSclArNcrAdvanceCalcTabDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOebsSclArNcrAdvanceCalcTab
        fields = "__all__"


class CrmSalesPlanningBottomUpTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmSalesPlanningBottomUpTarget
        fields = "__all__"


class TargetSalesPlanningMonthlySerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = TargetSalesPlanningMonthly
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "target_bucket1",
            "target_bucket2",
            "target_bucket3",
            "bottom_up_targets_sum",
            "state",
            "district",
            "brand",
            "packaging",
            "product",
            "current_month_bucket1",
            "current_month_bucket2",
            "current_month_bucket3",
            "current_month_total_sales",
            "status",
            "month",
            "year",
            "status_by_nsh",
            "deviation",
            "planned",
        }
        read_only_fields = (
            "id",
            # "current_month_bucket1",
            # "current_month_bucket2",
            # "current_month_bucket3",
            # "current_month_total_sales",
        )


class DistrictWisePricingProposalSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    monthly_estimated_revenue = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = CrmPricing
        exclude = (
            "taluka",
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "wsp_price",
            "rsp_price",
        }
        read_only_fields = (
            "id",
            "district",
            "date",
            "brand",
            "product",
        )

    def get_status(self, data):
        pricing_proposal_approval = PricingProposalApproval.objects.filter(
            crm_pricing_key=data
        ).first()
        if pricing_proposal_approval:
            return pricing_proposal_approval.status
        return None

    def get_comment(self, data):
        pricing_proposal_approval = PricingProposalApproval.objects.filter(
            crm_pricing_key=data
        ).first()
        if pricing_proposal_approval:
            return pricing_proposal_approval.comment
        return None

    def get_monthly_estimated_revenue(self, data):
        month = data.date.month - 1
        year = data.date.year

        premium_product = PremiumProductsMasterTmp.objects.filter(
            revised_name=data.product
        ).first()
        if premium_product:
            grade = premium_product.grade
            bag_type = premium_product.bag_type
            brand_mapping = {
                "Shree": 102,
                "Bangur": 103,
                "Rockstrong": 104,
            }
            org_id = brand_mapping.get(data.brand, None)

            monthly_estimated_sale_object = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                invoice_date__date__range=[
                    date(day=1, month=month, year=year),
                    date(day=monthrange(year, month)[1], month=month, year=year),
                ],
                district=data.district,
                product=grade,
                org_id=org_id,
            ).aggregate(Sum("quantity_invoiced"))

        try:
            sale = monthly_estimated_sale_object["quantity_invoiced__sum"]
        except:
            sale = None

        try:
            revenue = sale * data.wsp_price
        except:
            revenue = None

        return revenue


class PricingProposalApprovalListSerializer(serializers.ListSerializer):
    """Parent list serializer class for PricingProposalApprovalSerializer."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class PricingProposalApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingProposalApproval
        exclude = ("created_by", "last_updated_by", "last_update_login")
        list_serializer_class = PricingProposalApprovalListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "created_by": self.context.get("request_user"),
                "last_updated_by": self.context.get("request_user"),
                "last_update_login": self.context.get("request_user"),
            }
        )

        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance


class NetworkAdditionPlanSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    target_numeric_reach = serializers.SerializerMethodField()

    class Meta:
        model = NetworkAdditionPlan
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"status", "comments_for_revision_by_sh"}
        read_only_fields = (
            "id",
            "city",
            "state",
            "district",
            "taluka",
            "shree_counter",  # total_shree_dealer
            "total_counter",  # total_dealer_market
            "revised_plan",  # dealer addition plan
            "created_ts",
            "modified_ts",
            "type_pk_string",
            "owner_pk_string",
            "revised_plan",
            "reason",
            "applicable_to",
            "raised_by",
            "brand",
            "revised_target_by_tsm",
            "revised_by_tsm",
            "comments_for_revision_tsm",
            "action_performed",
            "action_performed_date",
            "action_performed_by",
            "target_sent_for_revision",
            "is_target_approved",
            "revised_by_rh",
            "revised_target_by_rh",
            "revision_reason_by_rh",
            "comments_for_revision_by_rh",
            "revised_target_by_sh",
            "revised_by_sh",
            "revision_reason_by_sh",
            "approval_level",
            "approved_by",
            "month",
            "year",
        )

    def get_target_numeric_reach(self, data):
        try:
            target_numeric_reach_object = round(
                (data.shree_counter + data.revised_plan) / data.total_counter * 100, 2
            )
        except:
            target_numeric_reach_object = None
        return target_numeric_reach_object


class NetworkAdditionPlanStateSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    target_numeric_reach = serializers.SerializerMethodField()

    class Meta:
        model = NetworkAdditionPlanState
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"status", "month", "year", "comments_by_nsh"}
        read_only_fields = ("id",)

    def get_target_numeric_reach(self, data):
        try:
            target_numeric_reach_object = round(
                (data.shree_counter + data.revised_plan) / data.total_counter * 100, 2
            )
        except:
            target_numeric_reach_object = None
        return target_numeric_reach_object


class TradeOrderPlacementApprovalserializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    dealer_name = serializers.SerializerMethodField()
    retailer_name = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()

    class Meta:
        model = TradeOrderPlacementApproval

        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer

        editable_fields = {
            "comments_by_rh",
            "status_code",
            "rejection_reasons",
            "reason_by_sh",
        }

    def get_dealer_name(self, instance):
        dealer_name = (
            f"{instance.user_name} | {instance.user_uid} | {instance.user_customer_no}"
        )

        return dealer_name

    def get_retailer_name(slef, instance):
        retailer_name = f"{instance.retailer_name} | {instance.retailer_uid} | {instance.retailer_customer_no}"
        return retailer_name

    def get_source(slef, instance):
        source = f"{instance.source_code} | {instance.source_name}"
        return source

    def to_representation(self, instance):
        grouped_instances = TradeOrderPlacementApproval.objects.filter(
            code_crm_order_no=instance.code_crm_order_no
        )
        serialized_data = super().to_representation(instance)

        serialized_data["grouped_instances"] = [
            self.grouped_instance_representation(instance)
            for instance in grouped_instances
        ]

        return serialized_data

    def grouped_instance_representation(self, instance):
        return {
            "id": instance.id,
            "quantity_in_mt": instance.quantity_in_mt,
            "expected_delivery_slot": instance.expected_delivery_slot,
            "expected_delivery_date": instance.expected_delivery_date,
            "sequence": instance.sequence,
            "truck_no": instance.truck_no,
            "driver_contact_no": instance.driver_contact_no,
            "is_dealer_provide_own_transport": instance.is_dealer_provide_own_transport,
        }


# class AnnualDistrictLevelTargetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AnnualDistrictLevelTarget
#         fields = "__all__"


class AnnualDistrictLevelTargetSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = AnnualDistrictLevelTarget
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "state",
            "year",
            "rh_id",
            "region",
            "status",
            "revised_target_by_sh",
            "comments_by_sh",
            "district",
            "brand",
            "grade",
            "packaging_condition",
            "bag_type",
            "total",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
            "january",
            "february",
            "march",
            "is_target_sent_for_review",
        }
        read_only_fields = ("id",)


class AnnualStateLevelTargetSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    class Meta:
        model = AnnualStateLevelTarget
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "zh_id",
            "zone",
            "year",
            "sh_id",
            "state",
            "status",
            "revised_target_by_zh",
            "comments_by_zh",
            "grade",
            "packaging_condition",
            "bag_type",
            "total",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
            "january",
            "february",
            "march",
            "is_target_sent_for_review",
        }
        read_only_fields = ("id",)


class RevisedBucketsApprovalSerializer(BulkOperationsAutoGenerateFieldsModelSerializer):
    delta = serializers.SerializerMethodField()

    class Meta:
        model = RevisedBucketsApproval
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {"status", "reason"}

        read_only_fields = ("id",)

    def get_delta(self, value):
        delta = ((value.revised_target - value.new_revised_target) * 100) / (
            value.revised_target
        )
        return delta


class CrmExceptionApprovalForReplacementOfProductSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = CrmExceptionApprovalForReplacementOfProduct
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "status_by_sh",
            "comment_by_sh",
            "status_by_nsh",
            "comment_by_nsh",
            "approved_by",
        }

        read_only_fields = ("id",)


class CrmVerificationAndApprovalOfDealerSpFormSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    company_details = serializers.SerializerMethodField()
    financial_info = serializers.SerializerMethodField()
    potential = serializers.SerializerMethodField()
    vehical_master = serializers.SerializerMethodField()
    driver_details = serializers.SerializerMethodField()
    potential_sum = serializers.SerializerMethodField()
    fleet_count = serializers.SerializerMethodField()
    capacity_total_sum = serializers.SerializerMethodField()
    no_of_drivers = serializers.SerializerMethodField()

    class Meta:
        model = CrmVerificationAndApprovalOfDealerSpForm
        exclude = (
            "created_by",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "status_by_sh",
            "status_by_nsh",
            "comment_by_sh",
            "comment_by_nsh",
        }
        read_only_fields = ("id",)

    def get_company_details(self, data):
        if CrmCompanyDetails.objects.filter(
            verfication_dealer_sp_form=data.id
        ).values():
            return CrmCompanyDetails.objects.filter(
                verfication_dealer_sp_form=data.id
            ).values()
        return None

    def get_financial_info(self, data):
        try:
            crm_company_details_id = CrmCompanyDetails.objects.get(
                verfication_dealer_sp_form=data.id
            )
            financial_info = CrmFinancialInfo.objects.filter(
                crm_company_details=crm_company_details_id.id
            ).values(
                "id",
                "nominee_name",
                "nominee_father_name",
                "address",
                "crm_company_details",
                "pan",
                "pan_link",
                "created_by",
                "creation_date",
                "last_updated_by",
                "last_update_date",
                "last_update_login",
                "crm_company_details__director_name",
            )
            return financial_info
        except:
            return None

    def get_potential(self, data):
        if CrmPotential.objects.filter(customer_uid=data.id).values():
            return CrmPotential.objects.filter(customer_uid=data.id).values()
        return None

    def get_vehical_master(self, data):
        if CrmVehicleMaster.objects.filter(customer_uid=data.id).values():
            return CrmVehicleMaster.objects.filter(customer_uid=data.id).values()
        return None

    def get_driver_details(self, data):
        if CrmDriverDetails.objects.filter(customer_uid=data.id).values():
            return CrmDriverDetails.objects.filter(customer_uid=data.id).values()
        return None

    def get_potential_sum(self, data):
        if CrmPotential.objects.filter(customer_uid=data.id).aggregate(
            potential_sum=Sum("brand_wise_sale_in_mt")
        ):
            avc = CrmPotential.objects.filter(customer_uid=data.id).aggregate(
                potential_sum=Sum("brand_wise_sale_in_mt")
            )
            # avc = avc["potential_sum"]
            return avc["potential_sum"]
        return None

    def get_fleet_count(self, data):
        if CrmVehicleMaster.objects.filter(customer_uid=data.id).values():
            return (
                CrmVehicleMaster.objects.filter(customer_uid=data.id)
                .values("vehicle_number")
                .distinct()
                .count()
            )
        return None

    def get_capacity_total_sum(self, data):
        if CrmVehicleMaster.objects.filter(customer_uid=data.id).aggregate(
            capacity_total_sum=Sum("vehicle_capacity")
        ):
            total_sum_capacity = CrmVehicleMaster.objects.filter(
                customer_uid=data.id
            ).aggregate(capacity_total_sum=Sum("vehicle_capacity"))
            return total_sum_capacity["capacity_total_sum"]
        return None

    def get_no_of_drivers(self, data):
        if CrmDriverDetails.objects.filter(customer_uid=data.id).values():
            return CrmDriverDetails.objects.filter(customer_uid=data.id).count()
        return None


class ExceptionDisbursementApprovalSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    class Meta:
        model = ExceptionDisbursementApproval
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "status_by_sh",
            "comment_by_sh",
            "status_by_nsh",
            "comment_by_nsh",
            "approved_by",
        }


class GiftRedeemRequestApprovalRewardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftRedeemRequestApprovalRewards
        fields = "__all__"


class GiftRedeemRequestApprovalSerializer(
    BulkOperationsAutoGenerateFieldsModelSerializer
):
    rewards = serializers.SerializerMethodField()

    class Meta:
        model = GiftRedeemRequestApproval
        exclude = (
            "created_by",
            "creation_date",
            "last_updated_by",
            "last_update_date",
            "last_update_login",
            "approved_by",
        )
        list_serializer_class = BulkUpdateOrCreateListSerializer
        editable_fields = {
            "status",
            "status_by_sh",
            "status_by_nsh",
            "comment_by_sh",
            "comment_by_nsh",
            "approved_by",
            "nsh_approved",
            "comment_by_do",
        }

        read_only_fields = ("id",)

    def get_rewards(self, data):
        queryset = GiftRedeemRequestApprovalRewards.objects.filter(
            gift_redeem_request_approval__id=data.id
        ).values("reward_value", "reward_name", "reward_type")
        if queryset:
            return queryset
        return None


class NetworkAdditionPlanStateUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkAdditionPlanState
        fields = "__all__"
