from django.db import models

from apps.users.models import User


class Author(models.Model):
    description = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
