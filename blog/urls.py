from django.urls import path

from .views import tags

urlpatterns = [
    path('/categories', tags.index),
    # path('/tags/<int:tag_id>', tags.detail),
    path('/tags', tags.index),
    path('/tags/<int:tag_id>', tags.detail),
]
