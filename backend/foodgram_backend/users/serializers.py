import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import NewUser, Following
from recipes.models import Recipe
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class NewUserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)
    class Meta:
        fields = (
            'email', 'username', 'first_name', 'last_name', 'id', 'is_subscribed', 'avatar'
        )

        model = NewUser
    def get_is_subscribed(self, obj):
        get_request = self.context.get('request')
        if get_request:
            current_user = get_request.user
            if not current_user.is_anonymous:
                return current_user.follower.filter(following = obj.id).exists()
        return False

class ShortRecipeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class NewUserWithRecipeGetSerializer(NewUserGetSerializer):

    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        fields =  ('email', 'username', 'first_name', 'last_name', 'id', 'is_subscribed', 'avatar', 'recipes','recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def get_recipes(self, obj):

        query_params_dict = self.context.get('request').query_params
        recipes = obj.recipes.all()
        if 'recipes_limit' in query_params_dict:
            recipes_limit_value = int(query_params_dict.get('recipes_limit'))
            recipes = recipes[:recipes_limit_value]
     
        serializer = ShortRecipeGetSerializer(recipes, read_only=True, many=True)

        return serializer.data


class NewUserCreateSerializer(UserCreateSerializer, SetPasswordSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    class Meta:
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password','id'
        )
        model = NewUser

class AvatarSerializer(serializers.ModelSerializer):
    avatar =  Base64ImageField(allow_null=True)

    class Meta:
        fields = (
  
            'avatar',
        )
        model = NewUser

class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', write_only=True,
        queryset=NewUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(slug_field= 'username', queryset=NewUser.objects.all())
    class Meta:
        model = Following
        fields = ('following', 'user',)

        validators = [
            UniqueTogetherValidator(
                queryset=Following.objects.all(),
                fields=('user', 'following'), message= 'Ошибка: вы уже подписаны на этого автора.'
            )
        ]

    def validate_following(self, author_recipes):
        current_user = self.context.get('request').user
        if current_user == author_recipes:
            raise serializers.ValidationError(
                'Ошибка: вы не можете подписаться сами на себя.'
            )
        return author_recipes

    def to_representation(self, instance):
        serializer = NewUserWithRecipeGetSerializer(instance.following, 
                                                    context = self.context)
        return serializer.data
