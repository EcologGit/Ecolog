from rest_framework import serializers
from base.content_type_dicts import ReportContentTypeDict
from eco.models import (
    Reports,
    Rates,
    Results,
    WasteTypes,
    SortPoints,
    NatureObjects,
    Routes,
    Events,
)
from django.db import transaction
from eco.models import Reports, StatusesReport
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg
from report.util import get_content_type_and_content_object, update_report

User = get_user_model()


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
    class Meta:
        model = Results
        fields = (
            "amount",
            "waste_id",
        )


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

    @transaction.atomic
    def create(self, validated_data):
        results_data = validated_data.pop("results")
        rates_data = validated_data.pop("rate")
        report_status = get_object_or_404(
            StatusesReport, name=validated_data.pop("report_status")
        )
        type_obj, model_instance = get_content_type_and_content_object(
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
            result_instance = Results.objects.create(
                report_id=report_instance,
                amount=result_data["amount"],
                waste_id=result_data["waste_id"],
            )

        # Create the related rates instance
        rates_instance = Rates.objects.create(report_id=report_instance, **rates_data)
        return report_instance


class SearchListSortPointSerialzer(serializers.ModelSerializer):
    class Meta:
        model = SortPoints
        fields = (
            "pk",
            "name",
        )


class SearchListNatureObjectsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = NatureObjects
        fields = (
            "pk",
            "name",
        )


class SearchListRoutesSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = (
            "pk",
            "name",
        )


class SearchListEventsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = (
            "pk",
            "name",
        )


class UserCreatedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "photo",
            "first_name",
            "last_name",
            "pk",
            "username",
        )


class SortPointDetailReportSerializer(serializers.ModelSerializer):
    wast_types = WasteTypesSerializer(many=True)
    photo = serializers.SerializerMethodField()

    def get_photo(self, object):
        return object.photo.url if object.photo else None

    class Meta:
        model = SortPoints
        fields = (
            "pk",
            "name",
            "locality",
            "schedule",
            "description",
            "wast_types",
            "photo",
        )


class DetailReportSerializer(serializers.ModelSerializer):
    rates = CreateRatesSerializer()
    results = CreateResultsSerializer(many=True)
    user_id = UserCreatedReportSerializer()
    point_id = SortPointDetailReportSerializer()
    obj = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_photo(self, object):
        return object.photo.url if object.photo else None

    def get_obj(self, report):
        report_object = report.content_object
        model_object = type(report_object)
        rates_obj = report_object.reports.values("object_id").annotate(
            avg_availability=Avg("rates__availability"),
            avg_beauty=Avg("rates__beauty"),
            avg_purity=Avg("rates__purity"),
        )
        info_obj = {
            "photo": report_object.photo.url,
            "name": report_object.name,
            "pk": report_object.pk,
            "rates": rates_obj[0] if rates_obj else [],
            "type_obj": ReportContentTypeDict.get_type_string_by_model_or_404(
                model_object
            ),
        }
        return info_obj

    class Meta:
        model = Reports
        fields = (
            "description",
            "photo",
            "rates",
            "results",
            "user_id",
            "point_id",
            "obj",
        )


"""from rest_framework import serializers
from eco.models import Reports, WasteTypes, Rates, Results

"""


class UpdateResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = (
            "amount",
            "waste_id",
            "report_id",
        )


class UpdateReportSerializer(serializers.ModelSerializer):
    rate = CreateRatesSerializer()
    results = UpdateResultsSerializer(many=True)
    report_status = serializers.CharField(max_length=64)
    point_id = serializers.PrimaryKeyRelatedField(
        required=False, queryset=SortPoints.objects.all()
    )
    type_obj = serializers.CharField()
    id_obj = serializers.IntegerField()

    def update(self, instance, validated_data):
        update_report(instance, validated_data)
        super().update(instance, validated_data)
        return instance

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
