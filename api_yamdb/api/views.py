from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
<<<<<<< HEAD
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
=======
from django.shortcuts import get_object_or_404
>>>>>>> develop
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
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
<<<<<<< HEAD
    TitleReadSerializer
)
from core.models import Category, Comment, CustomUser, Genre, Review, Title

from .permissions import (IsAdminPermission, IsAdminOrReadOnly,
                          IsAdminAuthorModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly)
from .filters import TitlesFilter


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().anotate(Avg("rewiews_score")).order_by("name")
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminAuthorModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get("review_id"),
                                   title_id=self.kwargs.get("title_id")
                                   )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminAuthorModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id"),
        )
        serializer.save(author=self.request.user, title=title)
=======
)
from core.models import Category, Comment, CustomUser, Genre, Review, Title

from .permissions import IsAdminPermission


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
    permission_classes = (IsAdminPermission,)
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        detail=False,
        methods=("get", "patch"),
        url_name="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == "PATCH":
            serializer = CustomUserSerializer(
                request.user, data=request.data, partial=True
            )
        # else: допишу еще блок
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
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
        except ValidationError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            CustomUser, username=serializer.data["username"]
        )
        confirmation_code = default_token_generator.make_token(user)
        email = serializer.data["email"]
        send_mail(
            subject="Код для регистрации",
            message=confirmation_code,
            from_email="from@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class Token(APIView):
    """Получение токена"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, username=serializer.data["username"]
        )
        if default_token_generator.check_token(
            user, serializer.data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        else:
            return Response(
                "Неверный код", status=status.HTTP_400_BAD_REQUEST
            )
>>>>>>> develop
