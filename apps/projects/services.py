from django.http import Http404

from apps.common.cache import get_or_cache_project_page
from apps.projects.models import Project


def get_project_page_data(projects, user_id, page):
    """
    Considering each page has 10 projects,
    Use get_or_cache_project_page() for pages 1-5,
    Otherwise query directly.
    """
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size

    if page <= 5:
        return get_or_cache_project_page(projects, user_id, page, start, end)

    return [{'id':p.id, 'name':p.name, 'created_at':p.created_at.isoformat()} for p in projects[start:end]]


def get_own_project(user, project_id):
    try:
        project = Project.owned_projects.owned_by(user).get(id=project_id)
        return project
    except Project.DoesNotExist:
        raise Http404("Project not found")
