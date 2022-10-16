from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin, get_requesting_author, paginate_queryset

from ..models.post import Post
from ..serializers.post import Post as PostSerializer
from ..utils import filter_posts, sort_posts


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        posts = Post.objects.filter(is_draft=False)
        filtered_posts = filter_posts(posts, request.query_params)
        sorted_posts = sort_posts(filtered_posts, request.query_params)
        paginator, paginated_posts = paginate_queryset(sorted_posts, request)
        post_serializer = PostSerializer(paginated_posts, many=True)

        return paginator.get_paginated_response(post_serializer.data)

    requesting_author = get_requesting_author(request)

    if requesting_author:
        post_serializer = PostSerializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save(author_id=requesting_author.id)

        return Response(post_serializer.validated_data, status=status.HTTP_201_CREATED)

    return Response({'error': 'only authors can create posts'}, status=status.HTTP_403_FORBIDDEN)


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.patch.value, HttpRequestMethods.delete.value])
def detail(request: Request, post_id: int) -> Response:
    try:
        post = Post.objects.get(id=post_id, is_draft=False)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.get.value:
        return Response(PostSerializer(post).data)

    if check_if_requesting_user_admin(request):
        if request.method == HttpRequestMethods.patch.value:
            post_serializer = PostSerializer(
                post, data=request.data, partial=True)
            post_serializer.is_valid(raise_exception=True)
            post_serializer.save()

            return Response(post_serializer.validated_data)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
