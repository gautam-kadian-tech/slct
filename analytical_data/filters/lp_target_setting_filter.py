"""Filter module for Lp target setting."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import LpTargetSetting


class LpTargetSettingFilter(FilterSet):
    """Lp target setting filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    freight_type = CharInFilter(field_name="freight_type", lookup_expr="in")
    target = CharInFilter(field_name="target", lookup_expr="in")

    class Meta:
        model = LpTargetSetting
        fields = ()
