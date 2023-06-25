# views.py
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.utils.translation import gettext_lazy as _
from .serializers import CookieTokenRefreshSerializer, CreateProfileUserSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class CreateProfileApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateProfileUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise APIException(serializer.errors)
        return Response(serializer.validated_data)
