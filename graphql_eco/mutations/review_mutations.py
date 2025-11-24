import strawberry
from typing import Optional
from review.models import Review
from graphql_eco.graphql_types.review_types import ReviewType


@strawberry.type
class ReviewMutation:

    # CREATE REVIEW
    @strawberry.mutation
    def create_review(
        self,
        info,
        product_id: int,
        rating: int,
        comment: Optional[str] = None,
    ) -> ReviewType:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        # Only one review per product per user
        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise Exception("You have already reviewed this product.")

        review = Review.objects.create(
            user=user,
            product_id=product_id,
            rating=rating,
            comment=comment,
        )

        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            product_id=review.product_id,
            rating=review.rating,
            comment=review.comment,
            created_at=str(review.created_at),
        )

    # ✏ UPDATE REVIEW
    @strawberry.mutation
    def update_review(
        self,
        info,
        review_id: int,
        rating: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> Optional[ReviewType]:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None

        # Only owner or admin can update
        if not user.is_admin and review.user != user:
            raise Exception("Not allowed.")

        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment

        review.save()

        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            product_id=review.product_id,
            rating=review.rating,
            comment=review.comment,
            created_at=str(review.created_at),
        )

    #  DELETE REVIEW
    @strawberry.mutation
    def delete_review(self, info, review_id: int) -> bool:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return False

        if not user.is_admin and review.user != user:
            raise Exception("Not allowed.")

        review.delete()
        return True
