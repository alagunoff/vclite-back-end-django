from django.urls import path

from .views import posts, comments, authors, categories, tags

urlpatterns = [
    #     path('/posts', posts.ListCreateAPIView.as_view()),
    #     path('/posts/<int:post_id>/comments',
    #          comments.ListCreateDestroyAPIView.as_view()),
    #     path('/authors', authors.ListCreateAPIView.as_view()),
    #     path('/authors/<int:pk>', authors.RetrieveUpdateDestroyAPIView.as_view()),
    #     path('/categories', categories.ListCreateAPIView.as_view()),
    #     path('/categories/<int:pk>',
    #          categories.RetrieveCreateUpdateDestroyAPIView.as_view()),
    path('/tags', tags.index),
    path('/tags/<int:tag_id>', tags.detail),
]
