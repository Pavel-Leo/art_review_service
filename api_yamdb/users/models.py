from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = ("user", "Пользователь")
    MODERATOR = ("moderator", "Модератор")
    ADMIN = ("admin", "Администратор")
    SUPERUSER = ("superuser", "Суперпользователь")


class CustomUser(AbstractUser):
    """Модель пользователя"""

    bio = models.TextField("биография", blank=True)
    role = models.CharField(
        "роль пользователя",
        choices=UserRole.choices,
        default=UserRole.USER,
        max_length=20,
    )
    first_name = models.CharField(
        "имя", max_length=50, blank=True, null=True,
    )
    last_name = models.CharField(
        "фамилия", max_length=50, blank=True, null=True,
    )

    def __str__(self: "CustomUser") -> str:
        return self.username

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    @property
    def is_admin(self: "CustomUser") -> bool:
        return self.is_superuser or self.role == UserRole.ADMIN

    def is_moderator_or_admin_or_superuser(self: "CustomUser") -> bool:
        return (
            self.is_admin
            or self.is_moderator
            or self.role == UserRole.SUPERUSER
        )

    @property
    def is_moderator(self: "CustomUser") -> bool:
        return self.role == UserRole.MODERATOR
