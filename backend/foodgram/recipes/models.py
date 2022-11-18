from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тега',
    )
    slug = models.SlugField(
        unique=True,
    )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    amount = models.PositiveSmallIntegerField()
    measurement_unit = models.CharField(
        max_length=50,
    )


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    ingredient = models.ManyToManyField(
        'Ingredient',
        related_name='ingredients'
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='tags'
    )
