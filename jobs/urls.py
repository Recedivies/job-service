from django.urls import path  # noqa

from jobs.views.detail_job import DetailJobAPI
from jobs.views.job import JobAPI

jobs_urls = [
    path("", JobAPI.as_view(), name="job-api"),
    path("<uuid:job_id>/", DetailJobAPI.as_view(), name="detail-job-api"),
]

urlpatterns = []
urlpatterns += jobs_urls
