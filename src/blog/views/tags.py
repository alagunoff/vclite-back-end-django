# from django.http import HttpRequest, HttpResponse,JsonResponse, HttpResponseNotAllowed

# from api.types import HttpRequestMethods

# from ..models.tag import Tag

# def index(request:HttpRequest) -> HttpResponse:
#     if request.method == HttpRequestMethods.get.value:
#         return JsonResponse()

#     return HttpResponseNotAllowed([HttpRequestMethods.get.value, HttpRequestMethods.post.value])
