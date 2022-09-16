from rest_framework import status, generics, mixins, permissions, exceptions, response
from rest_framework.authtoken.models import Token

from api.types import HttpRequestMethods
from api.utils import check_if_requester_admin

from ..models import User
from ..serializers import UserSerializer


class UserRetrieveCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == HttpRequestMethods.get.value:
            return [permissions.IsAuthenticated()]

        return []

    def get(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(request.user)

        return response.Response(user_serializer.data)

    def post(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        headers = self.get_success_headers(user_serializer.data)
        token_key = Token.objects.get(user=user_serializer.instance).key

        return response.Response({'token': token_key}, status=status.HTTP_201_CREATED, headers=headers)


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def initial(self, request, *args, **kwargs):
        if not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)
