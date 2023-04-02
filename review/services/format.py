from django.db.models import QuerySet, Model
from review.config import OBJECT_TYPE_MAP, KM_DISTANCE_NEAR_POINT
from rest_framework.exceptions import NotFound

def object_type_handler(func, object_type: Model, object_id: int) -> QuerySet:
    '''
    Выбирает модель и применяет на неё функцию, которая выбирает объекты с object_id
    '''

    try:
        model_object = OBJECT_TYPE_MAP[object_type]
        queryset = func(model_object, object_id)
    except KeyError:
        raise NotFound

    return queryset