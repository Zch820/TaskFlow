from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TasksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            raise PermissionDenied()
        return project

    def get(self, request, project_id):  # List tasks per project (only project owner)
        project = self.get_object(request, project_id)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):  # Create task under a project (only project owner)
        project = self.get_object(request, project_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)  # get project only from URL
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_object(self, *args, **kwargs):
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id, project_id=project_id)
        if task.project.owner != self.request.user:
            raise PermissionDenied()
        return task





