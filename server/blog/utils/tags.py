from typing import Any


def map_tag_to_dict(tag: Any) -> dict[str, int | str]:
    return {
        'id': tag.id,
        'tag': tag.tag
    }
