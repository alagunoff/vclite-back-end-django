from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin, paginate_queryset

from ..models.comment import Comment
from ..models.post import Post
from ..serializers.comment import Comment as CommentSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value, HttpRequestMethods.delete.value])
def index(request: Request, post_id: int) -> Response:
    try:
        Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(post_id=post_id)

    if request.method == HttpRequestMethods.get.value:
        paginator, paginated_comments = paginate_queryset(comments, request)
        comment_serializer = CommentSerializer(paginated_comments, many=True)

        return paginator.get_paginated_response(comment_serializer.data)

    if check_if_requesting_user_admin(request):
        if request.method == HttpRequestMethods.post.value:
            comment_serializer = CommentSerializer(data=request.data)
            comment_serializer.is_valid(raise_exception=True)
            comment_serializer.save(post_id=post_id)

            return Response(comment_serializer.data)

        comments.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
