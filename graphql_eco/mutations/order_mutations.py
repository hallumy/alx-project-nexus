import strawberry
from order.models import Order, OrderItem, Shipment
from users.models import User
from graphql_eco.graphql_types.order_types import OrderType

@strawberry.type
class OrderMutation:
    @strawberry.mutation
    def create_order(
        self,
        info,
        address_id: int,
        payment_method: str
    ) -> OrderType:
        user = info.context["request"].user
        if not user.is_authenticated:
            raise Exception("Authentication required")

        order = Order.objects.create(
            user=user,
            address_id=address_id,
            order_number=f"ORD-{user.id}-{Order.objects.count() + 1}",
            total_amount=0.0, 
            payment_status="PENDING",
            payment_method=payment_method
        )
        return OrderType(
            id=order.id,
            user_id=order.user_id,
            address_id=order.address_id,
            order_number=order.order_number,
            total_amount=float(order.total_amount),
            payment_status=order.payment_status,
            order_date=str(order.order_date),
            shipped_date=None,
            payment_method=order.payment_method,
            items=[],
            shipment=None
        )