from django.urls import path
from .views import *

urlpatterns = [
    path("create_favorite/<str:object_type>/<int:object_id>/", CreateDeleteFavoriteApi.as_view()),
    path("<str:object_type>/<int:user_id>/", GetPlacesFavoritesApi.as_view()),
]
