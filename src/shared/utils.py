from typing import Any
from collections import OrderedDict
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.pagination import LimitOffsetPagination


def check_if_requesting_user_admin(request: Request) -> bool:
    return request.user.is_authenticated and request.user.is_admin


def filter_out_none_values(ordered_dict: OrderedDict) -> OrderedDict:
    return OrderedDict([(key, ordered_dict[key]) for key in ordered_dict if ordered_dict[key] is not None])


def paginate_queryset(queryset: QuerySet[Any], request: Request) -> tuple[LimitOffsetPagination, QuerySet[Any]]:
    paginator = LimitOffsetPagination()

    return paginator, paginator.paginate_queryset(queryset, request)
