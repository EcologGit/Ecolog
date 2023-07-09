from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.settings import api_settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.utils import datetime_from_epoch
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

User = get_user_model()


class CustomRefreshToken(RefreshToken):
    def blacklist(self):
        user_id = self.payload["user_id"]
        jti = self.payload[api_settings.JTI_CLAIM]
        exp = self.payload["exp"]
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise NotFound("User with data not found")

        token, _ = OutstandingToken.objects.get_or_create(
            user=user,
            jti=jti,
            defaults={
                "token": str(self),
                "expires_at": datetime_from_epoch(exp),
            },
        )

        return BlacklistedToken.objects.get_or_create(token=token)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    token_class = CustomRefreshToken


class CookieTokenRefreshSerializer(CustomTokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh_token'")


class CreateProfileUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data | {"is_active": True})
        return user

    class Meta:
        model = User
        exclude = ("groups", "user_permissions",)
