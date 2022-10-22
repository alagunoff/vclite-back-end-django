from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shared.types import HttpRequestMethods
from shared.permissions import IsAdmin

from ..models.category import Category
from ..serializers.category import Category as CategorySerializer


class Index(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class Detail(GenericAPIView, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'category_id'

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(parent_category=self.get_object())

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
