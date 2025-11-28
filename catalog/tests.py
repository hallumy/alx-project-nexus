from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from catalog.models import (
    Category,
    Product,
    Variant,
    Inventory,
    Discount,
    ProductDiscount,
    Wishlist,
    WishlistItem,
    Cart,
    CartItem
)

User = get_user_model()

class CatalogModelTests(TestCase):
    def setUp(self):
        # User
        self.user = User.objects.create_user(username="alice", email="alice@example.com", password="password123")

        # Category
        self.category = Category.objects.create(name="Electronics")

        # Product
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="High-end laptop",
            price=Decimal("1500.00"),
            stock_quantity=5,
            sku="LAP123",
            is_active=True,
            brand="TechBrand"
        )

        # Variant
        self.variant = Variant.objects.create(
            product=self.product,
            variant_name="16GB RAM, 512GB SSD",
            price=Decimal("1600.00"),
            stock=3,
            sku="LAP123-16-512"
        )

        # Inventory
        self.inventory = Inventory.objects.create(
            variant=self.variant,
            quantity=3
        )

        # Discount
        self.discount = Discount.objects.create(
            code="BLACKFRIDAY",
            description="Black Friday Sale",
            discount_type="percentage",
            minimum_purchase=Decimal("1000.00"),
            maximum_discount=Decimal("500.00"),
            is_active=True
        )

        # ProductDiscount
        self.product_discount = ProductDiscount.objects.create(
            discount=self.discount,
            product=self.product
        )

        # Wishlist & Item
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist_item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            product=self.product
        )

        # Cart & Item
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
            price=self.variant.price
        )

    # --- Category ---
    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    # --- Product ---
    def test_product_str(self):
        self.assertEqual(str(self.product), f"{self.product.name} - {self.product.price}")

    # --- Variant ---
    def test_variant_str(self):
        self.assertEqual(str(self.variant), f"{self.product.name} - {self.variant.variant_name}")

    # --- Inventory ---
    def test_inventory_str(self):
        self.assertEqual(str(self.inventory), f"Inventory for {self.variant.variant_name}: {self.inventory.quantity}")

    # --- Discount ---
    def test_discount_str(self):
        self.assertEqual(str(self.discount), f"Discount {self.discount.code}")

    # --- ProductDiscount ---
    def test_product_discount_str(self):
        self.assertEqual(str(self.product_discount), f"{self.discount.code} -> {self.product.name}")

    # --- Wishlist ---
    def test_wishlist_str(self):
        self.assertEqual(str(self.wishlist), f"Wishlist of {self.user}")

    # --- WishlistItem ---
    def test_wishlist_item_str(self):
        self.assertEqual(str(self.wishlist_item), f"{self.product.name} in wishlist {self.wishlist.id}")

    # --- Cart ---
    def test_cart_str(self):
        self.assertEqual(str(self.cart), f"Cart of {self.user}")

    # --- CartItem ---
    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), f"{self.variant.variant_name} x {self.cart_item.quantity}")

    # --- Relationships ---
    def test_product_category_relationship(self):
        self.assertEqual(self.product.category, self.category)

    def test_variant_product_relationship(self):
        self.assertEqual(self.variant.product, self.product)

    def test_inventory_variant_relationship(self):
        self.assertEqual(self.inventory.variant, self.variant)

    def test_product_discount_relationships(self):
        self.assertEqual(self.product_discount.product, self.product)
        self.assertEqual(self.product_discount.discount, self.discount)

    def test_wishlist_item_relationships(self):
        self.assertEqual(self.wishlist_item.wishlist, self.wishlist)
        self.assertEqual(self.wishlist_item.product, self.product)

    def test_cart_item_relationships(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.variant, self.variant)
