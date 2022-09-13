from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
