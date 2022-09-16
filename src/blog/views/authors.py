from rest_framework import generics, exceptions

from api.utils import check_if_requester_admin

from ..models.author import Author
from ..serializers.author import AuthorSerializer


class ListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def initial(self, request, *args, **kwargs):
        if not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def initial(self, request, *args, **kwargs):
        if not check_if_requester_admin(request.user):
            raise exceptions.NotFound()

        super().initial(request, *args, **kwargs)
