from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Versioned APIs
    path('api/<str:version>/users/', include('apps.users.urls')),
    path('api/<str:version>/projects/', include('apps.projects.urls')),
    path('api/<str:version>/tasks/', include('apps.tasks.urls')),

    # API schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
