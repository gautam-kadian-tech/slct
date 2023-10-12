from accounts.models import TgtRlsRoleData, ZoneMappingNeww


def user_details(user_email, django_queryset):
    try:
        output_fields = ["district", "regions", "state", "zone", "plant_name"]
        output = {field: [] for field in output_fields}

        queryset = TgtRlsRoleData.objects.filter(email=user_email).values(
            *output_fields
        )

        for entry in queryset:
            for field in output_fields:
                if entry[field] is not None:
                    output[field].append(entry[field])

        if django_queryset:
            filter_mapping = {
                "district": "district__in",
                "regions": "region__in",
                "state": "state__in",
                "zone": "zone__in",
                "plant_name": "plant_name__startswith",
                "plant": "plant__startswith",
            }

            for field in output_fields:
                if output[field]:
                    try:
                        filter_key = filter_mapping[field]
                        filter_value = output[field]
                        if field == "plant_name":
                            current_source = getattr(
                                django_queryset[0], "current_source", None
                            )
                            plant_name = getattr(django_queryset[0], "plant_name", None)
                            plant = getattr(django_queryset[0], "plant", None)
                            plant_id = getattr(django_queryset[0], "plant_id", None)

                            if current_source:
                                new_queryset = django_queryset.filter(
                                    current_source__startswith=filter_value[0]
                                )
                            elif plant_name:
                                new_queryset = django_queryset.filter(
                                    plant_name__startswith=filter_value[0]
                                )
                            elif plant:
                                new_queryset = django_queryset.filter(
                                    plant__startswith=filter_value[0]
                                )
                            elif plant_id:
                                new_queryset = django_queryset.filter(
                                    plant_id__startswith=filter_value[0]
                                )
                            else:
                                new_queryset = django_queryset
                        else:
                            try:
                                new_queryset = django_queryset.filter(
                                    **{filter_key: filter_value}
                                )
                            except:
                                new_queryset = django_queryset
                        return new_queryset
                    except KeyError:
                        pass

            return django_queryset

    except Exception:
        pass

    return django_queryset


def GetDistrictsDataByState(user_email, django_queryset):
    states = TgtRlsRoleData.objects.filter(email=user_email).values_list(
        "state", flat=True
    )
    if states:
        districts_list = (
            ZoneMappingNeww.objects.filter(state__in=states)
            .values_list("district", flat=True)
            .distinct()
        )
        new_queryset = django_queryset.filter(district__in=districts_list)
        return new_queryset
    return None
