from rest_framework import viewsets
from .models import Category, Product, Variant
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related(
        'children',
        'product__variants',
    )
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related(
        "variants",
        "category",
    )
    serializer_class = ProductSerializer
    lookup_field = 'id'


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().select_related('product')
    serializer_class = VariantSerializer
    lookup_field = 'sku'