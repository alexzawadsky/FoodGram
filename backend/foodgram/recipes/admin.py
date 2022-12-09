from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Subscription, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов в рецепте."""

    list_display = ('pk', 'ingredient', 'recipe', 'amount',)
    search_fields = ('ingredient', 'recipe')
    list_filter = ('ingredient', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = ('pk', 'name', 'author', 'cooking_time', 'pub_date',)
    search_fields = ('name', 'author',)
    list_filter = ('author', 'cooking_time', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('pk', 'author', 'recipe',)
    search_fields = ('author', 'recipe',)
    list_filter = ('author', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка подписок."""

    list_display = ('pk', 'user', 'author',)
    search_fields = ('author', 'user',)
    list_filter = ('author', 'user',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('pk', 'author', 'recipe',)
    search_fields = ('author', 'recipe',)
    list_filter = ('author', 'recipe',)
    empty_value_display = '-пусто-'
