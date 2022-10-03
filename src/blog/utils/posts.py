from typing import Any

from ..models.post import Post, PostExtraImage
from ..models.comment import Comment
from ..models.author import Author
from ..constants import DEFAULT_POST_BASE64_IMAGE
from .authors import map_author_to_dict
from .categories import map_category_to_dict
from .tags import map_tag_to_dict
from .comments import map_comment_to_dict


def create_post(data: dict[str, Any], author: Author, is_draft: bool = False) -> Post:
    post = Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        author=author,
        category_id=data.get('category_id'),
        image=data.get('image', DEFAULT_POST_BASE64_IMAGE),
        is_draft=is_draft
    )
    post.tags.set(data.get('tags'))

    for extra_image in data.get('extra_images', []):
        PostExtraImage.objects.create(image=extra_image, post=post)

    return post


def update_post(post: Post, data: dict[str, Any]) -> Post:
    if 'title' in data:
        post.title = data.get('title')

    if 'content' in data:
        post.content = data.get('content')

    if 'category_id' in data:
        post.category_id = data.get('category_id')

    if 'tags' in data:
        post.tags.set(data.get('tags'))

    if 'image' in data:
        post.image = data.get('image')

    if 'is_draft' in data:
        post.is_draft = data.get('is_draft')

    post.save()

    return post


def map_post_to_dict(post: Any) -> dict[str, Any]:
    post_dict: dict[str, Any] = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': map_author_to_dict(post.author),
        'category': map_category_to_dict(post.category),
        'tags': list(map(map_tag_to_dict, post.tags.all())),
        'creation_date': post.creation_date,
        'image': post.image
    }

    comments = Comment.objects.filter(post_id=post.id)
    if comments.exists():
        post_dict['comments'] = list(map(map_comment_to_dict, comments))

    extra_images = PostExtraImage.objects.filter(post=post)
    if extra_images.exists():
        for extra_image in extra_images:
            if 'extra_images' in post_dict:
                post_dict['extra_images'].append(extra_image)
            else:
                post_dict['extra_images'] = [extra_image]

    return post_dict
