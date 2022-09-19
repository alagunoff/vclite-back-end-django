import json
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound

from api.types import HttpRequestMethods
from api.utils import check_if_requester_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated

from ..models.tag import Tag
from ..utils import map_tag_to_dict


def index(request: HttpRequest) -> HttpResponse:
    is_requester_admin = check_if_requester_admin(request)

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(list(map(map_tag_to_dict, Tag.objects.all())), safe=False)

    if request.method == HttpRequestMethods.post.value:
        if is_requester_admin:
            created_tag = Tag.objects.create(tag=request.POST.get('tag'))

            return JsonResponseCreated(map_tag_to_dict(created_tag))
        else:
            return HttpResponseNotFound()

    if is_requester_admin:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])


def detail(request: HttpRequest, tag_id: int) -> HttpResponse:
    try:
        tag_for_dealing = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return HttpResponseNotFound()
    is_requester_admin = check_if_requester_admin(request)

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(map_tag_to_dict(tag_for_dealing))

    if request.method == HttpRequestMethods.put.value:
        if is_requester_admin:
            data = json.loads(request.body)

            tag_for_dealing.tag = data.get('tag')
            tag_for_dealing.save()

            return JsonResponse(map_tag_to_dict(tag_for_dealing))
        else:
            return HttpResponseNotFound()

    if request.method == HttpRequestMethods.delete.value:
        if is_requester_admin:
            tag_for_dealing.delete()

            return HttpResponseNoContent()
        else:
            return HttpResponseNotFound()

    if is_requester_admin:
        return HttpResponseNotAllowed([
            HttpRequestMethods.get.value,
            HttpRequestMethods.put.value,
            HttpRequestMethods.delete.value
        ])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])
