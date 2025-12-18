from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.projects.models import Project
from apps.projects.permissions import IsOwnerOrReadOnly
from apps.projects.serializers import ProjectSerializer


class ProjectsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('created_at')



