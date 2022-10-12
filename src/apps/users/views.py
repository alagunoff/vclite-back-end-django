from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from shared.types import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin

from .models import User
from .serializers import User as UserSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    created_user = User.objects.create_user(**user_serializer.validated_data)

    return Response(UserSerializer(created_user).data)


@api_view([HttpRequestMethods.delete.value])
def detail(request: Request, user_id: int) -> Response:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if check_if_requesting_user_admin(request):
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view([HttpRequestMethods.post.value])
def login(request: Request) -> Response:
    authenticated_user = authenticate(username=request.data.get(
        'username'), password=request.data.get('password'))

    if authenticated_user:
        return Response(Token.objects.get(user=authenticated_user).key)

    return Response(status=status.HTTP_400_BAD_REQUEST)
