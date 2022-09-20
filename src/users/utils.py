from typing import Any
from django.conf import settings

from shared.utils import encode_image_file_to_base64


def get_user_avatar_directory_path(instance: Any, filename: str) -> str:
    return f'users/{instance.username}/{filename}'


def map_user_to_dict(user: Any) -> dict[str, int | str | bool]:
    user_dictionary: dict[str, int | str | bool] = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'creation_date': user.creation_date,
        'is_admin': user.is_admin,
    }

    with open(f'{settings.MEDIA_ROOT}/{user.avatar}', 'rb') as avatar_file:
        user_dictionary['avatar'] = encode_image_file_to_base64(avatar_file)

    if user.last_name:
        user_dictionary['last_name'] = user.last_name

    return user_dictionary
