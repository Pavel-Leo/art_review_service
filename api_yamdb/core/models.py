from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        "адрес электронной почты",
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        "имя пользователя. Не более 150 символов. Только буквы, цифры и знаки @/./+/-/_",
        max_length=150,
        unique=True,
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
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def is_admin(self):
        return self.is_superuser or self.role == settings.CHOISES[2][0]

    def is_moderator(self):
        return self.role == settings.CHOISES[1][0]


class Category(models.Model):
    name = models.CharField("название категории", max_length=256)
    slug = models.SlugField(
        "идентификатор категории",
        unique=True,
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField("название жанра", max_length=256)
    slug = models.SlugField(
        "идентификатор жанра",
        unique=True,
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        "название произведения",
        max_length=256,
    )
    year = models.PositiveIntegerField("год выпуска")
    description = models.TextField("описание произведения")
    rating = models.PositiveIntegerField(
        "рейтинг на основе отзывов",
        blank=True,
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
        blank=True,
    )


class Review(models.Model):
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
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        "дата публикации",
        auto_now_add=True,
        blank=True,
    )


class Comment(models.Model):
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
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        "дата публикации",
        auto_now_add=True,
        blank=True,
    )
