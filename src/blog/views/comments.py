from rest_framework import exceptions, permissions

from api.types import HttpRequestMethods
from api.utils import check_if_requester_admin
import generics as custom_generics

from ..models.comment import Comment
from ..models.post import Post
from ..serializers.comment import CommentSerializer


class ListCreateDestroyAPIView(custom_generics.ListCreateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'post'

    def initial(self, request, *args, **kwargs):
        if self.request.method == HttpRequestMethods.delete.value and not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method != HttpRequestMethods.get.value:
            return [permissions.IsAuthenticated()]

        return []

    def perform_create(self, serializer):
<<<<<<< HEAD
        post = Post.objects.get(pk=self.kwargs.get('post_id'))

        serializer.save(post=post)
=======
        serializer.save(post=self.kwargs.get('post_id'))
>>>>>>> 0ffe7538fa5e033de81203da93352293b4e8f4d0

    def get_queryset(self):
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))
