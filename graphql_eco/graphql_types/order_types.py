import strawberry
from typing import List, Optional
from strawberry import django as strawberry_django
from order.models import Order, OrderItem, Shipment


@strawberry_django.type(OrderItem)
class OrderItemType:
    id: strawberry.ID
    variant_id: int
    quantity: int
    price: float
    subtotal: float


@strawberry_django.type(Shipment)
class ShipmentType:
    id: strawberry.ID
    order_id: int
    tracking_number: Optional[str]
    carrier: Optional[str]
    status: str
    shipped_at: Optional[str]
    delivered_at: Optional[str]


@strawberry_django.type(Order)
class OrderType:
    id: strawberry.ID
    user_id: int
    address_id: int
    order_number: str
    total_amount: float
    payment_status: str
    order_date: str
    shipped_date: Optional[str]
    payment_method: str

    @strawberry.field
    def items(self) -> List[OrderItemType]:
        return list(self.orderitem_set.all())

    @strawberry.field
    def shipment(self) -> Optional[ShipmentType]:
        return getattr(self, "shipment", None)
