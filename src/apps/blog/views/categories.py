from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.types import HttpRequestMethods
from shared.utils import check_if_requesting_user_admin, paginate_queryset

from ..models.category import Category
from ..serializers.category import Category as CategorySerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        paginator, paginated_categories = paginate_queryset(
            Category.objects.filter(parent_category=None), request)
        category_serializer = CategorySerializer(
            paginated_categories, many=True)

        return paginator.get_paginated_response(category_serializer.data)

    if check_if_requesting_user_admin(request):
        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()

        return Response(category_serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value, HttpRequestMethods.put.value, HttpRequestMethods.delete.value])
def detail(request: Request, category_id: int) -> Response:
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.get.value:
        return Response(CategorySerializer(category).data)

    if check_if_requesting_user_admin(request):
        if request.method == HttpRequestMethods.post.value:
            category_serializer = CategorySerializer(data=request.data)
            category_serializer.is_valid(raise_exception=True)
            category_serializer.save(parent_category_id=category_id)

            return Response(category_serializer.data, status=status.HTTP_201_CREATED)

        if request.method == HttpRequestMethods.put.value:
            category_serializer = CategorySerializer(
                category, data=request.data)
            category_serializer.is_valid(raise_exception=True)
            category_serializer.save()

            return Response(category_serializer.data)

        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
