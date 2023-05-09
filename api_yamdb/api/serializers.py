from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from core.models import Comment, Category, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        read_only_fields = ('id', 'author', 'pub_date')
        fields = ('text', 'author', 'pub_date', 'id')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        read_only_fields = ('pub_date', 'author', 'id')
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_field = ('id',)
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title
