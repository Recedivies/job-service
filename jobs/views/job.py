from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.serializers import CreateJobResponseSerializer, JobRequestSerializer, ListJobResponseSerializer
from jobs.services.create_job import CreateJobService
from jobs.services.list_job import ListJobService


class JobAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        list_jobs = ListJobService.run(user_id=request.user.id)

        return Response(ListJobResponseSerializer(list_jobs.dict()).data)

    def post(self, request: Request) -> Response:
        serializer = JobRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            response_data = CreateJobService.run(user=request.user, **serializer.validated_data)

            return Response(CreateJobResponseSerializer(response_data).data, status=status.HTTP_201_CREATED)
