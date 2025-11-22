import strawberry


from graphql_eco.queries.user_queries import UserQuery
from graphql_eco.queries.product_queries import ProductQuery
from graphql_eco.queries.order_queries import OrderQuery
from graphql_eco.queries.review_queries import ReviewQuery
from graphql_eco.queries.wishlist_queries import WishlistQuery
from graphql_eco.queries.cart_queries import CartQuery

from graphql_eco.mutations.user_mutations import UserMutation
from graphql_eco.mutations.cart_mutations import CartMutation
from graphql_eco.mutations.order_mutations import OrderMutation
from graphql_eco.mutations.review_mutations import ReviewMutation
from graphql_eco.mutations.wishlist_mutations import WishlistMutation
from graphql_eco.mutations.product_mutations import ProductMutations


@strawberry.type
class Query(
    CartQuery,
    UserQuery,
    ProductQuery,
    OrderQuery,
    ReviewQuery,
    WishlistQuery,
):
    """
    Combine all top-level query classes
    """
    pass


@strawberry.type
class Mutation(
    UserMutation,
    CartMutation,
    OrderMutation,
    ReviewMutation,
    WishlistMutation,
):
    """
    Combine all top-level mutation classes
    """
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
