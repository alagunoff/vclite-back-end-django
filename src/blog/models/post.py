from django.db import models

from .author import Author
from .category import Category
from .tag import Tag


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateField(auto_now_add=True)
    image = models.CharField(max_length=900000)
    is_draft = models.BooleanField(default=False)


class PostExtraImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.CharField(max_length=900000)
