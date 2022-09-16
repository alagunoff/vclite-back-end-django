from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import users

urlpatterns = [
    path('', users.RetrieveCreateAPIView.as_view()),
    path('/<str:pk>', users.DestroyAPIView.as_view()),
    path('/tokens/', obtain_auth_token),
]
