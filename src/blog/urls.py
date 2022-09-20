from django.urls import path

from .views import posts, comments, authors, categories, tags

urlpatterns = [
    path('/posts', posts.index),
    path('/posts/<int:post_id>', posts.detail),
    path('/posts/<int:post_id>/comments', comments.index),
    path('/authors', authors.index),
    path('/authors/<int:author_id>', authors.detail),
    path('/categories', categories.index),
    path('/categories/<int:category_id>', categories.detail),
    path('/tags', tags.index),
    path('/tags/<int:tag_id>', tags.detail),
]
