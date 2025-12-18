from django.urls import path
from apps.tasks import views

urlpatterns = [
    path('tasks/', views.TasksListView.as_view(), name='projects-list'),
    path('tasks/<int:pk>/', views.TasksDetailView.as_view(), name='projects-detail'),
]
