from django.db import models
from django.conf import settings


class Author(models.Model):
    description = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)

    class Meta:
        db_table = 'authors'
        ordering = ['id']

    def __str__(self) -> str:
        return self.user.username
