from rest_framework import serializers

from apps.common.sanitizers import sanitize_plain_text
from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'owner',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def validate_name(self, value):
        return sanitize_plain_text(value)

    def validate_description(self, value):
        return sanitize_plain_text(value)

    def create(self, validated_data):
        """
        Create a new project for authenticated user as owner
        """
        project = Project(**validated_data)
        project.owner = self.context['request'].user
        project.save()
        return project


class ProjectListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
