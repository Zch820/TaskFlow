from django.http import Http404

from apps.tasks.models import Task


def get_task_under_project(user, project_id, task_id):
    try:
        task = Task.active_objects.get(project__owner=user, project_id=project_id, id=task_id)
        return task
    except Task.DoesNotExist:
        raise Http404("Task not found")



