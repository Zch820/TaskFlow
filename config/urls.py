from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Versioned APIs
    path('api/v1/', include(('apps.users.urls', 'users'), namespace='v1_users')),
    path('api/v1/', include(('apps.projects.urls', 'projects'), namespace='v1_projects')),
    path('api/v1/', include(('apps.tasks.urls', 'tasks'), namespace='v1_tasks')),

    # API schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui",),
]
