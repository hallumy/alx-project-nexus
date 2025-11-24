from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes Review objects for API responses and creation.
    Includes user, product, rating, comment, and timestamp fields.
    """

    user = serializers.StringRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "product", "created_at"]
