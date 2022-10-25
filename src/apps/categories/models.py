from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=70)
    parent_category = models.ForeignKey(
        'self', blank=True, null=True, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'
        ordering = ['id']

    def __str__(self) -> str:
        return self.category
