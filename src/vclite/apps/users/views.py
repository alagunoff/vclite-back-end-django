import json
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate

from shared.types.api import HttpRequestMethods
from shared.utils.api import get_requesting_user, check_if_requesting_user_admin
from shared.responses import HttpResponseNoContent, JsonResponseCreated

from .models import User, Token
from .utils import map_user_to_dict


def index(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.get.value:
        requesting_user = get_requesting_user(request)

        if requesting_user:
            return JsonResponse(map_user_to_dict(requesting_user))

        return HttpResponseNotFound()

    if request.method == HttpRequestMethods.post.value:
        data = json.loads(request.body)

        created_user = User.objects.create_user(
            data.get('username'), data.get('password'), first_name=data.get('first_name'), avatar=data.get('avatar'))

        return JsonResponseCreated({'token': Token.objects.get(user=created_user).token})

    return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])


def detail(request: HttpRequest, user_id: int) -> HttpResponse:
    try:
        user_for_dealing = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    is_requesting_user_admin = check_if_requesting_user_admin(request)

    if is_requesting_user_admin:
        if request.method == HttpRequestMethods.delete.value:
            user_for_dealing.delete()

            return HttpResponseNoContent()

        return HttpResponseNotAllowed([HttpRequestMethods.delete.value])

    return HttpResponseNotFound()


def login(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.post.value:
        data = json.loads(request.body)
        authenticated_user = authenticate(username=data.get(
            'username'), password=data.get('password'))

        if authenticated_user:
            return JsonResponse({'token': Token.objects.get(user=authenticated_user).token})

        return HttpResponseBadRequest()

    return HttpResponseNotAllowed([HttpRequestMethods.post.value])
