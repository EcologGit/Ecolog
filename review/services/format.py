from django.db.models import QuerySet, Model
from review.config import OBJECT_TYPE_MAP, KM_DISTANCE_NEAR_POINT
from rest_framework.exceptions import NotFound
from eco.models import Routes, NatureObjects

def get_model_or_not_found_error(object_type: str, object_type_map=OBJECT_TYPE_MAP) -> QuerySet:
    try:
        model_object = object_type_map[object_type]
    except KeyError:
        raise NotFound

    return model_object
