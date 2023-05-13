from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        "адрес электронной почты",
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        "имя пользователя",
        max_length=150,
        unique=True,
        null=False,
    )
    first_name = models.CharField("имя", max_length=150, blank=True, null=True)
    last_name = models.CharField(
        "фамилия",
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField("биография", blank=True)
    role = models.CharField(
        "роль пользователя",
        choices=settings.CHOISES,
        default=settings.CHOISES[0][0],
        max_length=20,
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    @property
    def is_admin(self):
        return self.is_superuser or self.role == settings.CHOISES[2][0]

    @property
    def is_moderator(self):
        return self.role == settings.CHOISES[1][0]


class Category(models.Model):
    """Модель категория произведения."""

    name = models.CharField("название категории", max_length=256)
    slug = models.SlugField(
        "идентификатор категории",
        unique=True,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField("название жанра", max_length=256)
    slug = models.SlugField(
        "идентификатор жанра",
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        "название произведения",
        max_length=256,
    )
    year = models.IntegerField(
        "год выпуска",
        blank=True,
        validators=[MaxValueValidator(int(datetime.now().year))],
    )
    description = models.TextField(
        "описание произведения", blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("текст отзыва", max_length=1000)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        "дата публикации",
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review",
            ),
        ]
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзыву на произведение."""

    text = models.TextField("текст комментария")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(
        "дата публикации",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-pub_date"]
