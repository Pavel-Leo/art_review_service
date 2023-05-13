import re


from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Category, Comment, CustomUser, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True,
    )

    class Meta:
        fields = ("text", "author", "pub_date", "id", "review")
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        lookup_field = "slug"
        model = Category
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        lookup_field = "slug"
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов """
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                "Рейтинг произведения по 10-бальной шкале."
            )

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwarg.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "Post":
            if Review.objects.filter(
                title=title, author=request.user,
            ).exists():
                raise ValidationError("Можно написать только один отзыв.")
            return data

    class Meta:
        read_only_fields = ("pub_date", "author", "id")
        fields = ("id", "author", "title", "text", "score", "pub_date")
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all()
    )
    class Meta:
        read_only_field = ("id",)
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор редактирование произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ],
    )

    def validate_username(self, value):
        """Проверка имени пользователя на валидность данных."""
        if value.lower() == "me":
            raise ValidationError("Нельзя использовать имя 'me или ME'")
        elif CustomUser.objects.filter(username=value).exists():
            raise ValidationError(
                "Пользователь с таким именем уже существует",
            )
        elif not re.match(r"^[\w.@+-]+\Z", value):
            error = (
                "Имя пользователя должно содержать только буквы, цифры и "
                "символы '@', '.', '+', '-'"
            )
            raise ValidationError(error)
        return value

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class NotAdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя с обязательным указанием роли."""

    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)

    def validate_username(self, value):
        """Проверка имени пользователя на валидность данных."""
        if value.lower() == "me":
            raise ValidationError("Нельзя использовать имя 'me или ME'")
        elif CustomUser.objects.filter(username=value).exists():
            raise ValidationError(
                "Пользователь с таким именем уже существует",
            )
        elif not re.match(r"^[\w.@+-]+\Z", value):
            error = (
                "Имя пользователя должно содержать только буквы, цифры и "
                "символы '@', '.', '+', '-'"
            )
            raise ValidationError(error)
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = CustomUser

    def validate(self, data):
        username = data.get("username")
        confirmation_code = data.get("confirmation_code")

        if not username or not confirmation_code:
            raise serializers.ValidationError("Некорректные данные")
        return data


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def validate_username(self, value):
        """Проверка имени пользователя на валидность данных."""
        if value.lower() == "me":
            raise serializers.ValidationError("Нельзя использовать имя 'me'")
        elif not re.match(r"^[\w.@+-]+\Z", value):
            error = (
                "Имя пользователя должно содержать только буквы, цифры и "
                "символы '@', '.', '+', '-'"
            )
            raise serializers.ValidationError(error)
        return value

    # проверка
