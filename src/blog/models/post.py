from django.db import models

from .author import Author
from .category import Category
from .tag import Tag


def get_path_to_store_post_primary_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return f'posts/{instance.id}/{filename}'


def get_path_to_store_post_secondary_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return f'posts/{instance.post.id}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(auto_now_add=True)
    primary_image = models.ImageField(
        upload_to=get_path_to_store_post_primary_image, blank=True)


class PostSecondaryImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.FileField(upload_to=get_path_to_store_post_secondary_image)
