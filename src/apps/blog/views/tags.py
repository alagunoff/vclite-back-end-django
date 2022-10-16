from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin, paginate_queryset

from ..models.tag import Tag
from ..serializers.tag import Tag as TagSerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        paginator, paginated_tags = paginate_queryset(
            Tag.objects.all(), request)
        tag_serializer = TagSerializer(paginated_tags, many=True)

        return paginator.get_paginated_response(tag_serializer.data)

    if check_if_requesting_user_admin(request):
        tag_serializer = TagSerializer(data=request.data)
        tag_serializer.is_valid(raise_exception=True)
        tag_serializer.save()

        return Response(tag_serializer.validated_data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.put.value, HttpRequestMethods.delete.value])
def detail(request: Request, tag_id: int) -> Response:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.get.value:
        return Response(TagSerializer(tag).data)

    if check_if_requesting_user_admin(request):
        if request.method == HttpRequestMethods.put.value:
            tag_serializer = TagSerializer(tag, data=request.data)
            tag_serializer.is_valid(raise_exception=True)
            tag_serializer.save()

            return Response(tag_serializer.validated_data)

        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
