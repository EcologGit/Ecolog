from django.urls import path
from .views import *

urlpatterns = [
    path("create_favorite/<str:object_type>/<int:object_id>/", CreateFavoriteApi.as_view()),
]
