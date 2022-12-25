import csv

from django.core.management import BaseCommand

from reviews.models import Categories, Title

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        if Title.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('./static/data/titles.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                titles = Title.objects.create()
                titles.id = row['id']
                titles.name = row['name']
                if row['year'] != '':
                    titles.year = row['year']
                else:
                    titles.year = '9999'
                if row['category'] != '':
                    titles.category = Categories.objects.get(
                        pk=row['category'])
                titles.save()

        print("Данные загружены")
