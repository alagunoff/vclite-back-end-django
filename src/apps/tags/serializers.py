from rest_framework import serializers

from .models import Tag as TagModel


class Tag(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id', 'tag']
