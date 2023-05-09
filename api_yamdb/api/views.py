from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets

from api.serializers import (
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
)

from core.models import Comment, Category, Genre, Title, Review


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
