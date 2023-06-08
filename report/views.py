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
)
from report.util import first_el_from_request_data
from rest_framework.generics import ListAPIView
from eco.models import (
    WasteTypes,
    SortPoints,
    NatureObjects,
    Routes,
    Events
)


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
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.create(serializer.validated_data)
        return Response()


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

