from drf_spectacular.utils import extend_schema
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

    @extend_schema(
        responses={
            200: TaskSerializer(many=True),
            403: {"detail": "Permission denied"},
            404: {"detail": "Not found"},
        },
        tags=["Tasks"],
    )
    def get(self, request, project_id):  # List tasks per project (only project owner)
        project = self.get_object(request, project_id)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: TaskSerializer,
            403: {"detail": "Permission denied"},
            404: {"detail": "Not found"},
        },
        tags=["Tasks"],
    )
    def post(self, request, project_id):  # Create task under a project (only project owner)
        project = self.get_object(request, project_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)  # get project only from URL
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Tasks"])
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





