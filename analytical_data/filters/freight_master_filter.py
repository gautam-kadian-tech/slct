# """Filter class module for freight master."""
# # pylint: disable=too-few-public-methods
# from django_filters.rest_framework import FilterSet

# from analytical_data.filters.base_filter import CharInFilter
# from analytical_data.models import FreightMaster


# class FreightMasterFilter(FilterSet):
#     """Freight master filter class."""

#     primary_frt = CharInFilter(field_name="primary_frt", lookup_expr="in")
#     secondary_frt = CharInFilter(field_name="secondary_frt", lookup_expr="in")
#     cust_category = CharInFilter(field_name="cust_category", lookup_expr="in")
#     pack_type = CharInFilter(field_name="pack_type", lookup_expr="in")

#     class Meta:
#         model = FreightMaster
#         fields = ("link_id",)
