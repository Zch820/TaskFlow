from django.urls import path

from apps.tasks import views

urlpatterns = [
    path('project/<int:project_id>/', views.TasksListView.as_view(), name='task-list'),
    path('<int:task_id>/project/<int:project_id>/', views.TasksDetailView.as_view(), name='task-detail'),
]
