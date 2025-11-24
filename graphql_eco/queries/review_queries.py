import strawberry
from typing import List, Optional
from review.models import Review
from graphql_eco.graphql_types.review_types import ReviewType


@strawberry.type
class ReviewQuery:

    @strawberry.field
    def reviews(self, info) -> List[ReviewType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return []

        if user.is_admin:
            querys = Review.objects.all()
        elif user.is_vendor:
            return []
        else:
            querys = Review.objects.filter(user=user)

        return [
            ReviewType(
                id=r.id,
                user_id=r.user_id,
                product_id=r.product_id,
                rating=r.rating,
                comment=r.comment,
                created_at=str(r.created_at),
            )
            for r in querys
        ]

    @strawberry.field
    def review(self, info, review_id: int) -> Optional[ReviewType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return None

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None

        if not user.is_admin and review.user != user:
            return None

        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            product_id=review.product_id,
            rating=review.rating,
            comment=review.comment,
            created_at=str(review.created_at),
        )
