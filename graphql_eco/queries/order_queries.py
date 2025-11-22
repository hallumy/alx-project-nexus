import strawberry
from typing import List, Optional
from order.models import Order, OrderItem, Shipment
from graphql_eco.graphql_types.order_types import OrderType, OrderItemType, ShipmentType


def get_order_items(order: Order) -> List[OrderItemType]:
    return [
        OrderItemType(
            id=item.id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            price=float(item.price),
            subtotal=float(item.subtotal),
        )
        for item in order.orderitem_set.all()
    ]


def get_order_shipment(order: Order) -> Optional[ShipmentType]:
    shipment = getattr(order, "shipment", None)
    if not shipment:
        return None

    return ShipmentType(
        id=shipment.id,
        order_id=shipment.order_id,
        tracking_number=shipment.tracking_number,
        carrier=shipment.carrier,
        status=shipment.status,
        shipped_at=str(shipment.shipped_at) if shipment.shipped_at else None,
        delivered_at=str(shipment.delivered_at) if shipment.delivered_at else None,
    )

@strawberry.type
class OrderQuery:

    @strawberry.field
    def orders(self, info) -> List[OrderType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return []

        # Admin sees all orders — customers only see theirs
        if user.is_admin:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=user)

        return [
            OrderType(
                id=o.id,
                user_id=o.user_id,
                address_id=o.address_id,
                order_number=o.order_number,
                total_amount=float(o.total_amount),
                payment_status=o.payment_status,
                order_date=str(o.order_date),
                shipped_date=str(o.shipped_date) if o.shipped_date else None,
                payment_method=o.payment_method,
                items=get_order_items(o),
                shipment=get_order_shipment(o),
            )
            for o in orders
        ]

    @strawberry.field
    def order(self, info, order_id: int) -> Optional[OrderType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return None

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

        # Only admin or owner can view
        if not user.is_admin and order.user != user:
            return None

        return OrderType(
            id=order.id,
            user_id=order.user_id,
            address_id=order.address_id,
            order_number=order.order_number,
            total_amount=float(order.total_amount),
            payment_status=order.payment_status,
            order_date=str(order.order_date),
            shipped_date=str(order.shipped_date) if order.shipped_date else None,
            payment_method=order.payment_method,
            items=get_order_items(order),
            shipment=get_order_shipment(order),
        )
