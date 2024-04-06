import uuid
from typing import Any, Dict

from commons.dataclasses import BaseDataClass


class CreateJobDataClass(BaseDataClass):
    id: uuid.UUID


class JobDataClass(BaseDataClass):
    id: uuid.UUID
    name: str
    is_recurring: bool
    interval: str
    max_retry_count: int
    callback_url: str
    job_type: str
    config: Dict[Any, Any]


class TaskHistoryDataClass(BaseDataClass):
    id: uuid.UUID
    execution_time: str
    status: str
    retry_count: int
