from django.urls import path
from .views import *

urlpatterns = [
    path('create_report/', CreateReportApi.as_view()),
    path('sort-points/', GetListSortPointsApi.as_view()),
    path('waste-types/', GetListWasteTypesApi.as_view()),
    path('nature-objects-search-line/', GetListNatureObjectsApi.as_view()),
    path('routes-search-line/', GetListRoutesObjectsApi.as_view()),
    path('events-search-line/', GetListEventsObjectsApi.as_view()),
    path('report/<int:pk>/', RetriveReportApi.as_view()),
    path('edit/<int:pk>/', UpdateReportApi.as_view()),
]
