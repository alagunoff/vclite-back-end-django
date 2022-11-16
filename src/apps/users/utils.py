def get_user_avatar_path(user, filename: str) -> str:
    return f'users/{user.username}/{filename}'
