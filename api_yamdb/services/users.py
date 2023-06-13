from django.shortcuts import get_object_or_404
from users.models import User


def get_user_object(username: str) -> User:
    """Возврашает модель пользователя по username."""

    return get_object_or_404(User, username=username)


def get_all_users() -> User:
    """Возвращает список всех пользователей."""

    return User.objects.all()


def user_exists(username: str) -> bool:
    """Возвращает True при наличии пользователя в БД."""

    return User.objects.filter(username=username).exists()


def get_user_with_username_email(username: str, email: str) -> User:
    """Возвращает пользователя по username и email."""

    return User.objects.filter(username=username,
                               email=email).first()
