from rest_framework import serializers
from .models import Product, Variant, Category


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


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category model"""
    children = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id','name', 'description', 'parent_id', 'children', 'products']


    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), may=True).data