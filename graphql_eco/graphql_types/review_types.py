import strawberry
from typing import Optional
from strawberry import django as strawberry_django
from review.models import Review


@strawberry_django.type(Review)
class ReviewType:
    id: strawberry.ID
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]
    created_at: str
