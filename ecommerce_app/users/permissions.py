from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):
    """Allows full access to admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Roles.ADMIN


class IsVendor(BasePermission):
    """Allows partial access to vendors"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Roles.VENDOR
    
class IsCustomer(BasePermission):
    """Allows partial access to customers"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Roles.CUSTOMER