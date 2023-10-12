"""Packaging master options dropdown api view helper."""
from django.db.models import Count

from analytical_data.models import (
    LpSchedulingPackerConstraints,
    PackagingMaster,
)
from analytical_data.view_helpers.plant_product_master_helper import (
    PlantProductMasterDropdownHelper,
)


class PackagingMasterDropdownViewHelper:
    """Helper class for PackagingMasterDropdownView."""

    @classmethod
    def get_packaging_master_dropdown_data(cls):
        brand_data = cls.__get_field_values("brand")
        product_data = cls.__get_field_values("product")
        packaging_data = cls.__get_field_values("packaging")

        options = {
            "brand": brand_data,
            "product": product_data,
            "packaging": packaging_data,
        }
        return options

    @classmethod
    def __get_field_values(cls, field):
        return (
            PackagingMaster.objects.all()
            .values_list(field, flat=True)
            .annotate(Count(field))
            .order_by(field)
        )


class LpSchedulingPackerConstraintsDropdownHelper(PlantProductMasterDropdownHelper):
    """Lp scheduling packer constraints dropdown view helper."""

    @classmethod
    def _get_dropdown_data(cls):
        """Get dropdown data."""
        return {
            "plant_id": super()._get_plant_query("plant_id"),
            "packer": LpSchedulingPackerConstraints.objects.values_list(
                "packer_no", flat=True
            ).annotate(Count("packer_no")),
        }
