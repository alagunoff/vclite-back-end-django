from rest_framework import status as status_codes
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserCreationSerializer


@api_view(['POST'])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = Token.objects.get(user=serializer.instance)

    return Response(token.key, status=status_codes.HTTP_201_CREATED)


@api_view(['GET'])
def login(request: Request) -> Response:
    queried_username = request.query_params.get('username')
    queried_password = request.query_params.get('password')

    if queried_username is not None and queried_password is not None:
        try:
            user = User.objects.get(username=queried_username)
            is_queried_password_correct = user.check_password(queried_password)

            if is_queried_password_correct:
                Token.objects.get(user=user).delete()
                new_token = Token.objects.create(user=user).key

                return Response(new_token)
            else:
                return Response('Password is not correct', status=status_codes.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response('There is no such user', status=status_codes.HTTP_400_BAD_REQUEST)
    else:
        return Response('Fields: username, password are required', status=status_codes.HTTP_400_BAD_REQUEST)
