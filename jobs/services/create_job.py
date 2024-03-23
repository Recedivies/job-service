import re
from datetime import datetime, timedelta
from typing import Any

import pytz
from django.conf import settings
from django_redis import get_redis_connection
from redis.exceptions import RedisError

from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import FAILED_SET_KEY, TASK_SCHEDULE_Z_SET
from jobs.dataclasses import CreateJobDataClass
from jobs.models import Job

logger = settings.LOGGER_INSTANCE


class CreateJobService(Runnable):
    @classmethod
    def _calculate_next_execution_time(cls, execution_interval: str):
        match = re.match(r"PT(\d+)([HMSD])", execution_interval)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)

            # Convert the unit to seconds
            if unit == "M":
                duration_seconds = amount * 60  # 1 minute = 60 seconds
            elif unit == "H":
                duration_seconds = amount * 3600  # 1 hour = 3600 seconds
            elif unit == "D":
                duration_seconds = amount * 86400  # 1 day = 86400 seconds

            current_time = datetime.now(pytz.timezone("UTC"))
            next_execution_time = current_time + timedelta(seconds=duration_seconds)

            epoch_seconds = int(next_execution_time.timestamp())
            next_execution_time_minutes = epoch_seconds // 60

            return next_execution_time_minutes
        else:
            raise ValueError("Invalid execution interval format")

    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        is_recurring: bool,
        interval: str,
        max_retry_count: int,
        callback_url: str,
        job_type: str,
        config: Any,
    ) -> CreateJobDataClass:
        redis_connection = get_redis_connection()
        try:
            job = Job.objects.create(
                name=name,
                is_recurring=is_recurring,
                interval=interval,
                max_retry_count=max_retry_count,
                callback_url=callback_url,
                user=user,
                job_type=job_type,
                config=config,
            )

            next_execution_time = cls._calculate_next_execution_time(execution_interval=interval)

            ok = redis_connection.zadd(TASK_SCHEDULE_Z_SET, {str(job.id): next_execution_time})
            if not ok:
                raise BadRequestException(FAILED_SET_KEY)
            return CreateJobDataClass(id=job.id)

        except RedisError as e:
            raise BadRequestException(str(e))
        except Exception as e:
            logger.info(e)
            raise BadRequestException(str(e))
