from django.db import models

# from .author import Author
from .category import Category
from .tag import Tag


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return f'post_{instance.pk}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(auto_now_add=True)
    # main_image = models.ImageField(upload_to=post_directory_path)
