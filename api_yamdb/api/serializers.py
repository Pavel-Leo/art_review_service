import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date', 'id')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self: any, review: Review) -> Review:
        review_already_exists = Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context['view'].kwargs.get('title_id'),
        ).exists()
        if self.instance is None and review_already_exists:
            raise serializers.ValidationError(
                'Отзыв пользователя уже существует',
            )
        return review

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор редактирования произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title


class UsernameValidation:
    """Проверка username на корректность данных."""

    def check_username(value: str) -> str:
        """Проверка имени пользователя на валидность данных."""
        if value.lower() == 'me':
            raise ValidationError('Нельзя использовать имя "me" или "ME"')
        if not re.match(r'^[\w.@+-]+\Z', value):
            error = (
                'Имя пользователя должно содержать только буквы, цифры и '
                'символы "@", ".", "_", "+", "-"'
            )
            raise ValidationError(error)
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        required=True,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ],
    )

    def validate_username(self: any, value: str) -> str:
        """Проверка имени пользователя на валидность данных."""
        return UsernameValidation.check_username(value)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class NotAdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя с обязательным указанием роли."""

    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)

    def validate_username(self: any, value: str) -> str:
        """Проверка имени пользователя на валидность данных."""
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError(
                'Пользователь с таким именем уже существует',
            )
        return UsernameValidation.check_username(value)


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = CustomUser


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self: any, value: str) -> str:
        """Проверка имени пользователя на валидность данных."""
        return UsernameValidation.check_username(value)
