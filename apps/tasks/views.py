import logging
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.tasks.services import get_task_under_project
from apps.projects.services import get_owned_project

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer

logger = logging.getLogger("task")

@extend_schema(
    tags=["Tasks"],
    responses={
        200: TaskSerializer(many=True),
        403: {"detail": "Permission denied"},
        404: {"detail": "Not found"},
    }
)
class TasksListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_project(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        return get_owned_project(user, project_id)

    def get_queryset(self):
        project = self.get_project()
        tasks = Task.objects.filter(project=project)
        return tasks

    def perform_create(self, serializer):
        project = self.get_project()
        task = serializer.save(project=project)
        logger.info(
            f"Create task | user_id={self.request.user.id} | task_id={task.id} | project_id={project.id}"
        )


@extend_schema(
    tags=["Tasks"],
    responses={
        200: TaskSerializer,
        403: {"detail": "Permission denied"},
        404: {"detail": "Not found"},
    }
)
class TasksDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_object(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        return get_task_under_project(user, project_id, task_id)

    def perform_update(self, serializer):
        task = serializer.save()
        logger.info(
            f"Update task | user_id={self.request.user.id} | task_id={task.id} | project_id={task.project.id}"
        )

    def perform_destroy(self, instance):
        logger.warning(
            f"Delete task | user_id={self.request.user.id} | task_id={instance.id} | project_id={instance.project.id}"
        )
        instance.delete()
