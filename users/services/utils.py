from django.forms import ValidationError


def add_refresh_token_to_blacklist(token_class, refresh_token):
    """
    token_class должен иметь метод blacklist
    """
    if not refresh_token:
        raise ValidationError("Refresh token not in cookie")
    refresh = token_class(refresh_token)
    try:
        refresh.blacklist()
    except AttributeError:
        raise ValueError("token_class не имеет метода blacklist")


def change_user_password_or_raise_error(user, old_password, new_password):
    if user.check_password(old_password):
        user.set_password(new_password)
    else:
        raise ValidationError("Старый и новый пароли не совпадают!")


def change_user_password_with_logout_jwt_token(
    refresh_token, refresh_token_class, data, user
):
    new_password = data.get("new_password")
    old_password = data.get("old_password")
    change_user_password_or_raise_error(user, old_password, new_password)
    add_refresh_token_to_blacklist(refresh_token_class, refresh_token)
