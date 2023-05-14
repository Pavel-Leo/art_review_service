from django.http import HttpRequest
from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Проверяет, имеет ли пользователь права администратора для запроса."""

    def has_permission(self, request: HttpRequest, view: any) -> bool:
        del view
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(
        self, request: HttpRequest, view: any, obj: any,
    ) -> bool:
        del view, obj
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
            )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: any) -> bool:
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self, request: HttpRequest, view: any, obj: any,
    ) -> bool:
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or (request.user == obj.author)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: any) -> bool:
        del view
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
