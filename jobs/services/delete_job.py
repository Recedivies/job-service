import uuid

from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import JOB_NOT_FOUND
from jobs.models import Job


class DeleteJobService(Runnable):
    @classmethod
    def run(cls, user: User, job_id: uuid.UUID) -> None:
        try:
            job = Job.objects.get(id=job_id)
            job.delete()
        except Job.DoesNotExist:
            raise NotFoundRequestException(JOB_NOT_FOUND)
