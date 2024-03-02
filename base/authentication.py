from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed,
    InvalidToken,
    TokenError,
)
from django.contrib.auth.models import AnonymousUser


class JWTAuthenticationWithoutRaiseError(JWTAuthentication):
    """
    В случае возникновения какой-либо ошибки, например если
    прислан невалидный токен, то возвращает AnonymousUser
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (AuthenticationFailed, InvalidToken, TokenError):
            return (AnonymousUser(), None)
