from rest_framework import serializers
from .models import (
    Product,
    Variant,
    Category,
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
    Discount,
    ProductDiscount,
    Inventory,
)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the product model"""

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "stock_quantity",
            "sku",
            "date_added",
            "is_active",
            "image_url",
            "brand",
        ]


class VariantSerializer(serializers.ModelSerializer):
    """Serializer for the variant model"""

    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "variant_name",
            "sku",
            "price",
            "stock",
            "image_url",
            "created_at",
            "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category model"""
    children = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "parent_id", "children", "products"]

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model.."""

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at"]


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for items inside a cart."""

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "variant",
            "quantity",
            "price",
            "created_at",
            "updated_at",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for user Wishlist."""

    class Meta:
        model = Wishlist
        fields = ["id", "user", "created_at"]


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for products added to a Wishlist."""

    class Meta:
        model = WishlistItem
        fields = ["id", "wishlist", "product"]


class DiscountSerializer(serializers.ModelSerializer):
    """Serializer for Discount rules."""

    class Meta:
        model = Discount
        fields = [
            "id",
            "code",
            "description",
            "discount_type",
            "minimum_purchase",
            "maximum_discount",
            "start_date",
            "end_date",
            "is_active",
        ]


class ProductDiscountSerializer(serializers.ModelSerializer):
    """Serializer linking Discounts to Products."""

    class Meta:
        model = ProductDiscount
        fields = ["id", "discount", "product"]


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Variant inventory."""

    class Meta:
        model = Inventory
        fields = ["id", "variant", "quantity", "updated_at"]
