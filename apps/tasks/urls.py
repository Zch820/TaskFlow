from django.urls import path

from apps.tasks import views

urlpatterns = [
    path('project/<int:project_id>/tasks/', views.TasksListView.as_view(), name='task-list'),
    path('project/<int:project_id>/task/<int:task_id>/', views.TasksDetailView.as_view(), name='task-detail'),
]
