from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.posts.models import Post
from shared.types import HttpRequestMethods
from shared.permissions import IsAdmin

from .serializers import Comment as CommentSerializer


class Index(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = CommentSerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        return get_object_or_404(Post, id=self.kwargs['post_id']).comments.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['post_id'])

    def delete(self, request: Request, *args, **kwargs) -> Response:
        self.get_queryset().delete()

        return Response(status=HTTP_204_NO_CONTENT)
