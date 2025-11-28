from django.db import models
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

from catalog.models import Product


class Review(models.Model):
    """
    Represents a user’s review for a product with rating and comment.
    Tracks the creation time and ensures one review per user per product.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_review')
        ]

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} ({self.rating})"
