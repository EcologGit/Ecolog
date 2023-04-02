from review.services.db_query import get_nature_objects_with_avg_rates, get_events_with_avg_rates
from review.services.db_query import get_routes_with_avg_rates, get_list_sort_points_with_waste_types, get_object_by_id
from review.services.db_query import get_reports_information, get_events_actual, get_nearest_sort_points
from review.services.db_query import get_reports_for_object
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from eco.models import NatureObjects, Routes, Events, SortPoints, Favourites
from review.serializers import ReadonlyEventsWithAvgRatesSerializer, ReadOnlyListSortPointsSerializer
from review.serializers import ReadonlyNatureObjectsWithAvgRatesSerializer, ReadOnlyRoutesWithAvgRatesSerializer
from review.serializers import OneNatureObjectSerializer, EventListInfotSerializer, ReportsForObjectSeriralizer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, APIException
from review.services.format import object_type_handler
# Create your views here.

class GetPlacesView(ListAPIView):
    serializer_class = ReadonlyNatureObjectsWithAvgRatesSerializer

    def get_queryset(self):
        return get_nature_objects_with_avg_rates()

  
class GetOnePlaceView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            nature_object = get_object_by_id(NatureObjects, kwargs.get('id'))
        except ObjectDoesNotExist:
            raise NotFound
        
        try:
            actual_events = EventListInfotSerializer(get_events_actual() \
                                                    .filter(nature_objects__pk = kwargs.get('id')), many=True)
        
            nature_object_serializer = OneNatureObjectSerializer(instance=nature_object)

            reports_information = get_reports_information(nature_object)
            
            nearest_sort_points = get_nearest_sort_points((nature_object.latitude_n, nature_object.longitude_e), 
                                                      'name', 'point_id', 'schedule')
         
         
        except Exception:
            raise APIException
        
        

        return Response({'object_info': nature_object_serializer.data,
                          'statistic': reports_information,
                          'events': actual_events.data,
                          'nearest_sort_points': nearest_sort_points,
                          })


class GetRoutesView(ListAPIView):
    serializer_class = ReadOnlyRoutesWithAvgRatesSerializer

    def get_queryset(self):
        return get_routes_with_avg_rates()


class GetOneRouteView(RetrieveAPIView):
    queryset = Routes.objects.all()
    lookup_field = 'route_id'
    lookup_url_kwarg = 'id'
    serializer_class = ReadOnlyRoutesWithAvgRatesSerializer


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
        return object_type_handler(get_reports_for_object, self.kwargs['object_type'], 
                                   self.kwargs['object_id'])


class GetNearestSortPoints(ListAPIView):
    pass