from django.shortcuts import get_object_or_404

from apps.projects.models import Project


def get_owned_project(user, project_id):
    project = get_object_or_404(Project, id=project_id, owner=user)
    return project
