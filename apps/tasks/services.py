from django.shortcuts import get_object_or_404

from apps.tasks.models import Task


def get_task_under_project(user, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project_id=project_id, project__owner=user)
    return task
