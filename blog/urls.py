from django.urls import path

from .views import categories, tags

urlpatterns = [
    path('/categories', categories.index),
    path('/categories/<int:category_id>', categories.detail),
    path('/tags', tags.index),
    path('/tags/<int:tag_id>', tags.detail),
]
