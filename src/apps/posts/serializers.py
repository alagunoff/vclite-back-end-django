from rest_framework import serializers

from apps.authors.serializers import Author
from apps.categories.serializers import Category
from apps.tags.serializers import Tag
from apps.comments.serializers import Comment
from shared.utils import refine_serialized_model

from .models import Post as PostModel, PostExtraImage as PostExtraImageModel


class PostExtraImage(serializers.ModelSerializer):
    class Meta:
        model = PostExtraImageModel
        fields = ['id', 'image']


class Post(serializers.ModelSerializer):
    author = Author(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    category = Category(read_only=True)
    tags_ids = serializers.ListField(
        write_only=True, child=serializers.IntegerField())
    tags = Tag(read_only=True, many=True)
    extra_images = serializers.ListField(write_only=True,
                                         required=False, child=serializers.CharField(max_length=900000))
    comments = Comment(read_only=True, many=True)

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'author', 'category', 'tags', 'creation_date', 'image', 'is_draft',
                  'category_id', 'tags_ids', 'extra_images', 'comments']

    def create(self, validated_data):
        validated_data['tags'] = validated_data.pop('tags_ids')
        extra_images = validated_data.get('extra_images')

        if 'extra_images' in validated_data:
            del validated_data['extra_images']

        created_post = super().create(validated_data)

        if extra_images is not None:
            for extra_image in extra_images:
                post_extra_image_serializer = PostExtraImage(
                    data={'image': extra_image})
                post_extra_image_serializer.is_valid(raise_exception=True)
                post_extra_image_serializer.save(post=created_post)

        return created_post

    def to_representation(self, post):
        serialized_post = super().to_representation(post)

        extra_images = post.extra_images.all()
        if extra_images.exists():
            serialized_post['extra_images'] = PostExtraImage(
                extra_images, many=True).data

        return refine_serialized_model(serialized_post)
