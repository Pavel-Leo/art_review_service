from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    CustomUserViewSet,
    GenreViewSet,
    ReviewViewSet,
    Signup,
    TitleViewSet,
    Token,
)

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")

router.register("users", CustomUserViewSet, basename="users")

comment_router = DefaultRouter()
router.register("comments", CommentViewSet, basename="comments")

review_router = DefaultRouter()
router.register("reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path("v1/auth/signup/", Signup.as_view(), name="signup"),
    path("v1/auth/token/", Token.as_view(), name="token"),
    path("v1/", include(router.urls)),
    path("v1/<int:title_id>/reviews/<int:review_id>/",
         include(comment_router.urls)),
    path("v1/<int:title_id>/reviews/", include(review_router.urls)),
]
