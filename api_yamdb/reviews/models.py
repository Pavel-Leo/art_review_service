from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Модель категория произведения."""

    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        'идентификатор категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self: 'Category') -> str:
        return self.slug


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('название жанра', max_length=256)
    slug = models.SlugField(
        'идентификатор жанра',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self: 'Genre') -> str:
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        'год выпуска',
        blank=True,
        validators=[MaxValueValidator(int(datetime.now().year))],
    )
    description = models.TextField(
        'описание произведения',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self: 'Title') -> str:
        return self.name


class Review(models.Model):
    """Отзыв на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('текст отзыва', max_length=1000)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
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
        'дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]
        ordering = ['-pub_date']

    def __str__(self: 'Review') -> str:
        return self.text


class Comment(models.Model):
    """Комментарии к отзыву на произведение."""

    text = models.TextField('текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self: 'Comment') -> str:
        return self.text
