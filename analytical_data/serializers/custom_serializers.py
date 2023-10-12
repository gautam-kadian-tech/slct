"""
This module contains implementation of bulk create and bulk update in
serializers.
"""
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils import model_meta


class OptionChoiceField(serializers.ChoiceField):
    """all option select choice field"""

    def to_representation(self, value):
        if value == "" and self.allow_blank:
            return value
        return self._choices[value]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""
        for key, val in self._choices.items():
            if data in [key, val]:
                return key
        self.fail("invalid_choice", input=data)
        return None


class BulkUpdateListSerializer(serializers.ListSerializer):
    """List serializer to implement bulk_update."""

    def update(self, instances, validated_data):
        objects_updated = list()
        try:
            for index, attrs in enumerate(validated_data):
                updated_instance = self.child.update(instances[index], attrs)
                objects_updated.append(updated_instance)

            self.child.Meta.model.objects.bulk_update(
                objects_updated,
                fields=[*getattr(self.child.Meta, "editable_fields", None)],
            )
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": f"Data not saved, original exception was: {e}"}
            )
        except IndexError as e:
            raise serializers.ValidationError(
                {
                    "message": f"Some of the IDs provided are not available in the database, original exception was: {e}."
                }
            )

        return objects_updated


class BulkCreateListSerializer(serializers.ListSerializer):
    """Bulk create list serializer class."""

    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return result


class BulkUpdateOrCreateListSerializer(
    BulkCreateListSerializer, BulkUpdateListSerializer
):
    """List serializer to implement bulk_update_or_create."""

    def update(self, instances, validated_data):
        objects_updated = super().update(instances, validated_data[: len(instances)])

        objects_created = [
            self.child.create(attrs) for attrs in validated_data[len(instances) :]
        ]

        try:
            self.child.Meta.model.objects.bulk_create(objects_created)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return objects_updated + objects_created


class BulkOperationsModelSerializer(serializers.ModelSerializer):
    """Model serializer class to implement bulk operations as well as
    single object operations."""

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.create_only_fields = (
            {field.name for field in self.Meta.model._meta.get_fields()}
            - self.Meta.editable_fields
            - {"id"}
        )

    def create(self, validated_data):
        validated_data.update(self.get_auto_generated_fields())
        instance = self.Meta.model(**validated_data)
        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance

    def update(self, instance, validated_data):
        auto_generated_fields = self.get_auto_generated_fields()
        auto_generated_fields.pop("created_by", 1)
        validated_data.update(auto_generated_fields)
        info = model_meta.get_field_info(self.Meta.model)
        for attr, value in validated_data.items():
            if attr in self.create_only_fields or attr in info.relations:
                continue
            setattr(instance, attr, value)

        if isinstance(self._kwargs.get("data"), dict):
            instance.save()

        return instance

    def get_auto_generated_fields(self):
        return {}


class BulkOperationsAutoGenerateFieldsModelSerializer(BulkOperationsModelSerializer):
    def get_auto_generated_fields(self):
        user_id = self.context.get("request").user.id
        return {
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
