from django.http import HttpRequest
from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Проверяет, имеет ли пользователь права администратора для запроса."""

    def has_permission(self: any, request: HttpRequest, view: any) -> bool:
        return request.user.is_admin

    def has_object_permission(
        self: any,
        request: HttpRequest,
        view: any,
        obj: any,
    ) -> bool:
        return request.user.is_moderator_or_admin_or_superuser()


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Кастомный класс для проверки прав доступа.
    Проверяет, имеет ли пользователь права администратора для запроса, либо
    является автором.
    """

    def has_object_permission(
        self: any,
        request: HttpRequest,
        view: any,
        obj: any,
    ) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or (request.user == obj.author)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Кастомный класс для проверки прав доступа.
    Проверяет, является ли пользователь аутентифицированным администратором,
    либо дает право только на чтение.
    """

    def has_permission(self: any, request: HttpRequest, view: any) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
