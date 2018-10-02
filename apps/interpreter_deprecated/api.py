import logging

from rest_framework import mixins, filters
from rest_framework.schemas import AutoSchema
from rest_framework.viewsets import GenericViewSet

from edu_coresys.api_utils import ApiKeyPermission
from .models import SingleScoreComputeTask
from .serializer import SingleScoreComputeTaskSerializer

log = logging.getLogger(__name__)


class SingleScoreComputeTaskViewset(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.ListModelMixin,
                                    GenericViewSet):
    """
    Создание и чтение задач интерпретации
    """

    schema = AutoSchema()
    base_name = "single_score"
    permission_classes = ApiKeyPermission,
    serializer_class = SingleScoreComputeTaskSerializer

    def get_queryset(self):
        uid = self.request.query_params.get("user_uid")
        if uid:
            return SingleScoreComputeTask.objects.filter(user__uid=uid)
        else:
            return SingleScoreComputeTask.objects.all()

"""
class BulkStudentFilter(filters.BaseFilterBackend):
    Выбирает последние результаты для запрошенных юзеров
    def filter_queryset(self, request, queryset, view):
        try:
            user_uids = request.query_params.get('user_uids')
            user_uids = list(map(lambda x: int(x), user_uids))
        except (ValueError, TypeError) as e:
            user_uids = []
        filter_kwargs = {
            "user__uid__in": user_uids
        }
        if request.query_params.get('completed'):
            filter_kwargs['completed'] = True

        selected_users = queryset.filter(**filter_kwargs)


class SingleScoreUsersBulkComputeTaskViewset(mixins.ListModelMixin):
    permission_classes = ApiKeyPermission,
    serializer_class = SingleScoreComputeTaskSerializer

    def get_queryset(self):
        pass
"""