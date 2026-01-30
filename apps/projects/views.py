import logging
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from apps.projects.permissions import IsOwnerOrReadOnly
from apps.projects.serializers import ProjectSerializer

logger = logging.getLogger("project")


class ProjectsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save()
        logger.info(
            f"Create project | user_id={self.request.user.id} | project_id={project.id}"
        )


@extend_schema(
    responses={
        200: ProjectSerializer,
        403: {"detail": "Permission denied"},
    }
)
class ProjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('created_at')

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
