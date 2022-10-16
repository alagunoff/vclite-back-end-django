from django.urls import path, include

from .views import posts, drafts, comments, authors, categories, tags

urlpatterns = [
    path('/posts', include([
        path('', posts.index),
        path('/<int:post_id>', include([
            path('', posts.detail),
            path('/comments', comments.index),
        ])),
    ])),
    path('/drafts', include([
        path('', drafts.index),
        path('/<int:draft_id>', drafts.detail),
    ])),
    path('/authors', include([
        path('', authors.index),
        path('/<int:author_id>', authors.detail),
    ])),
    path('/categories', include([
        path('', categories.index),
        path('/<int:category_id>', categories.detail),
    ])),
    path('/tags', include([
        path('', tags.index),
        path('/<int:tag_id>', tags.detail),
    ])),
]
