from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as django_filters
from djoser import views as djviews
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredient, Recipe, ShoppingList,
                            Subscription, Tag)
from .filters import IngredientNameFilter, RecipeFilter
from .mixins import ShoppingListFavoriteMixin
from .permissions import IsAdminOrReadOnly, IsOwner, IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShoppingListSerializer, SubscriptionCreateSerializer,
                          SubscriptionSerializer, TagSerializer)


class FavoriteViewSet(ShoppingListFavoriteMixin):
    queryset = Favorite.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = FavoriteSerializer


class ShoppingListViewSet(ShoppingListFavoriteMixin):
    queryset = ShoppingList.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = ShoppingListSerializer


@api_view(['GET'])
@permission_classes([IsOwner])
def get_shopping_list(request):
    author = request.user
    recipes = Recipe.objects.filter(
        shopping_lists__author=author
    )
    ingredients = recipes.values_list(
        'ingredients__ingredient__name',
        'ingredients__ingredient__measurement_unit'
    ).order_by('ingredients__ingredient__name')

    result = ingredients.annotate(
        amount=Sum('ingredients__amount')
    )

    shopping_cart = 'Список покупок:'
    for ingredient in result:
        shopping_cart += f'\n{ingredient[0]} — {ingredient[2]} {ingredient[1]}'
    shopping_cart += '\n\nСкачано с сайта FootGram'

    filename = f'{author.first_name} shopping cart.txt'
    response = HttpResponse(
        shopping_cart,
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)

    return response


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionCreateViewSet(APIView):
    permission_classes = (IsOwner,)

    def post(self, request, pk):
        if not Subscription.objects.filter(
                user=request.user, author__id=pk).exists():
            data = {
                'user': request.user.id,
                'author': pk
            }
            serializer = SubscriptionCreateSerializer(
                data=data,
                context={'request': request}
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subscription = Subscription.objects.filter(
            user=request.user, author__id=pk)

        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateUpdateSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientNameFilter,)


class CustomUserViewSet(djviews.UserViewSet):
    http_method_names = ['get', 'post', 'head']
