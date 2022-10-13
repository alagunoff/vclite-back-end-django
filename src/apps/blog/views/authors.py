from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types_old.api import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin, paginate_queryset

from ..models.author import Author
from ..serializers.author import Author as AuthorSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    if check_if_requesting_user_admin(request):
        if request.method == HttpRequestMethods.get.value:
            paginator, paginated_authors = paginate_queryset(
                Author.objects.all(), request)
            author_serializer = AuthorSerializer(paginated_authors, many=True)

            return paginator.get_paginated_response(author_serializer.data)

        author_serializer = AuthorSerializer(data=request.data)
        author_serializer.is_valid(raise_exception=True)
        author_serializer.save()

        return Response(author_serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.patch.value, HttpRequestMethods.delete.value])
def detail(request: Request, author_id: int) -> Response:
    if check_if_requesting_user_admin(request):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == HttpRequestMethods.get.value:
            return Response(AuthorSerializer(author).data)

        if request.method == HttpRequestMethods.patch.value:
            author_serializer = AuthorSerializer(
                author, data=request.data, partial=True)
            author_serializer.is_valid(raise_exception=True)
            author_serializer.save()

            return Response(author_serializer.data)

        author.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
