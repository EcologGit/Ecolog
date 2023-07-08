"""Ecolog_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

app_all_urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^chaining/", include("smart_selects.urls")),
    path("review/", include("review.urls")),
    path("users/", include("users.urls")),
    path("report/", include("report.urls")),
    path("activities/", include("activities.urls")),
    path("user_profiles/", include("user_profiles.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path("django_api/", include(app_all_urlpatterns)),
]
