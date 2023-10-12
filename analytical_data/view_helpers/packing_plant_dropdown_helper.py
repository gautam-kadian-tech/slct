"""Plant name options dropdown api view helper."""
from django.db.models import Count

from analytical_data.models.packing_plant_models import TgtTruckCycleTat


class PlantDropdownViewHelper:
    """Helper class for PlantDropdownView."""

    @classmethod
    def get_demand_dropdown_data(cls, items):
        plant_name_data = cls.__get_field_values("plant_name", items)
        organization_code_data = cls.__get_field_values("organization_code", items)

        options = {
            "plant_name": plant_name_data,
            "organization_code": organization_code_data,
        }
        return options

    @classmethod
    def __get_field_values(cls, field, items):
        return (
            TgtTruckCycleTat.objects.filter(item__in=items)
            .values_list(field, flat=True)
            .annotate(Count(field))
        )
