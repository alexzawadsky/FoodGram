from django.conf.urls import include
from django.urls import path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import (CastomUserViewSet, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingListViewSet, SubscriptionViewSet,
                    TagViewSet, get_shopping_list)

app_name = 'api'


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('recipes/<int:pk>/shopping_cart/', ShoppingListViewSet.as_view()),
    path('recipes/download_shopping_cart/', get_shopping_list),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('users/<int:pk>/subscribe/', SubscriptionViewSet.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('', include(router.urls)),
    path('users/me/', CastomUserViewSet.as_view({'get': 'me'})),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/set_password/', CastomUserViewSet.as_view(
        {'post': 'set_password'})),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('auth/', include('djoser.urls.authtoken')),
]
