from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from catalog.models import Product, Category
from review.models import Review

class ReviewModelTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", email="test@example.com")

        # Create a category and product
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=1000,
            stock_quantity=10,
            category=self.category,
            is_active=True
        )

    def test_create_review(self):
        """Test that a review can be created successfully."""
        review = Review.objects.create(user=self.user, product=self.product, rating=5, comment="Great laptop!")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great laptop!")

    def test_rating_range(self):
        """Rating should be between 1 and 5."""
        valid_review = Review.objects.create(user=self.user, product=self.product, rating=3)
        self.assertTrue(1 <= valid_review.rating <= 5)

    def test_string_representation(self):
        """The string representation should show user, product, and rating."""
        review = Review.objects.create(user=self.user, product=self.product, rating=4)
        expected_str = f"Review by {self.user.username} for {self.product.name} (4)"
        self.assertEqual(str(review), expected_str)

    def test_one_review_per_user_per_product(self):
        """Ensure a user can’t create multiple reviews for the same product."""
        Review.objects.create(user=self.user, product=self.product, rating=5)
        with self.assertRaises(Exception):
            # Attempt to create a second review for the same product by the same user
            Review.objects.create(user=self.user, product=self.product, rating=4)
