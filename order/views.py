from rest_framework import viewsets
from .serializers import OrderItemSerializer, OrderSerializer, ShipmentSerializer
from .models import Order, OrderItem, Shipment
from rest_framework.permissions import IsAuthenticated
from catalog.utils.mixins import AuthenticatedQuerysetMixin

class OrderViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing orders.
    Provides list, create, retrieve, update, and delete actions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderItemViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing order items.
    Includes related product variant and parent order details.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class ShipmentViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing shipments.
    Includes shipment status, tracking number, and related order info.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]