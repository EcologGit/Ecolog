from base.content_type_dicts import FavoriteContentTypeDict
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Exists, OuterRef


def get_user_favorites_filter_by_content_type(user, object_type):
    return FavoriteContentTypeDict.get_filtred_queryset(user.favourites, object_type)


def get_favorite_or_404(user, object_type, object_id):
    try:
        return get_user_favorites_filter_by_content_type(user, object_type).get(
            object_id=object_id
        )
    except ObjectDoesNotExist:
        raise NotFound


def get_is_favourite_for_queryset(queryset: QuerySet, user, object_type) -> QuerySet:
    subquery = get_user_favorites_filter_by_content_type(user, object_type).filter(
        object_id=OuterRef("pk")
    )
    return queryset.annotate(is_favourite=Exists(subquery))
