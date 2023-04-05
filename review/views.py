from review.services.db_query import get_nature_objects_with_avg_rates, get_events_with_avg_rates
from review.services.db_query import get_routes_with_avg_rates, get_list_sort_points_with_waste_types
from review.services.db_query import get_reports_statistic, get_nearest_sort_points
from review.services.db_query import get_reports_for_object, get_actual_events_for_object
from review.services.db_query import get_one_object_with_rates_by_id_or_not_found_error
from review.services.format import get_model_or_not_found_error, ObjectInfoAndReportStatisitcView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from eco.models import NatureObjects, Routes, Events, SortPoints, Favourites
from review.serializers import ReadonlyEventsWithAvgRatesSerializer, ReadOnlyListSortPointsSerializer
from review.serializers import ReadonlyNatureObjectsWithAvgRatesSerializer, ReadOnlyRoutesWithAvgRatesSerializer
from review.serializers import OneNatureObjectSerializer, EventListInfotSerializer, ReportsForObjectSeriralizer
from review.serializers import NearestSortPointsSerialzier, OneRouteSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, APIException
from review.config import OBJECT_TYPE_MAP
# Create your views here.

class GetPlacesView(ListAPIView):
    serializer_class = ReadonlyNatureObjectsWithAvgRatesSerializer

    def get_queryset(self):
        return get_nature_objects_with_avg_rates()

  
class GetInformationOnePlaceView(ObjectInfoAndReportStatisitcView):
    serializer_class = OneNatureObjectSerializer
    model = NatureObjects


class GetRoutesView(ListAPIView):
    serializer_class = ReadOnlyRoutesWithAvgRatesSerializer

    def get_queryset(self):
        return get_routes_with_avg_rates()


class GetInformationOneRouteView(ObjectInfoAndReportStatisitcView):
    model = Routes
    serializer_class = OneRouteSerializer


class GetEventsView(ListAPIView):
    serializer_class = ReadonlyEventsWithAvgRatesSerializer
    queryset = get_events_with_avg_rates()



class GetOneEventView(RetrieveAPIView):
    queryset = Events.objects.all()
    lookup_field = 'eventid'
    lookup_url_kwarg = 'id'
    serializer_class = ReadonlyEventsWithAvgRatesSerializer


class GetGarbagePointsView(ListAPIView):
    queryset = get_list_sort_points_with_waste_types()
    serializer_class = ReadOnlyListSortPointsSerializer


class GetOneGarbagePointView(RetrieveAPIView):
    queryset = SortPoints.objects.all()
    lookup_field = 'pointid'
    lookup_url_kwarg = 'id'
    #serializer_class = SortPointsSerializer


class TestView(APIView):

    def get(self, request, *args, **kwargs):
        print(Favourites.objects.all()[0].content_object)
        return Response()


class GetReportsForObjectView(ListAPIView):
    serializer_class = ReportsForObjectSeriralizer

    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs['object_type'])
        return get_reports_for_object(model_object, self.kwargs['object_id'])


class GetEventsForModelView(ListAPIView):
    serializer_class = EventListInfotSerializer
    
    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs['object_type'])
        return get_actual_events_for_object(model_object, self.kwargs['object_id'])


class GetNearestSortPoint(ListAPIView):
    serializer_class = NearestSortPointsSerialzier
    
    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs['object_type'])
        queryset = get_nearest_sort_points(model_object, self.kwargs['object_id'], 
                                                      'name', 'pk', 'schedule', 'photo')
        
        return queryset
