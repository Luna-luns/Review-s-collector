from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminUser(permissions.BasePermission):
    """Доступ только для администрации."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin

        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_admin

        return request.method in SAFE_METHODS


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Доступ только для администрации или
    только на чтение любому пользователю.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )


class IsModeratorOrAuthor(permissions.BasePermission):
    """Доступ только для модератора или автора."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedForCreateOrReadOnly(permissions.BasePermission):
    """Доступ только для безопасных методов
    или необходимо быть авторизированным.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
