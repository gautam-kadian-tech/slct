"""Packaging master options dropdown api view helper."""
from django.db.models import Count, Q

from analytical_data.models import Demand


class DemandDropdownViewHelper:
    """Helper class for DemandDropdownView."""

    @classmethod
    def _get_demand_dropdown_data(cls, query_params):
        destination_state_data = cls.__get_field_values("destination__state")
        destination_district_data = cls.__get_field_values(
            "destination__district", Q(destination__state=query_params.get("state"))
        )
        destination_city_data = cls.__get_field_values(
            "destination__city",
            Q(
                destination__state=query_params.get("state"),
                destination__district=query_params.get("district"),
            ),
        )
        brand_data = cls.__get_field_values("brand")
        grade_data = cls.__get_field_values("grade")
        cust_category_data = cls.__get_field_values("cust_category")
        pack_type_data = cls.__get_field_values("pack_type")
        month_data = cls.__get_field_values("month__month")

        options = {
            "brand": brand_data,
            "grade": grade_data,
            "cust_category": cust_category_data,
            "pack_type": pack_type_data,
            "month": month_data,
            "destination_state_data": destination_state_data,
            "destination_district": destination_district_data,
            "destination_city": destination_city_data,
        }
        return options

    @classmethod
    def __get_field_values(cls, field, filter_query=Q()):
        return (
            Demand.objects.filter(filter_query)
            .values_list(field, flat=True)
            .annotate(Count(field))
        )
