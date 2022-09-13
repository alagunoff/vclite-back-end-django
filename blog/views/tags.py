from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.types import HttpRequestMethods, Messages
from api.utils import check_if_requester_authenticated, check_if_requester_admin

from ..models import Tag
from ..serializers import TagSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        return Response(TagSerializer(Tag.objects.all(), many=True).data)

    if check_if_requester_authenticated(request.user):
        if check_if_requester_admin(request.user):
            serializer = TagSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'detail': Messages.success.value}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Only admins are allowed to create tags'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'detail': Messages.credentials_are_required.value}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})
