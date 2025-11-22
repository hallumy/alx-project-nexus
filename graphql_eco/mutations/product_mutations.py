import strawberry
from catalog.models import Product, Variant
from graphql_eco.graphql_types.product_types import ProductType, VariantType
from typing import Optional, List
from django.db import transaction

@strawberry.type
class ProductMutations:

    @strawberry.mutation
    def create_product(
        self,
        info,
        name: str,
        description: str,
        price: float,
        brand: str,
        category_id: int,
        image_url: Optional[str] = None,
    ) -> ProductType:
        """
        Create a new product.
        """
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            brand=brand,
            category_id=category_id,
            image_url=image_url
        )
        return product

    @strawberry.mutation
    def update_product(
        self,
        info,
        product_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        brand: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Optional[ProductType]:
        """
        Update an existing product.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if brand is not None:
            product.brand = brand
        if image_url is not None:
            product.image_url = image_url

        product.save()
        return product

    @strawberry.mutation
    def delete_product(self, info, product_id: int) -> bool:
        """
        Delete a product by ID.
        """
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False
