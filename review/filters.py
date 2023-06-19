from django.db.models import Count, F
from base.filters import OrderingFilterWithFunction


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
