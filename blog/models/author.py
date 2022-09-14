from django.db import models

from users.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
