import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import check_if_requesting_user_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated

from ..models.post import Post
from ..utils.posts import create_post, map_post_to_dict


def index(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(list(map(map_post_to_dict, Post.objects.all())), safe=False)

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.post.value:
            created_post = create_post(json.loads(request.body))

            return JsonResponseCreated(map_post_to_dict(created_post))

        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])


def detail(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        post_for_dealing = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(map_post_to_dict(post_for_dealing))

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.delete.value:
            post_for_dealing.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([
            HttpRequestMethods.get.value,
            HttpRequestMethods.delete.value
        ])

    return HttpResponseNotAllowed([HttpRequestMethods.get.value])
