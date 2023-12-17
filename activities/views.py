from activities.serializers import GeneralStatisticResultSerializer, ListReportsSerializer, ResultsReportSerializer
from rest_framework.generics import ListAPIView
from activities.services.db_query import (
    gathered_waste_statistic,
    get_activity_statistic,
    get_object_counter_statistic,
    get_reports_with_object_info,
)
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class GetListReportsView(ListAPIView):
    serializer_class = ListReportsSerializer
    queryset = get_reports_with_object_info()


class GetGeneralStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        gathered_waste_queryset = gathered_waste_statistic()
        gathered_waste = {
            "gathered_waste": GeneralStatisticResultSerializer(
                gathered_waste_queryset, many=True
            ).data
        }
        return Response(
            get_object_counter_statistic() | get_activity_statistic() | gathered_waste
        )
