from django.urls import path

from .views import users, tokens

urlpatterns = [
    path('', users.Index.as_view()),
    path('/<str:pk>', users.Detail.as_view()),
    path('/tokens', tokens.index),
]
