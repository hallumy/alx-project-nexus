from rest_framework import viewsets
from .serializers import UserSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User, Address
from .permissions import IsAdmin, IsVendor, IsCustomer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing role based data access:
    -Admin : Full access
    -Vendor: Customer details only
    -Customers: Access to their profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Roles.ADMIN:
            return User.objects.all()
        elif user.role == User.Roles.VENDOR:
            return User.objects.filter(role=User.Roles.CUSTOMER)
        else:
            return User.objects.filter(id=user.id)
    
    def get_permissions(self):
        """
        Assign permissions dynamically based on user role and action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action == 'list':
            permission_classes = [IsAdmin | IsVendor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
class AddressViewSet(viewsets.ModelViewSet):
    """
    Viewsets for managing addresses with role-based restrictions
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Roles.ADMIN:
            return Address.objects.all()
        elif user.role == User.Roles.VENDOR:
            return Address.objects.filter(user__role = User.Roles.Customer)
        return Address.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save = (self.request.user)