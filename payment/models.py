from django.db import models
from django.utils import timezone

class Payment(models.Model):
    """
    Stores payment details for an order, including method, amount, and status.
    Handles mobile money fields like M-Pesa transaction IDs and callbacks.
    """
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('mpesa', 'M-Pesa'),
        ('cod', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order               = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='payments')
    payment_method      = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number        = models.CharField(max_length=15, blank=True, null=True)
    transaction_id      = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    result_code         = models.CharField(max_length=10, blank=True, null=True)
    result_description  = models.TextField(blank=True, null=True)
    payment_status      = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    paid_at             = models.DateTimeField(blank=True, null=True)
    payment_date        = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.payment_method.upper()} Payment #{self.id}"