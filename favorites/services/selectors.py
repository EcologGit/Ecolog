from base.content_type_dicts import FavoriteContentTypeDict
from base.shortcuts import get_user_or_404


def get_user_favorites_filter_by_content_type(user_id, object_type):
    user = get_user_or_404(pk=user_id)
    return FavoriteContentTypeDict.get_filtred_queryset(user.favourites, object_type)