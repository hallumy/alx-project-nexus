import strawberry
from typing import List
from catalog.models import Cart, CartItem
from strawberry import django as strawberry_django


@strawberry_django.type(CartItem)
class CartItemType:
    id: strawberry.ID
    quantity: int
    price: float
    variant_id: int


@strawberry_django.type(Cart)
class CartType:
    id: strawberry.ID

    @strawberry.field
    def items(self) -> List[CartItemType]:
        return list(self.cartitem_set.all())
