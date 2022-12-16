from rest_framework import filters


class IngredientNameFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name').lower()

        if name is None:
            return queryset

        return queryset.filter(name__startswith=name)
