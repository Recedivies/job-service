from django.urls import path  # noqa

from jobs.views.detail_job import DetailJobAPI
from jobs.views.detail_task_history import DetailTaskHistoryAPI
from jobs.views.job import JobAPI
from jobs.views.task_history import TaskHistoryAPI

jobs_urls = [
    path("", JobAPI.as_view(), name="job-api"),
    path("<uuid:job_id>/", DetailJobAPI.as_view(), name="detail-job-api"),
    path("task-histories/", TaskHistoryAPI.as_view(), name="task-history-api"),
    path("task-histories/<uuid:task_history_id>/", DetailTaskHistoryAPI.as_view(), name="detail-task-history-api"),
]

urlpatterns = []
urlpatterns += jobs_urls
