from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(
        'адрес электронной почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        null=False,
    )
    first_name = models.CharField('имя', max_length=150, blank=True, null=True)
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField('биография', blank=True)
    role = models.CharField(
        'роль пользователя',
        choices=settings.CHOISES,
        default=settings.CHOISES[0][0],
        max_length=20,
    )

    def __str__(self: 'CustomUser') -> str:
        return self.username

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    @property
    def is_admin(self: 'CustomUser') -> bool:
        return self.is_superuser or self.role == settings.CHOISES[2][0]

    @property
    def is_moderator(self: 'CustomUser') -> bool:
        return self.role == settings.CHOISES[1][0]
