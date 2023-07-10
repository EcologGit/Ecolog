from eco.models import Favourites
from rest_framework import serializers


class CreateFavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = "__all__"
