from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CommentViewSet, TitleViewSet, GenreViewSet,
                       CategoryViewSet, ReviewViewSet)

router = SimpleRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
