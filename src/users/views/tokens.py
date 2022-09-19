from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token

from api.types import HttpRequestMethods

from ..models.user import User


@api_view([HttpRequestMethods.get.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    queried_username = request.query_params.get('username')
    queried_password = request.query_params.get('password')

    if queried_username is not None and queried_password is not None:
        try:
            user = User.objects.get(pk=queried_username)
        except User.DoesNotExist:
            raise NotFound()

        is_queried_password_correct = user.check_password(queried_password)

        if is_queried_password_correct:
            Token.objects.get(user=user).delete()
            new_token = Token.objects.create(user=user).key

            return Response({'token': new_token})
        else:
            return Response({'detail': 'Password isn\'t correct'}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'detail': 'Fields "username", "password" are required'}, status=status.HTTP_400_BAD_REQUEST)
