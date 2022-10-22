from django.urls import path, include

from .views import posts, drafts, comments, authors, categories, tags

urlpatterns = [
    path('/posts', include([
        path('', posts.Index.as_view()),
        path('/<int:post_id>', include([
            path('', posts.Detail.as_view()),
            path('/comments', comments.Index.as_view()),
        ])),
    ])),
    path('/drafts', include([
        path('', drafts.Index.as_view()),
        path('/<int:draft_id>', drafts.Detail.as_view()),
    ])),
    path('/authors', include([
        path('', authors.Index.as_view()),
        path('/<int:author_id>', authors.Detail.as_view()),
    ])),
    path('/categories', include([
        path('', categories.Index.as_view()),
        path('/<int:category_id>', categories.Detail.as_view()),
    ])),
    path('/tags', include([
        path('', tags.Index.as_view()),
        path('/<int:tag_id>', tags.Detail.as_view()),
    ])),
]
