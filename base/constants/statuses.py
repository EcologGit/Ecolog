from rest_framework.exceptions import ValidationError
from abc import ABC


class Status(ABC):
    @classmethod
    def get_status_by_key_or_400(cls, key):
        statusess = cls.get_statuses()
        new_key = key.lower().strip()
        for num, status in enumerate(statusess):
            if status.lower() == new_key:
                return statusess[num]
        raise ValidationError(
            f"Статуса для {cls.__name__} с таким значением: {key} не существует!"
        )


class EventStatus(Status):
    COMPLETED = "Завершено"
    PLANNED = "Запланировано"
    CANCELLED = "Отменено"
    ACTIVE = "Активно"

    @classmethod
    def get_statuses(cls):
        print(cls.__dict__)
        return (
            cls.COMPLETED,
            cls.PLANNED,
            cls.CANCELLED,
            cls.ACTIVE,
        )
