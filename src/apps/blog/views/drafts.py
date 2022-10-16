from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types import HttpRequestMethods
from shared.utils import get_requesting_author, paginate_queryset

from ..models.post import Post
from ..serializers.post import Post as PostSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    requesting_author = get_requesting_author(request)

    if request.method == HttpRequestMethods.get.value:
        paginator, paginated_drafts = paginate_queryset(Post.objects.filter(
            author=requesting_author, is_draft=True), request)
        post_serializer = PostSerializer(paginated_drafts, many=True)

        return paginator.get_paginated_response(post_serializer.data)

    if requesting_author:
        post_serializer = PostSerializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save(author=requesting_author)

        return Response(post_serializer.validated_data, status=status.HTTP_201_CREATED)

    return Response({'error': 'only authors can create drafts'}, status=status.HTTP_403_FORBIDDEN)


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.patch.value, HttpRequestMethods.delete.value])
def detail(request: Request, draft_id: int) -> Response:
    requesting_author = get_requesting_author(request)

    try:
        draft = Post.objects.get(
            id=draft_id, author=requesting_author, is_draft=True)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.get.value:
        return Response(PostSerializer(draft).data)

    if request.method == HttpRequestMethods.patch.value:
        post_serializer = PostSerializer(
            draft, data=request.data, partial=True)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()

        return Response(post_serializer.validated_data)

    draft.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
