from activities.serializers import ResultsReportSerializer
from eco.models import (
    Events,
    NatureObjects,
    Reports,
    Routes,
    SortPoints,
    Rates,
    Results,
)
from django.db.models import F, Sum


def get_reports_with_object_info():
    query = (
        Reports.objects.all()
        .prefetch_related("results", "results__waste_id", "content_object")
        .select_related("user_id", "content_type")
    )
    return query


def get_object_counter_statistic():
    return {
        "place_count": NatureObjects.objects.count(),
        "route_count": Routes.objects.count(),
        "event_count": Events.objects.count(),
        "sort_point_count": SortPoints.objects.count(),
    }


def get_activity_statistic():
    return {
        "report_count": Reports.objects.count(),
        "rates_count": Rates.objects.count(),
        "photo_count": Reports.objects.filter(photo__isnull=False).count(),
    }


def gathered_waste_statistic():
    query = Results.objects.values("waste_id").annotate(
        amount=Sum("amount"),
        type=F("waste_id__name"),
        unit=F("waste_id__unit_of_waste"),
    )
    return query
