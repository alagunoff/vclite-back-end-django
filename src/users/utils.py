def get_avatar_directory_path(instance, filename: str) -> str:
    return f'users/{instance.username}/{filename}'
