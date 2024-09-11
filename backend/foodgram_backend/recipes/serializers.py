from rest_framework import serializers
from users.serializers import Base64ImageField, NewUserGetSerializer
from .models import (Tag, Recipe, Ingredient, IngredientInRecipe, 
                     Favorite, ShortLink, Shopping_cart)
from rest_framework.exceptions import ValidationError
import string, random

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
 
class IngredientInRecipeGetSerializer(serializers.Serializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields=['id', 'name', 'measurement_unit', 'amount']

class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    name = serializers.CharField(required=True, max_length=256)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    author = NewUserGetSerializer(read_only=True)
    ingredients = IngredientInRecipeGetSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=True)

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'image', 'name',
                   'text', 'cooking_time', 'author']
     
    def validate(self, initial_data):
        ingredients = initial_data.get('ingredients')
        tags = initial_data.get('tags')
        if not ingredients:
            raise ValidationError(
                    ('Список ингредиентов пуст!'))
        if not tags:
            raise ValidationError('Список тэгов пуст!')
        if len(tags)!=len(set(tags)):
            raise ValidationError('Повторяющиеся тэги не допускаются')
        ingredients_id = set()
        for ingredient in ingredients:
            ingredients_id.add(ingredient.get('id'))
        if len(ingredients)!=len(ingredients_id):
            raise ValidationError('Повторяющиеся ингредиенты не допускаются')
        return initial_data

    def create_update_ingredients(self, ingredients, recipe):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_instance = IngredientInRecipe(recipe=recipe,
                                                     amount=ingredient.get('amount'),
                                                     ingredient=ingredient.get('id'))
            ingredient_list.append(ingredient_instance)
        IngredientInRecipe.objects.bulk_create(ingredient_list)
        return recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        print(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_instance = IngredientInRecipe(recipe=recipe,
                                                     amount=ingredient.get('amount'),
                                                     ingredient=ingredient.get('id'))
            ingredient_list.append(ingredient_instance)
        IngredientInRecipe.objects.bulk_create(ingredient_list)
        return recipe

    def update(self, instance, validated_data):
        
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        if ingredients:
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            instance = self.create_update_ingredients(ingredients, instance)
        if tags:
            instance.tags.set(tags)

        instance.image = validated_data.get(
            'image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()
        return instance

    def to_representation(self, value):

        serializer = RecipeGetSerializer(value)
        return serializer.data


class RecipeGetSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    name = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)
    author = NewUserGetSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientInRecipeGetSerializer(many=True, source='ingredients_in_recipe')
    is_favorited = serializers.SerializerMethodField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(default=False)
    
    class Meta:
        model = Recipe
        fields = ['id', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author', 'is_in_shopping_cart', 'is_favorited']

    def get_is_favorited(self, obj):
        get_request = self.context.get('request')
        if get_request:
            current_user = get_request.user
            if not current_user.is_anonymous:
                return Favorite.objects.filter(recipe = obj.id, user = get_request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        get_request = self.context.get('request')
        if get_request:
            current_user = get_request.user
            if not current_user.is_anonymous:
                return Shopping_cart.objects.filter(recipe = obj.id, user = get_request.user).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', 'user',)
    
    def validate(self, initial_data):
        recipe = initial_data.get('recipe')
        request = self.context.get('request')
        obj = Favorite.objects.filter(recipe=recipe.id, user = request.user.id)
        if obj.exists():
            raise ValidationError('Рецепт уже находится в избранном данного пользователя!')
        return initial_data
    
    def to_representation(self, instance):
        serializer = ShortRecipeGetSerializer(instance.recipe)

        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_cart
        fields = ('recipe', 'user',)

    def validate(self, initial_data):
        recipe = initial_data.get('recipe')
        request = self.context.get('request')
        obj = Shopping_cart.objects.filter(recipe=recipe.id, user = request.user.id)
        if obj.exists():
            raise ValidationError('Рецепт уже находится в списке покупок данного пользователя!')
        return initial_data

    def to_representation(self, instance):
        serializer = ShortRecipeGetSerializer(instance.recipe)
        return serializer.data



class ShortRecipeGetSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id', 'name','image', 'cooking_time')
        model = Recipe

class ShortLinkSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField(method_name='get_short_link_in_response')
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
        symbols = string.digits + string.ascii_lowercase + string.ascii_uppercase
        short_code_path = ''.join(random.choice(symbols) for i in range(4))
        obj.short_code_path = short_code_path
        obj.save()
        return short_code_path

    def get_short_link_in_response(self, obj): 
        request = self.context.get('request')
        original_path = f'/api/recipes/{obj.id}/'
        obj_with_paths, created = ShortLink.objects.get_or_create(recipe=obj, original_path=original_path)
        if not obj_with_paths.short_code_path or created:
            self.create_short_url(obj_with_paths, request)
        short_absolute_uri = request.build_absolute_uri(f'/s/{obj_with_paths.short_code_path}/')
        return short_absolute_uri
      
