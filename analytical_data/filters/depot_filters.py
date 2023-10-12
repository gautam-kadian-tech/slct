from django_filters.rest_framework import DateFilter, FilterSet

from analytical_data.filters.base_filter import CharInFilter
from analytical_data.models.sales_planning_models import ExistingDepotLocations


class ExistingDepotLocationsFilter(FilterSet):
    """crm infl assist req filter class."""

    state = CharInFilter(field_name="state", lookup_expr="in")
    district = CharInFilter(field_name="district", lookup_expr="in")
    taluka = CharInFilter(field_name="taluka", lookup_expr="in")
    type = CharInFilter(field_name="type", lookup_expr="in")
    existing_depo_lead = CharInFilter(field_name="existing_depo_lead", lookup_expr="in")
    run_id = CharInFilter(field_name="run_id", lookup_expr="in")

    class Meta:
        model = ExistingDepotLocations
        fields = ()
