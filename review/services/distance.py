from geopy.distance import geodesic


def check_none_dict_and_tuples(*args):
    for it_obj in args:
        if isinstance(it_obj, dict):
            for el in it_obj.values():
                if el is None:
                    return True
        else:
            for el in it_obj:
                if el is None:
                    return True
    return False


def get_distance(coor_objects: tuple, coords: tuple) -> float:
    if check_none_dict_and_tuples(coor_objects, coords):
        return float("inf")
    return geodesic(coor_objects, coords).km