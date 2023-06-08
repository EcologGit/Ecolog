from eco.models import Reports

def get_reports_with_object_info():
    query = (
        Reports.objects.all()
        .prefetch_related("results", "results__waste_id")
        .select_related("user_id", "content_type")
    )
    return query
