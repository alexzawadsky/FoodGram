from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, ShoppingList, Subscription,
                     Tag, RecipeIngredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount',)
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'cooking_time',)
    search_fields = ('name',)
    list_filter = ('author', 'cooking_time',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author',)
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'user',)
    search_fields = ('author',)
    list_filter = ('author', 'user',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author',)
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'
