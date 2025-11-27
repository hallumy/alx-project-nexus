from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer
from utils.mixins import AuthenticatedQuerysetMixin
from utils.pagination import DefaultPagination


class ReviewViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    Represents a user’s review for a product with rating and comment.
    Tracks the creation time and ensures one review per user per product.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination


    user_field = "user"

    def get_queryset(self):
        user = getattr(self.request, "user", None)

        if getattr(user, "is_admin", False):
            return self.queryset.all()

        if getattr(user, "is_vendor", False):
            return self.queryset.none()

        return super().get_queryset()

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get("product_id")

        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise ValidationError("You have already reviewed this product.")
        serializer.save(user=user, product_id=product_id)
