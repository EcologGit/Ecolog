from review.services.db_query import (
    get_nature_objects_with_avg_rates,
    get_events_list,
    get_nearest_nature_objects_for_sort_points,
    get_nearest_routes_for_sort_points,
    get_one_event,
    get_one_object_with_rates_by_id_or_not_found_error,
    get_rates_statistic,
    get_reports_statistic,
)
from review.services.db_query import (
    get_routes_with_avg_rates,
    get_list_sort_points_with_waste_types,
)
from review.services.db_query import get_nearest_sort_points
from review.services.db_query import (
    get_reports_for_object,
    get_actual_events_for_object,
)
from review.services.format import (
    get_model_or_not_found_error,
    ObjectInfoAndReportStatisitcView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from eco.models import NatureObjects, Routes, SortPoints
from review.serializers import (
    EventsRoutesSerializer,
    NearestNatureObjectsToSortPointSerializer,
    NearestRoutesToSortPointSerializer,
    OneSortPointSerializer,
    ReadonlyEventsListSerializer,
    ReadOnlyListSortPointsSerializer,
)
from review.serializers import (
    ReadonlyNatureObjectsWithAvgRatesSerializer,
    ReadOnlyRoutesWithAvgRatesSerializer,
)
from review.serializers import (
    OneNatureObjectSerializer,
    EventListInfotSerializer,
    ReportsForObjectSeriralizer,
)
from review.serializers import (
    NearestSortPointsSerialzier,
    OneRouteSerializer,
    OneNotFinishedEventSerializer,
)
from rest_framework import filters
from review.filters import FilterOrderingForNatureObjectsAndRoutes, FilterOrderingForEventsAndSortPoint
# Create your views here.


class GetPlacesView(ListAPIView):
    serializer_class = ReadonlyNatureObjectsWithAvgRatesSerializer
    filter_backends = (FilterOrderingForNatureObjectsAndRoutes, filters.SearchFilter, )
    search_fields = ('name', )

    def get_queryset(self):
        return get_nature_objects_with_avg_rates()


class GetInformationOnePlaceView(ObjectInfoAndReportStatisitcView):
    serializer_class = OneNatureObjectSerializer
    model = NatureObjects


class GetRoutesView(ListAPIView):
    serializer_class = ReadOnlyRoutesWithAvgRatesSerializer
    filter_backends = (FilterOrderingForNatureObjectsAndRoutes, filters.SearchFilter, )
    search_fields = ('name', )

    def get_queryset(self):
        return get_routes_with_avg_rates()


class GetInformationOneRouteView(ObjectInfoAndReportStatisitcView):
    model = Routes
    serializer_class = OneRouteSerializer


class GetEventsView(ListAPIView):
    serializer_class = ReadonlyEventsListSerializer
    queryset = get_events_list()
    filter_backends = (FilterOrderingForEventsAndSortPoint, filters.SearchFilter, )
    search_fields = ('name', )


class GetOneEventView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = kwargs["id"]
        event = get_one_event(event_id)
        data_event = OneNotFinishedEventSerializer(event).data
        if event.status_id.name != "Завершено":
            return Response(data_event)
        else:
            return Response(
                data_event
                | get_rates_statistic(event)
                | {"reports_statistic": get_reports_statistic(event)}
            )


class GetEventsNatureObjects(ListAPIView):
    serializer_class = NearestNatureObjectsToSortPointSerializer

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return NatureObjects.objects.filter(events__pk=event_id)


class GetEventsRoutes(ListAPIView):
    serializer_class = EventsRoutesSerializer

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return Routes.objects.filter(events__pk=event_id)


class GetGarbagePointsView(ListAPIView):
    queryset = get_list_sort_points_with_waste_types()
    serializer_class = ReadOnlyListSortPointsSerializer
    filter_backends = (FilterOrderingForEventsAndSortPoint, filters.SearchFilter, )
    search_fields = ('name', )


class GetOneGarbagePointView(RetrieveAPIView):
    queryset = SortPoints.objects.prefetch_related("wast_types")
    lookup_field = "pk"
    lookup_url_kwarg = "id"
    serializer_class = OneSortPointSerializer


class GetReportsForObjectView(ListAPIView):
    serializer_class = ReportsForObjectSeriralizer

    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs["object_type"])
        return get_reports_for_object(model_object, self.kwargs["object_id"])


class GetEventsForModelView(ListAPIView):
    serializer_class = EventListInfotSerializer

    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs["object_type"])
        return get_actual_events_for_object(model_object, self.kwargs["object_id"])


class GetNearestSortPoint(ListAPIView):
    serializer_class = NearestSortPointsSerialzier

    def get_queryset(self):
        model_object = get_model_or_not_found_error(self.kwargs["object_type"])
        queryset = get_nearest_sort_points(
            model_object, self.kwargs["object_id"], "name", "pk", "schedule", "photo"
        )

        return queryset


class GetNearestNatureObjectsToSortPoint(ListAPIView):
    serializer_class = NearestNatureObjectsToSortPointSerializer

    def get_queryset(self):
        return get_nearest_nature_objects_for_sort_points(
            self.kwargs["sort_point_id"],
            nature_objects_fields_output=("pk", "name", "locality", "photo"),
        )


class GetNearestRoutesToSortPoint(ListAPIView):
    serializer_class = NearestRoutesToSortPointSerializer

    def get_queryset(self):
        return get_nearest_routes_for_sort_points(
            self.kwargs["sort_point_id"], routes_fields_output=("pk", "name", "photo")
        )
