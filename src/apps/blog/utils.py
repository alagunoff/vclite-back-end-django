from django.db.models import QuerySet, Q, Count
from django.http import QueryDict

from .models.post import Post


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
    queried_sorting_field = query_params.get('sort_by')

    if queried_sorting_field:
        if queried_sorting_field in ('creation_date', '-creation_date'):
            posts = posts.order_by(queried_sorting_field)

        if queried_sorting_field == 'author_name':
            posts = posts.order_by('author__user__first_name')

        if queried_sorting_field == '-author_name':
            posts = posts.order_by('-author__user__first_name')

        if queried_sorting_field == 'category':
            posts = posts.order_by('category__category')

        if queried_sorting_field == '-category':
            posts = posts.order_by('-category__category')

        if queried_sorting_field == 'images':
            posts = posts.annotate(extra_images_number=Count(
                'extra_images')).order_by('extra_images_number')

        if queried_sorting_field == '-images':
            posts = posts.annotate(extra_images_number=Count(
                'extra_images')).order_by('-extra_images_number')

    return posts.distinct()
