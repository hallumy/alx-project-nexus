from django.test import TestCase
from users.models import User

class UserLogicTests(TestCase):
    """Test custom User model logic like roles and utilities."""

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", role=User.Roles.ADMIN)
        self.customer = User.objects.create_user(username="customer", role=User.Roles.CUSTOMER)
        self.vendor = User.objects.create_user(username="vendor", role=User.Roles.VENDOR)

    def test_user_roles(self):
        self.assertEqual(self.admin.role, User.Roles.ADMIN)
        self.assertEqual(self.customer.role, User.Roles.CUSTOMER)
        self.assertEqual(self.vendor.role, User.Roles.VENDOR)

    def test_is_admin_method(self):
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.customer.is_admin())

