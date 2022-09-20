from django.db import models
from typing import Any

from .author import Author
from .category import Category
from .tag import Tag


def get_post_image_directory_path(instance: Any, filename: str) -> str:
    return f'posts/author_{instance.author.id}({instance.title})/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=get_post_image_directory_path)


def get_post_extra_image_directory_path(instance: Any, filename: str) -> str:
    return f'posts/author_{instance.post.author.id}({instance.post.title})/{filename}'


class PostExtraImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_post_extra_image_directory_path)
