from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

def get_user_or_404(**kwargs):
    return get_object_or_404(User, **kwargs)

def get_first_key_by_value(dt, key_val):
    for key, val in dt.items():
        if val == key_val:
            return key
    raise ValueError("Такого значения нет в словаре!")