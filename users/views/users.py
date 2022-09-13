from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.types import HttpRequestMethods, Messages
from api.utils import check_if_requester_authenticated
from api.permissions import IsRequesterAdmin

from ..models import User
from ..serializers import UserSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        if check_if_requester_authenticated(request.user):
            return Response(UserSerializer(request.user).data)
        else:
            return Response({'detail': Messages.credentials_are_required.value}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = Token.objects.get(user=serializer.instance)

    return Response(token.key, status=status.HTTP_201_CREATED)


@api_view([HttpRequestMethods.delete.value])
@permission_classes([IsRequesterAdmin])
@renderer_classes([JSONRenderer])
def detail(request: Request, username: str) -> Response:
    try:
        user = User.objects.get(username=username).delete()
    except User.DoesNotExist:
        return Response({'detail': Messages.there_is_no_such_user.value}, status=status.HTTP_404_NOT_FOUND)

    user.delete()

    return Response({'detail': Messages.success.value})
