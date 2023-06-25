from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('api/browser_token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/browser_refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/mobile_token/', TokenObtainPairView.as_view()),
    path('api/mobile_refresh/', TokenRefreshView.as_view()),

    path('api/create_user/', CreateProfileApi.as_view()),
]