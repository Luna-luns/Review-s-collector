from api.filters import TitleFilter
from api.permissions import (IsAdminUser, IsAdminUserOrReadOnly,
                             IsAuthenticatedForCreateOrReadOnly,
                             IsModeratorOrAuthor)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitlePostSerializer, TitleSerializer,
                             TokenSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review, Title
from services import (categories, comments, genres, mails, reviews, titles,
                      users)
from users.serializers import (AdminUserSerializer, UserSerializer,
                               UserSignUpSerializer)


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """Создаёт, удаляет объект и
    возвращает список объектов.
    """

    pass


class CategoryViewSet(CreateRetrieveListViewSet):
    """Обрабатывает категории произведений и
    делает поиск по названию категории.
    """

    queryset = categories.get_all_categories()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateRetrieveListViewSet):
    """Обрабатывает жанры произведений и
    делает поиск по названию жанра.
    """

    queryset = genres.get_all_genres()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает пользователей,
    редактирует частичную информацию личного профиля.
    """

    queryset = users.get_all_users()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        if not partial:
            raise MethodNotAllowed(request.method)
        return super(UserViewSet, self).update(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,))
    def self_information(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data, status=HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывает произведения."""

    queryset = titles.get_all_titles()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработка отзывов."""

    queryset = reviews.get_all_reviews()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedForCreateOrReadOnly,
                          IsModeratorOrAuthor)

    def perform_create(self, serializer):
        title_id = serializer.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title,
                        author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Обработка комментариев."""

    queryset = comments.get_all_comments()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedForCreateOrReadOnly,
                          IsModeratorOrAuthor)

    def perform_create(self, serializer):
        review_id = serializer.context.get('view').kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review,
                        author=self.request.user)


class SignUpView(APIView):
    """Обрабатывает регистрацию пользователя, отправляя ему код."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        user = users.get_user_with_username_email(username=username,
                                                  email=email)
        if user:
            mails.create_confirmation_code_and_send_email(username, email)
            return Response(
                {"username": username,
                 "email": email},
                status=HTTP_200_OK)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            mails.create_confirmation_code_and_send_email(
                serializer.data.get('username'),
                email)
            return Response(
                serializer.data, status=HTTP_200_OK)


class TokenView(APIView):
    """Обрабатывает получения токена, проверяя confirmation_code."""

    permission_classes = (AllowAny,)

    def post(self, request) -> Response:
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = users.get_user_object(request.data['username'])
            if default_token_generator.check_token(
                user=user,
               token=request.data['confirmation_code']):
                token = AccessToken.for_user(user)

                return Response(
                    {'token': str(token)}, status=HTTP_200_OK)
            return Response(
                {'confirmation_code': 'Некорректный код подтверждения'},
                status=HTTP_400_BAD_REQUEST)
