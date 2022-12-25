from django.contrib import admin
from django.contrib.admin import display

from .models import (Favorite, Ingredient, IngredientList, Recipe,
                     ShoppingList, Tag)

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(IngredientList)
admin.site.register(ShoppingList)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )

    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'quantity_favorites'
    )

    search_fields = ('name', 'author',)
    list_filter = ('name', 'tags', 'author',)
    empty_value_display = '-пусто-'

    @display(description='Количество в избранных')
    def quantity_favorites(self, obj):
        return obj.favorites.count()
