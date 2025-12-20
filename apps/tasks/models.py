from django.db import models
from apps.projects.models import Project
from apps.users.models import User


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = ('todo', 'Todo')
        IN_PROGRESS = ('in_progress', 'In Progress')
        DONE = ('done', 'Done')
    class PriorityChoices(models.TextChoices):
        LOW = ('low', 'Low')
        MEDIUM = ('medium', 'Medium')
        HIGH = ('high', 'High')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.TODO, max_length=11)
    priority = models.CharField(choices=PriorityChoices.choices, default=PriorityChoices.LOW, max_length=6)
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return f'{self.title} for project {self.project.id} till {self.due_date}'

