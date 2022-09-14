from rest_framework.serializers import ModelSerializer

from ..models.tag import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
