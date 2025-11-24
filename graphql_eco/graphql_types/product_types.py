import strawberry
from typing import List, Optional
from strawberry import django as strawberry_django
from catalog.models import Product, Variant, Category


@strawberry_django.type(Variant)
class VariantType:
    id: strawberry.ID
    variant_name: str
    sku: str
    price: float
    stock: int
    image_url: Optional[str]


@strawberry_django.type(Category)
class CategoryType:
    id: strawberry.ID
    name: str
    parent: Optional["CategoryType"]

    @strawberry.field
    def children(self) -> List["CategoryType"]:
        return list(self.children.all())


@strawberry_django.type(Product)
class ProductType:
    id: strawberry.ID
    name: str
    description: str
    price: float
    brand: str
    image_url: Optional[str]
    category: CategoryType

    @strawberry.field
    def variants(self) -> List[VariantType]:
        return list(self.variant_set.all())
