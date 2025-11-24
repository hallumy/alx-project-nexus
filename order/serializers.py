from rest_framework import serializers
from .models import Order, OrderItem, Shipment


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, including user, address,
    payment information, and order details.
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "address",
            "order_number",
            "total_amount",
            "payment_status",
            "order_date",
            "shipped_date",
            "payment_method",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model, including product variant,
    quantity, price, and subtotal.
    """

    class Meta:
        model = OrderItem
        fields = ["id", "order", "variant", "quantity", "price", "subtotal"]


class ShipmentSerializer(serializers.ModelSerializer):
    """Serializer for the Shipment model including order and status details."""

    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "order",
            "tracking_number",
            "carrier",
            "status",
            "shipped_at",
            "delivered_at",
        ]
        read_only_fields = ["shipped_at", "delivered_at"]
