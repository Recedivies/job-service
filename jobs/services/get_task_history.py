from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from jobs.constants import TASK_HISTORY_NOT_FOUND
from jobs.dataclasses import TaskHistoryDataClass
from jobs.models import TaskExecutionHistory


class GetTaskHistoryService(Runnable):
    @classmethod
    def run(cls, user: User, task_history_id: str) -> TaskHistoryDataClass:
        try:
            task_history = TaskExecutionHistory.objects.get(id=task_history_id)
        except TaskExecutionHistory.DoesNotExist:
            raise NotFoundRequestException(TASK_HISTORY_NOT_FOUND)

        return TaskHistoryDataClass(
            id=task_history.id,
            execution_time=task_history.execution_time,
            status=task_history.status,
            retry_count=task_history.retry_count,
        )
