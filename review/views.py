from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from eco.models import NatureObjects, Routes, Events, SortPoints, Favourites
from .serializers import NatureObjectsSerializer, RoutesSerializer, EventsSerializer, SortPointsSerializer
# Create your views here.

class GetPlacesView(ListAPIView):
    queryset = NatureObjects.objects.all()
    serializer_class = NatureObjectsSerializer


class GetOnePlaceView(RetrieveAPIView):
    queryset = NatureObjects.objects.all()
    lookup_field = 'objectid'
    lookup_url_kwarg = 'id'
    serializer_class = NatureObjectsSerializer


class GetRoutesView(ListAPIView):
    queryset = Routes.objects.all()
    serializer_class = RoutesSerializer


class GetOneRouteView(RetrieveAPIView):
    queryset = Routes.objects.all()
    lookup_field = 'route_id'
    lookup_url_kwarg = 'id'
    serializer_class = RoutesSerializer


class GetEventsView(ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class GetOneEventView(RetrieveAPIView):
    queryset = Events.objects.all()
    lookup_field = 'eventid'
    lookup_url_kwarg = 'id'
    serializer_class = EventsSerializer


class GetGarbagePointsView(ListAPIView):
    queryset = SortPoints.objects.all()
    serializer_class = SortPointsSerializer


class GetOneGarbagePointView(RetrieveAPIView):
    queryset = SortPoints.objects.all()
    lookup_field = 'pointid'
    lookup_url_kwarg = 'id'
    serializer_class = SortPointsSerializer


class TestView(APIView):

    def get(self, request, *args, **kwargs):
        print(Favourites.objects.all()[0].content_object)
        return Response()