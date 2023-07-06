from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.contrib.contenttypes.models import ContentType
from base.content_type_dicts import REPORT_CONTENTTYPE
from base.shortcuts import get_first_key_by_value

from user_profiles.services.selectors import get_annotate_by_content_type_and_point_id

User = get_user_model()


def check_usual_user(user):
    """
    Проверяет является ли данный пользователь простым(не суперюзер и не персонал)
    #Переделать, когда появится нормальная система групп и прав
    """
    if (user.is_staff == False) and (user.is_superuser == False):
        return True
    return False


def get_usual_user_or_not_found(user_pk):
    """
    Возвращает обычного юзера или ошибку
    """
    user = get_object_or_404(User, pk=user_pk)
    if check_usual_user(user):
        return user
    raise NotFound("Пользователя с таким id не существует!")


def get_different_object_count_in_reports(user):
    """Возвращает количество каждого вида объектов, на которые был написан репорт пользователем"""
    query = get_annotate_by_content_type_and_point_id(user)
    sort_point_count = 0
    result = {}

    for obj_data in query:
        content_type = obj_data["content_type"]
        model = ContentType.objects.get_for_id(content_type).model_class()
        type_obj = get_first_key_by_value(REPORT_CONTENTTYPE, model)
        sort_point_count += obj_data["sort_point_count"]
        result[type_obj] = obj_data["object_count"]
    result["sort_points"] = sort_point_count
    return result
