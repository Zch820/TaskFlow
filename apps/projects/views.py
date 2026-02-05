import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.models import Project
from apps.projects.permissions import IsOwnerOrReadOnly
from apps.projects.serializers import ProjectSerializer, ProjectListSerializer
from apps.projects.services import get_project_page_data
from apps.projects.schemas import (
    project_retrieve_schema,
    project_update_schema,
    project_delete_schema,
    project_create_schema,
    project_list_schema,
)

logger = logging.getLogger("project")


class ProjectsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.active_objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectListSerializer
        return ProjectSerializer

    @project_list_schema()
    def list(self, request, *args, **kwargs):
        """
        Call get_project_page_data() for pagination and formatting.
        Get paginated list of projects with : "id", "name", "created_at".
        Return serialized list of projects.
        """
        projects = Project.active_objects.filter(owner=self.request.user)
        page_number = int(request.query_params.get("page", 1))
        projects_list = get_project_page_data(projects=projects, user_id=self.request.user.id, page=page_number)
        serializer = self.get_serializer(projects_list, many=True)
        return Response(serializer.data)

    @project_create_schema()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = serializer.save()
        logger.info(
            f"Create project | user_id={self.request.user.id} | project_id={project.id}"
        )


class ProjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.owned_projects.owned_by(self.request.user)

    @project_retrieve_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @project_update_schema()
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @project_delete_schema()
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_update(self, serializer):
        project = serializer.save()
        logger.info(
            f"Update project | user_id={self.request.user.id} | project_id={project.id}"
        )

    def perform_destroy(self, instance):
        logger.warning(
            f"Delete project | user_id={self.request.user.id} | project_id={instance.id}"
        )
        instance.delete()
