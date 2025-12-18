from django.tasks import Task
from django.utils import timezone
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError('Due date cannot be in the past')
        return value
