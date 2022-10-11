from django.urls import path, include

urlpatterns = [
    path('users', include('vclite.apps.users.urls')),
    path('blog', include('vclite.apps.blog.urls')),
]
