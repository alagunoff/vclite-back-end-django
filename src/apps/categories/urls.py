from django.urls import path

from .views import Index, Detail

urlpatterns = [
    path('', Index.as_view()),
    path('/<int:category_id>', Detail.as_view()),
]
