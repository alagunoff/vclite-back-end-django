from django.urls import path

from .views import users, tokens

urlpatterns = [
    path('', users.index),
    path('/<str:username>', users.detail),
    path('/tokens', tokens.index),
]
