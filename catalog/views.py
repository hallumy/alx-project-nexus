from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdmin, IsCustomer, IsVendor
from .utils.mixins import AuthenticatedQuerysetMixin
from .models import (
    Category,
    Product,
    Variant,
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
    Discount,
    ProductDiscount,
    Inventory,
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    VariantSerializer,
    CartSerializer,
    CartItemSerializer,
    WishlistSerializer,
    WishlistItemSerializer,
    DiscountSerializer,
    ProductDiscountSerializer,
    InventorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Supports nested retrieval of child categories and related products.
    """

    queryset = Category.objects.all().prefetch_related(
        "children",
        "products",
        "product__variant_set",
    )
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    Prefetches variants and selects related category for optimization.
    """

    queryset = (
        Product.objects.all()
        .select_related(
            "category",
        )
        .prefetch_related(
            "variant_set",
        )
    )
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class VariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product variants.
    Selects related product to optimize queries.
    """

    queryset = Variant.objects.all().select_related("product")
    serializer_class = VariantSerializer
    lookup_field = "sku"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class CartViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing user shopping carts.
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class CartItemViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing items inside a shopping cart.
    Selects related cart and variant for optimization.
    """

    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    user_field = "cart__user"


class WishlistViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing user wishlists.
    """

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]


class WishlistItemViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing products inside a wishlist.
    Selects related wishlist and product for optimization.
    """

    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    user_field = "wishlist__user"


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discount codes and rules.
    """

    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ProductDiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for linking discounts to products.
    Prefetches related discount and product for optimization.
    """

    serializer_class = ProductDiscountSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = ProductDiscount.objects.all().select_related("discount", "product")


class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory of variants.
    Selects related variant to optimize queries.
    """

    queryset = Inventory.objects.all().select_related("variant")
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, (IsAdmin | IsVendor)]
