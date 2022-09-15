from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import users

urlpatterns = [
    path('', users.UserRetrieveCreateAPIView.as_view()),
    path('/<str:pk>', users.UserDestroyAPIView.as_view()),
    path('/tokens/', obtain_auth_token),
]
