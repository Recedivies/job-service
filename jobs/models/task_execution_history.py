from django.db import models

from commons.base_model import BaseModel


class TaskExecutionHistory(BaseModel):
    class StatusType:
        SCHEDULED = "scheduled"
        COMPLETED = "completed"
        FAILED = "failed"

    STATUS_TYPE_CHOICES = {
        StatusType.SCHEDULED: "Scheduled",
        StatusType.COMPLETED: "Completed",
        StatusType.FAILED: "Failed",
    }

    execution_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_TYPE_CHOICES.items())
    retry_count = models.PositiveIntegerField()
    job = models.ForeignKey(to="jobs.Job", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(to="identities.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "task_execution_history"
        verbose_name = "TaskExecutionHistory"
        verbose_name_plural = "TaskExecutionHistories"

    def __str__(self):
        return f"{self.job} - {self.status}"
