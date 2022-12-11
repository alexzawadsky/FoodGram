from django.conf.urls import include
from django.urls import path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingListViewSet, SubscriptionViewSet,
                    TagViewSet, get_shopping_list)

app_name = 'api'


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path(
        'recipes/<int:pk>/shopping_cart/', ShoppingListViewSet.as_view(),
        name='shopping_cart'),
    path(
        'recipes/download_shopping_cart/', get_shopping_list,
        name='download_shopping_cart'),
    path(
        'users/subscriptions/', SubscriptionViewSet.as_view(),
        name='subscriptions'),
    path(
        'users/<int:pk>/subscribe/', SubscriptionViewSet.as_view(),
        name='subscribe'),
    path(
        'recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(),
        name='favorite'),
    path('', include(router.urls)),
    path(
        'users/me/', CustomUserViewSet.as_view({'get': 'me'}),
        name='me'),
    path(
        'users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}),
        name='users_detail'),
    path(
        'users/set_password/',
        CustomUserViewSet.as_view({'post': 'set_password'}),
        name='set_password'),
    path(
        'users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users'),
    path('auth/', include('djoser.urls.authtoken')),
]
