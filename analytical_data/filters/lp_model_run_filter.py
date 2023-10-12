"""Filter module for lp model run ."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import GdWharfageRunInput, LpModelRun


class LpModelRunFilter(FilterSet):
    """Lp model run filter class."""

    user = CharInFilter(field_name="user", lookup_expr="in")
    run_status = CharInFilter(field_name="run_status", lookup_expr="in")
    contribution = CharInFilter(field_name="contribution", lookup_expr="in")
    tlc = CharInFilter(field_name="tlc", lookup_expr="in")
    dmnd_fulfiled = CharInFilter(field_name="dmnd_fulfiled", lookup_expr="in")
    direct_dispatch = CharInFilter(field_name="direct_dispatch", lookup_expr="in")
    plan_date_month = CharInFilter(field_name="plan_date__month", lookup_expr="in")
    plan_date_year = CharInFilter(field_name="plan_date__year", lookup_expr="in")

    class Meta:
        model = LpModelRun
        fields = ()


class GdWharfageRunInputFilter(FilterSet):
    run_status = CharInFilter(field_name="run_status", lookup_expr="in")
    run_date = CharInFilter(field_name="run_date", lookup_expr="in")
    run_id = CharInFilter(field_name="run_id", lookup_expr="in")
    rake_point_code = CharInFilter(field_name="rake_point_code", lookup_expr="in")
    rake_point = CharInFilter(field_name="rake_point", lookup_expr="in")
    rake_id = CharInFilter(field_name="rake_id", lookup_expr="in")

    class Meta:
        model = GdWharfageRunInput
        fields = ()
