from django.conf.urls import include
from django.urls import path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import CastomUserViewSet, IngredientViewSet, TagViewSet

app_name = 'api'


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', CastomUserViewSet.as_view({'get': 'me'})),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/set_password/', CastomUserViewSet.as_view(
        {'post': 'set_password'})),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('auth/', include('djoser.urls.authtoken')),
]
