import strawberry
from typing import Optional
from graphql_eco.graphql_types.wishlist_types import WishlistType
from catalog.models import Wishlist


@strawberry.type
class WishlistQuery:

    @strawberry.field
    def wishlist(self, info) -> Optional[WishlistType]:
        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return Wishlist.objects.filter(user=user).first()
