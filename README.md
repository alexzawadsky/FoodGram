Ссылка: [foodgram.ru](http://130.193.51.107/recipes)
Логин: admin
Пароль: Admin11ddqd
Email: a@a.ru

## Foodgram «Продуктовый помощник»
##### На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Как запустить проект в Docker контейнерах:
- [x] 1) Скачать и настроить приложение Docker.
- [x] 2) Клонировать репозиторий и перейти в него в командной строке.

- [x] 3) Перейти в репозиторий infra/.

```
cd infra
```

- [x] 4) Создать файл .env:

```
touch .env
```

- [x] 5) Наполнить файл .env по шаблону:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY='your_secret_key' # ваш секретный ключ из настроек Django проекта
```

- [x] 6) Запустить сборку образа и запуск контейнера командой:

```
docker-compose up -d --build
```

- [x] 7) Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

- [x] 8) Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input 
```

- [x] 9) Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

- [x] 10) Загрузить ингредиенты в БД:

```
docker-compose exec web python manage.py load_ingredients
```

- [x] 11) Сайт будет доступен по адресу:

```
http://localhost/recipes/
```

## Технические особенности проекта:
- Взаимодействие с Frontend происходит через API.
- В папке data/ находятся файлы .csv и .json с ингредиентами.
- С помощью команды load_ingredients можно вызвать скрипт по заполнению БД ингредиентами из файла ingredients.csv.
- Чтобы поднять Frontend, Backend, Nginx и Postgresql необходимо воспользоваться Docker (папка infra/)
- По умолчанию используется БД Postgresql (при желании можно раскоментировать код с SQLite3 в настройках проекта)

## Используемые технологии:

- JS React
- Python
- Django
- Djangorestframework
- Djoser
- Docker
- Postgresql

## Автор:

Алексей Завадский
Студент факультета Бэкенд. Когорта №37.
Яндекс Практикум.
