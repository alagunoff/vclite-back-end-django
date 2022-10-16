from rest_framework import serializers

from shared.utils import filter_out_none_values

from ..models.post import Post as PostModel, PostExtraImage
from .author import Author as AuthorSerializer
from .category import Category as CategorySerializer
from .tag import Tag as TagSerializer
from .comment import Comment as CommentSerializer


class Post(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    tags_ids = serializers.ListField(
        write_only=True, child=serializers.IntegerField())
    extra_images = serializers.ListField(write_only=True,
                                         required=False, child=serializers.CharField(max_length=900000))

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'creation_date', 'image', 'is_draft',
                  'category_id', 'tags_ids', 'extra_images']

    def create(self, validated_data):
        validated_data['tags'] = validated_data.pop('tags_ids')
        extra_images = validated_data.get('extra_images')

        if 'extra_images' in validated_data:
            del validated_data['extra_images']

        created_post = super().create(validated_data)

        if extra_images is not None:
            for extra_image in extra_images:
                PostExtraImage.objects.create(
                    image=extra_image, post_id=created_post.id)

        return created_post

    def to_representation(self, post):
        serialized_post = super().to_representation(post)

        serialized_post['author'] = AuthorSerializer(post.author).data
        serialized_post['category'] = CategorySerializer(post.category).data
        serialized_post['tags'] = TagSerializer(
            post.tags.all(), many=True).data

        extra_images = post.extra_images.all()
        if extra_images.exists():
            for extra_image in extra_images:
                if 'extra_images' in serialized_post:
                    serialized_post['extra_images'].append(extra_image.image)
                else:
                    serialized_post['extra_images'] = [extra_image.image]

        comments = post.comments.all()
        if comments.exists():
            serialized_post['comments'] = CommentSerializer(
                comments, many=True).data

        return filter_out_none_values(serialized_post)
