from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This model adds a `role` field to differentiate between different user types
    (e.g., admin, customer, vendor) within the e-commerce platform. It also includes
    additional contact information such as phone number and address.
    """
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        VENDOR = "vendor", "Vendor"

    username      = models.CharField(max_length=20)
    email         = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=30)
    first_name    = models.CharField(max_length=30)
    last_name     = models.CharField(max_length=30)
    phone         = models.CharField(max_length=15)
    role          = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Address(models.Model):
    """
    Represents a users bill or shipping address.
    """
    class AddressType(models.TextChoices):
        BILLING = "billing", "Billing"
        SHIPPING = "shipping", "Shipping"
        HOME = "home", "Home"
        OFFICE = "office", "Office"

    user            = models.ForeignKey("User", on_delete=models.CASCADE)
    street          = models.CharField(max_length=30)
    city            = models.CharField(max_length=30)
    region          = models.CharField(max_length=30)
    country         = models.CharField(max_length=30)
    postal_code     = models.CharField(max_length=10)
    address_type    = models.CharField(max_length=50, choices=AddressType.choices, default=AddressType.SHIPPING)

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"