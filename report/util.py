from typing import Any
from json import loads
from django.contrib.contenttypes.models import ContentType
from review.config import OBJECT_TYPE_MAP
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


def first_el_from_request_data(data: dict) -> dict:
    return {key: val[0] if isinstance(val, list) else val for key, val in data.items()}


def pack_to_new_dict(name_dict: str, data: dict, *args) -> dict:
    new_dict = {key: data.pop(key) if key in data else None for key in args}
    return {name_dict: new_dict}


def prepare_data_report(request):
    data = first_el_from_request_data(request.data)
    rate_data = loads(request.data["rate"])
    results_data = loads(request.data["results"])
    return data | {
        "user_id": request.user.id,
        "rate": rate_data,
        "results": results_data,
    }

def get_content_type_and_content_object(type_obj, id_obj):
        try:
            model_obj = OBJECT_TYPE_MAP[type_obj]
        except KeyError:
            raise NotFound("Такого места уборки не существуют!")
        model_instance = get_object_or_404(model_obj, pk=id_obj)
        return ContentType.objects.get_for_model(model_obj), model_instance


def update_m2m_related_fields(validated_data, model, instance, name):
    prev_values = getattr(instance, name, None)
    if prev_values:
        prev_values.all().delete()
    for val in validated_data.pop(name, []):
        model.objects.create(**val)
     
