from django.contrib.auth.models import UserManager

from api_yamdb.settings import RESERVED_NAME


class CustomUserManager(UserManager):
    """Обработчик создания пользователей,
    проверющий наличие почты при создании.
    """

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required field')
        if username == RESERVED_NAME:
            raise ValueError(f'{RESERVED_NAME} is reserved name!')

        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):

        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)
