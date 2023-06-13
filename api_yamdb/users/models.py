from django.db import models
from django.core.validators import RegexValidator
import re
from users.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )

    username = models.CharField(
        'Псевдоним',
        max_length=150, unique=True,
        validators=[
            RegexValidator(regex=re.compile(r"^[\w.@+-]+\Z"),
                           message='Проверьте правильность написания никнейма')
        ])
    email = models.EmailField(
        'Электронная почта',
        unique=True, max_length=254)
    bio = models.TextField(
        'Биография',
        blank=True)
    role = models.CharField(
        'Роль',
        max_length=256, choices=ROLES, default='user')
    first_name = models.CharField('Имя пользователя',
                                  max_length=150, blank=True)
    last_name = models.CharField('Фамилия пользователя',
                                 max_length=150, blank=True)

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return f'{self.username}: {self.role}'
