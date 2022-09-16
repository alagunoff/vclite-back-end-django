from rest_framework import generics, exceptions

from api.types import HttpRequestMethods
from api.utils import check_if_requester_admin

from ..models.tag import Tag
from ..serializers.tag import TagSerializer


class ListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def initial(self, request, *args, **kwargs):
        if self.request.method != HttpRequestMethods.get.value and not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def initial(self, request, *args, **kwargs):
        if self.request.method != HttpRequestMethods.get.value and not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)
