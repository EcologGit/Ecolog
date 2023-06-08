from review.config import OBJECT_TYPE_MAP
from django.contrib.contenttypes.models import ContentType

def get_object_types_from_id_in_contenttypes_dict():
    """
    Возвращает словарь id_таблицы_модели: тип_объекта
    """
    dt_type = {}
    for obj_type, model in OBJECT_TYPE_MAP.items():
        dt_type[ContentType.objects.get_for_model(model)] = obj_type
    return dt_type