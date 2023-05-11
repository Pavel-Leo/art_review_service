from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an Email')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        'Required. 150 characters or fewer. Letters, digits and @/./+/-/_only',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(choices=[('user', 'User'),
                                     ('moderator', 'Moderator'),
                                     ('admin', 'Admin')],
                            default='user', max_length=20)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Category(models.Model):
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField('название жанра', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('название', max_length=100)
    year = models.PositiveIntegerField('год выпуска')
    rating = models.PositiveIntegerField('рейтинг на основе отзывов',
                                         blank=True)
    description = models.TextField('описание', blank=True)
    genre = models.ForeignKey(Genre, related_name='genre',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category',
                                 on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0),
        ],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            ),
        ]
        ordering = ('pub_date')

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField('текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    rewiew = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментируемый отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
