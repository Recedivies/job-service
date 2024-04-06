from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.serializers import ListTaskHistoryResponseSerializer
from jobs.services.list_task_history import ListTaskHistoryService


class TaskHistoryAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        list_task_history = ListTaskHistoryService.run(user_id=request.user.id)

        return Response(ListTaskHistoryResponseSerializer(list_task_history.dict()).data)
