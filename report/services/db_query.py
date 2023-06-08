from eco.models import Reports
from django.shortcuts import get_object_or_404


def get_report_by_pk_or_404(pk):
    report = get_object_or_404(
        Reports.objects.prefetch_related("results", "results__waste_id").select_related(
            "rates"
        ),
        pk=pk,
    )
    return report