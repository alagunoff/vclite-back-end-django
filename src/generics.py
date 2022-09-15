from rest_framework import mixins, generics


class RetrieveCreateAPIView(mixins.CreateModelMixin, generics.RetrieveAPIView):
    '''
    Concrete view for retrieving or creating a model instance.
    '''

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveCreateUpdateDestroyAPIView(mixins.CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    '''
    Concrete view for retrieving, creating, updating or deleting a model instance.
    '''

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
