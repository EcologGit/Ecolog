from eco.models import Rates, Events, NatureObjects, Routes, SortPoints, Reports
from django.db.models import Avg, F, Sum, Q, ExpressionWrapper, FloatField
from django.db.models import QuerySet, Model
from datetime import datetime
from geopy.distance import geodesic
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound
from review.config import OBJECT_TYPE_MAP, KM_DISTANCE_NEAR_POINT
from django.shortcuts import get_object_or_404
'''
    ПРИМЕЧАНИЕ:
    Если нет ни одного объекта в бд, то выведет строку с None - значениями
'''

def get_nature_objects_with_avg_rates() -> QuerySet:

    query = NatureObjects.objects \
                .values(
                    'object_id', 'locality', 'name',
                    'description', 'photo',
                    ) \
                .annotate(
                    avg_availability=Avg('reports__rates__availability'),
                    avg_beauty=Avg('reports__rates__beauty'),
                    avg_purity=Avg('reports__rates__purity'),
                    ) 
    return query


def get_routes_with_avg_rates() -> QuerySet:

    query = Routes.objects \
                .values(
                    'route_id', 'name', 'locality', 'length',
                    'duration', 'photo',
                    ) \
                .annotate(
                        avg_availability=Avg('reports__rates__availability'), 
                        avg_beauty=Avg('reports__rates__availability'),
                        avg_purity=Avg('reports__rates__availability'),
                        ) 
    return query


def get_events_with_avg_rates() -> QuerySet:

    query = Events.objects \
                .select_related('status_id') \
                .prefetch_related('routes') \
                .prefetch_related('nature_objects') \
                .annotate(
                    avg_availability=Avg('reports__rates__availability'),
                    avg_beauty=Avg('reports__rates__beauty'),
                    avg_purity=Avg('reports__rates__purity'),
                    ) \
                .annotate(
                    datetime_start=F('time_start'),
                    status=F('status_id__name'),
                    )

    
    return query


def get_list_sort_points_with_waste_types() -> QuerySet:

    query = SortPoints.objects.all().prefetch_related('wast_types')
    
    return query


def get_one_object_with_rates_by_id(model: Model, id: int) -> Model:

    query = NatureObjects.objects \
                            .annotate(
                                avg_availability=Avg('reports__rates__availability'),
                                avg_beauty=Avg('reports__rates__beauty'),
                                avg_purity=Avg('reports__rates__purity'),
                                ) \
                            .get(pk=id)
    
    return query


def get_events_actual() -> QuerySet:
    return Events.objects.filter(time_of_close__gt = datetime.now())


def get_reports_information(object_with_reports: Model) -> dict:

    reports_info = object_with_reports.reports.all() \
                        .values('results__waste_id__unit_of_waste') \
                        .annotate(
                            sum_amount = Sum('results__amount'),
                            ) \
                        .annotate(
                            type = F('results__waste_id__name'),
                            unit = F('results__waste_id__unit_of_waste')
                        )
    return reports_info


def get_nearest_sort_points(object_type: Model, id: int, *args) -> dict:
    def get_distance(coor_objects, x) -> float:
        return geodesic(coor_objects, (x.get('latitude_n'), x.get('longitude_e'))).km
    
    query = SortPoints.objects.values('latitude_n', 'longitude_e', *args)

    try:
        if object_type is NatureObjects:
            object = NatureObjects.objects.get(pk=id)
            coor_objects = (object.latitude_n, object.longitude_e)
            sort_points = filter(lambda x: get_distance(coor_objects, x) < KM_DISTANCE_NEAR_POINT, query)
        elif object_type is Routes:
            object = Routes.objects.get(pk=id)
            coor_objects_begin = (object.start_n, object.start_e)
            coor_objects_end = (object.end_n, object.end_e)
            sort_points = filter(lambda x: get_distance(coor_objects_begin, x) < KM_DISTANCE_NEAR_POINT 
                                 or get_distance(coor_objects_end, x), query)
    except Exception:
        raise NotFound

    return sort_points


def get_reports_for_object(object_type: Model, id: int) -> QuerySet:
    model_id = ContentType.objects.get_for_model(object_type).pk
    return Reports.objects.filter(Q(content_type=model_id) & Q(object_id=id)).prefetch_related('rates').select_related('user_id')


def get_actual_events_for_object(object_type: Model, id: int) -> QuerySet:
    if object_type is NatureObjects:
        return get_events_actual().filter(nature_objects__pk=id)
    elif object_type is Routes:
        return get_events_actual().filter(route_objects__pk=id)


'''def test_query():
    query = NatureObjects.objects \
                        .values('pk') \
                        .annotate(
                            sum_amount = Sum('reports__results__amount'),
                            ) \
                        .annotate(
                            type = F('reports__results__waste_id__name'),
                            unit = F('reports__results__waste_id__unit_of_waste')
                            ) \
                        .annotate(
                                avg_availability=Avg('reports__rates__availability'),
                                avg_beauty=Avg('reports__rates__beauty'),
                                avg_purity=Avg('reports__rates__purity'),
                                ) \
                        .filter(pk=1)
    return query'''
