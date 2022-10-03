from typing import Any


def map_user_to_dict(user: Any) -> dict[str, int | str | bool]:
    user_dictionary: dict[str, int | str | bool] = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'avatar': user.avatar,
        'creation_date': user.creation_date,
        'is_admin': user.is_admin,
    }

    if user.last_name:
        user_dictionary['last_name'] = user.last_name

    return user_dictionary
