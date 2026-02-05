from django.urls import path

from apps.projects import views

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='project-list'),
    path('<int:pk>/', views.ProjectsDetailView.as_view(), name='project-detail'),
]
