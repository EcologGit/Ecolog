from rest_framework.serializers import ModelSerializer
from eco.models import NatureObjects, CategoryObjDict, Organizations, Admarea
from eco.models import Routes, StatusesDict, Events, Districts, SortPoints


class CategoryObjDictSerializer(ModelSerializer):

    class Meta:
        model = CategoryObjDict
        fields = '__all__'


class OrganizationsSerializer(ModelSerializer):

    class Meta:
        model = Organizations
        fields = '__all__'


class AdmareaSerializer(ModelSerializer):

    class Meta:
        model = Admarea
        fields = '__all__'


class NatureObjectsSerializer(ModelSerializer):
    category_obj_id = CategoryObjDictSerializer()
    organization_inn = OrganizationsSerializer()
    admareaid = AdmareaSerializer()
    
    class Meta:
        model = NatureObjects
        fields = '__all__'


class RoutesSerializer(ModelSerializer):

    class Meta:
        model = Routes
        fields = '__all__'


class StatusesDictSerializer(ModelSerializer):

    class Meta:
        model = StatusesDict
        fields = '__all__'


class EventsSerializer(ModelSerializer):

    class Meta:
        model = Events
        fields = '__all__'


class DistrictsSerializer(ModelSerializer):

    class Meta:
        model = Districts
        fields = '__all__'


class SortPointsSerializer(ModelSerializer):
    admareaid = AdmareaSerializer(read_only=True)
    districtid = DistrictsSerializer(read_only=True)
    organization_inn = OrganizationsSerializer(read_only=True)

    class Meta:
        model = SortPoints
        fields = '__all__'
