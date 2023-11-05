from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from base.content_type_dicts import FavoriteContentTypeDict
from base.utils import is_exist_model_instance
from eco.models import Favourites
from favorites.serializers import (
    CreateFavouritesSerializer,
    ListFavoritesPlacesSerializer,
    ListFavoritesRoutesSerializer,
    ListFavoritesEventsSerializer,
    ListFavoritesSortPointsSerializer,
)
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound

from favorites.services.selectors import (
    get_user_favorites_filter_by_content_type,
    get_favorite_or_404,
)

# Create your views here.


class CreateDeleteFavoriteApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        content_type = FavoriteContentTypeDict.get_content_type_object_or_404(
            kwargs.get("object_type")
        )

        data = {
            "user_id": request.user.id,
            "content_type": content_type.id,
            "object_id": kwargs.get("object_id"),
        }
        is_exist_model_instance(Favourites, **data)
        serializer = CreateFavouritesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        get_favorite_or_404(
            request.user.id, kwargs.get("object_type"), kwargs.get("object_id")
        ).delete()
        return Response()


class GetPlacesFavoritesApi(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_contenttype = {
        "places": ListFavoritesPlacesSerializer,
        "routes": ListFavoritesRoutesSerializer,
        "events": ListFavoritesEventsSerializer,
        "sort_points": ListFavoritesSortPointsSerializer,
    }

    def get_serializer_class(self):
        try:
            serializer = self.serializer_contenttype[self.kwargs["object_type"]]
        except KeyError:
            raise NotFound("Не существует такого типа объектов!")
        return serializer

    def get_queryset(self):
        return get_user_favorites_filter_by_content_type(
            self.kwargs["user_id"], self.kwargs["object_type"]
        )
