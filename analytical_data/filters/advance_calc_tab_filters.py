"""Filter module for T_OEBS_SCL_AR_NCR_ADVANCE_CALC_TAB."""
# pylint: disable=too-few-public-methods
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models import TOebsSclArNcrAdvanceCalcTab


class AdvanceCalcTabFilter(FilterSet):
    """Advanced calc tab filter class."""

    month = CharInFilter(field_name="creation_date__month", lookup_expr="in")
    year = CharInFilter(field_name="creation_date__year", lookup_expr="in")
    product = CharInFilter(field_name="product", lookup_expr="in")
    state = CharInFilter(field_name="state", lookup_expr="in")

    class Meta:
        model = TOebsSclArNcrAdvanceCalcTab
        # fields = ("state", "product", "month", "key")
        fields = ()
