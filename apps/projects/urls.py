from django.urls import path
from apps import projects

urlpatterns = [
    path('projects/', projects, name='projects-list'),
    path('projects/<pk:pk>/', projects, name='projects-detail'),
]
