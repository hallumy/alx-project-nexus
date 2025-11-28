from django.test import TestCase
from users.models import User, Address

class UserModelTests(TestCase):
    """Tests for the custom User model and role properties."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="password123",
            role=User.Roles.ADMIN,
            first_name="Admin",
            last_name="User",
            phone="1234567890"
        )
        self.customer = User.objects.create_user(
            username="customeruser",
            email="customer@example.com",
            password="password123",
            role=User.Roles.CUSTOMER,
            first_name="Customer",
            last_name="User",
            phone="0987654321"
        )
        self.vendor = User.objects.create_user(
            username="vendoruser",
            email="vendor@example.com",
            password="password123",
            role=User.Roles.VENDOR,
            first_name="Vendor",
            last_name="User",
            phone="5555555555"
        )

    def test_user_roles_properties(self):
        """Check that role properties return correct boolean values."""
        self.assertTrue(self.admin.is_admin)
        self.assertFalse(self.admin.is_customer)
        self.assertFalse(self.admin.is_vendor)

        self.assertTrue(self.customer.is_customer)
        self.assertFalse(self.customer.is_admin)
        self.assertFalse(self.customer.is_vendor)

        self.assertTrue(self.vendor.is_vendor)
        self.assertFalse(self.vendor.is_admin)
        self.assertFalse(self.vendor.is_customer)

    def test_user_str_method(self):
        """__str__ method returns expected string."""
        self.assertEqual(str(self.admin), "adminuser (admin)")
        self.assertEqual(str(self.customer), "customeruser (customer)")

class AddressModelTests(TestCase):
    """Tests for the Address model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123"
        )
        self.address = Address.objects.create(
            user=self.user,
            street="123 Main St",
            city="New York",
            region="NY",
            country="USA",
            postal_code="10001",
            address_type=Address.AddressType.HOME
        )

    def test_address_belongs_to_user(self):
        """Address is linked to the correct user."""
        self.assertEqual(self.address.user, self.user)

    def test_address_str_method(self):
        """__str__ method returns expected string."""
        self.assertEqual(str(self.address), "john - home")
