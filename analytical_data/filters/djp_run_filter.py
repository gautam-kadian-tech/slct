"""Filter class module for DJP Run."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import DjpRun


class DjpRunFilter(FilterSet):
    """DJP Run filter class."""

    plan_date = CharInFilter(field_name="plan_date", lookup_expr="in")

    class Meta:
        model = DjpRun
        fields = ()
