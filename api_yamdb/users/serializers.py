from rest_framework import serializers
from users.models import User

from api_yamdb.settings import RESERVED_NAME


class StandartUsernameValidateSerializer:
    """Проверяет поле username на различие с RESERVED_NAME."""

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(
                'Запрещено использовать зарезервированные имена!')
        return value


class AdminUserSerializer(StandartUsernameValidateSerializer,
                          serializers.ModelSerializer):
    """Обработчик пользователей для администраторов."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserSerializer(StandartUsernameValidateSerializer,
                     serializers.ModelSerializer):
    """Обработчик пользователя."""

    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class UserSignUpSerializer(StandartUsernameValidateSerializer,
                           serializers.ModelSerializer):
    """Обработчик пользователя при регистрации."""

    class Meta:
        model = User
        fields = ('username', 'email',)
