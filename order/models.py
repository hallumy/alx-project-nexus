from django.db import models
from django.conf import settings

class Order(models.Model):
    """
    Represents a completed purchase made by a user, including order details,
    payment information, and the status of the transaction.
    """
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address         = models.ForeignKey('users.Address', on_delete=models.CASCADE)
    order_number    = models.IntegerField()
    total_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status  = models.CharField(max_length=45)
    order_date      = models.DateTimeField(auto_now_add=True)
    shipped_date    = models.DateTimeField(auto_now_add=True)
    payment_method  = models.CharField(max_length=45)

    def __str__(self):
        return f"Order #{self.order_number} - {self.payment_status}"
    
class OrderItem(models.Model):
    """
    Represents an individual product within an order, storing the product,
    quantity, and price at the time of purchase.
    """
    order       = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    variant     = models.ForeignKey('catalog.Variant', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal    = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name} ({self.order.order_number})"

class Shipment(models.Model):
    """
    Tracks the shipment of an order, including tracking number, 
    shipment status, and timestamps for updates.
    """
    class Status(models.TextChoices):
        PENDING     = 'pending', 'Pending'
        PROCESSING  = 'processing', 'Processing'
        SHIPPED     = 'shipped', 'Shipped'
        IN_TRANSIT  = 'in_transit', 'In Transit'
        DELIVERED   = 'delivered', 'Delivered'
        CANCELLED   = 'cancelled', 'Cancelled'
        RETURNED    = 'returned', 'Returned'

    order           = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='order')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    carrier         = models.CharField(max_length=30)
    status          = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    shipped_at      = models.DateTimeField(auto_now_add=True)
    delivered_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"