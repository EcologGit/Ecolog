from base.content_type_dicts import FavoriteContentTypeDict
from base.shortcuts import get_user_or_404
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist


def get_user_favorites_filter_by_content_type(user_id, object_type):
    user = get_user_or_404(pk=user_id)
    return FavoriteContentTypeDict.get_filtred_queryset(user.favourites, object_type)


def get_favorite_or_404(user_id, object_type, object_id):
    try:
        return get_user_favorites_filter_by_content_type(user_id, object_type).get(
            object_id=object_id
        )
    except ObjectDoesNotExist:
        raise NotFound
