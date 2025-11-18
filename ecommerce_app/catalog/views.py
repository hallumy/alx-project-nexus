from rest_framework import viewsets
from .models import (
    Category, Product, Variant, Cart, CartItem, Wishlist,
    WishlistItem, Discount, ProductDiscount, Inventory
)
from .serializers import (
    CategorySerializer, ProductSerializer, VariantSerializer,
    CartSerializer, CartItemSerializer, WishlistSerializer,
    WishlistItemSerializer,DiscountSerializer, ProductDiscountSerializer,
    InventorySerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Supports nested retrieval of child categories and related products.
    """
    queryset = Category.objects.all().prefetch_related(
        'children',
        'products',
        'product__variant_set',
    )
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    Prefetches variants and selects related category for optimization.
    """
    queryset = Product.objects.all().select_related(
        "category",
    ).prefetch_related(
        "variant_set",
    )
    serializer_class = ProductSerializer
    lookup_field = 'id'


class VariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product variants.
    Selects related product to optimize queries.
    """
    queryset = Variant.objects.all().select_related('product')
    serializer_class = VariantSerializer
    lookup_field = 'sku'

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user shopping carts.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing items inside a shopping cart.
    Selects related cart and variant for optimization.
    """
    queryset = CartItem.objects.all().select_related('cart', 'variant')
    serializer_class = CartItemSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user wishlists.
    """
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class WishlistItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products inside a wishlist.
    Selects related wishlist and product for optimization.
    """
    queryset = WishlistItem.objects.all().select_related('wishlist', 'product')
    serializer_class = WishlistItemSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discount codes and rules.
    """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class ProductDiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for linking discounts to products.
    Prefetches related discount and product for optimization.
    """
    queryset = ProductDiscount.objects.all().select_related('discount', 'product')
    serializer_class = ProductDiscountSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory of variants.
    Selects related variant to optimize queries.
    """
    queryset = Inventory.objects.all().select_related('variant')
    serializer_class = InventorySerializer