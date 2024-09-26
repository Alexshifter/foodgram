from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend.constants import LEN_LIMIT


class NewUser(AbstractUser):

    """Кастомная модель пользователя."""

    email = models.EmailField(blank=False,
                              unique=True,
                              verbose_name='электронная почта',
                              max_length=254)

    avatar = models.ImageField(upload_to='users/',
                               null=True, default=None,
                               blank=True)

    class Meta:

        """Ограничение на единственную пару username-email."""

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_pair_username_email',
            )
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'{self.username}')[:LEN_LIMIT]


class Following(models.Model):

    """Модель подписок пользователя на авторов."""

    user = models.ForeignKey(
        NewUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользватель'
    )
    following = models.ForeignKey(
        NewUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписки'
    )

    class Meta:

        """
        Ограничение повторной подписки.
        Ограничение подписки на самого себя.

        """
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='%(app_label)s _ %(class)s _unique_relationships',
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Подписки {self.user}')[:LEN_LIMIT]
