from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from foodgram_backend.constants import (LEN_LIMIT, MIN_VALUE_AMOUNT,
                                        MIN_VALUE_COOK_TIME)


class Ingredient(models.Model):

    """Модель Ингредиента."""

    name = models.CharField(max_length=128,
                            verbose_name='название ингредиента')
    measurement_unit = models.CharField(max_length=64,
                                        verbose_name='Единица измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'[:LEN_LIMIT]


class Tag(models.Model):

    """Модель тега."""

    name = models.CharField(unique=True, max_length=32,
                            verbose_name='Название тега')
    slug = models.SlugField(unique=True,
                            max_length=32,
                            verbose_name='Слаг',
                            validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$')])

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'[:LEN_LIMIT]


class Recipe(models.Model):

    """Модель рецепта."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', null=True,
                              default=None,
                              verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(MIN_VALUE_COOK_TIME)]
    )
    published = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-published']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}: {self.text}'[:LEN_LIMIT]


class IngredientInRecipe(models.Model):

    """Модель ингредиентов в рецепте."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_VALUE_AMOUNT)],
        default=MIN_VALUE_AMOUNT,
        verbose_name='Количество'
    )

    class Meta:

        """Ограничение повторного ингредиента в рецепте."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='%(app_label)s _ %(class)s _unique_relationships',
            )
        ]
        default_related_name = 'ingredients_in_recipe'
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'

    def __str__(self):
        return f'{self.ingredient} для рецепта {self.recipe.name}'[:LEN_LIMIT]


class Favorite(models.Model):

    """Модель избранных рецептов пользователя."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=None
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:

        """Ограничение повторного добавления рецепта в избранное."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s _ %(class)s _unique_relationships',
            )]

        default_related_name = 'favorite'
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'рецепт {self.recipe} в избранном у {self.user}'[:LEN_LIMIT]


class ShoppingCart(models.Model):

    """Модель корзины покупок пользователя."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=None
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт в списке покупок')

    class Meta:

        """Ограничение повторного добавления рецепта в корзину."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s _ %(class)s _unique_relationships',
            )]

        default_related_name = 'shopping_cart'
        verbose_name = 'карта покупок'
        verbose_name_plural = 'Карты покупок'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'[:LEN_LIMIT]


class ShortLink(models.Model):

    """Модель коротких ссылок на рецепт."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='short_code_path',
        null=True, blank=True,
        verbose_name='рецепт'
    )
    short_code_path = models.CharField(max_length=4, blank=True,
                                       verbose_name='код для короткой ссылки')
    original_path = models.URLField(max_length=300,
                                    verbose_name='оригинальная ссылка')

    class Meta:
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    def __str__(self):
        return f'/s/{self.short_code_path} -> {self.original_path}'[:LEN_LIMIT]
