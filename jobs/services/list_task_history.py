import uuid

from django.db.models import QuerySet

from commons.dataclasses import BaseDataClass
from commons.patterns.runnable import Runnable
from jobs.models import TaskExecutionHistory


class ListTaskHistoryData(BaseDataClass):
    task_histories: QuerySet[TaskExecutionHistory]

    class Config:
        arbitrary_types_allowed = True


class ListTaskHistoryService(Runnable):
    @classmethod
    def run(cls, user_id: uuid.UUID) -> ListTaskHistoryData:
        qs = TaskExecutionHistory.objects.filter(user_id=user_id).values_list(
            "id", "execution_time", "status", "retry_count"
        )

        return ListTaskHistoryData(task_histories=qs)
