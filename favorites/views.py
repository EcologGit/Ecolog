from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from base.content_type_dicts import FavoriteContentTypeDict
from base.utils import is_exist_model_instance
from eco.models import Favourites
from favorites.serializers import CreateFavouritesSerializer
from rest_framework.response import Response

# Create your views here.


class CreateFavoriteApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        content_type = FavoriteContentTypeDict().get_content_type_object_or_404(
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
