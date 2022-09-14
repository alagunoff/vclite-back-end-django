from email.policy import default
from django.db import models

from .author import Author
from .category import Category
from .tag import Tag


# class Post(models.Model):
#     title = models.CharField(max_length=30)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     tags = models.ManyToManyField(Tag)
#     text = models.TextField()
#     main_image = models.ImageField(upload_to='images/blog')
