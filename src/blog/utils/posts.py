from typing import Any
from django.db.models import QuerySet, Q, Count
from django.http import QueryDict

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
                post_dict['extra_images'].append(extra_image.image)
            else:
                post_dict['extra_images'] = [extra_image.image]

    return post_dict


def filter_posts(posts: QuerySet[Post], query_params: QueryDict) -> QuerySet[Post]:
    if 'title' in query_params:
        posts = posts.filter(title__contains=query_params.get('title'))

    if 'content' in query_params:
        posts = posts.filter(content__contains=query_params.get('content'))

    if 'creation_date' in query_params:
        posts = posts.filter(creation_date=query_params.get('creation_date'))

    if 'creation_date__lt' in query_params:
        posts = posts.filter(
            creation_date__lt=query_params.get('creation_date__lt'))

    if 'creation_date__gt' in query_params:
        posts = posts.filter(
            creation_date__gt=query_params.get('creation_date__gt'))

    if 'author_name' in query_params:
        posts = posts.filter(
            author__user__first_name=query_params.get('author_name'))

    if 'category_id' in query_params:
        posts = posts.filter(category_id=query_params.get('category_id'))

    if 'tag' in query_params:
        posts = posts.filter(tags__id=query_params.get('tag'))

    if 'tags__in' in query_params:
        posts = posts.filter(tags__id__in=list(
            map(int, query_params.getlist('tags__in'))))

    if 'tags__all' in query_params:
        for tag_id in query_params.getlist('tags__all'):
            posts = posts.filter(tags__id=tag_id)

    if 'search' in query_params:
        search = query_params.get('search')
        posts = posts.filter(Q(title__contains=search) | Q(content__contains=search) | Q(
            author__user__first_name=search) | Q(category__category=search) | Q(tags__tag=search))

    return posts


def sort_posts(posts: QuerySet[Post], query_params: QueryDict) -> QuerySet[Post]:
    sorting_field = query_params.get('sort_by')

    if sorting_field:
        if sorting_field in ('creation_date', '-creation_date'):
            posts = posts.order_by(sorting_field)

        if sorting_field == 'author_name':
            posts = posts.order_by('author__user__first_name')

        if sorting_field == '-author_name':
            posts = posts.order_by('-author__user__first_name')

        if sorting_field == 'category':
            posts = posts.order_by('category__category')

        if sorting_field == '-category':
            posts = posts.order_by('-category__category')

        if sorting_field == 'images':
            posts = posts.annotate(extra_images_number=Count(
                'postextraimage')).order_by('extra_images_number')

        if sorting_field == '-images':
            posts = posts.annotate(extra_images_number=Count(
                'postextraimage')).order_by('-extra_images_number')

    return posts.distinct()
