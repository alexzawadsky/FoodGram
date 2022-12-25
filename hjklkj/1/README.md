# я устал, босс
![работай штука](https://github.com/Zizeka/foodgram-project-react/actions/workflows/main.yml/badge.svg)

приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


**[Продуктовый помощник](http://84.201.139.41/recipes)**


# Запуск проекта:

Клонировать проект:

```https://github.com/Zizeka/foodgram-project-react.git```

Cоздать и активировать виртуальное окружение:
   ```source env/bin/activate```
   ```python -m venv venv```


```scp docker-compose.yml <username>@<host>:/home/<username>/```

```scp nginx.conf <username>@<host>:/home/<username>/```

```scp .env <username>@<host>:/home/<username>/```

Установите docker и docker-compose:
```sudo apt install docker.io``` 

```sudo apt install docker-compose```

Соберите контейнер и выполните миграции:
```sudo docker-compose up -d --build```

```sudo docker-compose exec backend python manage.py migrate```

Создайте суперюзера и соберите статику:

```sudo docker-compose exec backend python manage.py createsuperuser```

```sudo docker-compose exec backend python manage.py collectstatic --no-input```


Данные для проверки работы приложения: Суперпользователь:

email: ya@ya.ru

password: adminzizeka

ну допустим кря кря 

