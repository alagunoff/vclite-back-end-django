from rest_framework import serializers

from apps.users.serializers import User

from .models import Comment as CommentModel


class Comment(serializers.ModelSerializer):
    author = User(read_only=True)

    class Meta:
        model = CommentModel
        fields = ['id', 'comment', 'author', 'creation_date']
