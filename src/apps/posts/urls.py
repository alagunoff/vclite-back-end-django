from django.urls import path, include

from .views import Index, Detail

urlpatterns = [
    path('', Index.as_view()),
    path('/<int:post_id>', include([
        path('', Detail.as_view()),
        path('/comments', include('apps.comments.urls')),
    ])),
]
