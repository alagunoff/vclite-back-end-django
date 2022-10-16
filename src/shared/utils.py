from typing import Any
from collections import OrderedDict
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.pagination import LimitOffsetPagination

from apps.blog.models.author import Author


def check_if_requesting_user_admin(request: Request) -> bool:
    return request.user.is_authenticated and request.user.is_admin


def get_requesting_author(request: Request) -> Author | None:
    if request.user.is_authenticated:
        try:
            return Author.objects.get(user_id=request.user.id)
        except Author.DoesNotExist:
            return None

    return None


def filter_out_none_values(ordered_dict: OrderedDict[str, str]) -> OrderedDict[str, str]:
    return OrderedDict([(key, ordered_dict[key]) for key in ordered_dict if ordered_dict[key] is not None])


def paginate_queryset(queryset: QuerySet[Any], request: Request) -> tuple[LimitOffsetPagination, list[Any]]:
    paginator = LimitOffsetPagination()

    return paginator, paginator.paginate_queryset(queryset, request)
