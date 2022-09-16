from rest_framework import serializers

from ..models.post import Post
from ..models.category import Category
from ..serializers.category import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # def get_fields(self):
    #     fields = super().get_fields()
    #     fields['category'] = CategorySerializer(fields['category'],
    #                                             many=True, read_only=True)

    #     return fields
