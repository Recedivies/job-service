from typing import Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.serializers import TaskHistoryResponseSerializer
from jobs.services.get_task_history import GetTaskHistoryService


class DetailTaskHistoryAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        task_history_id = self.kwargs.get("task_history_id")
        service = GetTaskHistoryService.run(user=request.user, task_history_id=task_history_id)

        return Response(TaskHistoryResponseSerializer(service).data)
