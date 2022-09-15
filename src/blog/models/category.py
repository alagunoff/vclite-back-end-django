from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey(
        'self', blank=True, null=True, related_name='subcategories', on_delete=models.CASCADE)
