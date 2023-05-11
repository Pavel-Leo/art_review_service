from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from core.models import Category, Comment, CustomUser, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True
    )

    class Meta:
        read_only_fields = ("id", "author", "pub_date", "review")
        fields = ("text", "author", "pub_date", "id", "rewiew")
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
    author = SlugRelatedField(
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
                title=title, author=request.user
            ).exists():
                raise ValidationError("Можно написать только один отзыв.")
            return data

    class Meta:
        read_only_fields = ("pub_date", "author", "id")
        fields = ("id", "author", "title", "text", "score", "pub_date")
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


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title
