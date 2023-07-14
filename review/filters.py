from django.db.models import Count, F
from base.exception_handlers import get_number_or_validation_400
from base.filters import OrderingFilterWithFunction
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import NotFound


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
        if length_great_then := request.query_params.get("length_great_then", None):
            length_great_then = get_number_or_validation_400(length_great_then, "length_great_then")
            queryset = queryset.filter(length__gt=length_great_then)
        if length_less_than := request.query_params.get("length_less_than", None):
            length_less_than = get_number_or_validation_400(length_less_than, "length_less_than")
            queryset = queryset.filter(length__lt=length_less_than)
        return queryset