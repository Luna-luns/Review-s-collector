from reviews.models import Genre


def get_all_genres() -> Genre:
    """Возвращает список всех жанров."""

    return Genre.objects.all()
