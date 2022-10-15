from rest_framework import serializers

from ..models.comment import Comment as CommentModel


class Comment(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'comment']
