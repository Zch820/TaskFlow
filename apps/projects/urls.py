from django.urls import path
from apps.projects import views

urlpatterns = [
    path('projects/', views.ProjectsListView.as_view(), name='projects-list'),
    path('projects/<int:pk>/', views.ProjectsDetailView.as_view(), name='projects-detail'),
]
