from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdmin, IsCustomer, IsVendor
from utils.mixins import AuthenticatedQuerysetMixin, CachedQuerysetMixin
from utils.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.renderers import JSONRenderer
from .models import (
    Category, Product, Variant, Cart, CartItem, Wishlist,
    WishlistItem, Discount, ProductDiscount, Inventory,
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


class CategoryViewSet(CachedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Supports nested retrieval of child categories and related products.
    """

    queryset = Category.objects.all().prefetch_related(
        "children",
        "products",
        "products__variant_set",
    )
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]

    cache_prefix = "categories"
    cache_timeout = 60 * 30

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["parent_id", "name"]
    ordering_fields = ["name", "created_at", "id"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class ProductViewSet(CachedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    Prefetches variants and selects related category for optimization.
    """

    queryset = (
        Product.objects.all()
        .select_related("category")
        .prefetch_related("variant_set")
    )
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]
    lookup_field = "id"

    cache_prefix = "products"
    cache_timeout = 60 * 20

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "brand", "is_active"]
    ordering_fields = ["price", "date_added", "name", "id"]
    ordering = ["-date_added"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class VariantViewSet(CachedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing product variants.
    Selects related product to optimize queries.
    """

    queryset = Variant.objects.all().select_related("product")
    serializer_class = VariantSerializer
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]
    lookup_field = "sku"

    cache_prefix = "variants"
    cache_timeout = 60 * 10

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["product", "sku"]
    ordering_fields = ["price", "stock", "id"]
    ordering = ["-id"]

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
    renderer_classes = [JSONRenderer]


class CartItemViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing items inside a shopping cart.
    Selects related cart and variant for optimization.
    """

    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    user_field = "cart__user"

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["variant", "cart"]
    ordering_fields = ["quantity", "price"]
    ordering = ["-created_at"]



class WishlistViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing user wishlists.
    """

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]


class WishlistItemViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing products inside a wishlist.
    Selects related wishlist and product for optimization.
    """

    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    user_field = "wishlist__user"


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discount codes and rules.
    """

    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated, IsAdmin]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["code", "discount_type", "is_active"]


class ProductDiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for linking discounts to products.
    Prefetches related discount and product for optimization.
    """

    serializer_class = ProductDiscountSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    renderer_classes = [JSONRenderer]
    queryset = ProductDiscount.objects.all().select_related("discount", "product")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "discount"]



class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory of variants.
    Selects related variant to optimize queries.
    """

    queryset = Inventory.objects.all().select_related("variant")
    serializer_class = InventorySerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated, (IsAdmin | IsVendor)]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["variant"]
    ordering_fields = ["quantity", "updated_at"]
    ordering = ["-updated_at"]
