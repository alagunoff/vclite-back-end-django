from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.types import HttpRequestMethods, ResponseMessages
from api.permissions import IsRequesterAdmin

from ..models.author import Author
from ..serializers.author import AuthorSerializer


@api_view([HttpRequestMethods.post.value, HttpRequestMethods.get.value])
@permission_classes([IsAuthenticated, IsRequesterAdmin])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.post.value:
        author_serializer = AuthorSerializer(data=request.data)
        author_serializer.is_valid(raise_exception=True)
        author_serializer.save(user=request.user)

        return Response({'detail': ResponseMessages.success.value}, status=status.HTTP_201_CREATED)

    return Response(AuthorSerializer(Author.objects.all(), many=True).data)


@api_view([HttpRequestMethods.patch.value, HttpRequestMethods.delete.value])
@permission_classes([IsAuthenticated, IsRequesterAdmin])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def detail(request: Request, username: str) -> Response:
    try:
        author = Author.objects.get(user__username=username)
    except Author.DoesNotExist:
        return Response({'detail': ResponseMessages.there_is_no_such_author.value}, status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.patch.value:
        author_serializer = AuthorSerializer(author, request.data)
        author_serializer.is_valid(raise_exception=True)
        author_serializer.save()

        return Response({'detail': ResponseMessages.success.value})

    author.delete()

    return Response({'detail': ResponseMessages.success.value})
