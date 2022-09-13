from django.db import models

from users.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=255)
