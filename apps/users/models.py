from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from apps.common.managers import ActiveManager


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

    # managers
    active_objects = ActiveManager()
    objects = UserManager()

    def delete(self, using=None, keep_parents=False):
        """
        Soft-delete the instance by setting is_deleted to True.
        """
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
