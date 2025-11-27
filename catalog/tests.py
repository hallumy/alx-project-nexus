from django.test import TestCase
from users.models import User
from catalog.models import Product, Variant, Inventory, Cart, CartItem, Discount

class ProductInventoryTests(TestCase):
    """Test Product, Variant, and Category methods."""
    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price=1000)
        self.variant = Variant.objects.create(product=self.product, sku="LAP123")
        self.inventory = Inventory.objects.create(variant=self.variant, stock=10)

    def test_inventory_stock_reduction(self):
        # Simulate a purchase reducing stock
        self.inventory.stock -= 3
        self.inventory.save()
        self.assertEqual(self.inventory.stock, 7)

    def test_variant_belongs_to_product(self):
        self.assertEqual(self.variant.product, self.product)

class CartLogicTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="john")
        self.cart = Cart.objects.create(user=self.user)
        self.variant = Variant.objects.create(sku="SKU001")
    
    def test_add_item_to_cart(self):
        item = CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=2)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(self.cart.items.count(), 1)

    def test_cart_total_quantity(self):
        CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=2)
        CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=3)
        total_quantity = sum(item.quantity for item in self.cart.items.all())
        self.assertEqual(total_quantity, 5)


class DiscountLogicTests(TestCase):

    def setUp(self):
        self.discount = Discount.objects.create(code="NEW10", discount_type="percentage", discount_value=10)
        self.product = Product.objects.create(name="Laptop", price=1000)

    def test_discount_application(self):
        discounted_price = self.product.price - (self.product.price * self.discount.discount_value / 100)
        self.assertEqual(discounted_price, 900)