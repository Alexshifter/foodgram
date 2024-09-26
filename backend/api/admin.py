from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, ShortLink, Tag)
from users.models import Following, NewUser


class IngrInRecAdmin(admin.StackedInline):
    model = IngredientInRecipe
    extra = 0


class FollowingAdmin(admin.TabularInline):
    model = Following
    extra = 0
    fk_name = 'user'


@admin.register(NewUser)
class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'date_joined',)
    search_fields = ('email', 'username',)
    inlines = (FollowingAdmin,)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'image', 'published',
                    'text', 'get_tags', 'get_count_favorite')
    list_display_links = ('author', 'name')
    list_filter = [('tags', admin.RelatedFieldListFilter)]
    search_fields = ('author__username', 'name')
    inlines = (IngrInRecAdmin,)

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return [tag.get('name') for tag in obj.tags.values('name')]

    @admin.display(description='Число добавлений в избранное')
    def get_count_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'short_code_path', 'original_path')
    list_display_links = ('short_code_path',)


@admin.register(ShoppingCart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
