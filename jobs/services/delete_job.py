import uuid

from django_redis import get_redis_connection

from commons.exceptions import BadRequestException, NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import FAILED_DELETE_KEY, JOB_NOT_FOUND
from jobs.models import Job


class DeleteJobService(Runnable):
    @classmethod
    def run(cls, user: User, job_id: uuid.UUID) -> None:
        try:
            redis_connection = get_redis_connection()
            job = Job.objects.get(id=job_id)

            ok = redis_connection.delete(str(job.id))
            if not ok:
                raise BadRequestException(FAILED_DELETE_KEY)
            job.delete()
        except Job.DoesNotExist:
            raise NotFoundRequestException(JOB_NOT_FOUND)
