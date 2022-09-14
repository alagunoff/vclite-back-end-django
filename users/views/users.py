from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import Token

from api.types import HttpRequestMethods, ResponseMessages
from api.utils import check_if_requester_authenticated, check_if_requester_admin

from ..models import User
from ..serializers import UserSerializer


@api_view([HttpRequestMethods.post.value, HttpRequestMethods.get.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.post.value:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = Token.objects.get(user=serializer.instance)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    if check_if_requester_authenticated(request.user):
        return Response(UserSerializer(request.user).data)
    else:
        raise NotAuthenticated()


@api_view([HttpRequestMethods.delete.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def detail(request: Request, username: str) -> Response:
    if check_if_requester_admin(request.user):
        try:
            user = User.objects.get(pk=username)
        except User.DoesNotExist:
            raise NotFound()

        user.delete()

        return Response({'detail': ResponseMessages.success.value})

    raise NotFound()
