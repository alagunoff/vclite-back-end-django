from django.urls import path

from .views.users import index, detail, login

urlpatterns = [
    path('', index),
    path('/<int:user_id>', detail),
    path('/login', login),
]
