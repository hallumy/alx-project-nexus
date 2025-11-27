from django.test import TestCase
from review.models import Review

class ReviewLogicTests(TestCase):

    def setUp(self):
        self.review = Review.objects.create(user_id=1, product_id=1, rating=5)

    def test_rating_range(self):
        self.assertTrue(1 <= self.review.rating <= 5)

