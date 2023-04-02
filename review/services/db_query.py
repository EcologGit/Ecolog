from eco.models import Rates, Events, NatureObjects, Routes, SortPoints, Reports
from django.db.models import Avg, F, Sum, Q, ExpressionWrapper, FloatField
from django.db.models import QuerySet, Model
from datetime import datetime
from geopy.distance import geodesic
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound
from review.config import OBJECT_TYPE_MAP, KM_DISTANCE_NEAR_POINT
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


def get_object_by_id(model: Model, id: int) -> Model:

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


def get_nearest_sort_points(coor_objects: tuple, *args) -> dict:

    def get_distance(x):
        return geodesic(coor_objects, (x.get('latitude_n'), x.get('longitude_e'))).km
    
    query = SortPoints.objects.values('latitude_n', 'longitude_e', *args)
    sort_points = filter(lambda x: get_distance(x) < KM_DISTANCE_NEAR_POINT, query)
    return sort_points


def get_reports_for_object(object_type: Model, id: int) -> QuerySet:
    model_id = ContentType.objects.get_for_model(object_type).pk
    return Reports.objects.filter(Q(content_type=model_id) & Q(object_id=id)).prefetch_related('rates').select_related('user_id')


