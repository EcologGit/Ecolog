from eco.models import NatureObjects, Routes, Events, SortPoints
from abc import ABC, abstractmethod
from rest_framework.exceptions import NotFound
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.shortcuts import get_object_or_404


class ContentTypeDict(ABC):
    @property
    @abstractmethod
    def content_type_dict(self):
        pass

    def get_model_or_not_found_error(self, object_type) -> Model:
        try:
            model_object = self.content_type_dict[object_type]
        except KeyError:
            raise NotFound(
                f"В классе {self.__class__.__name__} значения с ключом {object_type} не существует!"
            )

        return model_object

    def get_content_type_object_or_404(self, object_type):
        obj_model = self.get_model_or_not_found_error(object_type)
        return ContentType.objects.get_for_model(obj_model)


class ReportContentTypeDict(ContentTypeDict):
    content_type_dict = {
        "place": NatureObjects,
        "route": Routes,
        "event": Events,
    }


class FavoriteContentTypeDict(ContentTypeDict):
    content_type_dict = {
        "place": NatureObjects,
        "route": Routes,
        "event": Events,
        "sort_points": SortPoints,
    }


REPORT_CONTENTTYPE = {
    "place": NatureObjects,
    "route": Routes,
    "event": Events,
}
