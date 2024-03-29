# views.py
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenBlacklistView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from Ecolog_django.settings import SECURE_COOKIE
from users.services.utils import add_refresh_token_to_blacklist, change_user_password_with_logout_jwt_token
from .serializers import CookieTokenRefreshSerializer, CreateProfileUserSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.data["id"] = RefreshToken(
                response.data.get("refresh")
            ).payload.get("user_id")
        else:
            response.data["id"] = None
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
                secure=SECURE_COOKIE.lower() == "true" if SECURE_COOKIE else False,
                samesite="None"
                if (SECURE_COOKIE and SECURE_COOKIE.lower() == "true")
                else None,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.data["id"] = RefreshToken(
                response.data.get("refresh")
            ).payload.get("user_id")
        else:
            response.data["id"] = None
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
                secure=SECURE_COOKIE.lower() == "true" if SECURE_COOKIE else False,
                samesite="None"
                if (SECURE_COOKIE and SECURE_COOKIE.lower() == "true")
                else None,
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
        return Response({"is_success": True})


class LogoutWithCookieApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    token_class = RefreshToken

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        add_refresh_token_to_blacklist(self.token_class, refresh_token)
        return Response({})


class ChangeUserPasswordView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        refresh_token = request.COOKIES.get("refresh_token")
        change_user_password_with_logout_jwt_token(
            refresh_token, RefreshToken, data, user
        )
        return Response(status=204)
