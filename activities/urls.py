from django.urls import path
from .views import *

urlpatterns = [
    path("reports/", GetListReportsView.as_view()),
    path("general-statistic/", GetGeneralStatisticView.as_view()),
]
