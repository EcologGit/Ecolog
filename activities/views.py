from activities.serializers import ListReportsSerializer
from rest_framework.generics import ListAPIView
from activities.services.db_query import get_reports_with_object_info
# Create your views here.

class GetListReportsView(ListAPIView):
    serializer_class = ListReportsSerializer
    queryset = get_reports_with_object_info()