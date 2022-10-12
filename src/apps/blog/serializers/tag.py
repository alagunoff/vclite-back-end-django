from rest_framework import serializers

from ..models.tag import Tag as TagModel


class Tag(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id', 'tag']
