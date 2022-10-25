from django.db import models

from apps.posts.models import Post


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.comment[:10]}...'
