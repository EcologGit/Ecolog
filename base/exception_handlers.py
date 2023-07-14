from rest_framework.exceptions import ValidationError


def get_number_or_validation_400(val, name):
    try:
        val = int(val)
    except ValueError:
        raise ValidationError(f"{name} должен быть числом!")
    return val
