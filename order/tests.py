from django.test import TestCase
from decimal import Decimal
from users.models import User, Address
from catalog.models import Category, Product, Variant
from order.models import Order, OrderItem, Shipment


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", email="john@example.com", password="password123")
        self.address = Address.objects.create(
            user=self.user,
            street="123 Main St",
            city="New York",
            region="NY",
            country="USA",
            postal_code="10001"
        )

        # MUST CREATE CATEGORY FIRST
        self.category = Category.objects.create(name="Electronics")

        # Product
        self.product = Product.objects.create(
            name="Laptop",
            price=1000,
            stock_quantity=10,
            category=self.category,   # FIXED
            is_active=True
        )

        # Variant
        self.variant = Variant.objects.create(
            product=self.product,
            sku="LAP123",
            stock=10
        )

        # Order
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            order_number=1,
            total_amount=0,
            status="pending",
            payment_method="credit_card"
        )

        # Order Items
        self.item1 = OrderItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=2,
            price=Decimal("1000.00"),
            subtotal=Decimal("2000.00")
        )
        self.item2 = OrderItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=1,
            price=Decimal("500.00"),
            subtotal=Decimal("500.00")
        )

        # Update total
        self.order.total_amount = sum(item.subtotal for item in self.order.orderitem_set.all())
        self.order.save()

class ShipmentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jane", email="jane@example.com", password="password123")
        self.address = Address.objects.create(
            user=self.user,
            street="456 Elm St",
            city="Los Angeles",
            region="CA",
            country="USA",
            postal_code="90001"
        )

        self.category = Category.objects.create(name="Electronics")

        self.product = Product.objects.create(
            name="Phone",
            price=500,
            stock_quantity=20,
            category=self.category
        )

        self.variant = Variant.objects.create(
            product=self.product,
            sku="PHN001",
            stock=5            
        )

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            order_number=2,
            total_amount=500,
            status="processing",
            payment_method="paypal"
        )

        self.shipment = Shipment.objects.create(
            order=self.order,
            tracking_number="TRACK123",
            carrier="UPS",
            status=Shipment.Status.SHIPPED
        )
