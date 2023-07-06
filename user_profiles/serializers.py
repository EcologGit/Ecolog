from rest_framework import serializers
from eco.models import NatureObjects, Reports
from eco.models import (
    Routes,
    StatusesEvent,
    Events,
    SortPoints,
    WasteTypes,
    Rates,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileInfoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = User
        fields = (
            "pk",
            "photo",
            "first_name",
            "last_name",
            "username",
            "locality",
            "birth_date",
        )

class UserStatisticSerializer(serializers.ModelSerializer):
    pass