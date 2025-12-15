from apps.projects.models import Project
from apps.users import serializers


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
