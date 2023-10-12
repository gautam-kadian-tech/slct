from datetime import date as datetime_date
from datetime import datetime

from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analytical_data.filters import *
from analytical_data.models import *
from analytical_data.serializers import *
from analytical_data.utils import CustomPagination, Responses


class NshContributionScenarioViewSet(ModelViewSet):
    queryset = NshContributionScenario.objects.all().order_by("-id")
    serializer_class = NshContributionScenarioSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NshContributionScenarioFilter
    pagination_class = CustomPagination
    lookup_field = "id"

    @transaction.atomic()
    def post(self, request):
        dataset = request.data
        dataset["created_by"] = request.user.id
        dataset["last_updated_by"] = request.user.id
        dataset["last_update_login"] = request.user.id
        nsh_contribution_serializer = NshContributionScenarioSerializer(data=dataset)
        if not nsh_contribution_serializer.is_valid(raise_exception=True):
            return Responses.error_response(
                "some issue rise", data=nsh_contribution_serializer.errors
            )
        nsh_contribution_serializer.save()
        nsh_contribution_data = nsh_contribution_serializer.data
        return Responses.success_response(
            "Data inserted success", status.HTTP_201_CREATED, nsh_contribution_data
        )


class NshScenarioAnalysisContributionData(ModelViewSet):
    def get_previous_month(self, date):
        if date.month == 1:
            return datetime_date(date.year - 1, 12, 1)
        else:
            return datetime_date(date.year, date.month - 1, date.day)

    def get(self, request, *args, **kwargs):
        state = request.query_params.get("state")
        district = request.query_params.get("district")
        product = request.query_params.get("product")
        brand = request.query_params.get("brand")
        date = datetime.strptime((request.query_params.get("date")), "%Y-%m-%d")
        month = date.month
        year = date.year
        prv_month_date = self.get_previous_month(date)
        prv_month = prv_month_date.month
        prv_year = prv_month_date.year
        price = None
        freight = None
        other_tlc = None
        avg_vpc = None
        sum_of_quantity_invoice = None
        prv_mnth_price = None
        prv_mnth_freight = None
        prv_mnth_other_tlc = None
        prv_mnth_avg_vpc = None
        prv_mnth_sum_of_quantity_invoice = None
        try:
            sum_of_quantity_invoice = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                ~Q(sales_type="DM"),
                Q(active__isnull=True) | Q(active=1),
                org_id=brand,
                state=state,
                district=district,
                product=product,
                invoice_date__month=month,
                invoice_date__year=year,
            ).aggregate(quantity_invoice=Sum("quantity_invoiced"))
        except:
            sum_of_quantity_invoice = None
        try:
            sum_of_unit_selling_and_quantity_invoiced = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=month,
                    invoice_date__year=year,
                ).aggregate(price=Sum(F("unit_selling_price") * F("quantity_invoiced")))
            )

            price = round(
                (
                    (sum_of_unit_selling_and_quantity_invoiced["price"])
                    / sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            price = None
        try:
            other_tlc_sales_tax_and_rebate_sum = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=month,
                    invoice_date__year=year,
                ).aggregate(
                    other_tlc_sales_tax_and_rebate=Sum(
                        (
                            F("sales_tax_pmt")
                            + F("rebate_and_discount")
                            + F("misc_charges")
                            + F("packing_charges")
                        )
                        * F("quantity_invoiced")
                    )
                )
            )

            other_tlc = round(
                (
                    (
                        other_tlc_sales_tax_and_rebate_sum[
                            "other_tlc_sales_tax_and_rebate"
                        ]
                    )
                    / sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            other_tlc = None
        try:
            sum_of_freight_data = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                ~Q(sales_type="DM"),
                Q(active__isnull=True) | Q(active=1),
                org_id=brand,
                state=state,
                district=district,
                product=product,
                invoice_date__month=month,
                invoice_date__year=year,
            ).aggregate(
                freight_data=Sum(
                    (
                        F("ha_commission")
                        + F("shortage")
                        + F("demurrages_and_warfages")
                        + F("rake_charges")
                        + F("unloading_charges")
                        + F("primary_freight")
                        + F("secondary_freight")
                        + F("sp_commission")
                    )
                    * F("quantity_invoiced")
                )
            )

            freight = round(
                (
                    (sum_of_freight_data["freight_data"])
                    / sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            freight = None

        try:
            subsidy_lots = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=month,
                    invoice_date__year=year,
                ).values_list("subsidy_lot", flat=True)
            ).distinct()
            sum_vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=subsidy_lots, month__month=month, month__year=year
            ).aggregate(vpc=Sum("vpc"))
            vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=subsidy_lots, month__month=month, month__year=year
            ).values_list("vpc", flat=True)

            avg_vpc = round(
                (sum_vpc_historical_data["vpc"] / len(vpc_historical_data)), 2
            )
        except:
            avg_vpc = None

        try:
            prv_mnth_sum_of_quantity_invoice = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=prv_month,
                    invoice_date__year=prv_year,
                ).aggregate(quantity_invoice=Sum("quantity_invoiced"))
            )
        except:
            prv_mnth_sum_of_quantity_invoice = None
        try:
            prv_mnth_sum_of_unit_selling_and_quantity_invoiced = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=prv_month,
                    invoice_date__year=prv_year,
                ).aggregate(price=Sum(F("unit_selling_price") * F("quantity_invoiced")))
            )

            prv_mnth_price = round(
                (
                    (prv_mnth_sum_of_unit_selling_and_quantity_invoiced["price"])
                    / prv_mnth_sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            prv_mnth_price = None
        try:
            prv_mnth_other_tlc_sales_tax_and_rebate_sum = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=prv_month,
                    invoice_date__year=prv_year,
                ).aggregate(
                    other_tlc_sales_tax_and_rebate=Sum(
                        (
                            F("sales_tax_pmt")
                            + F("rebate_and_discount")
                            + F("misc_charges")
                            + F("packing_charges")
                        )
                        * F("quantity_invoiced")
                    )
                )
            )

            prv_mnth_other_tlc = round(
                (
                    (
                        prv_mnth_other_tlc_sales_tax_and_rebate_sum[
                            "other_tlc_sales_tax_and_rebate"
                        ]
                    )
                    / prv_mnth_sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            prv_mnth_other_tlc = None
        try:
            prv_mnth_sum_of_freight_data = TOebsSclArNcrAdvanceCalcTab.objects.filter(
                ~Q(sales_type="DM"),
                Q(active__isnull=True) | Q(active=1),
                org_id=brand,
                state=state,
                district=district,
                product=product,
                invoice_date__month=prv_month,
                invoice_date__year=prv_year,
            ).aggregate(
                freight_data=Sum(
                    (
                        F("ha_commission")
                        + F("shortage")
                        + F("demurrages_and_warfages")
                        + F("rake_charges")
                        + F("unloading_charges")
                        + F("primary_freight")
                        + F("secondary_freight")
                        + F("sp_commission")
                    )
                    * F("quantity_invoiced")
                )
            )

            prv_mnth_freight = round(
                (
                    (prv_mnth_sum_of_freight_data["freight_data"])
                    / prv_mnth_sum_of_quantity_invoice["quantity_invoice"]
                ),
                2,
            )
        except:
            prv_mnth_freight = None

        try:
            prv_mnth_subsidy_lots = (
                TOebsSclArNcrAdvanceCalcTab.objects.filter(
                    ~Q(sales_type="DM"),
                    Q(active__isnull=True) | Q(active=1),
                    org_id=brand,
                    state=state,
                    district=district,
                    product=product,
                    invoice_date__month=prv_month,
                    invoice_date__year=prv_year,
                ).values_list("subsidy_lot", flat=True)
            ).distinct()
            prv_mnth_sum_vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=prv_mnth_subsidy_lots,
                month__month=prv_month,
                month__year=prv_year,
            ).aggregate(vpc=Sum("vpc"))
            prv_mnth_vpc_historical_data = VpcHistorical.objects.filter(
                plant_id__in=subsidy_lots, month__month=prv_month, month__year=prv_year
            ).values_list("vpc", flat=True)

            prv_mnth_avg_vpc = round(
                (
                    prv_mnth_sum_vpc_historical_data["vpc"]
                    / len(prv_mnth_vpc_historical_data)
                ),
                2,
            )
        except:
            prv_mnth_avg_vpc = None

        data_dict = {
            "price": price,
            "freight": freight,
            "other_tlc": other_tlc,
            "vpc": avg_vpc,
            "prv_mnth_price": prv_mnth_price,
            "prv_mnth_freight": prv_mnth_freight,
            "prv_mnth_other_tlc": prv_mnth_other_tlc,
            "prv_mnth_vpc": prv_mnth_avg_vpc,
            "quantity_invoiced": sum_of_quantity_invoice["quantity_invoice"],
        }

        return Responses.success_response(
            "Data fetched successfully", status.HTTP_201_CREATED, data_dict
        )


class TOebsSclArNcrAdvanceCalcTabDropdown(GenericAPIView):
    product_list = ["AACB", "BLOCKJOIN", "RUBBLE", "RHPC", "CLINKER"]
    query = Q()
    for letter in product_list:
        query = query | Q(product__startswith=letter)
    queryset = TOebsSclArNcrAdvanceCalcTab.objects.exclude(query)
    filter_backends = (DjangoFilterBackend,)
    filter_class = (DjangoFilterBackend,)
    filterset_fields = ("state", "district", "product")

    def __get_cal_tab2_query(self, query_string):
        return (
            self.filter_queryset(self.get_queryset())
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    def get(self, request, *args, **kwargs):
        data = {
            "state": self.__get_cal_tab2_query("state"),
            "district": self.__get_cal_tab2_query("district"),
            "product": self.__get_cal_tab2_query("product"),
        }
        return Responses.success_response(
            "toebs scl ncr advance calc tab2 dropdown", data=data
        )
