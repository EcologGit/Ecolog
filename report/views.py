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
    UpdateReportSerializer,
)
from report.util import prepare_data_report
from rest_framework.generics import ListAPIView, UpdateAPIView
from eco.models import Reports, WasteTypes, SortPoints, NatureObjects, Routes, Events
from report.services.db_query import get_report_by_pk_or_404


# Create your views here.
class CreateReportApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        data = prepare_data_report(request)
        serializer = CreateReportSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        report = serializer.create(serializer.validated_data)
        return Response({"id": report.pk})


class RetriveReportApi(APIView):
    def get(self, request, *args, **kwargs):
        report = get_report_by_pk_or_404(kwargs["pk"])
        response = Response(DetailReportSerializer(report).data)
        return response

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


class UpdateReportApi(UpdateAPIView):
    queryset = Reports.objects.all()
    authentication_classes = (JWTAuthentication,)

    def update(self, request, *args, **kwargs):
        report = get_report_by_pk_or_404(kwargs.get('pk'))
        data = prepare_data_report(request)
        serializer = UpdateReportSerializer(data=data, instance=report)
        serializer.is_valid(raise_exception=True)
        report = serializer.update(report, serializer.validated_data)
        return Response({"id": report.pk})
