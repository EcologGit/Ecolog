from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from eco.models import NatureObjects, Reports
from eco.models import Routes, StatusesDict, Events, Districts, SortPoints, WasteTypes, Rates
from django.contrib.auth import get_user_model

User = get_user_model()

class ReadonlyNatureObjectsWithAvgRatesSerializer(ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()
    
    class Meta:
        model = NatureObjects
        fields = ('locality', 'object_id', 'name', 'description', 'photo', 'avg_availability', 'avg_beauty', 'avg_purity',)


class RoutesWithNameAndPkSerializer(ModelSerializer):

    class Meta:
        model = Routes
        fields = ['name', 'pk']


class NatureObjectsNameAndIdSerializer(ModelSerializer):

    class Meta:
        model = NatureObjects
        fields = ['name', 'pk']


class ReadonlyEventsWithAvgRatesSerializer(ModelSerializer):
    routes = RoutesWithNameAndPkSerializer(many=True)
    nature_objects = NatureObjectsNameAndIdSerializer(many=True)
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()
    datetime_start = serializers.DateTimeField()
    status = serializers.CharField(max_length=64)

    class Meta:
        model = Events
        fields = ['name', 'photo', 'description', 'event_id',
                  'nature_objects', 'routes', 'avg_availability', 
                  'avg_beauty', 'avg_purity', 'datetime_start',
                  'status'
                  ]


class ReadOnlyRoutesWithAvgRatesSerializer(ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = Routes
        fields = [
            'route_id', 'name', 'locality', 'length',
            'duration', 'avg_availability', 'avg_beauty',
            'avg_purity', 'photo',
            ]


class WastTypePointNameSerializer(ModelSerializer):

    class Meta:
        model = WasteTypes
        fields = ['name']


class ReadOnlyListSortPointsSerializer(ModelSerializer):

    wast_types = WastTypePointNameSerializer(many=True)
    
    class Meta:
        model = SortPoints
        fields = [
            'point_id', 'name', 'locality', 'schedule',
            'description', 'wast_types',
        ]


class EventListInfotSerializer(ModelSerializer):

    class Meta:
        model = Events
        fields = ('photo', 'name', 'time_start')


class OneNatureObjectSerializer(ModelSerializer):
    avg_availability = serializers.FloatField()
    avg_beauty = serializers.FloatField()
    avg_purity = serializers.FloatField()

    class Meta:
        model = NatureObjects
        fields = ('locality', 'object_id', 'name', 'description',
                  'photo', 'latitude_n', 'longitude_e', 'avg_availability', 
                  'avg_beauty', 'avg_purity',
                  )


class ReportRatesSerializer(ModelSerializer):
    
    class Meta:
        model = Rates
        fields = ('availability', 'beauty', 'purity')


class UserNameSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('public_name',)


class ReportsForObjectSeriralizer(ModelSerializer):
    rates = ReportRatesSerializer()
    user_id = UserNameSerializer()

    class Meta:
        model = Reports
        fields = ('description', 'created_at', 'rates', 'user_id')