import random
import string


from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.fields import Base64ImageField
from api.users.serializers import NewUserGetSerializer
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingСart, ShortLink, Tag)


class TagSerializer(serializers.ModelSerializer):

    """Сериалилзатор тегов."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class IngredientSerializer(serializers.ModelSerializer):

    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientInRecipeGetSerializer(serializers.ModelSerializer):

    """Сериализатор получения ингредиентов, используемых в рецепте."""

    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.IntegerField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngredientInRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientInRecipeCreateSerializer(serializers.Serializer):

    """Сериализатор ингрендиентов в рецепте при его создании."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ['id', 'amount']


class RecipeCreateSerializer(serializers.ModelSerializer):

    """Сериализатор создания рецепта."""

    image = Base64ImageField(required=True)
    name = serializers.CharField(required=True, max_length=256)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    author = NewUserGetSerializer(read_only=True)
    ingredients = IngredientInRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time', 'author']

    def validate(self, initial_data):
        ingredients = initial_data.get('ingredients')
        tags = initial_data.get('tags')
        if not ingredients:
            raise ValidationError('Список ингредиентов пуст.')
        if not tags:
            raise ValidationError('Список тегов пуст.')
        if len(tags) != len(set(tags)):
            raise ValidationError('Повторяющиеся теги не допускаются.')
        ingredients_id = set()
        for ingredient in ingredients:
            ingredients_id.add(ingredient.get('id'))
        if len(ingredients) != len(ingredients_id):
            raise ValidationError('Повторяющиеся ингредиенты не допускаются')
        return initial_data

    def create_update_ingredients(self, ingredients, recipe):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_instance = IngredientInRecipe(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )
            ingredient_list.append(ingredient_instance)
        IngredientInRecipe.objects.bulk_create(ingredient_list)
        return recipe

    def create(self, validated_data):

        """Переопределение create() для вложенных сериализаторов."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_update_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):

        """Переопределение update() для вложенных сериализаторов."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        if ingredients:
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            instance = self.create_update_ingredients(ingredients, instance)
            super().update(instance, validated_data)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, value):

        """Переопределение to_representation() для правильного response."""

        serializer = RecipeGetSerializer(value)
        return serializer.data


class RecipeGetSerializer(serializers.ModelSerializer):

    """Сериализатор получения рецепта."""

    image = Base64ImageField(required=True)
    name = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)
    author = NewUserGetSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientInRecipeGetSerializer(
        many=True,
        source='ingredients_in_recipe',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(default=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'ingredients', 'tags', 'image', 'name', 'text',
            'cooking_time', 'author', 'is_in_shopping_cart', 'is_favorited'
        ]

    def get_boolean_value_field(self, obj, Model):

        """Получение значения поля для is_favorited и shopping_cart."""

        request = self.context.get('request')
        if request:
            current_user = request.user
            if not current_user.is_anonymous:
                return Model.objects.filter(recipe=obj.id,
                                            user=request.user).exists()
        return False

    def get_is_favorited(self, obj):

        """Рецепты в избранном у пользователя."""

        return self.get_boolean_value_field(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):

        """Рецепты в корзине у корзине у пользователя."""

        return self.get_boolean_value_field(obj, ShoppingСart)


class FavoriteSerializer(serializers.ModelSerializer):

    """Сериализатор избранных рецептов."""

    class Meta:
        model = Favorite
        fields = ['recipe', 'user', ]

    def validate(self, initial_data):
        recipe = initial_data.get('recipe')
        request = self.context.get('request')
        obj = Favorite.objects.filter(recipe=recipe.id,
                                      user=request.user.id)
        if obj.exists():
            raise ValidationError(
                'Рецепт уже находится в избранном данного пользователя.')
        return initial_data

    def to_representation(self, instance):

        """Вывод короткого представления рецепта."""

        serializer = ShortRecipeGetSerializer(instance.recipe)
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):

    """Сериализатор корзины покупок."""

    class Meta:
        model = ShoppingСart
        fields = ('recipe', 'user',)

    def validate(self, initial_data):
        recipe = initial_data.get('recipe')
        request = self.context.get('request')
        obj = ShoppingСart.objects.filter(
            recipe=recipe.id,
            user=request.user.id
        )
        if obj.exists():
            raise ValidationError(
                'Рецепт уже находится в списке покупок данного пользователя.'
            )
        return initial_data

    def to_representation(self, instance):
        serializer = ShortRecipeGetSerializer(instance.recipe)
        return serializer.data


class ShortRecipeGetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'image', 'cooking_time']
        model = Recipe


class ShortLinkSerializer(serializers.ModelSerializer):

    """Сериализатор создания коротких ссылок на рецепт."""

    short_link = serializers.SerializerMethodField(
        method_name='get_short_link_in_response'
    )

    class Meta:
        model = ShortLink
        fields = ('short_link',)
        extra_kwargs = {
            'short-link': {'source': 'short_link'},
        }

    def get_fields(self):
        fields = super().get_fields()
        fields["short-link"] = fields.pop("short_link")
        return fields

    @classmethod
    def create_short_url(self, obj, request):

        """Создание короткой ссылки на рецепт."""

        symbols = string.digits + string.ascii_lowercase + \
            string.ascii_uppercase
        short_code_path = ''.join(random.choice(symbols) for i in range(4))
        obj.short_code_path = short_code_path
        obj.save()
        return short_code_path

    def get_short_link_in_response(self, obj):

        """Получение адреса с короткой ссылкой в response."""

        request = self.context.get('request')
        original_path = f'/recipes/{obj.id}'
        obj, created = ShortLink.objects.get_or_create(
            recipe=obj,
            original_path=original_path)
        if not obj.short_code_path or created:
            self.create_short_url(obj, request)
        short_absolute_uri = request.build_absolute_uri(
            f'/s/{obj.short_code_path}/'
        )
        return short_absolute_uri
