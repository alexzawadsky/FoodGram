import csv

from django.core.management import BaseCommand

from reviews.models import Categories

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        if Categories.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('./static/data/category.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                data_load = Categories(
                    id=row['id'], name=row['name'], slug=row['slug'])
                data_load.save()

        print("Данные загружены")
