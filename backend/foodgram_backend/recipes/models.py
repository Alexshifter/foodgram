from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from .constants import LEN_LIMIT, MIN_VALUE_AMOUNT, MIN_VALUE_COOK_TIME


class Ingredient(models.Model):

    """Модель Ингредиента."""

    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        ordering = ['id']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'Ингредиент {self.name}'


class Tag(models.Model):

    """Модель тега."""

    name = models.CharField(unique=True, max_length=32)
    slug = models.SlugField(unique=True,
                            max_length=32,
                            validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$')])

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.name} со слагом {self.slug}'[:LEN_LIMIT]


class Recipe(models.Model):

    """Модель рецепта."""

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
        validators=[MinValueValidator(MIN_VALUE_COOK_TIME)]
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт {self.name} c описанием: {self.text}'[:LEN_LIMIT]


class IngredientInRecipe(models.Model):

    """Модель ингредиентов в рецепте."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_VALUE_AMOUNT)],
        default=MIN_VALUE_AMOUNT
    )

    class Meta:
        default_related_name = 'ingredients_in_recipe'
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient} для рецепта {self.recipe.name}'[:LEN_LIMIT]


class Favorite(models.Model):

    """Модель избранных рецептов пользователя."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий рецепт в избранное',
        default=None
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'favorite'
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'


class Shopping_cart(models.Model):

    """Модель корзины покупок пользователя."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий рецепт в список покупок',
        default=None
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'карта покупок'
        verbose_name_plural = 'Карты покупок'


class ShortLink(models.Model):

    """Модель коротких ссылок на рецепт."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='short_code_path',
        null=True, blank=True
    )
    short_code_path = models.CharField(max_length=4, blank=True)
    original_path = models.URLField(max_length=300)

    class Meta:
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    def __str__(self):
        return f'{self.short_code_path} -> {self.original_path}'[:LEN_LIMIT]
