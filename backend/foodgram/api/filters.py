import django_filters as djfilters
# from rest_framework import filters
from recipes.models import Tag, Recipe


# class IngredientNameFilter(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         name = request.query_params.get('name').lower()

#         if name is None:
#             return queryset

#         return queryset.filter(name__startswith=name)


class RecipeFilter(djfilters.FilterSet):
    tags = djfilters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = djfilters.NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_list = djfilters.NumberFilter(
        method='get_is_in_shopping_list'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_list')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites__user=user)

        return Recipe.objects.all()

    def get_is_in_shopping_list(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(purchases__user=user)

        return Recipe.objects.all()
