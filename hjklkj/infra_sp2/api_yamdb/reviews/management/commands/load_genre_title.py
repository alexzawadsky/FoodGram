import csv

from django.core.management import BaseCommand

from reviews.models import Genres, Title

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        print("Загрузка данных")

        with open('./static/data/genre_title.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                if row['title_id'] != '':
                    title = Title.objects.get(
                        pk=row['title_id']
                    )
                if row['genre_id'] != '':
                    genre = Genres.objects.get(
                        pk=row['genre_id']
                    )
                title.genre.add(genre)

        print("Данные загружены")
