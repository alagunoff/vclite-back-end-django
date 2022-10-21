from django.urls import path

from .views import IndexView, DetailView, LoginView

urlpatterns = [
    path('', IndexView.as_view()),
    path('/<int:user_id>', DetailView.as_view()),
    path('/login', LoginView.as_view()),
]
