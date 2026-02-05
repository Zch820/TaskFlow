from django.utils import timezone
from rest_framework import serializers

from apps.common.sanitizers import sanitize_plain_text
from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'project',
            'assigned_to',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'project', 'created_at', 'updated_at')

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError('Due date cannot be in the past')
        return value

    def validate_title(self, value):
        return sanitize_plain_text(value)

    def validate_description(self, value):
        return sanitize_plain_text(value)
