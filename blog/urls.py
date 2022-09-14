from django.urls import path

from .views import authors, categories, tags

urlpatterns = [
    path('/authors', authors.index),
    path('/authors/<str:username>', authors.detail),
    path('/categories', categories.index),
    path('/categories/<int:category_id>', categories.detail),
    path('/tags', tags.index),
    path('/tags/<int:tag_id>', tags.detail),
]
