from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, TitleViewSet

router = SimpleRouter()
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
