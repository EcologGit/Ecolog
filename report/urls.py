from django.urls import path
from .views import *

urlpatterns = [
    path('create_report/', CreateReportApi.as_view()),
    path('sort-points/', SortPointsApi.as_view()),
    path('waste-types/', WasteTypesApi.as_view()),
]
