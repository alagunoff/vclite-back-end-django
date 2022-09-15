from django.urls import path

from .views import authors, comments, categories, tags

urlpatterns = [
    path('/authors', authors.index),
    path('/authors/<str:username>', authors.detail),
    path('/posts/<int:post_id>/comments', comments.index),
    path('/categories', categories.Index.as_view()),
    path('/categories/<int:pk>', categories.Detail.as_view()),
    path('/tags', tags.Index.as_view()),
    path('/tags/<int:pk>', tags.Detail.as_view()),
]
