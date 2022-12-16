import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Загрузка ингредиентов из CSV в БД."""

    def handle(self, *args, **options):
        with open('ingredients.csv', newline='', encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for string in spamreader:
                ingredient = ' '.join(string)
                splited_ingredient = ingredient.split(',')

                if '"' not in ingredient:
                    name = splited_ingredient[0]
                    measurement_unit = splited_ingredient[1]
                elif ingredient.count('"') == 2:
                    end = ingredient[1:].index('"') + 1
                    name = ingredient[1:end]
                    measurement_unit = ingredient[end + 2:]
                else:
                    name_with = splited_ingredient[0][1:]
                    name = (
                        name_with[1:name_with.index('"')] +
                        name_with[name_with.index('"') + 1:len(name_with) - 2]
                    )
                    measurement_unit = splited_ingredient[1]

                if not Ingredient.objects.filter(
                    name=name
                ).exists():
                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
