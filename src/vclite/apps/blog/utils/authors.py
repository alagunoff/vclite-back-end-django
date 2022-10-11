from typing import Any


def map_author_to_dict(author: Any) -> dict[str, int | str]:
    return {
        'id': author.id,
        'user_id': author.user.id,
        'description': author.description
    }
