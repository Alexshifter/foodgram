from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор')
]


class NewUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    ]

    role = models.CharField(choices=ROLE_CHOICES,
                            default=USER,
                            verbose_name='роль',
                            max_length=20)
    email = models.EmailField(blank=False,
                              unique=True,
                              verbose_name='электронная почта',
                              max_length=254)

    avatar = models.ImageField(upload_to='users/', null=True, default=None, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_pair_username_email',
            )
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return (f'Пользователь {self.username}, '
                f'роль {self.role}')

class Following(models.Model):
    user = models.ForeignKey(
        NewUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Текущий пользватель'
        )
    following = models.ForeignKey(NewUser,
                                   on_delete=models.CASCADE,
                                   related_name='following',
                                   verbose_name='Подписки пользователя')


# Ограничение повторной подписки(уникальная пара);
# Ограничение подписки на самого себя;

class Meta:

    constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
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
        return f'{self.follower} подписан на {self.following}'
