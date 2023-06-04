from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from json import loads
from report.serializers import ReportCreateSerializer, SortPointNamesSerialzer, WasteTypesSerializer
from report.util import first_el_from_request_data
from rest_framework.generics import ListAPIView
from eco.models import SortPoints, WasteTypes



# Create your views here.
class CreateReportApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def prepare_data(self, request):
        data = first_el_from_request_data(request.data)
        rate_data = loads(request.data['rate'])
        results_data = loads(request.data['results'])
        return data|{'user_id': request.user.id, 'rate': rate_data, 'results': results_data}

    def post(self, request, *args):
        data = self.prepare_data(request)
        serializer = ReportCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.create(serializer.validated_data)
        return Response()


class SortPointsApi(ListAPIView):
    serializer_class = SortPointNamesSerialzer
    queryset = SortPoints.objects.all()


class WasteTypesApi(ListAPIView):
    serializer_class = WasteTypesSerializer
    queryset = WasteTypes.objects.all()