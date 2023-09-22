from rest_framework import permissions


class IsOwnerOrHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['Owner', 'HR']
