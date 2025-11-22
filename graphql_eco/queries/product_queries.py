import strawberry
from typing import List, Optional
from catalog.models import Product, Category, Variant
from graphql_eco.graphql_types.product_types import ProductType, VariantType, CategoryType

@strawberry.type
class ProductQuery:

    @strawberry.field
    def products(self, info, category_id: Optional[int] = None) -> List[ProductType]:
        """
        Fetch all products, optionally filtered by category.
        """
        queryset = Product.objects.all().select_related("category").prefetch_related("variant_set")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @strawberry.field
    def product(self, info, product_id: int) -> Optional[ProductType]:
        """
        Fetch a single product by ID.
        """
        try:
            return Product.objects.select_related("category").prefetch_related("variant_set").get(id=product_id)
        except Product.DoesNotExist:
            return None

    @strawberry.field
    def categories(self, info) -> List[CategoryType]:
        """
        Fetch all categories.
        """
        return Category.objects.all()

    @strawberry.field
    def category(self, info, category_id: int) -> Optional[CategoryType]:
        """
        Fetch a single category by ID.
        """
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None
