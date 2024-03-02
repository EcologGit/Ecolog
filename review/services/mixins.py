from base.authentication import JWTAuthenticationWithoutRaiseError
from favorites.services.selectors import get_is_favourite_for_queryset_if_user_auth

class ObjectsMixin:
    authentication_classes = (JWTAuthenticationWithoutRaiseError,)
    """
    В этот миксин вынесены общие методы для апишек, которые отдают списки объектов в обзорах,
    должен стоят самым первым в линни наследования!
    """

    def get_queryset(self):
        user = self.request.user
        base_queryset = self.base_queryset
        return get_is_favourite_for_queryset_if_user_auth(
            base_queryset, user, self.object_type
        )
