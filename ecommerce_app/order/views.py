from rest_framework import viewsets
from .serializers import OrderItemSerializer, OrderSerializer, ShipmentSerializer
from .models import Order, OrderItem, Shipment


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing orders.
    Provides list, create, retrieve, update, and delete actions.
    """
    queryset = Order.objects.all().select_related('user', 'address')
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing order items.
    Includes related product variant and parent order details.
    """
    queryset = OrderItem.objects.all().select_related('order', 'variant', 'variant__product')
    serializer_class = OrderItemSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing shipments.
    Includes shipment status, tracking number, and related order info.
    """
    queryset = Shipment.objects.all().select_related('order')
    serializer_class = ShipmentSerializer