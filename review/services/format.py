from django.db.models import QuerySet
from review.config import OBJECT_TYPE_MAP
from rest_framework.exceptions import NotFound, APIException
from rest_framework.views import APIView
from review.services.db_query import get_one_object_with_rates_by_id_or_not_found_error
from rest_framework.response import Response
from review.services.db_query import get_reports_statistic

def get_model_or_not_found_error(object_type: str, object_type_map=OBJECT_TYPE_MAP) -> QuerySet:
    try:
        model_object = object_type_map[object_type]
    except KeyError:
        raise NotFound

    return model_object


class ObjectInfoAndReportStatisitcView(APIView):
    serializer_class = None
    model = None
    object_name = 'object_info'

    def get(self, request, *args, **kwargs):

        try:
            obj = get_one_object_with_rates_by_id_or_not_found_error(self.model, kwargs.get('id'))
            report_information = get_reports_statistic(obj)
            serializer = self.serializer_class(instance=obj)

        except Exception:
            raise APIException

        return Response({self.object_name: serializer.data,
                         'reports_statistic': report_information})