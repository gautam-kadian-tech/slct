"""Filter module for godown master."""
# pylint: disable=too-few-public-methods
from django_filters import DateFilter
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharFilter, CharInFilter
from analytical_data.models.scheme_models import Schemes


class SchemeDateRangeFilter(FilterSet):
    """Scheme filter class."""

    eff_start_date = DateFilter(field_name="eff_start_date", lookup_expr=("gte"))
    eff_end_date = DateFilter(field_name="eff_end_date", lookup_expr=("lte"))
    state = CharFilter(field_name="locations__state", lookup_expr="exact")
    district = CharFilter(field_name="locations__district", lookup_expr="exact")

    class Meta:
        model = Schemes
        fields = ()
