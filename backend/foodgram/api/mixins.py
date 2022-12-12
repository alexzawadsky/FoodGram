from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ShoppingListFavoriteMixin(APIView):
    """Миксин создания и удаления рецепта из избранного и списка покупок."""

    def post(self, request, pk):
        data = {
            'author': request.user.id,
            'recipe': pk
        }
        serializer = self.serializer_class(
            data=data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        obj = self.queryset.filter(author=request.user, recipe__id=pk)

        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
