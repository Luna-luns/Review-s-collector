import csv
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment,
                            Genre, Review, Title)
from users.models import User


def validate_required_fields(row: dict) -> bool:
    """"Проверяет наличие обязательных полей."""

    ignore_fields: list = [
        'description',
        'role',
        'bio',
        'first_name',
        'last_name',
        'author',
        'pub_date'
    ]

    for key, value in row.items():
        if not value and key not in ignore_fields:
            return False

    return True


def upload_users():
    """Загружает пользователей."""

    with open('static/data/users.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            user = User()
            user.id = row['id']
            user.username = row['username']
            user.email = row['email']
            user.role = row['role']
            user.bio = row['bio']
            user.first_name = row['first_name']
            user.last_name = row['last_name']

            user.save()


def upload_category():
    """Загружает категории."""

    with open('static/data/category.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            category = Category()
            category.id = row['id']
            category.name = row['name']
            category.slug = row['slug']

            category.save()


def upload_genre():
    """Загружает жанры."""

    with open('static/data/genre.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            genre = Genre()
            genre.id = row['id']
            genre.name = row['name']
            genre.slug = row['slug']

            genre.save()


def upload_titles():
    """Загружает произведения."""

    with open('static/data/titles.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            title = Title()
            title.id = row['id']
            title.name = row['name']
            title.year = row['year']
            title.category = Category.objects.get(id=row['category'])

            title.save()


def upload_genre_title():
    """Загружает промежуточную таблицу с жанрами и произведениями."""

    with open('static/data/genre_title.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])

            title.genre.add(genre)
            title.save()


def upload_review():
    """Загружает отзывы."""

    with open('static/data/review.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            review = Review()
            review.id = row['id']
            review.title = Title.objects.get(id=row['title_id'])
            review.text = row['text']
            review.author = User.objects.get(id=row['author'])
            review.score = row['score']
            review.pub_date = row['pub_date']

            review.save()


def upload_comments():
    """Загружает комментарии."""

    with open('static/data/comments.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if not validate_required_fields(row):
                continue

            comment = Comment()
            comment.id = row['id']
            comment.review = Review.objects.get(id=row['review_id'])
            comment.text = row['text']
            comment.author = User.objects.get(id=row['author'])
            comment.pub_date = row['pub_date']

            comment.save()


class Command(BaseCommand):

    def handle(self):
        upload_users()
        upload_category()
        upload_genre()
        upload_titles()
        upload_genre_title()
        upload_review()
        upload_comments()
