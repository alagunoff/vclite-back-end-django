# from rest_framework import generics, exceptions, permissions

# from api.types import HttpRequestMethods
# from api.utils import check_if_requester_admin

# from ..models.post import Post
# from ..serializers.post import PostSerializer


# class ListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get_permissions(self):
#         if self.request.method == HttpRequestMethods.post.value:
#             return [permissions.IsAuthenticated()]

#         return []


# class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def initial(self, request, *args, **kwargs):
#         if self.request.method != HttpRequestMethods.get.value and not check_if_requester_admin(request.user):
#             raise exceptions.NotFound()

#         super().initial(request, *args, **kwargs)
