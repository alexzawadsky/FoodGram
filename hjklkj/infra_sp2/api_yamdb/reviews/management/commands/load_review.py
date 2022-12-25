import csv

from django.core.management import BaseCommand

from reviews.models import Review, User

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        if Review.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('./static/data/review.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                author = User.objects.get(pk=row['author'])
                data_load = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                data_load.save()

        print("Данные загружены")
