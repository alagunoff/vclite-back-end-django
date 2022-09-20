import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import check_if_requesting_user_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated

from ..models.category import Category
from ..utils import map_category_to_dict


def index(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(list(map(map_category_to_dict, Category.objects.filter(parent_category=None))), safe=False)

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.post.value:
            data = json.loads(request.body)
            created_category = Category.objects.create(
                category=data.get('category'))

            return JsonResponseCreated(map_category_to_dict(created_category))

        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])


def detail(request: HttpRequest, category_id: int) -> HttpResponse:
    try:
        category_for_dealing = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == HttpRequestMethods.get.value:
        return JsonResponse(map_category_to_dict(category_for_dealing))

    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.post.value:
            data = json.loads(request.body)
            created_subcategory = Category.objects.create(
                category=data.get('category'), parent_category=category_for_dealing)

            return JsonResponseCreated(map_category_to_dict(created_subcategory))

        if request.method == HttpRequestMethods.put.value:
            data = json.loads(request.body)
            category_for_dealing.category = data.get('category')
            category_for_dealing.save()

            return JsonResponse(map_category_to_dict(category_for_dealing))

        if request.method == HttpRequestMethods.delete.value:
            category_for_dealing.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([
            HttpRequestMethods.get.value,
            HttpRequestMethods.post.value,
            HttpRequestMethods.put.value,
            HttpRequestMethods.delete.value
        ])
    else:
        return HttpResponseNotAllowed([HttpRequestMethods.get.value])
