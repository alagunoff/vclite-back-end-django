from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.types import HttpRequestMethods, Messages

from ..models import User


@api_view([HttpRequestMethods.get.value])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    queried_username = request.query_params.get('username')
    queried_password = request.query_params.get('password')

    if queried_username is not None and queried_password is not None:
        try:
            user = User.objects.get(username=queried_username)
            is_queried_password_correct = user.check_password(queried_password)

            if is_queried_password_correct:
                Token.objects.get(user=user).delete()
                new_token = Token.objects.create(user=user).key

                return Response({'token': new_token})
            else:
                return Response({'detail': 'Password isn\'t correct'}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'detail': Messages.there_is_no_such_user.value}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Fields "username", "password" are required'}, status=status.HTTP_400_BAD_REQUEST)
