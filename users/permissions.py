from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):
    """Allows full access to admins"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsVendor(BasePermission):
    """Allows partial access to vendors"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_vendor


class IsCustomer(BasePermission):
    """Allows partial access to customers"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
