from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    CustomUserViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    Token,
    Signup,
)

router = DefaultRouter()
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review",
)
router.register("users", CustomUserViewSet, basename="users")

urls_auth = [
    path("auth/token/", Token.as_view(), name="token"),
    path("auth/signup/", Signup.as_view(), name="signup"),
]

urlpatterns = [
    path("v1/", include(urls_auth)),
    path("v1/", include(router.urls)),
]
