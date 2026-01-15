from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to Super Admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(BasePermission):
    """Allow access only to Gym Manager"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsTrainer(BasePermission):
    """Allow access only to Trainer"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainer'


class IsMember(BasePermission):
    """Allow access only to Member"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'


class IsAdminOrManager(BasePermission):
    """Allow access to Admin or Manager"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']


class IsAdminOrManagerOrTrainer(BasePermission):
    """Allow access to Admin, Manager or Trainer"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager', 'trainer']
