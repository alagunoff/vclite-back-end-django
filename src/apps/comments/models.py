from django.db import models
from django.conf import settings

from apps.posts.models import Post


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.comment[:10]}...'
