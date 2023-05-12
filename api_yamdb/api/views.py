from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomUserSerializer,
    GenreSerializer,
    NotAdminUserSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    TokenSerializer,
    TitleReadSerializer
)
from core.models import Category, Comment, CustomUser, Genre, Review, Title

from .permissions import (IsAdminModeratorOwnerOrReadOnly, IsAdminPermission)
from .filters import TitlesFilter


class TitleViewSet(viewsets.ModelViewSet):
    # queryset = Title.objects.annotate(
    #     rating=Avg("rewiews__score")).order_by("-id")
    queryset = Title.objects.all().order_by("-id")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get("review_id"),
                                   title_id=self.kwargs.get("title_id"),
                                   )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id"),
        )
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет информации о пользователе."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = [
        IsAdminPermission,
    ]
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin or request.user.is_superuser:
                serializer = CustomUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True,
                )
            else:
                serializer = NotAdminUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(APIView):
    """Регистрация пользователя"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            CustomUser.objects.get_or_create(
                username=serializer.data.get("username"),
                email=serializer.data.get("email"),
            )
        except IntegrityError as e:
            return Response(
                f"Данные уже существуют: {str(e)}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(
            CustomUser, username=serializer.data["username"],
        )
        confirmation_code = default_token_generator.make_token(user)
        email = serializer.data["email"]
        send_mail(
            subject="Код для регистрации",
            message=confirmation_code,
            from_email="from@example.com",
            recipient_list=[email],
            fail_silently=False,
        ),
        return Response(serializer.data, status=status.HTTP_200_OK)


class Token(APIView):
    """Получение токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, username=serializer.data["username"],
        )
        if default_token_generator.check_token(
            user, serializer.data["confirmation_code"],
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        else:
            return Response(
                "Неверный код", status=status.HTTP_400_BAD_REQUEST,
            )
