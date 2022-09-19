import base64
from typing import Any
from django.conf import settings


def get_avatar_directory_path(instance: Any, filename: str) -> str:
    return f'users/{instance.username}/{filename}'


def map_user_to_dict(user: Any) -> dict[str, str]:
    user_dict: dict[str, str] = {}
    user_dict['username'] = user.username
    user_dict['first_name'] = user.first_name

    if user.last_name:
        user_dict['last_name'] = user.last_name

    with open(f'{settings.MEDIA_ROOT}/{user.avatar}', 'rb') as avatar:
        user_dict['avatar'] = base64.b64encode(
            avatar.read()).decode('utf-8')

    user_dict['creation_date'] = user.creation_date
    user_dict['is_admin'] = user.is_admin

    return user_dict
