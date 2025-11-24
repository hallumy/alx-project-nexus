from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    VariantViewSet,
    InventoryViewSet,
    DiscountViewSet,
    ProductDiscountViewSet,
    WishlistItemViewSet,
    WishlistViewSet,
    CartItemViewSet,
    CartViewSet,
)

router = DefaultRouter()

router.register(r"category", CategoryViewSet, basename="category")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"variant", VariantViewSet, basename="variant")
router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(r"discount", DiscountViewSet, basename="discount")
router.register(r"product-discount", ProductDiscountViewSet, basename="productdiscount")
router.register(r"wishlist", WishlistViewSet, basename="wishlist")
router.register(r"wishlist-item", WishlistItemViewSet, basename="wishlistitem")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-item", CartItemViewSet, basename="cartitem")

urlpatterns = [path("", include(router.urls))]
