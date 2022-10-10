import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import check_if_requesting_user_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated
from shared.utils import paginate_queryset

from ..models.comment import Comment
from ..models.post import Post
from ..utils.comments import create_comment, map_comment_to_dict


def index(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()

    comments = Comment.objects.filter(post_id=post_id)

    if request.method == HttpRequestMethods.get.value:
        paginated_comments = paginate_queryset(comments, request.GET)

        return JsonResponse([map_comment_to_dict(comment) for comment in paginated_comments], safe=False)

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.post.value:
            created_comment = create_comment(json.loads(request.body), post_id)

            return JsonResponseCreated(map_comment_to_dict(created_comment))

        if request.method == HttpRequestMethods.delete.value:
            comments.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value, HttpRequestMethods.delete.value])

    return HttpResponseNotAllowed([HttpRequestMethods.get.value])
