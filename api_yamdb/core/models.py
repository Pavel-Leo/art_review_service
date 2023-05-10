from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CHOISES = [
    ("user", "User"),
    ("moderator", "Moderator"),
    ("admin", "Admin"),
]


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name="Имя пользователя. Не более 150 символов. Только буквы, цифры и знаки @/./+/-/_",
        max_length=150,
        unique=True,
    )
    first_name = models.CharField("Имя", max_length=150, blank=True, null=True)
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=True, null=True,
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(
        verbose_name="Роль пользователя",
        choices=CHOISES,
        default=CHOISES[0][0],
        max_length=20,
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def is_admin(self):
        return self.is_superuser or self.role == CHOISES[2][0]

    def is_moderator(self):
        return self.role == CHOISES[1][0]


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=256)
    slug = models.SlugField(
        verbose_name="Идентификатор категории", unique=True, max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=256)
    slug = models.SlugField(
        verbose_name="Идентификатор жанра", unique=True, max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название произведения", max_length=100,
    )
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание произведения")
    rating = models.PositiveIntegerField(
        "рейтинг на основе отзывов", blank=True,
    )
    genre = models.ManyToManyField(
        Genre, verbose_name="жанр произведения", related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews",
    )
    text = models.TextField(verbose_name="Текст отзыва", max_length=1000)
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
        verbose_name="Дата публикации", auto_now_add=True, blank=True,
    )


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ревью",
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True, blank=True,
    )
