from django.db import models

from users.models import User


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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Еденица измерения ингредиента',
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.ingredient.name


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
        RecipeIngredient,
        related_name='recipes',
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    author = models.ForeignKey(
        User,
        related_name='shopping_lists',
        on_delete=models.CASCADE,
    )
    recipe = models.ManyToManyField(
        'Recipe',
        related_name='shopping_lists',
    )

    def __str__(self):
        return self.author.username


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        related_name='subscribed',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='subscribing',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.author.username


class Favorite(models.Model):
    author = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ManyToManyField(
        'Recipe',
        related_name='favorites',
    )

    def __str__(self):
        return self.author.username
