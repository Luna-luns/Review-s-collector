# Yamdb

![Django-app workflow](https://github.com/Luna-luns/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Описание проекта:

Проект YaMDb собирает отзывы пользователей на произведения, позволяет ставить произведениям оценку и комментировать чужие отзывы.

Произведения делятся на категории, и на жанры. Список произведений, категорий и жанров может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Доступ к БД проекта осуществляется через Api.

Полный список запросов и эндпоинтов описан в документации ReDoc, доступна после запуска проекта по адресу:
```
http://127.0.0.1:8000/redoc/
```

### Как запустить проект на тестовом сервере:
Клонировать репозиторий, перейти в директорию с проектом.

```
git clone git@github.com:Luna-luns/Review-s-collector.git
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/source/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


### Примеры запросов к API:

Получение списка всех категорий:

```
http://127.0.0.1:8000/api/v1/categories/
```
Получение списка всех жанров:

```
http://127.0.0.1:8000/api/v1/genres/
```
Получение списка всех произведений:

```
http://127.0.0.1:8000/api/v1/titles/
```

## Шаблон наполнения env-файла:
Задайте переменные окружения в контейнере:
```
ENV <ключ> <значение> 
```
Например:
```
ENV DATABASE_NAME yamdb
ENV DATABASE_PORT 5432 
```

## Как запустить приложения в контейнерах:
```
docker-compose up
```

## Как перезапустить приложения в контейнерах:
```
docker-compose up -d --build 
```

## 🚀 Обо мне

Начинающий backend-разработчик на Python
- [@Елизавета Струнникова](https://github.com/Luna-luns)
  
## Обратная связь

Email: liza.strunnikova@yandex.ru<br>
Telegram: @l_lans
