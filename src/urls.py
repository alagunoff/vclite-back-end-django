from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger', get_schema_view(
        openapi.Info(title='Vclite API', default_version='v1'),
        public=True,
    ).with_ui('swagger', cache_timeout=0)),
    path('users', include('apps.users.urls')),
    path('blog', include('apps.blog.urls')),
]
