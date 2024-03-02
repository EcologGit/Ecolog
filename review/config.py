from eco.models import Routes, NatureObjects, Events

OBJECT_TYPE_MAP = {
        'place': NatureObjects,
        'route': Routes,
        'event': Events,
    }

KM_DISTANCE_NEAR_POINT = 10