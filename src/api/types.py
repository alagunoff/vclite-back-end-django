from enum import Enum


class HttpRequestMethods(Enum):
    get = 'GET'
    post = 'POST'
    delete = 'DELETE'
    put = 'PUT'
    patch = 'PATCH'
