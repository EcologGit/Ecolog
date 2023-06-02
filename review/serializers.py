from rest_framework import serializers
from eco.models import NatureObjects, Reports
from eco.models import (
    Routes,
    StatusesEvent,
    Events,
    SortPoints,
    WasteTypes,
    Rates,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadonlyNatureObjectsWithAvgRatesSerializer(serializers.ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = NatureObjects
        fields = (
            "locality",
            "object_id",
            "name",
            "description",
            "photo",
            "avg_availability",
            "avg_beauty",
            "avg_purity",
        )


class RoutesWithNameAndPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ["name", "pk"]


class NatureObjectsNameAndIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureObjects
        fields = ["name", "pk"]


class ReadonlyEventsListSerializer(serializers.ModelSerializer):
    datetime_start = serializers.DateTimeField()
    status = serializers.CharField(max_length=64)

    class Meta:
        model = Events
        fields = [
            "name",
            "photo",
            "description",
            "event_id",
            "datetime_start",
            "status",
            "adress",
        ]


class ReadOnlyRoutesWithAvgRatesSerializer(serializers.ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = Routes
        fields = [
            "route_id",
            "name",
            "locality",
            "length",
            "duration",
            "avg_availability",
            "avg_beauty",
            "avg_purity",
            "photo",
        ]


class WastTypePointNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypes
        fields = ["name"]


class ReadOnlyListSortPointsSerializer(serializers.ModelSerializer):
    wast_types = WastTypePointNameSerializer(many=True)

    class Meta:
        model = SortPoints
        fields = [
            "point_id",
            "name",
            "locality",
            "schedule",
            "description",
            "wast_types",
            "photo",
        ]


class EventListInfotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ("photo", "name", "time_start")


class OneNatureObjectSerializer(serializers.ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = NatureObjects
        fields = (
            "locality",
            "object_id",
            "name",
            "description",
            "photo",
            "latitude_n",
            "longitude_e",
            "avg_availability",
            "avg_beauty",
            "avg_purity",
        )


class ReportRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = ("availability", "beauty", "purity")


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("public_name",)


class ReportsForObjectSeriralizer(serializers.ModelSerializer):
    rates = ReportRatesSerializer()
    user_id = UserNameSerializer()

    class Meta:
        model = Reports
        fields = ("description", "created_at", "rates", "user_id")


class NearestSortPointsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SortPoints
        fields = ("pk", "name", "schedule", "photo")


class NearestNatureObjectsToSortPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureObjects
        fields = ("pk", "name", "locality", "photo")


class NearestRoutesToSortPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ("pk", "name", "photo")


class EventsRoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ("pk", "name", "photo", "locality")


class OneRouteSerializer(serializers.ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = Routes
        fields = (
            "pk",
            "name",
            "duration",
            "length",
            "description",
            "start_n",
            "start_e",
            "end_n",
            "end_e",
            "avg_availability",
            "avg_beauty",
            "avg_purity",
            "photo",
        )


class StatusEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusesEvent
        fields = ("name",)


class RoutesNameAndLocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = (
            "name",
            "locality",
        )


class NatureAndLocalityObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureObjects
        fields = (
            "name",
            "locality",
        )


class OneNotFinishedEventSerializer(serializers.ModelSerializer):
    status_id = StatusEventSerializer()

    class Meta:
        model = Events
        fields = (
            "pk",
            "name",
            "time_start",
            "time_of_close",
            "status_id",
            "photo",
            "description",
            "adress",
        )



class OneSortPointSerializer(serializers.ModelSerializer):
    wast_types = WastTypePointNameSerializer(many=True)

    class Meta:
        model = SortPoints
        fields = (
            "photo",
            "pk",
            "name",
            "schedule",
            "description",
            "locality",
            "latitude_n",
            "longitude_e",
            "wast_types",
        )
