from rest_framework import serializers
from .models import Product, Variant, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category model"""
    class Meta:
        model = Category
        fields = ['id','name', 'description', 'parent_id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the product model"""
    class Meta:
        models = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'stock_quantity', 'sku',
                  'date_added', 'is_active', 'image_url', 'brand']


class VariantSerializer(serializers.ModelSerializer):
    """Serializer for the variant model"""
    class Meta:
        model = Variant
        fields = ['id', 'product', 'variant_name', 'sku', 'price', 
                  'stock', 'image_url', 'created_at', 'updated_at']