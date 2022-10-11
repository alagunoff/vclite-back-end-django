from typing import Any


def map_category_to_dict(category: Any) -> dict[str, Any]:
    return {
        'id': category.id,
        'category': category.category,
        'subcategories': list(map(map_category_to_dict, category.subcategories.all()))
    }
