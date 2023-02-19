from django.shortcuts import get_object_or_404
from djoser import serializers as djserializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Subscription, Tag)
from users.models import User


class CustomUserSerializer(djserializers.UserSerializer):
    """Сериализатор модели User"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=obj).exists()

        return False


class SubscriptionOrFavoriteRecipeSerializer(serializers.ModelSerializer):
    """Дополнительный сериализатор для рецепта."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image',)


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingList
        fields = ('id', 'author', 'recipe',)

    def validate_recipe(self, value):
        if ShoppingList.objects.filter(
            author=self.context['request'].user,
            recipe=value
        ).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок',
            )

        return value

    def to_representation(self, favorite):
        serializer = SubscriptionOrFavoriteRecipeSerializer(
            favorite.recipe, context=self.context)

        return serializer.data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки."""

    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    email = serializers.ReadOnlyField(source='author.email')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'id', 'email', 'username', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes_count', 'recipes',
        )

    def validate_author(self, author):
        user = self.context.get('request').user
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя'
            )
        return author

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.author)

        recipes_limit_param = (
            self.context.get('request').query_params.get('recipes_limit')
        )
        if recipes_limit_param is not None and recipes_limit_param.isdigit():
            recipes_limit = int(recipes_limit_param)
            recipes = Recipe.objects.filter(author=obj.author)[:recipes_limit]

        serializer = SubscriptionOrFavoriteRecipeSerializer(
            instance=recipes, many=True)

        return serializer.data

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, subscription):
        serializer = SubscriptionSerializer(
            subscription, context=self.context)

        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('id', 'author', 'recipe',)

    def validate_recipe(self, value):
        if Favorite.objects.filter(
            author=self.context['request'].user,
            recipe=value
        ).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже есть в избранном',
            )

        return value

    def to_representation(self, favorite):
        serializer = SubscriptionOrFavoriteRecipeSerializer(
            favorite.recipe, context=self.context)

        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для связи рецепта и ингредиентов."""

    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField(required=True)
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания или редактирования рецепта."""

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'ingredients', 'author',
            'image', 'text', 'cooking_time', 'tags',
        )

    def validate_ingredients(self, value):
        ingredients = []

        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']

            if not Ingredient.objects.filter(
                id=ingredient_id,
            ).exists():
                raise serializers.ValidationError(
                    'Нет такого ингредиента.')
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    'Нельзя добавлять ингредиенты с кол-вом меньше 1.'
                )
            if ingredient_id in ingredients:
                raise serializers.ValidationError(
                    'Нельзя добавлять несколько одинаковых ингредиентов.')

            ingredients.append(ingredient_id)

        return value

    def to_representation(self, recipe):
        serializer = RecipeSerializer(recipe, context=self.context)

        return serializer.data

    def creating_ingredients(self, recipe, ingredients):
        ingredients_for_create = [RecipeIngredient(
            recipe=recipe,
            ingredient=get_object_or_404(
                Ingredient,
                id=ingredient['ingredient']['id']
            ),
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        RecipeIngredient.objects.bulk_create(ingredients_for_create)

        created_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        for ingredient_created in created_ingredients:
            recipe.ingredients.add(ingredient_created)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            recipe.tags.add(tag)

        self.creating_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()

        RecipeIngredient.objects.filter(recipe=instance).delete()

        self.creating_ingredients(instance, ingredients)

        return instance


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'tags', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

    def exists_validate(self, obj=None, model_class=None):
        user = self.context['request'].user

        if user.is_authenticated:
            return model_class.objects.filter(author=user, recipe=obj).exists()

        return False

    def get_is_favorited(self, obj):
        return self.exists_validate(obj=obj, model_class=Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.exists_validate(obj=obj, model_class=ShoppingList)


class CustomUserCreateSerializer(djserializers.UserCreateSerializer):
    """Кастомный сериализатор создания модели User."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password',)
        read_only_fields = ('id',)
