from django.urls import path
from user_profiles.views import *

urlpatterns = [
    path("profile_info/<int:pk>/", GetInfoProfileApi.as_view()),
    path("reports/<int:user_pk>/", GetUserReportsApi.as_view()),
    path("statistics/<int:user_pk>/", GetUserStatistic.as_view()),
    path("update_profile_info/<int:pk>/", UpdateProfileInfo.as_view()),
]
