import logging
import redis
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.projects.models import Project

r = redis.Redis(host='localhost', port=6379, db=0)
logger = logging.getLogger("project")
MAX_CACHED_PAGES = 6


@receiver(post_delete, sender=Project)
def project_deletion_log(sender, instance, **kwargs):
    """
    Log project deletion performed by the owner or an admin.
    """
    logger.warning(
        f"Delete project | project_id={instance.id}"
    )

@receiver(post_save, sender=Project)
def remove_project_cache(sender, instance, created, update_fields, **kwargs):
    """
    Clear project cache when a project is created, renamed, or soft-deleted.
    """
    fields_to_watch = {'name', 'is_deleted'}
    if created or (update_fields and fields_to_watch.intersection(update_fields)):
        for page in range(1, MAX_CACHED_PAGES + 1):
            r.delete(f"user:{instance.owner.id}:projects:{page}")
