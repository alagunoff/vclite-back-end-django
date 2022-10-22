from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shared.types import HttpRequestMethods
from shared.permissions import IsAuthor

from ..models.post import Post
from ..serializers.post import Post as PostSerializer


class Index(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = PostSerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAuthor()]

    def get_queryset(self):
        return Post.objects.filter(author=getattr(self.request.user, 'author', None), is_draft=True)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class Detail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = PostSerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated()]

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['draft_id'], author=getattr(self.request.user, 'author', None), is_draft=True)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
