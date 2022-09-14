from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.types import HttpRequestMethods, ResponseMessages
from api.utils import check_if_requester_authenticated, check_if_requester_admin
from api.permissions import IsRequesterAdmin

from ..models.tag import Tag
from ..serializers.tag import TagSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        return Response(TagSerializer(Tag.objects.all(), many=True).data)

    if check_if_requester_authenticated(request.user):
        if check_if_requester_admin(request.user):
            tag_serializer = TagSerializer(data=request.data)
            tag_serializer.is_valid(raise_exception=True)
            tag_serializer.save()

            return Response({'detail': ResponseMessages.success.value}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'detail': ResponseMessages.credentials_are_required.value}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})


@api_view([HttpRequestMethods.delete.value, HttpRequestMethods.patch.value])
@permission_classes([IsRequesterAdmin])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def detail(request: Request, tag_id: int) -> Response:
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist:
        return Response({'detail': ResponseMessages.there_is_no_such_tag.value}, status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.delete.value:
        tag.delete()

        return Response({'detail': ResponseMessages.success.value})

    tag_serializer = TagSerializer(tag, request.data)
    tag_serializer.is_valid(raise_exception=True)
    tag_serializer.save()

    return Response({'detail': ResponseMessages.success.value})
