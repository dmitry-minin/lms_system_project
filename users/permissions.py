from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Custom permission to only allow users in the 'moderators' group to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Moderator').exists()


class IsOwner(BasePermission):
    """
    Custom permission to only allow the owner of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUser(BasePermission):
    """
    Custom permission to only allow users to access their own data.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSelf(BasePermission):
    """
    Custom permission to only allow users to access their own data.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_superuser
