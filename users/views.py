from .serializers import UserSerializer
from rest_framework import status as status_codes
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from shared.constants import HTTP_REQUEST_METHODS

from .models import User


@api_view([HTTP_REQUEST_METHODS['get'], HTTP_REQUEST_METHODS['post'], HTTP_REQUEST_METHODS['delete']])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HTTP_REQUEST_METHODS['get']:
        if request.auth is not None and request.user is not None:
            serializer = UserSerializer(request.user)

            return Response(serializer.data)
        else:
            return Response({'detail': 'Credentials are required'}, status=status_codes.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})

    if request.method == HTTP_REQUEST_METHODS['delete']:
        if request.auth is not None and request.user is not None:
            serializer = UserSerializer(request.user)
            is_requester_admin = serializer.instance.is_admin

            if is_requester_admin:
                queried_id = request.query_params.get('id')

                if queried_id is not None:
                    try:
                        User.objects.get(id=queried_id).delete()

                        return Response({'detail': 'User has been deleted'})
                    except User.DoesNotExist:
                        return Response({'detail': 'There is no such user'}, status=status_codes.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Field "id" is required'}, status=status_codes.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Only admins are allowed to delete users'}, status=status_codes.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'Credentials are required'}, status=status_codes.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = Token.objects.get(user=serializer.instance)

    return Response(token.key, status=status_codes.HTTP_201_CREATED)
