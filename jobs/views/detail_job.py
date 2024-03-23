from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.services.delete_job import DeleteJobService


class DetailJobAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def delete(self, request: Request, **kwargs: Any) -> Response:
        job_id = self.kwargs.get("job_id")

        DeleteJobService.run(user=request.user, job_id=job_id)

        return Response(
            {"message": "Successfully deleted job"},
            status=status.HTTP_204_NO_CONTENT,
        )
