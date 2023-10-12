"""Filter module for case study master."""
# pylint: disable=too-few-public-methods
from django_filters import DateFilter
from django_filters.rest_framework import FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.influencer_manager_models import SclCaseStudy


class SclCaseStudyFilter(FilterSet):
    """Scl Case Study filter class."""

    state = CharInFilter(field_name="origin_state", lookup_expr="in")
    case_date = DateFilter(field_name="case_date")
    start_date = DateFilter(field_name="case_date__date", lookup_expr="gte")
    end_date = DateFilter(field_name="case_date__date", lookup_expr="lte")

    class Meta:
        model = SclCaseStudy
        fields = ()
