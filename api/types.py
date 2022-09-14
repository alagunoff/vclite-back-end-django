from enum import Enum


class HttpRequestMethods(Enum):
    get = 'GET'
    post = 'POST'
    delete = 'DELETE'
    put = 'PUT'
    patch = 'PATCH'


class ResponseMessages(Enum):
    success = 'success'
    credentials_are_required = 'Credentials are required'
