from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.tag
