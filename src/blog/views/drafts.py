import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import get_requesting_author
from api.responses import HttpResponseNoContent, JsonResponseCreated, JsonResponseForbidden
from shared.utils import paginate_queryset

from ..models.post import Post
from ..utils.posts import create_post, update_post, map_post_to_dict


def index(request: HttpRequest) -> HttpResponse:
    requesting_author = get_requesting_author(request)

    if request.method == HttpRequestMethods.get.value:
        paginated_drafts = paginate_queryset(Post.objects.filter(
            author=requesting_author, is_draft=True), request.GET)

        return JsonResponse(list(map(map_post_to_dict, paginated_drafts)), safe=False)

    if request.method == HttpRequestMethods.post.value:
        if requesting_author:
            created_post = create_post(
                json.loads(request.body), requesting_author, True)

            return JsonResponseCreated(map_post_to_dict(created_post))

        return JsonResponseForbidden({'error': 'only authors can create drafts'})

    return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])


def detail(request: HttpRequest, post_id: int) -> HttpResponse:
    requesting_author = get_requesting_author(request)

    try:
        post_for_dealing = Post.objects.get(
            id=post_id, author=requesting_author, is_draft=True)
    except Post.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(map_post_to_dict(post_for_dealing))

    if request.method == HttpRequestMethods.patch.value:
        update_post(post_for_dealing, json.loads(request.body))

        return JsonResponse(map_post_to_dict(post_for_dealing))

    if request.method == HttpRequestMethods.delete.value:
        post_for_dealing.delete()

        return HttpResponseNoContent()

    return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.patch.value, HttpRequestMethods.delete.value])
