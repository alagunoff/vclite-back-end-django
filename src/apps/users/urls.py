from django.urls import path

from .views import Index, Detail, Login

urlpatterns = [
    path('', Index.as_view()),
    path('/<int:user_id>', Detail.as_view()),
    path('/login', Login.as_view()),
]
