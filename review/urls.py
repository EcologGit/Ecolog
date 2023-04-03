from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('reports/<str:object_type>/<int:object_id>/', GetReportsForObjectView.as_view()),
    path('actual_events/<str:object_type>/<int:object_id>/', GetEventsForModelView.as_view()),
    path('places/', GetPlacesView.as_view()),
    path('places/<int:id>/', GetOnePlaceView.as_view()),
    path('routes/', GetRoutesView.as_view()),
    path('routes/<int:id>/', GetOneRouteView.as_view()),
    path('events/', GetEventsView.as_view()),
    path('events/<int:id>/', GetOneEventView.as_view()),
    path('sortPoints/', GetGarbagePointsView.as_view()),
    path('sortPoints/<int:id>/', GetOneGarbagePointView.as_view()),
    path('test/', TestView.as_view()),
]