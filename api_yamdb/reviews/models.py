from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class CommonAbstact(models.Model):
    """Модель абстрактного класса для категории и жанра."""

    name = models.CharField("название", max_length=256)
    slug = models.SlugField(
        "идентификатор",
        unique=True,
        max_length=50,
    )

    class Meta:
        abstract = True

    def __str__(self: any) -> str:
        return self.name


class Category(CommonAbstact):
    """Модель категория произведения."""

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Genre(CommonAbstact):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"


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
        "описание произведения",
        blank=True,
        null=True,
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
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    def __str__(self: any) -> str:
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

    def __str__(self: any) -> str:
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

    def __str__(self: any) -> str:
        return self.text
