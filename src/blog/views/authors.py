import json
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse

from api.types import HttpRequestMethods
from api.utils import check_if_requesting_user_admin
from api.responses import HttpResponseNoContent, JsonResponseCreated
from users.models import User

from ..models.author import Author
from ..utils import map_author_to_dict


def index(request: HttpRequest) -> HttpResponse:
    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.get.value:
            return JsonResponse(list(map(map_author_to_dict, Author.objects.all())), safe=False)

        if request.method == HttpRequestMethods.post.value:
            data = json.loads(request.body)
            related_user = User.objects.get(id=data.get('user_id'))
            created_author = Author.objects.create(
                user=related_user, description=data.get('description'))

            return JsonResponseCreated(map_author_to_dict(created_author))

        return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])

    return HttpResponseNotFound()


def detail(request: HttpRequest, author_id: int) -> HttpResponse:
    try:
        author_for_dealing = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound()
    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.get.value:
            return JsonResponse(map_author_to_dict(author_for_dealing))

        if request.method == HttpRequestMethods.patch.value:
            data = json.loads(request.body)
            author_for_dealing.description = data.get('description')
            author_for_dealing.save()

            return JsonResponse(map_author_to_dict(author_for_dealing))

        if request.method == HttpRequestMethods.delete.value:
            author_for_dealing.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([
            HttpRequestMethods.get.value,
            HttpRequestMethods.patch.value,
            HttpRequestMethods.delete.value
        ])

    return HttpResponseNotFound()
