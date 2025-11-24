import strawberry
from typing import Optional
from graphql_eco.graphql_types.cart_types import CartType
from catalog.models import Cart


@strawberry.type
class CartQuery:

    @strawberry.field
    def cart(self, info) -> Optional[CartType]:
        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return Cart.objects.filter(user=user).first()
