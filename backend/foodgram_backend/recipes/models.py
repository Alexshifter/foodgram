from typing import Iterable
from django.core.validators import MinValueValidator, RegexValidator
from django.conf import settings
from django.db import models
import string, random

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32)
    slug = models.SlugField(unique=True,
                            max_length=32,
                            validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$')])
    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=256,
                            unique=True,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', null=True,
                              default=None,
                              verbose_name='Изображение к рецепту')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    def __str__(self):
        return f'{self.name}'



class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        default_related_name = 'ingredients_in_recipe'
    
    def __str__(self):
        return f'{self.ingredient}'



class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь, добавляющий рецепт в избранное',
                               default=None)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'favorite'
   

class Shopping_cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь, добавляющий рецепт в список покупок',
                               default=None)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'shopping_cart'


class ShortLink(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='short_code_path', null=True, blank=True)
    short_code_path = models.CharField(max_length=4, blank=True)
    original_path = models.URLField(max_length=300)

    def __str__(self):
        return f'Редирект {self.short_code_path} -> {self.original_path}'
