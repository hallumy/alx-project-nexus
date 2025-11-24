from rest_framework import viewsets
from .serializers import UserSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User, Address
from .permissions import IsAdmin, IsVendor, IsCustomer
from catalog.utils.mixins import AuthenticatedQuerysetMixin


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
        if getattr(self, "swagger_fake_view", False):
            return User.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

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
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        elif self.action == "list":
            permission_classes = [IsAdmin | IsVendor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class AddressViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    Viewsets for managing addresses with role-based restrictions
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    user_field = "user"

    def perform_create(self, serializer):
        serializer.save = self.request.user
