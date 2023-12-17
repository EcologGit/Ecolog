from django.db.models import Count, Case, When


def get_user_reports(user):
    return user.reports.all()


def get_annotate_by_content_type_and_point_id(user):
    return user.reports.values("content_type").annotate(
        object_count=Count("content_type"), sort_point_count=Count("point_id")
    )


def get_activity_statistics(user):
    query = user.reports.values("user_id__pk").annotate(
        rates_count=Count("rates__pk"),
        photo_count=Count(Case(When(photo="", then=None), default=1)),
        report_count=Count(1),
    )
    return query
