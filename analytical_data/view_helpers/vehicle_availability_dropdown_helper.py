"""Vehicle availability options dropdown api view helper."""
from django.db.models import Count, Q

from analytical_data.models import (
    LpSchedulingVehicleConstraints,
    VehicleAvailability,
)
from analytical_data.view_helpers.plant_product_master_helper import (
    PlantProductMasterDropdownHelper,
)


class VehicleAvailabilityDropdownHelper(PlantProductMasterDropdownHelper):
    """Helper class"""

    @classmethod
    def __get_vehicle_type(cls):
        """Returns total distinct vehicle types present in db."""
        return (
            VehicleAvailability.objects.exclude(vehicle_type=None)
            .values_list("vehicle_type", flat=True)
            .annotate(Count("vehicle_type"))
        )

    @classmethod
    def __get_vehicle_availability_query(self, query_string, query=Q()):
        return (
            VehicleAvailability.objects.filter(query)
            .values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )

    @classmethod
    def get_dropdown_data(cls, query_params):
        """Returns dropdown data for vehicle availability list."""
        return {
            "state": cls.__get_vehicle_availability_query("state"),
            "district": cls.__get_vehicle_availability_query(
                "district", Q(state=query_params.get("state"))
            ),
            "city": cls.__get_vehicle_availability_query(
                "city",
                Q(
                    state=query_params.get("state"),
                    district=query_params.get("district"),
                ),
            ),
            "plant_id": super()._get_plant_query("plant_id"),
            "vehicle_type": cls.__get_vehicle_type(),
        }


class LpSchedulingVehicleConstraintsHelper(PlantProductMasterDropdownHelper):
    """Lp scheduling vehicle constraint dropdown view helper."""

    @classmethod
    def _get_dropdown_data(cls):
        """Returns Lp scheduling packer constraints dropdown data."""
        return {
            "plant_id": cls._get_plant_query("plant_id"),
            "vehicle_type": LpSchedulingVehicleConstraints.objects.filter(
                vehicle_type__isnull=False
            )
            .values_list("vehicle_type", flat=True)
            .annotate(Count("vehicle_type")),
        }
