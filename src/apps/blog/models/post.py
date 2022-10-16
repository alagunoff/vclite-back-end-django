from django.db import models

from ..constants import DEFAULT_POST_BASE64_IMAGE
from .author import Author
from .category import Category
from .tag import Tag


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    creation_date = models.DateField(auto_now_add=True)
    image = models.CharField(
        max_length=900000, default=DEFAULT_POST_BASE64_IMAGE)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.title


class PostExtraImage(models.Model):
    image = models.CharField(max_length=900000)
    post = models.ForeignKey(
        Post, related_name='extra_images', on_delete=models.CASCADE)
