from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate

from api.types import HttpRequestMethods
from api.utils import get_user_from_request
from api.responses import HttpResponseNoContent, JsonResponseCreated

from .models import User, Token
from .utils import map_user_to_dict


def index(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.get.value:
        user = get_user_from_request(request)

        if user:
            return JsonResponse(map_user_to_dict(user))
        else:
            return HttpResponseNotFound()
    if request.method == HttpRequestMethods.post.value:
        user = User.objects.create_user(
            request.POST.get('username'), request.POST.get('password'), request.POST.get('first_name'), avatar=request.FILES.get('avatar'))

        return JsonResponseCreated({'token': Token.objects.get(user=user).token})

    return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])


def detail(request: HttpRequest, user_id: int) -> HttpResponse:
    requesting_user = get_user_from_request(request)

    if requesting_user and requesting_user.is_admin:
        if request.method == HttpRequestMethods.delete.value:
            try:
                User.objects.get(id=user_id).delete()

                return HttpResponseNoContent()
            except User.DoesNotExist:
                return HttpResponseNotFound()

        return HttpResponseNotAllowed([HttpRequestMethods.delete.value])
    else:
        return HttpResponseNotFound()


def login(request: HttpRequest) -> HttpResponse:
    if request.method == HttpRequestMethods.post.value:
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))

        if user:
            return JsonResponse({'token': Token.objects.get(user=user).token})
        else:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed([HttpRequestMethods.post.value])
