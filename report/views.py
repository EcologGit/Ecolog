from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from json import loads
from report.serializers import (
    CreateReportSerializer,
    SearchListSortPointSerialzer,
    WasteTypesSerializer,
    SearchListRoutesSerialzer,
    SearchListNatureObjectsSerialzer,
    SearchListEventsSerialzer,
    DetailReportSerializer,
)
from report.util import first_el_from_request_data
from rest_framework.generics import ListAPIView
from eco.models import WasteTypes, SortPoints, NatureObjects, Routes, Events
from report.services.db_query import get_report_by_pk_or_404


# Create your views here.
class CreateReportApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def prepare_data(self, request):
        data = first_el_from_request_data(request.data)
        rate_data = loads(request.data["rate"])
        results_data = loads(request.data["results"])
        return data | {
            "user_id": request.user.id,
            "rate": rate_data,
            "results": results_data,
        }

    def post(self, request, *args):
        data = self.prepare_data(request)
        serializer = CreateReportSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        report = serializer.create(serializer.validated_data)
        return Response({"id": report.pk})


class RetriveReportApi(APIView):
    def get(self, request, *args, **kwargs):
        report = get_report_by_pk_or_404(kwargs["pk"])
        return Response(DetailReportSerializer(report).data)


class GetListSortPointsApi(ListAPIView):
    serializer_class = SearchListSortPointSerialzer
    queryset = SortPoints.objects.all()


class GetListWasteTypesApi(ListAPIView):
    serializer_class = WasteTypesSerializer
    queryset = WasteTypes.objects.all()


class GetListNatureObjectsApi(ListAPIView):
    serializer_class = SearchListNatureObjectsSerialzer
    queryset = NatureObjects.objects.all()


class GetListRoutesObjectsApi(ListAPIView):
    serializer_class = SearchListRoutesSerialzer
    queryset = Routes.objects.all()


class GetListEventsObjectsApi(ListAPIView):
    serializer_class = SearchListEventsSerialzer
    queryset = Events.objects.all()
