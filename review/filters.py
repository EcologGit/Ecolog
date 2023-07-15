from django.db.models import Count, F, Subquery
from base.constants.statuses import EventStatus
from base.exception_handlers import (
    get_datetime_or_400_from_str,
    get_number_or_validation_400,
    get_val_from_dict_or_404,
)
from base.filters import OrderingFilterWithFunction
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import NotFound
from eco.models import SortPoints

def get_sum_avg_rates_fields(queryset, rates_in_queryset):
    return queryset.annotate(
        sum_rating=sum((F(fields_name) for fields_name in rates_in_queryset))
    )


class FilterOrderingForNatureObjectsAndRoutes(OrderingFilterWithFunction):
    ordering_fields = {
        "report_count": lambda x: x.annotate(report_count=Count("reports")),
        "sum_rating": lambda x: get_sum_avg_rates_fields(
            x, ("avg_availability", "avg_beauty", "avg_purity")
        ),
        "name": lambda x: x,
    }


class FilterOrderingForEventsAndSortPoint(OrderingFilterWithFunction):
    ordering_fields = {
        "report_count": lambda x: x.annotate(report_count=Count("reports")),
        "name": lambda x: x,
    }


class AdmareaFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if admarea_name := request.query_params.get("admarea_name", None):
            queryset = queryset.filter(admarea_id__name=admarea_name)
        return queryset


class ReportsCountFilter(BaseFilterBackend):
    reports_conditions_queryset = {
        "no_matter": lambda x: x,
        "zero": lambda x: x.annotate(count_report=Count("reports")).filter(
            count_report=0
        ),
        "no_more_than_20": lambda x: x.annotate(count_report=Count("reports")).filter(
            count_report__lte=20
        ),
        "20_to_99": lambda x: x.annotate(count_report=Count("reports")).filter(
            count_report__range=(20, 99)
        ),
        "more_than_100": lambda x: x.annotate(count_report=Count("reports")).filter(
            count_report__gt=100
        ),
    }

    def filter_queryset(self, request, queryset, view):
        if report_count := request.query_params.get("report_count", None):
            try:
                queryset = self.reports_conditions_queryset[report_count](queryset)
            except KeyError:
                raise NotFound(
                    f"Ключа {report_count} для параметра report_count не существует!"
                )
        return queryset


class RouteLengthFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if length_great_then := request.query_params.get("length_greater_then", None):
            length_great_then = get_number_or_validation_400(
                length_great_then, "length_greater_then"
            )
            queryset = queryset.filter(length__gt=length_great_then)
        if length_less_than := request.query_params.get("length_less_than", None):
            length_less_than = get_number_or_validation_400(
                length_less_than, "length_less_than"
            )
            queryset = queryset.filter(length__lt=length_less_than)
        return queryset


class EventTimeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if time_start := request.query_params.get("time_start", None):
            time_start = get_datetime_or_400_from_str(time_start, "time_start")
            print(time_start)
            queryset = queryset.filter(time_start__gte=time_start)
        if time_of_close := request.query_params.get("time_of_close", None):
            time_of_close = get_datetime_or_400_from_str(time_of_close, "time_of_close")
            queryset = queryset.filter(time_of_close__lte=time_of_close)
        return queryset


class EventStatusFilter(BaseFilterBackend):
    statusess = {
        "completed": EventStatus.COMPLETED,
        "planned": EventStatus.PLANNED,
        "cancelled": EventStatus.CANCELLED,
        "active": EventStatus.ACTIVE,
    }

    def filter_queryset(self, request, queryset, view):
        if status := request.query_params.get("status", None):
            event_status = EventStatus.get_status_by_key_or_400(status)
            queryset = queryset.filter(status_id__name=event_status)
        return queryset

class WasteTypesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if wast_types := request.query_params.get("wast_types"):
            union_queries = []
            wast_types = wast_types.split(",")
            for wast in wast_types:
                union_queries.append(queryset.filter(wast_types__name=wast).values_list("pk"))
            filtred_pks = union_queries[0].intersection(*union_queries[1:])
            queryset = queryset.filter(pk__in=filtred_pks)
        return queryset