from django.shortcuts import get_object_or_404
from activities.serializers import (
    GeneralStatisticResultSerializer,
    ListReportsSerializer,
)
from base.shortcuts import get_user_or_404
from review.services.db_query import get_reports_statistic
from user_profiles.serializers import UserProfileInfoSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from user_profiles.services.other import (
    get_activity_statistic_dict,
    get_different_object_count_in_reports,
    get_usual_user_or_not_found,
)
from user_profiles.services.selectors import (
    get_annotate_by_content_type_and_point_id,
    get_user_reports,
    get_activity_statistics,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

User = get_user_model()


class GetInfoProfileApi(APIView):
    """
    Получение информации о пользователе на странице профиля
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileInfoSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_pk = kwargs["pk"]
        user = get_object_or_404(User, pk=user_pk)
        serializer = UserProfileInfoSerializer(user)
        return Response(serializer.data)


class GetUserReportsApi(ListAPIView):
    serializer_class = ListReportsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # TO DO ограничить просмотр репортов суперюзеров
        # user = get_usual_user_or_not_found(self.kwargs["user_pk"])
        return get_user_reports(get_object_or_404(User, pk=self.kwargs["user_pk"]))


class GetUserStatistic(RetrieveAPIView):
    serializer_class = None
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_user_or_404(pk=self.kwargs["user_pk"])
        activity_queryset = get_activity_statistics(user)
        activity_statistics = get_activity_statistic_dict(activity_queryset)
        gathered_wastes = GeneralStatisticResultSerializer(
            get_reports_statistic(user), many=True
        ).data
        data = (
            {"gathered_waste": gathered_wastes}
            | get_different_object_count_in_reports(user)
            | activity_statistics
        )
        return Response(data)
