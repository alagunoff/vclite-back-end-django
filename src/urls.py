from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', get_schema_view(
        openapi.Info(title='Vclite API', default_version='v1'),
        public=True,
    ).with_ui('swagger', cache_timeout=0)),
    path('blog', include([
        path('/authors', include('apps.authors.urls')),
        path('/categories', include('apps.categories.urls')),
        path('/drafts', include('apps.drafts.urls')),
        path('/posts', include('apps.posts.urls')),
        path('/tags', include('apps.tags.urls')),
    ])),
    path('users', include('apps.users.urls')),
]
