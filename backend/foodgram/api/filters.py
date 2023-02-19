from django_filters import rest_framework as django_filters
from rest_framework import filters

from recipes.models import Favorite, Recipe, ShoppingList, Tag


class IngredientNameFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')

        if name is None:
            return queryset

        return queryset.filter(name__startswith=name.lower())


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = django_filters.NumberFilter(
        method='favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='in_shopping_list'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def favorited(self, queryset, name, value):
        user = self.request.user

        if value == 1 and user.is_authenticated:
            favorites = Favorite.objects.filter(author=user)
            queryset = queryset.filter(favorites__in=favorites)

        return queryset

    def in_shopping_list(self, queryset, name, value):
        user = self.request.user

        if value == 1 and user.is_authenticated:
            shopping_list = ShoppingList.objects.filter(author=user)
            queryset = queryset.filter(shopping_lists__in=shopping_list)

        return queryset
