from reviews.models import Review


def get_all_reviews() -> Review:
    """Возвращает список всех ревью."""
    return Review.objects.all()
