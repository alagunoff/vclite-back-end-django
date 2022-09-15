from rest_framework import mixins, generics


class RetrieveCreateUpdateDestroyAPIView(mixins.CreateModelMixin,
                                         generics.RetrieveUpdateDestroyAPIView):
    '''
    Concrete view for retrieving, creating, updating or deleting a model instance.
    '''

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
