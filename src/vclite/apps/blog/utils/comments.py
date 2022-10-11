from typing import Any

from ..models.comment import Comment


def create_comment(data: dict[str, Any], post_id: int) -> Comment:
    created_comment = Comment.objects.create(
        comment=data.get('comment'), post_id=post_id)

    return created_comment


def map_comment_to_dict(comment: Any) -> dict[str, int | str]:
    return {
        'id': comment.id,
        'comment': comment.comment
    }
