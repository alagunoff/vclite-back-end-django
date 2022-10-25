from django.urls import path

from .views import Index, Detail

urlpatterns = [
    path('', Index.as_view()),
    path('/<int:tag_id>', Detail.as_view()),
]
