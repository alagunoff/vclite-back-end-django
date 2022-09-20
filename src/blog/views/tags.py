import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import check_if_requesting_user_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated

from ..models.tag import Tag
from ..utils.tags import map_tag_to_dict


def index(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(list(map(map_tag_to_dict, Tag.objects.all())), safe=False)

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.post.value:
            data = json.loads(request.body)
            created_tag = Tag.objects.create(tag=data.get('tag'))

            return JsonResponseCreated(map_tag_to_dict(created_tag))

        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])


def detail(request: HttpRequest, tag_id: int) -> HttpResponse:
    try:
        tag_for_dealing = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(map_tag_to_dict(tag_for_dealing))

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.put.value:
            data = json.loads(request.body)
            tag_for_dealing.tag = data.get('tag')
            tag_for_dealing.save()

            return JsonResponse(map_tag_to_dict(tag_for_dealing))

        if request.method == HttpRequestMethods.delete.value:
            tag_for_dealing.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([
            HttpRequestMethods.get.value,
            HttpRequestMethods.put.value,
            HttpRequestMethods.delete.value
        ])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])
