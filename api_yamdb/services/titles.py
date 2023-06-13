from django.db.models import Avg
from reviews.models import Title


def get_all_titles() -> Title:
    """Возвращает список всех произведений c рейтингом."""

    return Title.objects.all().annotate(rating=Avg('reviews__score'))
