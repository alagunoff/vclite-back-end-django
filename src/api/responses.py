from django.http import HttpResponse, JsonResponse


class HttpResponseNoContent(HttpResponse):
    status_code = 204


class JsonResponseCreated(JsonResponse):
    status_code = 201
