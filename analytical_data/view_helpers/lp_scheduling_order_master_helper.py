"""Lp scheduling order master dropdown helper."""
import pandas as pd
from django.conf import settings
from django.db.models import Count, Q

from analytical_data.models import (
    LpSchedulingDiDetails,
    LpSchedulingOrderMaster,
)
from analytical_data.view_helpers.plant_product_master_helper import (
    PlantProductMasterDropdownHelper,
)


class LpSchedulingOrderMasterDropdownHelper(PlantProductMasterDropdownHelper):
    """Helper class."""

    @classmethod
    def __get_order_master_query(cls, queryset, query, query_string):
        return (
            queryset.filter(query)
            .values_list(query_string, flat=True)
            .distinct(query_string)
            .order_by(query_string)
        )

    @classmethod
    def _get_dropdown_data(cls, queryset):
        """Return lp scheduling order master dropdown data."""
        return {
            "customer_type": cls.__get_order_master_query(
                queryset, Q(customer_type__isnull=False), "customer_type"
            ),
            "brand": cls.__get_order_master_query(
                queryset, Q(brand__isnull=False), "brand"
            ),
            "grade": cls.__get_order_master_query(
                queryset, Q(grade__isnull=False), "grade"
            ),
            "plant": super()._get_plant_query("plant_id"),
            "order_executable": cls.__get_order_master_query(
                queryset, Q(order_executable__isnull=False), "order_executable"
            ),
            "ship_city": cls.__get_order_master_query(
                queryset, Q(ship_city__isnull=False), "ship_city"
            ),
            "ship_state": cls.__get_order_master_query(
                queryset, Q(ship_state__isnull=False), "ship_state"
            ),
            "ship_district": cls.__get_order_master_query(
                queryset, Q(ship_district__isnull=False), "ship_district"
            ),
            "packaging": cls.__get_order_master_query(
                queryset, Q(packaging__isnull=False), "packaging"
            ),
            "order_type": cls.__get_order_master_query(
                queryset, Q(order_type__isnull=False), "order_type"
            ),
            "auto_tagged_source": cls.__get_order_master_query(
                queryset, Q(auto_tagged_source__isnull=False), "auto_tagged_source"
            ),
            "auto_tagged_mode": cls.__get_order_master_query(
                queryset, Q(auto_tagged_mode__isnull=False), "auto_tagged_mode"
            ),
            "changed_source": cls.__get_order_master_query(
                queryset, Q(changed_source__isnull=False), "changed_source"
            ),
            "changed_mode": cls.__get_order_master_query(
                queryset, Q(changed_mode__isnull=False), "changed_mode"
            ),
            "order_id": cls.__get_order_master_query(
                queryset, Q(order_id__isnull=False), "order_id"
            ),
        }

    @classmethod
    def _get_districts(cls, queryset, query_params):
        return cls.__get_order_master_query(
            queryset,
            Q(ship_district__isnull=False, ship_state=query_params.get("state", "")),
            "ship_district",
        )

    @classmethod
    def _get_cities(cls, queryset, query_params):
        return cls.__get_order_master_query(
            queryset,
            Q(
                ship_city__isnull=False,
                ship_state=query_params.get("state", ""),
                ship_district=query_params.get("district", ""),
            ),
            "ship_city",
        )


class PpSequenceDropdownHelper(LpSchedulingOrderMasterDropdownHelper):
    """Helper class."""

    @classmethod
    def _get_dropdown_data(cls):
        queryset = LpSchedulingOrderMaster.objects.all()
        data = {
            "prioritized_order": ["False", "True"],
            "di_number": LpSchedulingDiDetails.objects.values_list(
                "di_number", flat=True
            ).annotate(Count("di_number")),
        }
        data.update(super()._get_dropdown_data(queryset))
        return data


class LpSchedulingOrderExecutableDropdownHelper:
    """Helper class."""

    BRAND = {
        "Shree": 102,
        "Bangur": 103,
        "Rockstrong": 104,
    }

    @classmethod
    def _get_dropdown_data(cls, id):
        order = LpSchedulingOrderMaster.objects.filter(id=id).first()
        df = pd.read_csv(settings.LP_SOURCE_MAPPING_CSV_PATH)
        try:
            df = df.loc[
                (df.ORDER_TYPE == order.order_type)
                & (df.CUST_CATEGORY == order.customer_type)
                & (df.DESTINATION_CITY == order.ship_city)
                & (df.DESTINATION_DISTRICT == order.ship_district)
                & (df.DESTINATION_STATE == order.ship_state)
                & (df.BRAND == cls.BRAND.get(order.brand))
                & (df.GRADE == order.grade)
                & (df.PACKAGING == order.packaging)
            ]
        except ValueError as e:
            print(e)
            return {"changed_source": list(), "changed_mode": list()}
        else:
            return {
                "changed_source": df.SOURCE_ID.tolist(),
                "changed_mode": df.MODE.tolist(),
            }
