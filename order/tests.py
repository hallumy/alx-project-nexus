from django.test import TestCase
from order.models import Order, OrderItem
from catalog.models import Variant, Product

class OrderLogicTests(TestCase):
    """Test Order and OrderItem logic like totals and stock checks."""
    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price=1000)
        self.variant = Variant.objects.create(product=self.product, sku="LAP123")
        self.order = Order.objects.create(user_id=1)

    def test_order_total_calculation(self):
        OrderItem.objects.create(order=self.order, variant=self.variant, quantity=2, price=1000)
        OrderItem.objects.create(order=self.order, variant=self.variant, quantity=1, price=500)
        total = sum(item.price * item.quantity for item in self.order.items.all())
        self.assertEqual(total, 2500)

