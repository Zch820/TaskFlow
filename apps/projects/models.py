from django.contrib.auth.models import UserManager
from django.db import models

from apps.common.managers import ActiveManager, OwnedManager
from apps.users.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    # managers 
    active_objects = ActiveManager()
    owned_projects = OwnedManager()
    objects = UserManager()

    def delete(self, using = None, keep_parents = False):
        """
        Soft-delete the instance by setting is_deleted to True.
        """
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def __str__(self):
        return f'{self.name} by {self.owner}'

    class Meta:
        ordering = ['-created_at']

