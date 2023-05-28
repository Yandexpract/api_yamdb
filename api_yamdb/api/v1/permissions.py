from rest_framework import permissions


class UsersPermission(permissions.BasePermission):
    """Право работать с пользователями для администратора."""
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Право администратора создавать и удалять произведения, категории'''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAuthorOrModerator(permissions.BasePermission):
    '''Права удалять и редактировать отзывы и комментарии.'''
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)

