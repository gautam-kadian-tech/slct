"""State Head Module Filters"""
from django_filters.rest_framework import DateFilter, FilterSet
from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.state_head_models import SlctPartyWiseSchemeProps


class SlctPartyWiseSchemePropsFilter(FilterSet):
    """slct party wise scheme props filter class."""

    # status = CharInFilter(field_name="status", lookup_expr="in")
    # type_of_change = CharInFilter(field_name="type_of_change", lookup_expr="in")
    # request_date = DateFilter(field_name="request_date")

    class Meta:
        model = SlctPartyWiseSchemeProps
        fields = ()
