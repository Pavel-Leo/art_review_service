from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from core.models import Category, Comment, CustomUser, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        read_only_fields = ("id", "author", "pub_date")
        fields = ("text", "author", "pub_date", "id")
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        read_only_fields = ("pub_date", "author", "id")
        fields = ("id", "author", "text", "score", "pub_date")
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_field = ("id",)
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

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
        read_only_fields = ("role",)


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена"""

    username = serializers.CharField(required=True)
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
    """Сериализатор регистрации"""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = CustomUser
        fields = ("username", "email")
