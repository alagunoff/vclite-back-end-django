from typing import Any
from django.db.models import QuerySet
from django.http import QueryDict


def paginate_queryset(queryset: QuerySet[Any], query_params: QueryDict) -> QuerySet[Any]:
    queried_offset = query_params.get('offset')
    if queried_offset:
        queryset = queryset[int(queried_offset):]

    queried_limit = query_params.get('limit')
    if queried_limit:
        queryset = queryset[:int(queried_limit)]

    return queryset
