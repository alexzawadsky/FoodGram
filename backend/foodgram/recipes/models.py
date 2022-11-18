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
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Еденица измерения ингредиента',
    )


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        related_name='ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()


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
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        related_name='recipe_ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
    )


class ShoppingList(models.Model):
    author = models.ForeignKey(
        User,
        related_name='shopping_list',
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='recipes',
    )


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
    )
    user = models.ForeignKey(
        User,
        related_name='user',
    )


class Favorite(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='recipes',
    )
