from django.urls import path

from .views import tags

urlpatterns = [
    path('/tags', tags.index),
    # path('/tags/<str:name>', tags),
]
