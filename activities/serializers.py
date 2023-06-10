from rest_framework import serializers
from eco.models import WasteTypes, Results, Reports
from django.contrib.auth import get_user_model
from activities.utils import get_object_types_from_id_in_contenttypes_dict

User = get_user_model()


class WasteTypesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypes
        fields = ("name", "unit_of_waste")


class ResultsReportSerializer(serializers.ModelSerializer):
    waste_id = WasteTypesReportSerializer()

    class Meta:
        model = Results
        fields = ("amount", "waste_id")


class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "pk",
        )


class ListReportsSerializer(serializers.ModelSerializer):
    type_obj_dt = get_object_types_from_id_in_contenttypes_dict()
    user_id = UserReportSerializer()
    results = ResultsReportSerializer(many=True)
    obj = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    rates = serializers.SerializerMethodField()

    def get_rates(self, obj):
        return {
            "availability": obj.rates.availability,
            "beauty": obj.rates.beauty,
            "purity": obj.rates.purity,
        }

    def get_photo(self, object):
        return object.photo.url if object.photo else None

    def get_obj(self, obj):
        return {
            "name": obj.content_object.name,
            "locality": obj.content_object.locality
            if hasattr(obj.content_object, "locality")
            else None,
            "type_obj": self.type_obj_dt[obj.content_type]
        }

    class Meta:
        model = Reports
        fields = (
            "description",
            "pk",
            "photo",
            "created_at",
            "user_id",
            "results",
            "obj",
            "rates",
        )
