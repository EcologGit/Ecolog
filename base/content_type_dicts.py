from django.shortcuts import get_object_or_404
from eco.models import NatureObjects, Routes, Events, SortPoints
from abc import ABC, abstractmethod
from rest_framework.exceptions import NotFound
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model


class ContentTypeDict(ABC):
    @property
    @abstractmethod
    def content_type_dict(self):
        pass

    @classmethod
    def get_model_or_not_found_error(cls, object_type) -> Model:
        try:
            model_object = cls.content_type_dict[object_type]
        except KeyError:
            raise NotFound(
                f"В классе {cls.__name__} значения с ключом {object_type} не существует!"
            )

        return model_object

    @classmethod
    def get_content_type_object_or_404(cls, object_type):
        obj_model = cls.get_model_or_not_found_error(object_type)
        return ContentType.objects.get_for_model(obj_model)

    @classmethod
    def get_filtred_queryset(cls, queryset, object_type: str):
        """
        Возвращает queryset отфильтрованный по object_type, если он существует, иначе выдаёт 404 ошибку
        """
        content_type = cls.get_content_type_object_or_404(object_type)
        return queryset.filter(content_type=content_type)

    @classmethod
    def get_type_string_by_model_or_404(cls, model):
        for key, val in cls.content_type_dict.items():
            if val == model:
                return key
        raise NotFound()

    @classmethod
    def get_obj_or_404(cls, type_obj, **kwargs):
        model = cls.get_model_or_not_found_error(type_obj)
        return get_object_or_404(model, **kwargs)


class ReportContentTypeDict(ContentTypeDict):
    content_type_dict = {
        "places": NatureObjects,
        "routes": Routes,
        "events": Events,
    }


class FavoriteContentTypeDict(ContentTypeDict):
    content_type_dict = {
        "places": NatureObjects,
        "routes": Routes,
        "events": Events,
        "sort_points": SortPoints,
    }


REPORT_CONTENTTYPE = {
    "place": NatureObjects,
    "route": Routes,
    "event": Events,
}
