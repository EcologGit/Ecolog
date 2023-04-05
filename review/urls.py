from django.urls import path
from .views import *

urlpatterns = [
    path('reports/<str:object_type>/<int:object_id>/', GetReportsForObjectView.as_view()),
    path('actual_events/<str:object_type>/<int:object_id>/', GetEventsForModelView.as_view()),
    path('nearest_sort_points/<str:object_type>/<int:object_id>/', GetNearestSortPoint.as_view()),
    path('places/', GetPlacesView.as_view()),
    path('places/<int:id>/', GetInformationOnePlaceView.as_view()),
    path('routes/', GetRoutesView.as_view()),
    path('routes/<int:id>/', GetInformationOneRouteView.as_view()),
    path('events/', GetEventsView.as_view()),
    path('events/<int:id>/', GetOneEventView.as_view()),
    path('sortPoints/', GetGarbagePointsView.as_view()),
    path('sortPoints/<int:id>/', GetOneGarbagePointView.as_view()),
    path('test/', TestView.as_view()),
]