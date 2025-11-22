import strawberry
from catalog.models import Cart, CartItem, Variant


@strawberry.type
class CartMutation:

    @strawberry.mutation
    def add_to_cart(self, info, variant_id: int, quantity: int) -> bool:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Login required")

        cart, _ = Cart.objects.get_or_create(user=user)
        variant = Variant.objects.get(id=variant_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart, variant=variant,
            defaults={"quantity": quantity, "price": variant.price}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return True

    @strawberry.mutation
    def remove_cart_item(self, item_id: int) -> bool:
        CartItem.objects.filter(id=item_id).delete()
        return True
