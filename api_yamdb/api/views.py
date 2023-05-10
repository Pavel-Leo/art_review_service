from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomUserSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    TokenSerializer,
)
from core.models import Category, Comment, CustomUser, Genre, Review, Title


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


class CustomUserViewSet(viewsets.ModelViewSet):
    """Просмотр информации о пользователе"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ["get", "post", "patch", "delete"]

    # @action(
    #     detail=False,
    #     methods=["get", "patch"],
    #     url_path="me",
    #     permission_classes=[IsAuthenticated],
    # )
    # def me(self, request):
    #     serializer = CustomUserSerializer(request.user)
    #     if request.method == "PATCH":
    #         serializer = CustomUserSerializer(
    #             request.user, data=request.data, partial=True,
    #         )
    #         if not serializer.is_valid():
    #             return Response(
    #                 serializer.errors, status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(APIView):
    """Регистрация пользователя"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        try:
            user = CustomUser.objects.get_or_create(username=username)
            email = CustomUser.objects.get_or_create(email=email)
        except ValidationError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "Код для регистрации",
            confirmation_code,
            "from@example.com",
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class Token(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        username = serializer.validated_data["username"]
        confirmation_code = serializer.validated_data["confirmation_code"]
        user = get_object_or_404(CustomUser, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
