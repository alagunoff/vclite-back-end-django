from django.db import models

from apps.users.models import User


class Author(models.Model):
    description = models.CharField(max_length=255)
    user = models.OneToOneField(
        User, related_name='author', on_delete=models.CASCADE)

    class Meta:
        db_table = 'authors'
        ordering = ['id']

    def __str__(self) -> str:
        return self.user.username
