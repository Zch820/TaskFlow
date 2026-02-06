import logging
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.projects.services import get_own_project
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from apps.tasks.schemas import (
    task_list_schema,
    task_create_schema,
    task_retrieve_schema,
    task_update_schema,
    task_delete_schema,
)
from apps.tasks.services import get_task_under_project

logger = logging.getLogger("task")


@extend_schema_view(
    get=task_list_schema,
    post=task_create_schema,
)
class TasksListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_project(self):
        """
        Using project_id from Url,
        Return a project instance or raise 404.
        """
        user = self.request.user
        project_id = self.kwargs['project_id']
        return get_own_project(user=user, project_id=project_id)

    def get_queryset(self):
        """
        Getting a project instant from get_project(),
        Retrieve tasks under that project and log the action.
        """
        project = self.get_project()
        tasks = Task.active_objects.filter(project=project).select_related('assigned_to')
        return tasks

    def perform_create(self, serializer):
        """
        Getting a project instant from get_project(),
        Create a new task under that project and log the action.
        """
        project = self.get_project()
        task = serializer.save(project=project)
        logger.info(
            f"Create task | user_id={self.request.user.id} | task_id={task.id} | project_id={project.id}"
        )


@extend_schema_view(
    get=task_retrieve_schema,
    put=task_update_schema,
    delete=task_delete_schema,
    patch=extend_schema(exclude=True)
)
class TasksDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_object(self):
        """
        Using project_id and task_id from Url,
        Return user's Tasks under project.
        """
        user = self.request.user
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        return get_task_under_project(user=user, project_id=project_id, task_id=task_id)

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
