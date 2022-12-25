import csv

from django.core.management import BaseCommand

from reviews.models import Comments

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        if Comments.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('./static/data/comments.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                data_load = Comments(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=row['author'],
                    pub_date=row['pub_date']
                )
                data_load.save()

        print("Данные загружены")
