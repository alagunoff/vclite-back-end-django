import base64
from typing import Any
from django.conf import settings


def get_avatar_directory_path(instance: Any, filename: str) -> str:
    return f'users/{instance.username}/{filename}'


def map_user_to_dict(user: Any) -> dict[str, str]:
    user_dictionary: dict[str, str] = {
        'username': user.username,
        'first_name': user.first_name,
        'creation_date': user.creation_date,
        'is_admin': user.is_admin,
    }

    if user.last_name:
        user_dictionary['last_name'] = user.last_name

    with open(f'{settings.MEDIA_ROOT}/{user.avatar}', 'rb') as avatar:
        user_dictionary['avatar'] = base64.b64encode(
            avatar.read()).decode('utf-8')

    return user_dictionary
