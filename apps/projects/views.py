from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.projects.models import Project
from apps.projects.permissions import IsOwnerOrReadOnly
from apps.projects.serializers import ProjectSerializer


class ProjectsListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


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


