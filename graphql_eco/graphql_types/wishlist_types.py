import strawberry
from typing import List
from strawberry import django as strawberry_django
from catalog.models import Wishlist, WishlistItem


@strawberry_django.type(WishlistItem)
class WishlistItemType:
    id: strawberry.ID
    product_id: int


@strawberry_django.type(Wishlist)
class WishlistType:
    id: strawberry.ID

    @strawberry.field
    def items(self) -> List[WishlistItemType]:
        return list(self.wishlistitem_set.all())
