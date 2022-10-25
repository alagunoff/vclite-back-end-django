from django.urls import path

from .views import Index, Detail

urlpatterns = [
    path('', Index.as_view()),
    path('/<int:author_id>', Detail.as_view()),
]
