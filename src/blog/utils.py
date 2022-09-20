from typing import Any


def map_tag_to_dict(tag: Any) -> dict[str, int | str]:
    return {
        'id': tag.id,
        'tag': tag.tag
    }


def map_category_to_dict(category: Any) -> dict[str, Any]:
    return {
        'id': category.id,
        'category': category.category,
        'subcategories': list(map(map_category_to_dict, category.subcategories.all()))
    }
