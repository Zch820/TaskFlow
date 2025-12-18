from rest_framework import status
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

    def get(self, request, project_id):  # List tasks per project (all users ?)
        tasks = Task.objects.filter(project=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):  # Create task under a project (only owner)
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        if task.project.owner != request.user:
            raise PermissionDenied("You do not have permission to access this task")
        return task

    def get(self, request, task_id):
        task = self.get_object(request, task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        task = self.get_object(request, task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):
        task = self.get_object(request, task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = self.get_object(request, task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

