from rest_framework import generics, exceptions

from api.types import HttpRequestMethods
from api.utils import check_if_requester_admin
from generics import RetrieveCreateUpdateDestroyAPIView

from ..models.category import Category
from ..serializers.category import CategorySerializer


class Index(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

    def initial(self, request, *args, **kwargs):
        if self.request.method != HttpRequestMethods.get.value and not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)


class Detail(RetrieveCreateUpdateDestroyAPIView):
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

    def initial(self, request, *args, **kwargs):
        if self.request.method != HttpRequestMethods.get.value and not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(parent_category=self.get_object())
