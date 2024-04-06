from rest_framework import serializers

from commons.serializers import ReadOnlySerializer


class JobRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    is_recurring = serializers.BooleanField(required=False, default=False)
    interval = serializers.CharField(required=False)
    max_retry_count = serializers.IntegerField(required=False, default=3)
    callback_url = serializers.CharField(required=True)
    job_type = serializers.CharField(required=True)
    config = serializers.JSONField(required=True)

    def validate_job_type(self, value):
        valid_names = ["SEND_EMAIL"]
        if value not in valid_names:
            raise serializers.ValidationError("Invalid job type. Must be one of: SEND_EMAIL")
        return value

    def validate(self, attrs):
        is_recurring = attrs.get("is_recurring", False)
        interval = attrs.get("interval")

        if is_recurring and not interval:
            raise serializers.ValidationError("If job is recurring, interval must be provided.")

        return attrs


class CreateJobResponseSerializer(ReadOnlySerializer):
    job_id = serializers.UUIDField(source="id")


class JobResponseSerializer(ReadOnlySerializer):
    job_id = serializers.UUIDField(source="id")
    name = serializers.CharField(required=True)
    is_recurring = serializers.BooleanField(required=True)
    interval = serializers.CharField(required=True)
    max_retry_count = serializers.IntegerField(required=True)
    callback_url = serializers.URLField(required=True)
    job_type = serializers.CharField(required=True)
    config = serializers.JSONField(required=True)


class ListJobResponseSerializer(ReadOnlySerializer):
    jobs = serializers.ListField(child=JobResponseSerializer())


class UpdateJobRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    is_recurring = serializers.BooleanField(default=False)
    interval = serializers.CharField(required=True)
    max_retry_count = serializers.IntegerField(required=True)
    callback_url = serializers.URLField(required=True)
    job_type = serializers.CharField(required=True)
    config = serializers.JSONField(required=True)


class UpdateJobResponseSerializer(UpdateJobRequestSerializer):
    id = serializers.UUIDField()


class TaskHistoryResponseSerializer(ReadOnlySerializer):
    task_history_id = serializers.UUIDField(source="id")
    execution_time = serializers.DateTimeField(required=True)
    status = serializers.CharField(required=True)
    retry_count = serializers.IntegerField(required=True)


class ListTaskHistoryResponseSerializer(ReadOnlySerializer):
    task_histories = serializers.ListField(child=TaskHistoryResponseSerializer())
