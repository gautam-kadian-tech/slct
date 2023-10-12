"""Links master options dropdown api view helper."""
from django.db.models import Count

from analytical_data.models import LinksMaster


class LinksMasterDropdownViewHelper:
    """Helper class for LinksMasterDropdownView."""

    @classmethod
    def get_links_master_dropdown_data(cls):
        plant = cls.__get_field_values("plant")
        freight_type = cls.__get_field_values("freight_type")
        # destination_district = cls.__get_field_values("destination_district")
        destination_state = cls.__get_field_values("destination_state")
        warehouse = cls.__get_field_values("warehouse")

        options = {
            "plant": plant,
            "cust_category": ["NT", "TR"],
            "freight_type": freight_type,
            "mode": ["ROAD", "RAIL"],
            # "destination_district": destination_district,
            "destination_state": destination_state,
            "primary_secondary_route": ["PRIMARY", "SECONDARY"],
            "warehouse": warehouse,
        }
        return options

    @classmethod
    def __get_field_values(cls, field):
        return (
            LinksMaster.objects.all()
            .values_list(field, flat=True)
            .annotate(Count(field))
            .order_by(field)
        )
