from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.UserRegister, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('profile/', views.UserProfile, name='profile'),
]
