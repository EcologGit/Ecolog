from django.db.models import QuerySet, Model
from review.config import OBJECT_TYPE_MAP, KM_DISTANCE_NEAR_POINT
from rest_framework.exceptions import NotFound
from eco.models import Routes, NatureObjects

def object_type_handler(func, object_type: Model, object_id: int, object_type_map=OBJECT_TYPE_MAP) -> QuerySet:
    try:
        model_object = object_type_map[object_type]
        queryset = func(model_object, object_id)
    except KeyError:
        raise NotFound

    return queryset
