from reviews.models import Category


def get_all_categories() -> Category:
    """Возвращает список всех категорий."""

    return Category.objects.all()
