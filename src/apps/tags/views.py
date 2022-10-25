from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shared.types import HttpRequestMethods
from shared.permissions import IsAdmin

from .models import Tag
from .serializers import Tag as TagSerializer


class Index(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class Detail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_url_kwarg = 'tag_id'

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
