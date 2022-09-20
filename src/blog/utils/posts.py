from typing import Any
from django.conf import settings

from shared.utils import decode_base64_to_image, encode_image_file_to_base64

from ..models.post import Post, PostExtraImage
from .authors import map_author_to_dict
from .categories import map_category_to_dict
from .tags import map_tag_to_dict


def create_post(data: dict[str, Any]) -> Post:
    post = Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        author_id=data.get('author_id'),
        category_id=data.get('category_id'),
        image=decode_base64_to_image(data.get('image')),
    )
    post.tags.set(data.get('tags'))

    for extra_image in data.get('extra_images', []):
        PostExtraImage.objects.create(
            image=decode_base64_to_image(extra_image), post=post)

    return post


def map_post_to_dict(post: Any) -> dict[str, Any]:
    post_dictionary = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': map_author_to_dict(post.author),
        'category': map_category_to_dict(post.category),
        'tags': list(map(map_tag_to_dict, post.tags.all())),
        'creation_date': post.creation_date,
    }

    with open(f'{settings.MEDIA_ROOT}/{post.image}', 'rb') as image_file:
        post_dictionary['image'] = encode_image_file_to_base64(image_file)

    extra_images = PostExtraImage.objects.filter(post=post)
    if extra_images.count():
        for extra_image in extra_images:
            with open(f'{settings.MEDIA_ROOT}/{extra_image.image}', 'rb') as extra_image_file:
                base64_encoded_extra_image = encode_image_file_to_base64(
                    extra_image_file)

                if 'extra_images' in post_dictionary:
                    post_dictionary['extra_images'].append(
                        base64_encoded_extra_image)
                else:
                    post_dictionary['extra_images'] = [
                        base64_encoded_extra_image]

    return post_dictionary
