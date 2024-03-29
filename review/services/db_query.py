from eco.models import Events, NatureObjects, Routes, SortPoints, Reports
from django.db.models import Avg, F, Sum, Q
from django.db.models import QuerySet, Model
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound
from review.config import KM_DISTANCE_NEAR_POINT
from django.shortcuts import get_object_or_404
from review.services.distance import get_distance

"""
    ПРИМЕЧАНИЕ:
    Если нет ни одного объекта в бд, то выведет строку с None - значениями
"""


def get_objects_with_avg_rates(model: Model) -> QuerySet:
    """
    Возвращает запрос со средними оценками
    (Пока нигде не используется, по-хорошему переписать нижние методы используя этот)
    """
    query = model.objects.annotate(
        avg_availability=Avg("reports__rates__availability"),
        avg_beauty=Avg("reports__rates__beauty"),
        avg_purity=Avg("reports__rates__purity"),
    )
    return query


def get_nature_objects_with_avg_rates() -> QuerySet:
    query = NatureObjects.objects.only(
        "object_id",
        "locality",
        "name",
        "description",
        "photo",
    ).annotate(
        avg_availability=Avg("reports__rates__availability"),
        avg_beauty=Avg("reports__rates__beauty"),
        avg_purity=Avg("reports__rates__purity"),
    )
    return query


def get_routes_with_avg_rates() -> QuerySet:
    query = Routes.objects.only(
        "route_id",
        "name",
        "locality",
        "length",
        "duration",
        "photo",
    ).annotate(
        avg_availability=Avg("reports__rates__availability"),
        avg_beauty=Avg("reports__rates__beauty"),
        avg_purity=Avg("reports__rates__purity"),
    )
    return query


def get_events_list() -> QuerySet:
    query = (
        Events.objects.select_related("status_id")
        .prefetch_related("routes")
        .prefetch_related("nature_objects")
        .annotate(
            datetime_start=F("time_start"),
            status=F("status_id__name"),
        )
    )

    return query


def get_list_sort_points_with_waste_types() -> QuerySet:
    query = SortPoints.objects.all().prefetch_related("wast_types")

    return query


def get_one_object_with_rates_by_id_or_not_found_error(model: Model, id: int) -> Model:
    query = model.objects.annotate(
        avg_availability=Avg("reports__rates__availability"),
        avg_beauty=Avg("reports__rates__beauty"),
        avg_purity=Avg("reports__rates__purity"),
    )
    return get_object_or_404(query, pk=id)


def get_one_event(id: int):
    event = get_object_or_404(
        Events.objects.prefetch_related("routes", "nature_objects").select_related(
            "status_id"
        ),
        pk=id,
    )
    return event

def get_one_sort_point(id: int):
    event = get_object_or_404(
        SortPoints.objects.prefetch_related("wast_types"),
        pk=id,
    )
    return event


def get_events_actual() -> QuerySet:
    return Events.objects.filter(time_of_close__gt=datetime.now())


def get_reports_statistic(object_with_reports: Model) -> dict:
    reports_info = (
        object_with_reports.reports.values("results__waste_id__unit_of_waste")
        .annotate(
            sum_amount=Sum("results__amount"),
        )
        .annotate(
            type=F("results__waste_id__name"),
            unit=F("results__waste_id__unit_of_waste"),
        )
        .filter(type__isnull=False)
    )
    return reports_info


def get_rates_statistic(object_with_reports) -> dict:
    """
    Возвращает оценки у модели, в которой есть отчёты, иначе
    возвращает словарь с None значениями
    """
    try:
        rates_info = object_with_reports.reports.values("object_id").annotate(
            avg_availability=Avg("rates__availability"),
            avg_beauty=Avg("rates__beauty"),
            avg_purity=Avg("rates__purity"),
        )[0]
    except IndexError:
        rates_info = {"avg_availability": None, "avg_beauty": None, "avg_purity": None}

    return rates_info


def get_nearest_sort_points(object_type: Model, id: int, *args) -> dict:
    sort_points = SortPoints.objects.only("latitude_n", "longitude_e", *args)

    try:
        if object_type is NatureObjects:
            object = NatureObjects.objects.get(pk=id)
            coor_objects = (object.latitude_n, object.longitude_e)
            sort_points = tuple(
                filter(
                    lambda x: get_distance(coor_objects, (x.latitude_n, x.longitude_e))
                    < KM_DISTANCE_NEAR_POINT,
                    sort_points,
                )
            )
        elif object_type is Routes:
            object = Routes.objects.get(pk=id)
            coor_objects_begin = (object.start_n, object.start_e)
            coor_objects_end = (object.end_n, object.end_e)
            sort_points = tuple(
                filter(
                    lambda x: get_distance(
                        coor_objects_begin, (x.latitude_n, x.longitude_e)
                    )
                    < KM_DISTANCE_NEAR_POINT
                    or get_distance(coor_objects_end, (x.latitude_n, x.longitude_e))
                    < KM_DISTANCE_NEAR_POINT,
                    sort_points,
                )
            )
    except Exception:
        raise NotFound

    return sort_points


def get_nearest_nature_objects_for_sort_points(
    obj_id: int, nature_objects_fields_output: tuple[str] = ()
) -> list:
    sort_point = get_object_or_404(SortPoints, pk=obj_id)
    sort_point_coord = (sort_point.latitude_n, sort_point.longitude_e)
    nature_objects = NatureObjects.objects.only(
        "latitude_n", "longitude_e", *nature_objects_fields_output
    )
    nearest_nature_objects = list(
        tuple(
            filter(
                lambda x: get_distance(sort_point_coord, (x.latitude_n, x.longitude_e))
                < KM_DISTANCE_NEAR_POINT,
                nature_objects,
            )
        )
    )
    return nearest_nature_objects


def get_nearest_routes_for_sort_points(
    obj_id: int, routes_fields_output: tuple[str] = ()
) -> list:
    sort_point = get_object_or_404(SortPoints, pk=obj_id)
    sort_point_coord = (sort_point.latitude_n, sort_point.longitude_e)
    routes = Routes.objects.only(
        "start_n", "start_e", "end_e", "end_n", *routes_fields_output
    )
    nearest_nature_objects = filter(
        filter(
            lambda x: get_distance(sort_point_coord, (x.start_n, x.start_e))
            < KM_DISTANCE_NEAR_POINT
            or get_distance(sort_point_coord, (x.end_n, x.end_e))
            < KM_DISTANCE_NEAR_POINT,
            routes,
        )
    )
    return nearest_nature_objects


def get_reports_for_object(object_type: Model, id: int) -> QuerySet:
    model_id = ContentType.objects.get_for_model(object_type).pk
    return (
        Reports.objects.filter(Q(content_type=model_id) & Q(object_id=id))
        .prefetch_related("rates")
        .select_related("user_id")
    )


def get_actual_events_for_object(object_type: Model, id: int) -> QuerySet:
    if object_type is NatureObjects:
        return get_events_actual().filter(nature_objects__pk=id).order_by("name")
    elif object_type is Routes:
        return get_events_actual().filter(routes__pk=id).order_by("name")


"""def test_query():
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
    return query"""
