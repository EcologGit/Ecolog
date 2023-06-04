from typing import Any
def first_el_from_request_data(data: dict) -> dict:
    return {key: val[0] if isinstance(val, list) else val for key, val in data.items()}

def pack_to_new_dict(name_dict: str, data: dict, *args) -> dict:
    new_dict = {key: data.pop(key) if key in data else None for key in args}
    return {name_dict: new_dict}