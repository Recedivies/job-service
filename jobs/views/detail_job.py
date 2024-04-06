from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.serializers import JobResponseSerializer, UpdateJobRequestSerializer, UpdateJobResponseSerializer
from jobs.services.delete_job import DeleteJobService
from jobs.services.get_job import GetJobService
from jobs.services.update_job import UpdateJobService


class DetailJobAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        job_id = self.kwargs.get("job_id")
        service = GetJobService.run(user=request.user, job_id=job_id)

        return Response(JobResponseSerializer(service).data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UpdateJobRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job_id = self.kwargs.get("job_id")

        with transaction.atomic():
            response_data = UpdateJobService.run(user=request.user, job_id=job_id, **serializer.validated_data)
            return Response(UpdateJobResponseSerializer(response_data).data)

    @transaction.atomic
    def delete(self, request: Request, **kwargs: Any) -> Response:
        job_id = self.kwargs.get("job_id")

        DeleteJobService.run(user=request.user, job_id=job_id)

        return Response(
            {"message": "Successfully deleted job"},
            status=status.HTTP_204_NO_CONTENT,
        )
