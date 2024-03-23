import uuid

from django.db.models import QuerySet

from commons.dataclasses import BaseDataClass
from commons.patterns.runnable import Runnable
from jobs.models import Job


class ListJobData(BaseDataClass):
    jobs: QuerySet[Job]

    class Config:
        arbitrary_types_allowed = True


class ListJobService(Runnable):
    @classmethod
    def run(cls, user_id: uuid.UUID) -> ListJobData:
        qs = Job.objects.filter(user_id=user_id)

        return ListJobData(jobs=qs)
