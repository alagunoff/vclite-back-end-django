from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.types import HttpRequestMethods, ResponseMessages
from api.utils import check_if_requester_authenticated, check_if_requester_admin
from api.permissions import IsRequesterAdmin

from ..models.category import Category
from ..serializers.category import CategorySerializer


@api_view([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request) -> Response:
    if request.method == HttpRequestMethods.get.value:
        return Response(CategorySerializer(Category.objects.filter(parent_category=None), many=True).data)

    if check_if_requester_authenticated(request.user):
        if check_if_requester_admin(request.user):
            category_serializer = CategorySerializer(data=request.data)
            category_serializer.is_valid(raise_exception=True)
            category_serializer.save()

            return Response({'detail': ResponseMessages.success.value}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Only admins are allowed to create categories'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'detail': ResponseMessages.credentials_are_required.value}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Token'})


@api_view([HttpRequestMethods.post.value, HttpRequestMethods.delete.value, HttpRequestMethods.patch.value])
@permission_classes([IsAuthenticated, IsRequesterAdmin])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def detail(request: Request, category_id: int) -> Response:
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({'detail': ResponseMessages.there_is_no_such_category.value}, status=status.HTTP_404_NOT_FOUND)

    if request.method == HttpRequestMethods.post.value:
        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save(parent_category=category)

        return Response({'detail': ResponseMessages.success.value}, status=status.HTTP_201_CREATED)

    if request.method == HttpRequestMethods.delete.value:
        category.delete()

        return Response({'detail': ResponseMessages.success.value})

    category_serializer = CategorySerializer(category, request.data)
    category_serializer.is_valid(raise_exception=True)
    category_serializer.save()

    return Response({'detail': ResponseMessages.success.value})
