from enum import Enum


class HttpRequestMethods(Enum):
    get = 'GET'
    post = 'POST'
    delete = 'DELETE'
    put = 'PUT'


class ResponseMessages(Enum):
    success = 'success'
    credentials_are_required = 'Credentials are required'
    there_is_no_such_user = 'There is no such user'
    there_is_no_such_tag = 'There is no such tag'
