from rest_framework import serializers
from djoser import serializers as djserializers
from recipes.models import Ingredient, Tag, Subscription
from users.models import User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class CastomUserSerializer(djserializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        if user.is_authenticated:
            if Subscription.objects.filter(user=user, author=obj).exists():
                return True

        return False


class CastomUserCreateSerializer(djserializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password',)
        read_only_fields = ('id',)
