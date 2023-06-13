from reviews.models import Comment


def get_all_comments() -> Comment:
    """Возвращает список всех комментариев."""

    return Comment.objects.all()
