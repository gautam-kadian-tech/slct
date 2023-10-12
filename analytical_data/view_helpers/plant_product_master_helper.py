"""Plant product master options dropdown api view helper."""
from datetime import date

from background_task import background
from django.db.models import Count, Q

from analytical_data.models import PlantProductsMaster, VpcHistorical


class PlantProductMasterDropdownHelper:
    """Helper class"""

    @classmethod
    def _get_plant_query(cls, query_string):
        """Pass query string and get the dropdown data associated with
        string."""
        return (
            PlantProductsMaster.objects.values_list(query_string, flat=True)
            .annotate(Count(query_string))
            .order_by(query_string)
        )


@background(schedule=10)
def background_update_vpc_history(validated_data, user_id):
    month = (
        date.today().replace(day=1)
        if date.today().day <= 23
        else date.today().replace(day=1, month=date.today().month + 1)
    )
    auto_generated_fields = {
        "last_updated_by": user_id,
        "last_update_login": user_id,
    }

    if isinstance(validated_data, dict):
        fields = {
            "plant_id": validated_data.get("plant_id"),
            "grade": validated_data.get("grade"),
            "month": month,
        }
        try:
            obj = VpcHistorical.objects.get(**fields)
        except VpcHistorical.DoesNotExist:
            obj = VpcHistorical(**fields, created_by=user_id)

        obj.vpc = validated_data.get("variable_production_cost")
        for attr, value in auto_generated_fields.items():
            setattr(obj, attr, value)
        obj.save()
        return

    query = Q()
    for data in validated_data:
        query |= Q(plant_id=data.get("plant_id"), grade=data.get("grade"))

    validated_data.sort(key=lambda x: (x.get("plant_id"), x.get("grade")))
    instances = VpcHistorical.objects.filter(query, month=month).order_by(
        "plant_id", "grade"
    )

    # Objects updating process:
    objects_updated = []
    for index, instance in enumerate(instances):
        for attr, value in auto_generated_fields.items():
            setattr(instance, attr, value)
        data = validated_data[index]
        instance.vpc = data.get("variable_production_cost")
        instance.month = month
        objects_updated.append(instance)

    VpcHistorical.objects.bulk_update(
        objects_updated,
        fields=("vpc", "month", "last_updated_by", "last_update_login"),
    )

    # Objects creation process:
    objects_created = []
    for data in validated_data[len(instances) :]:
        instance = VpcHistorical(
            created_by=user_id,
            vpc=data.pop("variable_production_cost", 0),
            month=month,
            plant_id=data["plant_id"],
            grade=data["grade"],
            **auto_generated_fields
        )
        objects_created.append(instance)

    VpcHistorical.objects.bulk_create(objects_created)
