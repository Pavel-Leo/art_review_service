import re

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
    author = SlugRelatedField(slug_field="username", read_only=True,)

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

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Нельзя использовать имя 'me'")
        elif CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже существует"
            )
        elif not re.match(r"^[\w.@+-]+$", value):
            error = (
                "Имя пользователя должно содержать только буквы, цифры и "
                "символы '@', '.', '+', '-'"
            )
            raise serializers.ValidationError(error)
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
        # read_only_fields = ("role",) с ним не получается и без него не
        # получается оставил чтобы не забыть. 


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена"""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = CustomUser


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Нельзя использовать имя 'me'")
        elif not re.match(r"^[\w.@+-]+$", value):
            error = (
                "Имя пользователя должно содержать только буквы, цифры и "
                "символы '@', '.', '+', '-'"
            )
            raise serializers.ValidationError(error)
        return value
