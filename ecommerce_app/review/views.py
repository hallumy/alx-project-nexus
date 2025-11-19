from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Represents a user’s review for a product with rating and comment.
    Tracks the creation time and ensures one review per user per product.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)

