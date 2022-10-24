from django.contrib.auth import authenticate
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from shared.permissions import IsAdmin

from .models import User
from .serializers import User as UserSerializer


class Index(GenericAPIView, CreateModelMixin):
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={200: openapi.Response('user', UserSerializer)})
    def get(self, request: Request, *args, **kwargs) -> Response:
        if request.user.is_authenticated:
            return Response(self.get_serializer(request.user).data)

        return Response(status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, args, kwargs)

    def perform_create(self, serializer):
        User.objects.create_user(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class Detail(GenericAPIView, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class Login(GenericAPIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }), responses={200: 'user\'s token'})
    def post(self, request: Request, *args, **kwargs) -> Response:
        authenticated_user = authenticate(username=request.data.get(
            'username'), password=request.data.get('password'))

        if authenticated_user:
            return Response(authenticated_user.auth_token.key)

        return Response({'error': 'invalid credentials'}, status=HTTP_400_BAD_REQUEST)
