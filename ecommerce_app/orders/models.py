from django.db import models

class Cart(models.Model):
    """
    Represents a user's shopping cart, storing selected products and their quantities.
    Allows users to accumulate items before proceeding to checkout.
    """
    user        = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    """
    Represents a completed purchase made by a user, including order details,
    payment information, and the status of the transaction.
    """
    user            = models.ForeignKey('User', on_delete=models.CASCADE)
    address         = models.ForeignKey('Address', on_delete=models.CASCADE)
    order_number    = models.IntegerField()
    total_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status  = models.CharField(max_length=45)
    order_date      = models.DateTimeField(auto_now_add=True)
    shipped_date    = models.DateTimeField(auto_now_add=True)
    payment_method  = models.CharField(max_length=45)


class OrderItem(models.Model):
    """
    Represents an individual product within an order, storing the product,
    quantity, and price at the time of purchase.
    """
    order       = models.ForeignKey('Order', on_delete=models.CASCADE)
    variant     = models.ForeignKey('Variant', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal    = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    """
    Represents an individual product added to a user's cart, including the
    selected quantity and a reference to the related cart and product.
    """
    Cart        = models.ForeignKey('Cart', on_delete=models.CASCADE)
    variant     = models.ForeignKey('Variant', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
