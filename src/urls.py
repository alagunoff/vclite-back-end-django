from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from django_otp.admin import OTPAdminSite

from views import GoogleLogin


admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', get_schema_view(Info(title='Vclite API',
         default_version='v1'), public=True).with_ui('swagger', cache_timeout=0)),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('login/google', TemplateView.as_view(template_name='google-login.html')),
    path('authors', include('apps.authors.urls')),
    path('categories', include('apps.categories.urls')),
    path('drafts', include('apps.drafts.urls')),
    path('posts', include('apps.posts.urls')),
    path('tags', include('apps.tags.urls')),
    path('users', include('apps.users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
