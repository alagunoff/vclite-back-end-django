from typing import TypedDict, Literal


class HttpRequestMethods(TypedDict):
    get: Literal['GET']
    post: Literal['POST']
    delete: Literal['DELETE']


HTTP_REQUEST_METHODS: HttpRequestMethods = {
    'get': 'GET',
    'post': 'POST',
    'delete': 'DELETE',
}
