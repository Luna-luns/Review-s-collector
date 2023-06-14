from rest_framework import serializers
from rest_framework.exceptions import NotFound
from reviews.models import Category, Comment, Genre, Review, Title
from services import categories, genres, users
from users.serializers import StandartUsernameValidateSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Обработчик категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Обработчик жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Обработчик произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    """Обработчик создания произведений."""

    category = serializers.SlugRelatedField(
        queryset=categories.get_all_categories(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=genres.get_all_genres(),
        slug_field='slug',
        many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TokenSerializer(StandartUsernameValidateSerializer,
                      serializers.Serializer):
    """Обработчик получения токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate_username(self, value):
        if not users.user_exists(username=value):
            raise NotFound('Пользователь не найден!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Обработка отзыва, валидация рейтинга."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        max_value=10,
        min_value=0
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('author', 'title', 'pub_date',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context.get('view').kwargs.get('title_id')
        ).exists() and self.context.get('request').method == 'POST':
            raise serializers.ValidationError(
                'Вы можете создать только один отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Обработка комментария."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
