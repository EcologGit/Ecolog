from rest_framework import serializers
from eco.models import Reports, Rates, Results, WasteTypes, SortPoints, NatureObjects, Routes, Events
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from eco.models import Reports, StatusesReport
from django.shortcuts import get_object_or_404
from review.config import OBJECT_TYPE_MAP
from rest_framework.exceptions import NotFound


class CreateRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = [
            "availability",
            "beauty",
            "purity",
        ]


class WasteTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypes
        fields = [
            "name",
            "unit_of_waste",
        ]


class CreateResultsSerializer(serializers.ModelSerializer):
    waste_id = WasteTypesSerializer()

    class Meta:
        model = Results
        fields = ["amount", "waste_id"]


class CreateReportSerializer(serializers.ModelSerializer):
    rate = CreateRatesSerializer()
    results = CreateResultsSerializer(many=True)
    report_status = serializers.CharField(max_length=64)
    point_id = serializers.PrimaryKeyRelatedField(
        required=False, queryset=SortPoints.objects.all()
    )
    type_obj = serializers.CharField()
    id_obj = serializers.IntegerField()

    class Meta:
        model = Reports
        fields = (
            "description",
            "photo",
            "rate",
            "results",
            "user_id",
            "report_status",
            "point_id",
            "type_obj",
            "id_obj",
        )

    @staticmethod
    def get_content_type_and_content_object(type_obj, id_obj):
        try:
            model_obj = OBJECT_TYPE_MAP[type_obj]
        except KeyError:
            raise NotFound("Такого места уборки не существуют!")
        model_instance = get_object_or_404(model_obj, pk=id_obj)
        return ContentType.objects.get_for_model(model_obj), model_instance

    @transaction.atomic
    def create(self, validated_data):
        results_data = validated_data.pop("results")
        rates_data = validated_data.pop("rate")
        report_status = get_object_or_404(
            StatusesReport, name=validated_data.pop("report_status")
        )
        type_obj, model_instance = self.get_content_type_and_content_object(
            validated_data.pop("type_obj"), validated_data.pop("id_obj")
        )

        # Create the report instance
        report_instance = Reports.objects.create(
            **validated_data,
            content_type=type_obj,
            content_object=model_instance,
            status_id_r=report_status
        )

        # Create the related results instances
        for result_data in results_data:
            waste_type_instance = WasteTypes.objects.get(
                name=result_data["waste_id"]["name"]
            )
            result_instance = Results.objects.create(
                report_id=report_instance,
                amount=result_data["amount"],
                waste_id=waste_type_instance,
            )

        # Create the related rates instance
        rates_instance = Rates.objects.create(report_id=report_instance, **rates_data)
        return report_instance


class SearchListSortPointSerialzer(serializers.ModelSerializer):

    class Meta:
        model = SortPoints
        fields = ("pk", "name", )


class SearchListNatureObjectsSerialzer(serializers.ModelSerializer):

    class Meta:
        model = NatureObjects
        fields = ("pk", "name", )


class SearchListRoutesSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Routes
        fields = ("pk", "name", )


class SearchListEventsSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ("pk", "name", )

"""from rest_framework import serializers
from eco.models import Reports, WasteTypes, Rates, Results

"""
