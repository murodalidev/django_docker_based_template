from rest_framework import permissions


def has_role(user: object, roles: list) -> bool:
    user_groups = set(group.name for group in user.groups.all())
    return bool(user_groups.intersection(roles))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ['admin'])

    def has_object_permission(self, request, view, obj):
        return has_role(request.user, ['admin'])


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return has_role(request.user, ['admin'])

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return has_role(request.user, ['admin'])


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
