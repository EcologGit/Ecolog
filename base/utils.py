from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist

from base.exception import ModelInstanceExist
def is_exist_model_instance(model, exception=True, **kwargs):
    """
    Проверяет существует ли запись в бд с заданными параметрами, если существует выдаёт этот экземпляр
    """
    try:
        model_instance = model.objects.get(**kwargs)
    except (NotFound, ObjectDoesNotExist):
        return False
    if exception:
        raise ModelInstanceExist
    return model_instance