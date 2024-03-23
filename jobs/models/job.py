from django.db import models

from commons.base_model import BaseModel


class Job(BaseModel):
    name = models.CharField(max_length=32)
    is_recurring = models.BooleanField(default=False)
    interval = models.CharField()
    max_retry_count = models.PositiveIntegerField()
    callback_url = models.URLField()
    job_type = models.CharField()
    config = models.JSONField()
    user = models.ForeignKey(to="identities.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "job"
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.id} - {self.name}"
