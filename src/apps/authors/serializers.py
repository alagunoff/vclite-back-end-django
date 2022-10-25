from rest_framework import serializers

from .models import Author as AuthorModel


class Author(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = AuthorModel
        fields = ['id', 'description', 'user_id']
