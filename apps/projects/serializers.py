from rest_framework import serializers
from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

    def create(self, validated_data):
        project = Project(**validated_data)
        project.owner = self.context['request'].user
        project.save()
        return project



