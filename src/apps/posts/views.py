from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shared.types import HttpRequestMethods
from shared.permissions import IsAuthor, IsAdmin

from .models import Post
from .serializers import Post as PostSerializer
from .utils import filter_posts, sort_posts


class Index(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = PostSerializer

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAuthor()]

    def get_queryset(self):
        return sort_posts(
            filter_posts(Post.objects.filter(is_draft=False),
                         self.request.query_params),
            self.request.query_params
        )

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class Detail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Post.objects.filter(is_draft=False)
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'

    def get_permissions(self):
        return [] if self.request.method == HttpRequestMethods.get.value else [IsAuthenticated(), IsAdmin()]

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
