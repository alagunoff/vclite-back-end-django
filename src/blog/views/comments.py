from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from api.types import HttpRequestMethods, ResponseMessages
from api.utils import check_if_requester_authenticated

from ..models.comment import Comment
from ..serializers.comment import CommentSerializer


@api_view([HttpRequestMethods.post.value, HttpRequestMethods.get.value, HttpRequestMethods.delete.value])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def index(request: Request, post_id: int) -> Response:
    if request.method == HttpRequestMethods.post.value:
        if check_if_requester_authenticated(request.user):
            tag_serializer = CommentSerializer(data=request.data)
            tag_serializer.is_valid(raise_exception=True)
            tag_serializer.save()

            return Response({'detail': ResponseMessages.success.value}, status=status.HTTP_201_CREATED)
        else:
            raise NotAuthenticated()

    if request.method == HttpRequestMethods.delete.value:
        Comment.objects.filter(post__id=post_id).delete()

        return Response({'detail': ResponseMessages.success.value})

    return Response(CommentSerializer(Comment.objects.filter(post__id=post_id), many=True).data)
