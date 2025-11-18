from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, VariantViewSet, InventoryViewSet,
    DiscountViewSet, ProductDiscountViewSet, WishlistItemViewSet, WishlistViewSet,
    CartItemViewSet, CartViewSet
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'variants', VariantViewSet, basename='variant')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'product-discounts', ProductDiscountViewSet, basename='productdiscount')
router.register(r'wishlists', WishlistViewSet, basename='wishlist')
router.register(r'wishlist-items', WishlistItemViewSet, basename='wishlistitem')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', include(router.urls))
]