from django.http import HttpRequest

from users.models import User, Token


def get_user_from_request(request: HttpRequest) -> User | None:
    authorization_header = request.headers.get('Authorization')

    if authorization_header:
        if authorization_header.startswith('Token '):
            try:
                return Token.objects.get(token=authorization_header[6:]).user
            except Token.DoesNotExist:
                return None
    return None


def check_if_requester_admin(request: HttpRequest) -> bool:
    user = get_user_from_request(request)

    return bool(user and user.is_admin)
