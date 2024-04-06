import uuid
from typing import Any, Dict

from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import JOB_NOT_FOUND
from jobs.dataclasses import JobDataClass
from jobs.models import Job


class UpdateJobService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        job_id: uuid.UUID,
        name: str,
        is_recurring: bool,
        interval: str,
        max_retry_count: int,
        callback_url: str,
        job_type: str,
        config: Dict[Any, Any],
    ) -> JobDataClass:
        try:
            job = Job.objects.get(id=job_id)
        except job.DoesNotExist:
            raise NotFoundRequestException(JOB_NOT_FOUND)

        job.name = name
        job.is_recurring = is_recurring
        job.interval = interval
        job.max_retry_count = max_retry_count
        job.callback_url = callback_url
        job.job_type = job_type
        job.config = config

        job.save()

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
