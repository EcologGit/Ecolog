from eco.models import Favourites, NatureObjects, Routes, Events, SortPoints
from rest_framework import serializers


class CreateFavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = "__all__"


class FavoritePlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureObjects
        fields = (
            "pk",
            "name",
            "locality",
            "photo",
        )


class FavoriteRoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = (
            "pk",
            "name",
            "locality",
            "photo",
        )


class FavoriteEventsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        return obj.status_id.name

    class Meta:
        model = Events
        fields = (
            "pk",
            "name",
            "time_start",
            "photo",
            "status",
        )


class FavoriteSortPointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SortPoints
        fields = (
            "pk",
            "name",
            "locality",
            "photo",
            "schedule",
        )


class ListFavoritesPlacesSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()

    def get_places(self, obj):
        if not isinstance(obj.content_object, (NatureObjects, None)):
            raise TypeError
        return FavoritePlacesSerializer(obj.content_object).data

    class Meta:
        model = Favourites
        fields = ("pk", "places", "created_at")


class ListFavoritesRoutesSerializer(serializers.ModelSerializer):
    routes = serializers.SerializerMethodField()

    def get_routes(self, obj):
        if not isinstance(obj.content_object, (Routes, None)):
            raise TypeError
        return FavoriteRoutesSerializer(obj.content_object).data

    class Meta:
        model = Favourites
        fields = ("pk", "routes", "created_at")


class ListFavoritesEventsSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        if not isinstance(obj.content_object, (Events, None)):
            raise TypeError
        return FavoriteEventsSerializer(obj.content_object).data

    class Meta:
        model = Favourites
        fields = ("pk", "events", "created_at")


class ListFavoritesSortPointsSerializer(serializers.ModelSerializer):
    sort_points = serializers.SerializerMethodField()

    def get_sort_points(self, obj):
        if not isinstance(obj.content_object, (SortPoints, None)):
            raise TypeError
        return FavoriteSortPointsSerializer(obj.content_object).data

    class Meta:
        model = Favourites
        fields = ("pk", "sort_points", "created_at")
