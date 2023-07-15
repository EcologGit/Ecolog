from rest_framework.exceptions import ValidationError, NotFound
from datetime import datetime


def get_number_or_validation_400(val, name):
    try:
        val = int(val)
    except ValueError:
        raise ValidationError({name: f"Должен быть числом!"})
    return val


def get_val_from_dict_or_404(dt, key, param_name):
    try:
        val = dt[key]
    except KeyError:
        raise NotFound(f"Ключа {key} для параметра {param_name} не существует!")
    return val


def get_datetime_or_400_from_str(string, param_name, format="%Y-%m-%d %H-%M"):
    try:
        date = datetime.strptime(string, format)
    except:
        raise ValidationError({param_name: f"Введён неверный формат данных: {string}, должен быть: {format}"})
    return date