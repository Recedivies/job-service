from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import JOB_NOT_FOUND
from jobs.dataclasses import JobDataClass
from jobs.models import Job


class GetJobService(Runnable):
    @classmethod
    def run(cls, user: User, job_id: str) -> JobDataClass:
        try:
            job = Job.objects.get(id=job_id)
        except job.DoesNotExist:
            raise NotFoundRequestException(JOB_NOT_FOUND)

        return JobDataClass(
            id=job.id,
            name=job.name,
            is_recurring=job.is_recurring,
            interval=job.interval,
            max_retry_count=job.max_retry_count,
            callback_url=job.callback_url,
            job_type=job.job_type,
            config=job.config,
        )
