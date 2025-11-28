from rest_framework import viewsets
from .serializers import OrderItemSerializer, OrderSerializer, ShipmentSerializer
from .models import Order, OrderItem, Shipment
from rest_framework.permissions import IsAuthenticated
from utils.mixins import AuthenticatedQuerysetMixin, CachedQuerysetMixin
from utils.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.renderers import JSONRenderer


class OrderViewSet(CachedQuerysetMixin, AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing orders.
    Provides list, create, retrieve, update, and delete actions.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["user", "payment_status", "order_date", "shipped_date"]

    ordering_fields = ["order_date", "total_amount", "payment_status", "id"]
    ordering = ["-order_date"]

    cache_prefix = "order"
    cache_timeout = 60 * 10


class OrderItemViewSet(CachedQuerysetMixin, AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing order items.
    Includes related product variant and parent order details.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["order", "variant", "quantity", "price"]

    ordering_fields = ["quantity", "price", "subtotal", "id"]
    ordering = ["-id"]

    cache_prefix = "order_item"
    cache_timeout = 60 * 15


class ShipmentViewSet(CachedQuerysetMixin, AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing shipments.
    Includes shipment status, tracking number, and related order info.
    """

    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["order", "carrier", "status", "shipped_at", "delivered_at"]

    ordering_fields = ["status", "shipped_at", "delivered_at", "id"]
    ordering = ["-shipped_at"]

    cache_prefix = "shipment"
    cache_timeout = 60 * 20 

