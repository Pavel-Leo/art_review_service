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
router.register('users', CustomUserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

comments_router = DefaultRouter()
comments_router.register('comments', CommentViewSet, basename='comments')

reviews_router = DefaultRouter()
reviews_router.register('reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', Signup.as_view(), name='signup'),
    path('v1/auth/token/', Token.as_view(), name='token'),
    path('v1/titles/<int:title_id>/', include(reviews_router.urls)),
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/',
        include(comments_router.urls),
    ),
]
