import strawberry
from catalog.models import Wishlist, WishlistItem, Product


@strawberry.type
class WishlistMutation:

    @strawberry.mutation
    def add_to_wishlist(self, info, product_id: int) -> bool:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Login required")

        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        product = Product.objects.get(id=product_id)

        WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        return True

    @strawberry.mutation
    def remove_from_wishlist(self, item_id: int) -> bool:
        WishlistItem.objects.filter(id=item_id).delete()
        return True
